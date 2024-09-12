
import boto3
import os

import firebase_admin
from time import gmtime, strftime
from firebase_admin import credentials, firestore
# from weapondetector.encryption import encrypt

import json
import requests
import google.auth.transport.requests
from google.oauth2 import service_account

# Constants
MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

ENCRYPTION_KEY = "2b7e151628aed2a6abf7158809cf4f3c"
AWS_ACCESS_KEY_ID = "AKIA4VAG3ZGWG3XQC2XJ"
AWS_SECRET_ACCESS_KEY = "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"

FIREBASE_SECRET_KEY_PATH = f"{MAIN_PATH}/assets/secret-key.json"
SCHOOL_ID = os.environ.get("SCHOOL_ID")
BUCKET_NAME = 'weapondetection'
REGION_NAME = 'eu-north-1'
# print(f"School ID: {SCHOOL_ID}")

# New Firebase Contansts
PROJECT_ID = 'weapondetection-38e62'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


# Initialize Firebase
cred = credentials.Certificate(FIREBASE_SECRET_KEY_PATH)
app = firebase_admin.initialize_app(cred)
store = firestore.client()

# Firestore references
collection_name = 'schools'
fcm_field = 'school_fcm_token'
doc_ref = store.collection(collection_name).document(SCHOOL_ID)


# Notification flags
flags = {'alerts': 0,
         'critical_alerts': 0,
         'danger_alerts': 0,
         'red_alerts': 0}

# AWS S3 Client
s3 = boto3.resource(
    service_name='s3',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


# firebase notifications access token
def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

    :return: Access token.
    """
    credentials = service_account.Credentials.from_service_account_file(
        FIREBASE_SECRET_KEY_PATH, scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


def send_notification(device_tokens, data_dict):
    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
    }

    payload = {
        'message': {
            'notification': {
                'title': 'Weapon Detected',
                'body': 'Tap to view the Video'
            },
            'data': data_dict,
            'token': device_tokens
        }
    }

    response = requests.post(
        FCM_URL,
        headers=headers,
        data=json.dumps(payload),
    )

    # if response.status_code == 200:
    # print(f'Message sent to Firebase for delivery, response: {response.text}')
    # else:
    # print('Unable to send message to Firebase')
    # print(response.text)

    return response


def upload_media(video_file_path, img_file_path, camera_name, accuracy):

    video_f_name = video_file_path.split('/')[-1]
    img_f_name = img_file_path.split('/')[-1]

    s3.Bucket(BUCKET_NAME).upload_file(Filename=img_file_path, Key=f'thumbnails/{img_f_name}')
    s3.Bucket(BUCKET_NAME).upload_file(Filename=video_file_path, Key=f'videos/{video_f_name}')

    vid_url = f"https://d3j29qile9de9p.cloudfront.net/videos/{video_f_name}"
    img_url = f"https://d3j29qile9de9p.cloudfront.net/thumbnails/{img_f_name}"

    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    data = {'date_time': current_time,
            'location': camera_name,
            'thumbnail_url': img_url,
            'video_url': vid_url,
            'title': 'Weapon'
            }

    if 0 <= accuracy <= 0.75:
        doc = 'alerts'
    elif 0.75 < accuracy <= 0.80:
        doc = 'critical_alerts'
    elif 0.80 < accuracy <= 0.85:
        doc = 'danger_alerts'
    else:
        doc = 'red_alerts'

    notification_data = doc_ref.collection('notifications').document(doc)

    if not notification_data.get().exists:
        notification_data.create({
            'notification_list': firestore.ArrayUnion([data])
        })
    else:
        if flags[doc] == 0:
            notification_data.set({
                'notification_list': firestore.ArrayUnion([data])
            })
            flags[doc] = 1
        else:
            notification_data.update({
                'notification_list': firestore.ArrayUnion([data])
            })

    resp = doc_ref.update({
        'recent_detection': data
    })

    fcm = doc_ref.get().get(fcm_field)
    resp = send_notification(fcm, data)
