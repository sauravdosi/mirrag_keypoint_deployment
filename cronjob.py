# with open('timestamps.txt', 'a+') as file:
	# file.write(str(datetime.now()))
import os, datetime
import shutil
from config import ConfigTF

config = ConfigTF()
retention_period = int(config.get_config("retention_period"))

delete_day = datetime.datetime.now() - datetime.timedelta(retention_period)
delete_month = delete_day.strftime("%Y/%m")
delete_day = delete_day.strftime("%d")
print(delete_day)

retention_dir = config.get_config("out_path") + "/" + delete_month

list_dir = os.listdir(retention_dir)

delete_path = retention_dir + "/" + delete_day

l2 = os.walk(delete_path)
print()
# folders = os.listdir(violations_dir + str(datetime.today().strftime("%Y")))

if os.path.exists(delete_path):

	try:
		shutil.rmtree(delete_path)

	except:
		print("No such path exists.")