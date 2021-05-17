import os, datetime
import shutil
from config import ConfigTF

config = ConfigTF()
retention_period = int(config.get_config("retention_period"))

delete_day = datetime.datetime.now() - datetime.timedelta(retention_period)
delete_day = delete_day.strftime("%Y/%m/%d")

print("All the images captured on " + str(delete_day) + " will be erased.")

delete_dir = config.get_config("out_path") + "/" + delete_day

print(delete_dir)

totalFiles = 0
totalDir = 0

print("Counting files in: ", delete_dir)

for base, dirs, files in os.walk(delete_dir):
    
    for Files in files:
        totalFiles += 1

print(totalFiles, " files will be deleted.")


if os.path.exists(delete_dir):

	try:
		shutil.rmtree(delete_dir)
		print("The directory is erased.")

		with open('trash_log.txt', 'a+') as file:
			file.write("On " + str(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S:%f")) + ", " + str(totalFiles) + " files were deleted from " + str(delete_dir) + ".\n")

	except:
		print("No such path exists.")
