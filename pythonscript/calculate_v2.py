import os
import datetime
from ultralytics import YOLO
from pathlib import PureWindowsPath
import numpy as np
from PIL import Image
import sys
import cv2
from mailjet_rest import Client
import os
import base64
from pathlib import PureWindowsPath
import os
from dotenv import load_dotenv

load_dotenv()

def get_image_contrast(image_path: str) -> float:
    """Calculates the contrast of an image."""
    try:
        img = Image.open(image_path).convert('L')
        img_array = np.array(img)
        std_dev = np.std(img_array)
        return std_dev
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def process_image(image_path: str, model: YOLO) -> dict:
    """Processes an image using the YOLO model."""
    result = model(image_path, save=True, project=BASE_PATH+"/uploads/"+datenow+"_predict")
    if len(result) > 0:
        summary_result = result[0].summary()
        prediction_customer_on = None
        prediction_customer_off = None
        for prediction in summary_result:
            print(f"Image Prediction Result : {prediction}")
            if  prediction["name"] == "customer_on" and check_coordiate(prediction["box"]) and prediction["confidence"] > 0.75:
                prediction_customer_on = prediction
            elif prediction["name"] == "customer_off" and prediction["confidence"] > 0.9 and check_coordiate(prediction["box"]):
                prediction_customer_off = prediction
        return {"prediction_customer_on": prediction_customer_on, "prediction_customer_off": prediction_customer_off}
    return {"prediction_customer_on": prediction_customer_on, "prediction_customer_off": prediction_customer_off}

def check_coordiate(box):
    if 300 <= box["x1"] <= 550 and 150 <= box["y1"] <= 600 and 1000 <= box["x2"] <= 1250 and 800 <= box["y2"] <= 1300:
        return True
    return False

def get_minutes_seconds(total_seconds):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return minutes, seconds
    
def send_email(datenow):
    api_key = os.environ.get("API_KEY_EMAIL")
    api_secret = os.environ.get("API_SECRET_EMAIL")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
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
        date1 = datetime.datetime.strptime(temp1, "%H-%M-%S")
        timestamp_seconds = date1.hour*3600 + date1.minute*60 + date1.second
        date2 = datetime.datetime.strptime(temp2, "%H-%M-%S")
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
datenow = datetime.datetime.now().strftime('%Y.%m.%d')
BASE_PATH = os.getenv('BASE_PATH')
def main():
    print(BASE_PATH)
    log_file = open(BASE_PATH+"/pythonscript/logger/"+datenow+".log","w")
    sys.stdout = log_file
    start_time = datetime.datetime.now()
    print(f"Start {start_time}")
    model = YOLO(BASE_PATH+'/pythonscript/best.pt')
    upload_folder = BASE_PATH+"/uploads/"+datenow
    extract_folder = upload_folder + "_extract"
    os.makedirs(extract_folder, exist_ok=True)
    image_files = [os.path.join(upload_folder, f) for f in os.listdir(upload_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    image_files.sort()
    current_person = None
    haircut_images = []
    count_face = 0
    haircut_count = 0
    for i, image_path in enumerate(image_files):
        print(f"Progress {i} from {len(image_files)}")
        print(image_path)
        contrast = get_image_contrast(image_path)
        if contrast is not None:
            print(f"Image Contrast is: {contrast}")
            if contrast <= 45:
                print(f"Image Contrast too Low {contrast}")
                continue
        result = process_image(image_path, model)
        if result:
            prediction_customer_on = result["prediction_customer_on"]
            prediction_customer_off = result["prediction_customer_off"]
            print(f"choosed customer on {prediction_customer_on}")
            print(f"choosed customer off {prediction_customer_off}")
            if current_person is None:
                if prediction_customer_on is not None:
                    print("Start Counting")
                    current_person = image_path
            elif current_person is not None:
                print(f"current_person {current_person}")
                if prediction_customer_off is not None and prediction_customer_on is None:
                    date1 = datetime.datetime.strptime(current_person.split("/")[-1].split(".")[2][3:11], "%H-%M-%S")
                    date2 = datetime.datetime.strptime(image_path.split("/")[-1].split(".")[2][3:11], "%H-%M-%S")
                    timestamp_seconds = date1.hour*3600 + date1.minute*60 + date1.second
                    timestamp_seconds2 = date2.hour*3600 + date2.minute*60 + date2.second
                    diff_seconds = timestamp_seconds2 - timestamp_seconds
                    minutes, seconds = get_minutes_seconds(diff_seconds)
                    print(f"cutting hair take time {minutes} minutes {seconds} seconds")
                    if minutes > 15:
                        print("Counted")
                        os.popen('cp "'+current_person+'" "'+extract_folder+'"')
                        os.popen('cp "'+image_files[i-1]+'" "'+extract_folder+'"')
                    else:
                        print("Not Counted")
                    current_person = None
    
    end_time = datetime.datetime.now() - start_time
    print(f"Finish {end_time}")
    send_email(datenow)
    log_file.close()
if __name__ == "__main__":
    main()