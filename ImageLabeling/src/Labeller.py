import json
import os


def get_file_names(dir:str = "ImageData"):
    """
    Gets all file names in dir
    """
    return os.listdir(dir)

def to_json_file(label_dict:dict, dir:str = "ImageLabeling"):
    json_string = json.dumps(label_dict, sort_keys=True, indent=4, 
            separators=(',',':'))

    with open(dir + "/LabeledImages.json", "w") as f:
        f.write(json_string)

def load_json_file(file_loc:str = "ImageLabeling/LabeledImages.json"):
    with open(file_loc, "r") as f:
        data = json.load(f)
    return data

def main():
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

main()
