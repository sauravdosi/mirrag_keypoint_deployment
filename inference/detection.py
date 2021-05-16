import io
import os
import scipy.misc
import numpy as np
import six
import time
import glob
from IPython.display import display
import cv2
from pathlib import Path

from six import BytesIO

import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

import tensorflow as tf
from object_detection.utils import ops as utils_ops
# from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

from config import ConfigTF

config = ConfigTF()
base_path=Path(config.get_config("base_path"))
base_path=r"{}".format(base_path)

inference_path=Path(str(base_path)+config.get_config("inference_path"))
inference_path=r"{}".format(inference_path)
print("Inference path", inference_path)

checkpoint_path=Path(str(inference_path)+config.get_config("checkpoint_path"))
checkpoint_path=r"{}".format(checkpoint_path)
print("Checkpoint path",checkpoint_path)
# from google.colab.patches import cv2_imshow

# %matplotlib inline

tf.keras.backend.clear_session()

#change path
model = tf.saved_model.load(checkpoint_path)

def run_inference_for_single_image(model, image):
  image_np = np.asarray(image)

  input_tensor = tf.convert_to_tensor(image_np)
  input_tensor = input_tensor[tf.newaxis,...]


  # Run inference
  model_fn = model.signatures['serving_default']
  output_dict = model_fn(input_tensor)


  output_dict['keypoint_scores'] = output_dict['detection_keypoint_scores'][0].numpy()
  output_dict['kpts']  = output_dict['detection_keypoints'][0].numpy()
  output_dict['number_detections'] = output_dict['num_detections'][0].numpy()
  output_dict['person_scores'] = output_dict['detection_scores'][0].numpy()
  output_dict['person_box'] = output_dict['detection_boxes'][0].numpy()

 
  return output_dict


def load_image_into_numpy_array(path):
  
  img_data = tf.io.gfile.GFile(path, 'rb').read()
  image = Image.open(BytesIO(img_data))
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


frame_count = 0 # to count total frames
total_fps = 0 # to get the final frames per second

#make a function
lx,rx,ly,ry = None,None,None,None
# distances = []
distance_ankle_threshold = 58
distance_knee_threshold = 29 


def detect_side(img):
    violation = False

    print("calling detect side")
    image = img
    im_height, im_width, c = image.shape
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # get the start time
    start_time = time.time()
    
    frame = np.array(frame, dtype = np.uint8)
    input_tensor = np.expand_dims(frame, 0)
    # print("calling another function")
    output_dict = run_inference_for_single_image(model, frame)

    # print("for loop")
    for i in range(int(output_dict['number_detections'])):
        if output_dict['person_scores'][i] > 0.4:
            (x_min, x_max, y_min, y_max) = (output_dict['person_box'][i][1]*im_width, output_dict['person_box'][i][3]*im_width,output_dict['person_box'][i][0]*im_height, output_dict['person_box'][i][2]*im_height)
            #print(x_min, x_max, y_min, y_max)
            p1 = (int(x_min), int(y_min))
            p2 = (int(x_max), int(y_max))
            cv2.rectangle(image, p1, p2, (0,255,0), 1, 1)

            #left foot
            if output_dict['keypoint_scores'][i][15] > 0.35:
                (ly,lx) = (output_dict['kpts'][i][15][0]*im_height, output_dict['kpts'][i][15][1]*im_width)
                (lx,ly) = (int(lx),int(ly))
                #print(lx,ly)
                cv2.circle(image,(lx,ly),2,(0,255,0),cv2.FILLED)

                #right foot
                if output_dict['keypoint_scores'][i][16] > 0.35:
                    (ry,rx) = (output_dict['kpts'][i][16][0]*im_height, output_dict['kpts'][i][16][1]*im_width)
                    rx,ry = (int(rx),int(ry))
                    #print(rx,ry)
                    cv2.circle(image,(rx,ry),2,(0,255,0),cv2.FILLED)

                    distance_ankle = int(np.sqrt((lx-rx)**2+(ly-ry)**2))

                    cv2.putText(image,"{}".format(distance_ankle),(lx+10,ly+10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),)
                    #distances.append(distance)
                    #print(distance)
                    cv2.line(image,(lx,ly),(rx,ry),(255,0,0),1)
                    if distance_ankle > distance_ankle_threshold:
                        cv2.rectangle(image, p1, p2, (0,0,255), 1, 1)
                        violation = True
                    lx,rx,ly,ry = None,None,None,None

            #left knee
            if output_dict['keypoint_scores'][i][13] > 0.35:
                (ly,lx) = (output_dict['kpts'][i][13][0]*im_height, output_dict['kpts'][i][13][1]*im_width)
                (lx,ly) = (int(lx),int(ly))
                #print(lx,ly)
                cv2.circle(image,(lx,ly),2,(0,255,0),cv2.FILLED)

                #right knee
                if output_dict['keypoint_scores'][i][14] > 0.35:
                    (ry,rx) = (output_dict['kpts'][i][14][0]*im_height, output_dict['kpts'][i][14][1]*im_width)
                    rx,ry = (int(rx),int(ry))
                    #print(rx,ry)
                    cv2.circle(image,(rx,ry),2,(0,255,0),cv2.FILLED) 

                    distance_knee = int(np.sqrt((lx-rx)**2+(ly-ry)**2))

                    cv2.putText(image,"{}".format(distance_knee),(lx+10,ly+10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,0),)
                    #distances.append(distance)
                    #print(distance)
                    cv2.line(image,(lx,ly),(rx,ry),(255,0,0),1)

                    if distance_knee > distance_knee_threshold:
                        cv2.rectangle(image, p1, p2, (0,0,255), 1, 1)
                        violation = True
                    lx,rx,ly,ry = None,None,None,None

    return image, violation
        

lx,rx,ly,ry = None,None,None,None


def detect_front(img):
    violation = False

    print("calling detect front")
    image = img
    im_height, im_width, c = image.shape
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # print(counter)

    # get the start time
    start_time = time.time()
    
    frame = np.array(frame, dtype=np.uint8)
    input_tensor = np.expand_dims(frame, 0)
    # print("calling another function")
    output_dict = run_inference_for_single_image(model, frame)

    cv2.line(image,(380,281),(345,79),(0,0,255),2)
    cv2.line(image,(251,20),(181,209),(0,255,0),2)

    # print("calling for loop")
    for i in range(int(output_dict['number_detections'])):
        if output_dict['person_scores'][i] > 0.4:
            (x_min, x_max, y_min, y_max) = (output_dict['person_box'][i][1]*im_width, output_dict['person_box'][i][3]*im_width,output_dict['person_box'][i][0]*im_height, output_dict['person_box'][i][2]*im_height)
            #print(x_min, x_max, y_min, y_max)
            p1 = (int(x_min), int(y_min))
            p2 = (int(x_max), int(y_max))
            cv2.rectangle(image, p1, p2, (0,0,255), 1, 1)

            #left wrist
            if output_dict['keypoint_scores'][i][9] > 0.35:
                (ly,lx) = (output_dict['kpts'][i][9][0]*im_height, output_dict['kpts'][i][9][1]*im_width)
                (lx,ly) = (int(lx),int(ly))
                #print(lx,ly)
                cv2.circle(image,(lx,ly),2,(0,255,0),cv2.FILLED)

                R_line_x = (1912+ly)
                R_line_x = (R_line_x/5.78)
                R_line_x = int(R_line_x)

                L_line_x = (-697.7 + ly)
                L_line_x = (L_line_x/-2.7)
                L_line_x = int(L_line_x)

                cv2.line(image,(lx,ly),(R_line_x,ly),(0,0,0),1)
                cv2.line(image,(lx,ly),(L_line_x,ly),(0,0,255),1)
                

                R_line_x = R_line_x - 2 #adding few buffer
                L_line_x = L_line_x + 9 


                if lx >= R_line_x:
                    violation  = True
                    cv2.rectangle(image,p1,p2,(0,255,0),2)



                if lx <= L_line_x:
                    violation  = True
                    cv2.rectangle(image,p1,p2,(0,255,0),2)



            #right wrist
            if output_dict['keypoint_scores'][i][10] > 0.35:
                (ly,lx) = (output_dict['kpts'][i][10][0]*im_height, output_dict['kpts'][i][10][1]*im_width)
                (lx,ly) = (int(lx),int(ly))
                #print(lx,ly)
                cv2.circle(image,(lx,ly),2,(0,255,0),cv2.FILLED)

                R_line_x = (1912+ly)
                R_line_x = (R_line_x/5.78)
                R_line_x = int(R_line_x)

                L_line_x = (-697.7 + ly)
                L_line_x = (L_line_x/-2.7)
                L_line_x = int(L_line_x)


                cv2.line(image,(lx,ly),(R_line_x,ly),(0,0,0),1)
                cv2.line(image,(lx,ly),(L_line_x,ly),(0,0,255),1)
                

                R_line_x = R_line_x - 2 #adding few buffer
                L_line_x = L_line_x + 9 #adding few buffer

                if lx >= R_line_x:
                    violation  = True
                    cv2.rectangle(image,p1,p2,(0,255,0),2)



                if lx <= L_line_x:
                    violation  = True
                    cv2.rectangle(image,p1,p2,(0,255,0),2)

            #left elbow
            if output_dict['keypoint_scores'][i][7] > 0.35:
                (ly,lx) = (output_dict['kpts'][i][7][0]*im_height, output_dict['kpts'][i][7][1]*im_width)
                (lx,ly) = (int(lx),int(ly))
                #print(lx,ly)
                cv2.circle(image,(lx,ly),2,(0,255,0),cv2.FILLED)



                L_line_x = (-697.7 + ly)
                L_line_x = (L_line_x/-2.7)
                L_line_x = int(L_line_x)



                cv2.line(image,(lx,ly),(L_line_x,ly),(0,0,255),1)
                


                L_line_x = L_line_x + 9 #adding few buffer


                if lx <= L_line_x:
                    violation  = True
                    cv2.rectangle(image,p1,p2,(0,255,0),2)


        lx,rx,ly,ry = None,None,None,None

    return image, violation
