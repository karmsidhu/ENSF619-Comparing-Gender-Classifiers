import boto3
import base64
import os
import json

def create_resource(name:str = 'rekognition', access_keys_file_path:str = 
    'AWS-RekognitionAPI/AWSCredentials/accessKeys.csv', region:str = 'us-east-2'):
    """
    For a full list of AWS regions see:
    https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.Regions\AndAvailabilityZones.html
    """
    with open(access_keys_file_path, 'r') as keys:
        keys.readline()
        access_keys = keys.readline().split(',')
        aws_access_key_id=access_keys[0].strip()
        aws_secret_access_key=access_keys[1].strip()
    return boto3.client(name, aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key, region_name = region)

def file_count_warning(file_count:int):
    print("You are about to process ", file_count, " images!")
    user_response = input("Would you like to proceed? (Y/N) ")
    while(user_response.upper() not in ["Y", "N"]):
        print("Invalid response.")
        user_response = input("Would you like to proceed? (Y/N) ")
    if user_response.upper() == "Y":
        return True
    elif user_response.upper() == "N":
        return False

def get_image_paths(dir:str = "ImageData"):
    return os.listdir(dir)

def image_to_bytes(src_dir:str = "ImageData", file_names:list = None):
    byte_imgs = dict()
    for fname in file_names:
        path = src_dir + "/" + fname
        with open(path, "rb") as image_file:
            byte_imgs[fname] = image_file.read()
    return byte_imgs

def rekog_detect_faces(client, byte_imgs:dict = None, img_nums:int = 1):
    """
    client is the Rekognition service client. 
    Can be called from create_resource()
    """
    if file_count_warning(img_nums):
        counter = 0
        responses = dict()
        for path,img_bytes in byte_imgs.items():
            try:
                response = client.detect_faces(Image={"Bytes":img_bytes}, 
                    Attributes = ["ALL"])
                responses[path] = response
            except:
                responses[path] = None
            counter += 1
            if counter >= img_nums:
                break
    else:
        return None
    return responses

def to_json(json_dict:dict, dir_name:str = "AWS-RekognitionAPI/AWS-LabelledDataTest", 
    fname:str = "AWS-Labels.json"):
    json_string = json.dumps(json_dict, sort_keys=True, indent=4, 
        separators=(',',':'))

    try: os.makedirs(dir_name)
    except FileExistsError: pass

    with open(dir_name + "/" + fname, "w") as f:
        f.write(json_string)

def main():
    client = create_resource()
    byte_imgs = image_to_bytes(file_names = get_image_paths())
    responses = rekog_detect_faces(client, byte_imgs = byte_imgs, img_nums = 100)
    to_json(responses)

main()