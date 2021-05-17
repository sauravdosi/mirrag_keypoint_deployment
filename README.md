# Keypoint Detection Model - Staircase Predicitons for P&G

## Steps to run the deployment code in your local machine:

## Setting up
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

4. Download the keypoint-model detection [weights](). Unzip the weights file in the main directory and name the directory as weights.
5. 

