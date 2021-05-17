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
python client.py --cam_id 0
```
The value argument --cam_id is read from the camdata.json. Make sure to run the client.py file for whichever camera you need to run the model for.
E.g. If cam_id 0 belongs to a side view camera, the server will automatically process the feed for side view.

## Activating Cronjob:

If you are using a Windows system, please follow this [YouTube tutorial](https://www.youtube.com/watch?v=CAH0B1ErriI) to execute the [cronjob.py](https://github.com/sauravdosi/mirrag_keypoint_deployment/blob/main/cronjob.py) file at the end of each day.
