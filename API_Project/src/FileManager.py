"""
Used to mangage files for the project

Dependencies:
    json
    os
"""

import json
import os

class FileManager:
    """Used to open, save, list, convert, and general utility for files in the project.
        
        Aids in seperating any coupling between modules in project.

        Attributes:
            None
    """
    def get_file_names(self, dir:str = "ImageData"):
        """Gets all file names in dir.

            Equivalent to os.listdir(). 
            Redudandnt property and should be depreciated.

            Args:
                dir: directory for which it looks in

            Returns:
                All file names present in the directory as a list
        """
        return os.listdir(dir)

    def image_to_bytes(self, src_dir:str = "ImageData", file_names:list = None):
        """Converts file_names into bytes so it can be sent to Rekog Client.
        
            Args:
                src_dir: Directory in which files are located
                file_names: Names of files to be converted to bytes
            Returns:
                dictionary where keys are file paths and 
                values are the keys respective bytes.
        """
        byte_imgs = dict()
        for fname in file_names:
            path = src_dir + "/" + fname
            with open(path, "rb") as image_file:
                byte_imgs[fname] = image_file.read()
        return byte_imgs

    def file_count_warning(self, file_count:int):
        """Checks with the user if they want to proceed with processing images.

            Helps in accidently requesting too many images and incurring unwanted
            costs.

            Args:
                file_count: number of files to be processed
            
            Return:
                True if user wants to continue, False otherwise
        """
        print("You are about to process ", file_count, " images!")
        user_response = input("Would you like to proceed? (Y/N) ")
        while(user_response.upper() not in ["Y", "N"]):
            print("Invalid response.")
            user_response = input("Would you like to proceed? (Y/N) ")
        if user_response.upper() == "Y":
            return True
        elif user_response.upper() == "N":
            return False

    def to_json(self, json_dict:dict, dir_name:str):
        """Converts and saves dictionary into json format.

            Args:
                json_dict: dictionary to be converted to json format
                dir_name: location for where the file will be saved
        """
        json_string = json.dumps(json_dict, sort_keys=True, indent=4, 
            separators=(',',':'))

        try: os.makedirs(dir_name)
        except FileExistsError: pass
        i = 0
        while os.path.exists(dir_name + "/" + f"Labels-000{i}.json"):
            i += 1
        with open(dir_name + "/" + f"Labels-000{i}.json", "w") as f:
            f.write(json_string)
        print("Response saved to " + dir_name + f"Labels-000{i}.json")

    def load_labelled_data(self, dir_name:str):
        """Loads in previously labelled data as a dictionary

            Args:
                dir_name: directory containing all labelled JSON files

            Returns:
                Dictionary containing all the labelled data
        """
        fnames = self.get_file_names(dir_name)
        labelled_data = dict()
        for f in fnames:
            labelled_data.update(self.load_json(dir_name + "/" + f))
        return labelled_data

    def load_json(self, fname:str):
        with open(fname, "r") as json_file:
            data = json.load(json_file)
        return data

    def to_textfile(self, text:str, dir_name:str, fname:str):
        try: os.makedirs(dir_name)
        except FileExistsError: pass
        with open(dir_name + "/" + fname, "w") as f:
            f.write(text)
