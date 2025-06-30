from mailjet_rest import Client
import os
import base64
from pathlib import PureWindowsPath
from datetime import datetime
api_key = "bd0841ed74847f0cd42967e932c579d2"
api_secret = "42da03112f5607ab580cd383b03ada1d"
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
datenow = "2025.06.28"
# upload_folder = "C:\\work\\computer vision\\uploads\\"+datenow
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
##Create zip of images and send it as attachment
# os.popen('tar -a -c -f "'+extract_folder+'.zip" "C:\\work\\computer vision\\uploads"')
# with open(extract_folder+'.zip', "rb") as file:
# 	s = base64.b64encode(file.read()).decode("utf-8")
# 	attachments.append({
# 		"ContentType": "application/zip",
# 		"Filename": os.path.basename(extract_folder+'.zip'),
# 		"Base64Content": s
# 	})
data = {
  'Messages': [
				{
						"From": {
                            "Email": "sienshum@gmail.com",
                            "Name": "depin sutohap"
						},
						"To": [
								{
								"Email": "faceoffparlour@gmail.com",
								# "Email": "depinsutohap@gmail.com",
								"Name": "Owner of Faceoff Parlour"
								}
						],
                        "Cc": [{"Name" : "Developer", "Email": "depinsutohap@gmail.com"}],
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