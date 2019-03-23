from FileManager import FileManager
from RekognitionAPI import Rekognition
from VisionAPI import Vision


def load_prev_data(fm:FileManager):
	aws_data = fm.load_labelled_data("API_Project/AWS-LabelledData")
	gcv_data = fm.load_labelled_data("API_Project/GCV-LabelledData")
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

def make_master_files(fm, aws_data, gcv_data):
	fm.to_json(json_dict = aws_data, 
		dir_name = "API_Project/AWS-LabelledData/")
	fm.to_json(json_dict = gcv_data, 
		dir_name = "API_Project/GCV-LabelledData/")

def main():
	fm = FileManager()
	aws_Rekognition = Rekognition()
	gc_Vision = Vision()
	aws_data, gcv_data = load_prev_data(fm)
	aws_img_data = fm.image_to_bytes(file_names = fm.get_file_names())
	gcv_img_data = fm.image_to_bytes(file_names = fm.get_file_names())

	remove_repeats_rekog(aws_data, aws_img_data)
	remove_repeats_vision(gcv_data, gcv_img_data)

	# aws_response = aws_Rekognition.label_images(byte_imgs = aws_img_data, img_nums = 0)
	# if aws_response != None:
	# 	fm.to_json(json_dict = aws_response, 
	# 		dir_name = "API_Project/AWS-LabelledData/")

	# gcv_response = gc_Vision.label_images(byte_imgs = gcv_img_data, img_nums = 128)
	# if gcv_response != None:
	# 	fm.to_json(json_dict = gcv_response,
	# 		dir_name = "API_Project/GCV-LabelledData/")

	# make_master_files(fm,aws_data,gcv_data)


main()
