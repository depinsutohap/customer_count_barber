from mailjet_rest import Client
import os
import base64
from pathlib import PureWindowsPath
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.environ.get("API_KEY_EMAIL")
api_secret = os.environ.get("API_SECRET_EMAIL")
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
datenow = "2025.06.29"
# upload_folder = "C:\\work\\computer vision\\uploads\\"+datenow
BASE_PATH = os.getenv('BASE_PATH')
upload_folder = BASE_PATH+"/uploads/"+datenow
extract_folder = upload_folder + "_extract"
image_files = [os.path.join(extract_folder, f) for f in os.listdir(extract_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
image_files.sort()
header = "<h1>Total Customer: "+str(int(len(image_files)/2))+"</h1><table border='1px'><th>No.</th><th>Duration</th><th>Images</th>"
attachments = []
counter = 1
i=0
while i < len(image_files)-1:
	header += "<tr>"
	header += "<td>"+str(counter)+".</td>"
	counter+=1
	temp1 = PureWindowsPath(image_files[i]).parts[-1].split(".")[2][3:11]
	temp2 = PureWindowsPath(image_files[i+1]).parts[-1].split(".")[2][3:11]
	date1 = datetime.strptime(temp1, "%H-%M-%S")
	timestamp_seconds = date1.hour*3600 + date1.minute*60 + date1.second
	date2 = datetime.strptime(temp2, "%H-%M-%S")
	timestamp_seconds2 = date2.hour*3600 + date2.minute*60 + date2.second
	diff_seconds = timestamp_seconds2 - timestamp_seconds
	header += "<td>"+str(int(diff_seconds/60))+" Minutes "+str(diff_seconds%60) +"Seconds</td>"
	header += "<td>"+os.path.basename(image_files[i])+", "+os.path.basename(image_files[i+1])+"</td>"
	header += "</tr>"
	i+=2
header += "</table>"
data = {
  'Messages': [
				{
					"From": json.loads(os.getenv('EMAIL_FROM')),
					"To": json.loads(os.getenv('EMAIL_TO')),
					"Cc": json.loads(os.getenv('EMAIL_CC')),
					"Subject": "Auto Generate Report by Depin Sutohap "+datenow,
					# "TextPart": images,
					"HTMLPart": header,
					"Attachments": attachments
				}
		]
}
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())