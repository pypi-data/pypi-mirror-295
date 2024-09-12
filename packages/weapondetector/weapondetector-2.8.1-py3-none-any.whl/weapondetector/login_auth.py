import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCa4-p5B4K-y_IEc2ieuaPtSTcejDGy4Po",
    "authDomain": "weapondetection-38e62.firebaseapp.com",
    "databaseURL": "https://weapondetection-38e62.firebaseio.com",
    "projectId": "weapondetection-38e62",
    "storageBucket": "weapondetection-38e62.appspot.com",
    "messagingSenderId": "243118132308",
    "appId": "1:243118132308:web:6e43da7fa9d78a334e31c1",
    "measurementId": "G-M5JS2E7B95"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


def login_auth(email: str, password: str):

    try:
        login = auth.sign_in_with_email_and_password(email, password)
        return login
    except:
        return False
