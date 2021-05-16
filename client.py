##Setting up client side - Need to configure correct stream path and server address before sending frames to server
from imutils.video import FileVideoStream,VideoStream
import imagezmq
import socket
import os, sys, json, pickle, time
from pathlib import Path
import argparse
from configparser import ConfigParser

##Config file has all the connection information
from config import ConfigTF

##Import the new ConfigTF() function
config = ConfigTF()

##Read info from command line - from which camera to take feed from for this client instance
parser = argparse.ArgumentParser()
parser.add_argument('--cam_id', type=int, default="0")
args = parser.parse_args()

##Get info from config.json file about the server and client
cam_data = config.get_config(args.cam_id - 1)
print("Cam id ",args.cam_id)
server_ip=cam_data["server_ip"]
print(cam_data["cam_view"])  ##Server ip to which we want to send the frames

##Get streaming rate
original_fps = config.get_config("original_fps")
streaming_fps = config.get_config("streaming_fps")
print("Sending frames to the server at " + str(streaming_fps) + " FPS")
nth_frame = int(original_fps/streaming_fps)


cam_metadata = {}

##Read from the config.json file
cam_metadata["company_id"] = config.get_config("company_id")
cam_metadata["company_name"] = config.get_config("company_name")
cam_metadata["cam_id"] = args.cam_id
cam_metadata["cam_view"] = cam_data["cam_view"]

#Metion the video path to be processed in the config file depending on the cam view
if cam_metadata["cam_view"] == "side":
    video_path=Path(config.get_config("video_path_side"))

elif cam_metadata["cam_view"] == "front":
    video_path=Path(config.get_config("video_path_front"))

video_path=r"{}".format(video_path)


##To stream from file
cap = FileVideoStream(video_path)

##To stream address from camera 
# path = "rtsp://192.168.1.70:8080//h264_ulaw.sdp" # Set static IP address if streaming over router
# cap=VideoStream(src=path,resolution=(320,240)) #To read from camera device, if using webcam set src to '0'

##Sending a queue of images from the current video stream to the server to process
sender = imagezmq.ImageSender(connect_to='tcp://{}:5555'.format(server_ip), REQ_REP=True) 
print("Server ip is ", server_ip)
stream = cap.start()

##Sending frames
t0=time.time()
flag=True
counter=0

while flag:
    counter += 1
    frame = stream.read()

    if counter % nth_frame == 0:
     ##Control how many frames to be sent to the server, at what interval
	    try:
	        print("Sending number " + str(counter) +" frame to the server")
	        sender.send_image(cam_metadata, frame)

	    except:
	    	print("Could not send the frame")
	    	flag = False  
        
    else:
    	continue
    	
print("Breaking client at counter",counter)        
print("Total time elapsed:", time.time()-t0)


