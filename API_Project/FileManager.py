import os, json

class FileManager:
    def get_file_names(self, dir:str = "ImageData"):
        """
        Gets all file names in dir
        """
        return os.listdir(dir)

    def image_to_bytes(self, src_dir:str = "ImageData", file_names:list = None):
        """
        Converts file_names into bytes so it can be sent to Rekog Client.
        Returns dictionary where keys are file paths and
        values are the keys respective bytes.
        """
        byte_imgs = dict()
        for fname in file_names:
            path = src_dir + "/" + fname
            with open(path, "rb") as image_file:
                byte_imgs[fname] = image_file.read()
        return byte_imgs

    def file_count_warning(self, file_count:int):
        """
        Checks with the user if they want to proceed with processing images
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

    def to_json(self, json_dict:dict, dir_name:str = 
        "API_Project/AWS-LabelledDataTest", fname:str = "AWS-Labels-0000.json"):
        """
        Converts a dictionary into json format and saves it in dir_name/fname
        """
        json_string = json.dumps(json_dict, sort_keys=True, indent=4, 
            separators=(',',':'))

        try: os.makedirs(dir_name)
        except FileExistsError: pass

        with open(dir_name + "/" + fname, "w") as f:
            f.write(json_string)

    def load_json(self):
        #TODO
        pass

    def to_textfile(self, text:str, dir_name:str = 
        "API_Project/GCV-LabelledDataTest", fname:str = "GCV-Labels-0000.txt"):

        try: os.makedirs(dir_name)
        except FileExistsError: pass
        with open(dir_name + "/" + fname, "w") as f:
            f.write(text)