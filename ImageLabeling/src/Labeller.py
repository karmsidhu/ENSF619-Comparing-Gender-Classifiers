"""
Script to aid in labelling images

Was created to help a face by race but was unused due to a heavy uneven
distribution in the dataset

Dependencies:
    - json
    - os
"""

import json
import os

def get_file_names(dir:str = "ImageData"):
    """
    Gets all file names in provided directory

    Args:
        dir: Directory containing the images
    
    Returns:
        List of all files in provided directory
    """
    return os.listdir(dir)

def to_json_file(label_dict:dict, dir:str = "ImageLabeling"):
    """
    Writes provided dictionary to provided directory in JSON format

    Args:
        label_dict: Dictionary to be written to file as LabeledImages.json
        dir: Directory to where file will be written
    """
    json_string = json.dumps(label_dict, sort_keys=True, indent=4, 
            separators=(',',':'))

    with open(dir + "/LabeledImages.json", "w") as f:
        f.write(json_string)

def load_json_file(file_loc:str = "ImageLabeling/LabeledImages.json"):
    """
    Loads JSON file as a dictionary

    Args:
        file_loc: Location of JSON file

    Returns:
        Dictionary based on the provided file
    """
    with open(file_loc, "r") as f:
        data = json.load(f)
    return data

def main():
    """
    Begins labelling process

    Will first load already labelled images and then start labelling
    process for non-labelled images
    """
    img_dict = load_json_file()
    all_imgs = get_file_names()
    imgs = []
    for img in all_imgs:
        if img not in list(img_dict.keys()):
            imgs.append(img)
    print("Starting Labelling Process. Enter EXIT to stop and Save.")
    print("Acceptable inputs are: white, indian, asian, black, " + 
        "hispanic, native, NA")
    for img in imgs:
        user_input = 0
        races = ["white", "indian", "asian", "black", "hispanic", "native", "NA"]
        os.system("open ImageData/" + img)
        while user_input != 1234:
            user_input = input("What race? (EXIT to stop) ")
            if user_input == "EXIT":
                break
            elif user_input in races:
                img_dict[img] = user_input
                user_input = 1234
            else:
                print("Invalid response")
        if user_input == "EXIT":
            break
    to_json_file(img_dict)

# main()
