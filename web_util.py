import requests
import json

def get_data(company_id,api_key):
	url = "https://65dc8af024699b.localhost.run/edge_api/intrusion?company_code="+str(company_id)+"&api_key="+str(api_key)

	payload={}
	response = requests.request("GET", url, data=payload)
	print(response.text)
	return response

def insert_data(company_id,api_key,data_dict):
	url = "https://65dc8af024699b.localhost.run/edge_api/intrusion?company_code=" + str(company_id) + "&api_key=" + str(
		api_key)

	payload = json.dumps(data_dict)
	headers = {
		'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	print(response.text)
	return response
	'''payload = json.dumps({
	  "model_version": 1.0,
	  "camera_id": 1,
	  "is_violation": True,
	  "img_path": "/c1/2020/05/06/img.jpg",
	  "out_data": {
		"person": [
		  1,
		  2,
		  3,
		  4
		],
		"dist": [
		  20,
		  30,
		  12,
		  10
		]
	  },
	  "prediction_time": "2020-03-31 23:23:23"
	})'''


