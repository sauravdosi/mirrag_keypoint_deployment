import json

class ConfigTF:
    def __init__(self):
        self.model_details = {"birdseye_coordinates": [[120,422],[552,230],[637,697],[973,309]],
                              "new_calib_pt" : [[857, 330], [923, 339], [903, 373]],
                              "image_width" : 1200,
                              "image_height" : 720,
                              "distance_threshold" : 200,
                              "class_threshold" : 0.485,
                              "machine_point_x" : 810,
                              "machine_point_y" : 368,
                              "classes": {1: "person"},
                              "model_version": 1.0
                              
                              }
        self.db_details = {"model_version": 1.0,
                           "db_username": "root",
                           "db_password": "rhoc8FAIH-pat8yuwn",
                           "db_hostip": "mirrag-prd.ceitcse6sbtm.ap-south-1.rds.amazonaws.com",
                           "db_port": "5432",
                           "db_database": "mirrag_prd",
                           "db_table": "staircase_predictions"}

        self.path_details = {"base_path": "C:/Users/Asus/Desktop/Mirrag/Keypoint-Detection",
                             "inference_path":"",
                             "checkpoint_path":"/weights/saved_model",
                             "video_path_side":"C:/Users/Asus/Desktop/Mirrag/Keypoint-Detection/side-view.mp4",
                             "video_path_front": "C:/Users/Asus/Desktop/Mirrag/Keypoint-Detection/front-view.mp4",
                             "out_path": "C:/Users/Asus/Desktop/Mirrag/Keypoint-Detection/violations_data"}

        self.parameters = {"original_fps": 30, ##FPS of the original video
                           "streaming_fps": 4, ##Feed rate for frames sent to the image hub from the client to the server
                           "retention_period": 2, ##Number of days after which the images should be deleted
                           "buzzer_serial_address": "COM4" ##Buzzer's serial address
                          }

                             ## include all configurable numbers in the file

    def get_config(self, key):
        if key in (self.model_details):
            return self.model_details[key]
        elif key in (self.db_details):
            return self.db_details[key]
        elif key in (self.path_details):
            return self.path_details[key]
        elif key in (self.parameters):
            return self.parameters[key]
        else:
            with open('./config_final.json') as json_file:
                data = json.load(json_file)
                if key in data:
                    return data[key]
                return data["cameras"][key]
