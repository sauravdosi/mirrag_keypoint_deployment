# Keypoint Detection Model - Staircase Predicitons for P&G

## Setting up:
1. After having clonned the repository, install [Anaconda](https://www.anaconda.com/products/individual) in your Operating System.
2. Open Anaconda Prompt and make sure you are in (base) environment. Create a virtual environment in conda using python 3.9 by following the instructions given below.
```
conda create -n deploytest python==3.9
```
This will install all python and pip in your virtual environment. Activate your newly created conda environment using following command in (base) environment.

```
conda activate deploytest
```

3. We now need to install a few dependencies to run the staircase model. Run the following command in your virtual environment.

```
pip install -r requirements.txt
```
This command will take a while to execute and install all the required packages.

4. Download the keypoint-model detection [weights](http://download.tensorflow.org/models/object_detection/tf2/20200711/centernet_resnet50_v1_fpn_512x512_kpts_coco17_tpu-8.tar.gz). Unzip this weights folder in the main directory and rename the directory as weights.
5. Open the [config.py](https://github.com/sauravdosi/mirrag_keypoint_deployment/blob/main/config.py) file and make changes in the following fields:
* Verify and edit the Database credentials if necessary
* Edit all the path fields as required
* Make sure to download sample videos and store them preferably in the main directory. Assign these paths to the respective variables.
* Finally, edit the parameters as per the streaming video specifications, for how many days the violation images should be stored and the buzzer module's serial address

6. Make changes in [camdata.json](https://github.com/sauravdosi/mirrag_keypoint_deployment/blob/main/camdata.json) to edit the camera's client IP, camera view and other specifications as required.

## Setting up the Buzzer:

1. If the microprocessor is an Arduino device, download [Arduinio IDE ](https://www.arduino.cc/en/Main/Software_)on your local machine and [buzzer_setup.ino]() using Arduino IDE.
3. If you have your buzzer connected to your local machine via an USB port, you will first have to find out the serial address of the micrprocessor. This can be done by going to Tools options in the toolbar of the IDE and checking for the port of the current microproessor.
4. Once the port of the buzzer device is known, it can be edited in the config.py file and the following two lines in [server.py](https://github.com/sauravdosi/mirrag_keypoint_deployment/blob/main/server.py) can be uncommented.
```
#line 17
# from buzzer import *

#line 160
# buzzer_on()
```
These lines will import buzzer.py and call a function that sends a message to the microprocessor through serial communication which triggers the buzzer.
5.  Make changes in the [buzzer_setip.ino]() file to change the duration of the buzzer's ON status. To do this, change the following line in the code:

```
// Time in milliseconds for which the buzzer will be turned on once a trigger is received
   delay(3000);
```
6. Once this is done, compile and upload the buzzer_setup.ino to the microprocessor. Whenever buzzer.py is executed, it will turn on the buzzer for the desired duration forever until a new code or .ino file is dumped to the microprocessor.


## Architecture:



## Running the Model:

1. Open an Anaconda prompt and activate the already set up virtual environment, if not already.

```
conda activate deploytest
```

2. Run the following command:

```
python server.py
```

3. Open another Anaconda prompt and activate the virtual environment there as well. Now run the following command:

```
python client.py --cam_id 1
```
The value argument --cam_id is read from the [camdata.json](https://github.com/sauravdosi/mirrag_keypoint_deployment/blob/main/camdata.json). Make sure to run the client.py file for whichever camera you need to run the model for.
E.g. If cam_id 1 belongs to a side view camera, the server will automatically process the feed for side view.
You can configure views for each of the cameras in [camdata.json](https://github.com/sauravdosi/mirrag_keypoint_deployment/blob/main/camdata.json) file.

4. You should be seeing all the images being processed in a window with the instantaneous FPS and an Alert flag if there is a violation.



## Activating Cronjob:

If you are using a Windows system, please follow this [YouTube tutorial](https://www.youtube.com/watch?v=CAH0B1ErriI) to execute the [cronjob.py](https://github.com/sauravdosi/mirrag_keypoint_deployment/blob/main/cronjob.py) file at the end of each day.
