from FileManager import FileManager
from RekognitionAPI import Rekognition
from VisionAPI import Vision


def load_prev_data(fm:FileManager, aws_dir:str, gcv_dir:str):
	aws_data = fm.load_labelled_data(aws_dir)
	gcv_data = fm.load_labelled_data(gcv_dir)
	return aws_data, gcv_data

def remove_repeats_rekog(prev_data, new_data):
	keys = list(new_data.keys())
	for key in keys:
		check = prev_data.get(key)
		if check != None:
			print(f"AWS - Duplicate image found, removing: {key}")
			new_data.pop(key, None)
			
def remove_repeats_vision(prev_data, new_data):
	keys = list(new_data.keys())
	for key in keys:
		checkKey = prev_data.get(key)
		if checkKey != None:
			checkResp = prev_data[key]["responses"][0].get("faceAnnotations")
			if checkResp != None:
				new_data.pop(key, None)
				print(f"GCV - Duplicate image found, removing: {key}")

def make_master_files(fm, aws_data, gcv_data, aws_dir:str, gcv_dir:str):
	fm.to_json(json_dict = aws_data, 
		dir_name = aws_dir)
	fm.to_json(json_dict = gcv_data, 
		dir_name = gcv_dir)

def main():
	# Set directories -------
	aws_label_dir = "API_Project/AWS-Standard-Labels"
	gcv_label_dir = "API_Project/GCV-Standard-Labels"
	img_dir = "Images/Standard-Size"
	
	# Instantiate Objects -------
	fm = FileManager()
	aws_Rekognition = Rekognition()
	# gc_Vision = Vision()

	# Load Previously Labelled Data -------
	aws_data, gcv_data = load_prev_data(fm, aws_dir = aws_label_dir, 
		gcv_dir = gcv_label_dir)

	# Convert all images to bytes -------
	aws_img_data = fm.image_to_bytes(src_dir = img_dir, 
		file_names = fm.get_file_names(dir = img_dir))
	# gcv_img_data = fm.image_to_bytes(src_dir = img_dir, 
	# 	file_names = fm.get_file_names(dir = img_dir))

	# Remove already labelled data -------
	remove_repeats_rekog(aws_data, aws_img_data)
	# remove_repeats_vision(gcv_data, gcv_img_data)

	# Label using Rekognition -------
	# aws_response = aws_Rekognition.label_images(byte_imgs = aws_img_data, img_nums = 600)
	# if aws_response != None:
	# 	fm.to_json(json_dict = aws_response, 
	# 		dir_name = aws_label_dir)
	
	# Label using Vision -------
	# gcv_response = gc_Vision.label_images(byte_imgs = gcv_img_data, img_nums = 10)
	# if gcv_response != None:
	# 	fm.to_json(json_dict = gcv_response,
	# 		dir_name = gcv_label_dir)

	# Create Master Files that consolidates all labelled data -------
	make_master_files(fm,aws_data,gcv_data, aws_label_dir, gcv_label_dir)


main()
