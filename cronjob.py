import os, datetime
import shutil
from config import ConfigTF

config = ConfigTF()
retention_period = int(config.get_config("retention_period"))

delete_day = datetime.datetime.now() - datetime.timedelta(retention_period)
delete_day = delete_day.strftime("%Y/%m/%d")

print("All the images captured on " + str(delete_day) + " will be erased.")

retention_dir = config.get_config("out_path") + "/" + delete_day

totalFiles = 0
totalDir = 0

for base, dirs, files in os.walk(retention_dir):
    print('Counting files: ', base)
   
    for Files in files:
        totalFiles += 1

print('Total number of files',totalFiles)

if os.path.exists(delete_path):

	try:
# 		shutil.rmtree(delete_path)
		print("This directory is deleted.")

	except:
		print("No such path exists.")
