from FileManager import FileManager
import os
import requests
import base64
import json


class Vision:
    def __init__(self, API_key_path:str = 
        "../APICredentials/api_key.txt"):
        '''
        Puts the API Key in an environment variable.
        Sets the HTTP url for Vision API's
        Loads in the request format for API requests
        '''
        with open(API_key_path) as key:
            os.environ["GOOGLE_API_KEY"] = key.readline()
        self._key = os.environ["GOOGLE_API_KEY"]
        self._url = ("https://vision.googleapis.com/v1/images:annotate?key=" 
            + self._key)
        self._load_request()

    def _load_request(self):
        '''
        Loads the request format for API requests
        '''
        with open("API_Project/gcv_request.json", "r") as req:
           self._request = json.load(req)

    def _add_image_to_payload(self, img_bytes):
        '''
        Converts the image content into Base64 encoding and
        loads it into the request. Returns payload that is
        ready to be sent
        '''
        payload = self._request
        payload["requests"][0]["image"]["content"] = \
            str(base64.b64encode(img_bytes))[2:-1]
        return payload

    def label_images(self, byte_imgs:dict = None, img_nums:int = 1):
        '''
        Sends the request to the Vision API with the payload
        Returns the response in json format
        '''
        total_imgs = len(list(byte_imgs.keys()))
        if total_imgs < img_nums:
            img_nums = total_imgs
        print("====== GC Vision: Detect Faces ======")
        if FileManager().file_count_warning(img_nums):
            counter = 0
            responses = dict()
            for path,img_bytes in byte_imgs.items():
                try:
                    payload =  self._add_image_to_payload(img_bytes)
                    response = requests.post(self._url, json = payload)
                    responses[path] = response.json()
                except:
                    print("Error")
                    responses[path] = None
                counter += 1
                print("GCV - " + f"{counter/img_nums*100}% ({counter}/{img_nums}) Processed...")
                if counter >= img_nums:
                    break
        else:
            return None
        return responses