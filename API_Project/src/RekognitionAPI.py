import boto3
from FileManager import FileManager

class Rekognition:
    def __init__(self, name:str = 'rekognition', access_keys_file_path:str = 
        '../APICredentials/accessKeys.csv', 
        region:str = 'us-east-2'):
        """
        For a full list of AWS regions see:
        https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.Regions\AndAvailabilityZones.html
        """

        with open(access_keys_file_path, 'r') as keys:
            keys.readline()
            access_keys = keys.readline().split(',')
            aws_access_key_id=access_keys[0].strip()
            aws_secret_access_key=access_keys[1].strip()

        self.client = boto3.client(name, aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key, region_name = region)
    
    def label_images(self, byte_imgs:dict = None, img_nums:int = 1):
        """
        client is the Rekognition service client. 
        Can be called from create_resource()
        """
        total_imgs = len(list(byte_imgs.keys()))
        if total_imgs < img_nums:
            img_nums = total_imgs
        print("====== AWS Rekognition: Detect Faces ======")
        if FileManager().file_count_warning(img_nums):
            counter = 0
            responses = dict()
            for path,img_bytes in byte_imgs.items():
                try:
                    response = self.client.detect_faces(Image={"Bytes":img_bytes}, 
                        Attributes = ["ALL"])
                    responses[path] = response
                except:
                    print("Error")
                    responses[path] = None
                counter += 1
                print("AWS - " + f"{counter/img_nums*100}% Processed...")
                if counter >= img_nums:
                    break
        else:
            return None
        return responses