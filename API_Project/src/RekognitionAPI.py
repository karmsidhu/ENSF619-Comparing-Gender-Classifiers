"""Used to connect with and use Amazon's Rekognition model to label images

Dependencies:
    boto3
    FileManager
"""


import boto3
from FileManager import FileManager

class Rekognition:
"""Helper class for interfacing with AWS Rekognition APIs

    Functionality is limited to what was needed for the Gender classficiation
    project. Requires an AWS access key, and secret key

    Attributes:
        client: boto3 client used to make requests. Requires AWS keys and region
"""
    def __init__(self, name:str = 'rekognition', access_keys_file_path:str = 
        '../APICredentials/accessKeys.csv', 
        region:str = 'us-east-2'):
        """Creates a boto3 client to connect with AWS
        
            Need to have AWS keys to create the client.

            Args:
                name: Name of Service to be created
                access_keys_file_path: Path to file containing AWS access keys
                region: AWS server to connect with
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
        """Sends a dictionary of images as bytes to be labelled by AWS

            Args:
                byte_imgs: Images to be labelled as a dictioanry. Images must
                    be in byte format
                img_nums: Max number of images to be labelled
            Returns:
                Response from the AWS API's
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
                print("AWS - " + f"{counter/img_nums*100}% ({counter}/{img_nums}) Processed...")
                if counter >= img_nums:
                    break
        else:
            return None
        return responses