##Importing dependencies
import json
import os
import sys
import time
import datetime
from pathlib import Path

# Setting up server side (on the edge device - where we receive frames and processing happens)
import cv2
import imagezmq
import requests
from psql_util import *
from inference import detection

##Uncomment for buzzer triggering using serial communication
# from buzzer import * 

from config import ConfigTF

##Database credentials
config = ConfigTF()
db_username = config.get_config("db_username")
db_password = config.get_config("db_password")
db_hostip = config.get_config("db_hostip")
db_port = config.get_config("db_port")
db_database = config.get_config("db_database")
db_table = config.get_config("db_table") ##Different table for different use cases

##Model details
model_version = config.get_config("model_version")

##Path credentials
base_path = Path(config.get_config("base_path"))
base_path = r"{}".format(base_path)

inference_path=Path(str(base_path)+config.get_config("inference_path"))
inference_path=r"{}".format(inference_path)
print("Inference path",inference_path)

##For storing images
out_path=Path(config.get_config("out_path"))
out_path=r"{}".format(out_path)

streaming_fps = config.get_config("streaming_fps")

sys.path.insert(0, inference_path)

##Functions required for 
def get_date_path(today_date):
	return today_date.strftime("%Y/%m/%d")

def create_dir(out_path, FOLDER):
    os.makedirs(out_path + FOLDER, exist_ok=True)

def convert_timestamp(item_date_object):
    if isinstance(item_date_object, (datetime.date, datetime.datetime)):
        return item_date_object.timestamp()

def myconverter(o):
	if isinstance(o, datetime.datetime):
		return o.__str__()

print("Hosting the Server")

##Opening the portal to accept the stream from the clients
image_hub = imagezmq.ImageHub(open_port="tcp://*:5555", REQ_REP=True)	#Req-reply set to True where every frame sent by client to server should wait for reply before sending next frame

print("Server is ready!")

##Creating a database object for database credentials
dbobj = DatabaseUtil(db_username, db_password, db_hostip, db_port, db_database)

counter, total_fps, neg_counter, frame_count = 0, 0, 0, 0
violation_flag = None
total_fps = 0


while True:

	counter += 1
	
	##Receive images from the client's stream
	cam_metadata, img = image_hub.recv_image()
	cam_id = cam_metadata["cam_id"]
	cam_view = cam_metadata["cam_view"]
	image_hub.send_reply(b'OK')
	
	start_time = time.time()
	today_date = datetime.datetime.today()
	date_path = get_date_path(today_date) ##To save the violations for each day

	if cam_view == "side":
		result, violation_flag = detection.detect_side(img)

	elif cam_view == "front":
		result, violation_flag = detection.detect_front(img)

	print(violation_flag)

	end_time = time.time()
	
	fps = 1 / (end_time - start_time)
	print(fps) ##Prints the FPS of the last frame

	total_fps += fps
	frame_count += 1
	wait_time = max(1, int(fps/4))

	cv2.putText(result, f"{fps:.3f} FPS", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

	if violation_flag == True:
		cv2.putText(result, "Alert", (550, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

	cv2.imshow("Result", result) ##Immdiately shows the results
	cv2.waitKey(1)

	##Show results after every 5 seconds to verify the result shape
	if counter % (5 * int(streaming_fps)) == 0:
	   
		print("Result shape", result.shape)

	    # calculate and print the average FPS
		avg_fps = total_fps / frame_count
		print(f"Average FPS: {avg_fps:.3f}")

	##Create path to save image to disk
	dir = "/" + date_path + "/" + "cam " + str(cam_id) + "-" + cam_view


	file_name = today_date.strftime("%Y-%m-%d--%H-%M-%S-%f") + ".jpg" ##file name according to the timestamp
	
	save_path = "{}{}{}".format(out_path + dir, os.sep, file_name) ##savepath - absolute

	create_dir(out_path, dir) ##creates path if not already done

	##Data to be sent to the database
	predictions_data = {}

	##Add required columns to save to DB Table
	predictions_data["company_id"] = cam_metadata["company_id"]
	predictions_data["camera_id"] = cam_id
	predictions_data["model_version"] = model_version
	predictions_data["is_violation"] = violation_flag
	predictions_data["img_path"] = dir + '/' + file_name
	predictions_data["out_data"] = None #json.dumps(person_violate_dict)
	predictions_data["description"] = ""
	predictions_data["prediction_time"] = datetime.datetime.now()
	predictions_data["camera_view"] = cam_view

	##Inserting the record in the DB table
	dbobj.insert_record(predictions_data, db_table)

	##Save violation image to the disk
	if violation_flag == True:
		cv2.imwrite(save_path, result)
		print("Violation image is saved at: ", save_path)

		##Turn on the buzzer if connected - uncomment to enable buzzer trigger
		# buzzer_on()

	else:
		continue

