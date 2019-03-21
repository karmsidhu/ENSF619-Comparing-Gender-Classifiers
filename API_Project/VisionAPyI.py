from google.cloud import vision
from FileManager import FileManager
import os

class Vision:
    def __init__(self, credentials_path:str = 
        "API_Project/GoogleCloudCredentials/CloudVisionCredentials.json"):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = vision.ImageAnnotatorClient()

    def label_images(self, byte_imgs:dict = None, img_nums:int = 1):
        """
        client is the Rekognition service client. 
        Can be called from create_resource()
        """
        if FileManager().file_count_warning(img_nums):
            counter = 0
            responses = dict()
            for path,img_bytes in byte_imgs.items():
                try:
                    image = vision.types.Image(content = img_bytes)
                    response = self.client.face_detection(image = image)
                    responses[path] = response
                except:
                    responses[path] = None
                counter += 1
                print(f"{counter/img_nums*100}% Processed...")
                if counter >= img_nums:
                    break
        else:
            return None
        return response
        # return responses

fm = FileManager()
gcv = Vision()
byte_imgs = fm.image_to_bytes(file_names = fm.get_file_names())
response = gcv.label_images(byte_imgs=byte_imgs, img_nums=1)
print(response)
fm.to_textfile(text=response, fname = "gcvtest.txt")
