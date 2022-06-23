import firebase_admin
from firebase_admin import credentials, db
import os


import firebase_admin
from firebase_admin import credentials

# create firebaseCredential based on env
fc = {
    "type": os.getenv("FIREBASE_CREDENTIAL_TYPE"),
    "project_id": os.getenv("FIREBASE_CREDENTIAL_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_CREDENTIAL_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_CREDENTIAL_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CREDENTIAL_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CREDENTIAL_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_CREDENTIAL_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_CREDENTIAL_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_CREDENTIAL_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CREDENTIAL_CLIENT_X509_CERT_URL")
}


# di firebase, satu buah project bisa terdiri atas beberapa app. kita cuman pake satu
# once the code below this comment is run, a new app will be created. that app doesn't have to be stored in a variable. I'm not quite sure how it works underneath, but let's assume the data is stored inside the firebase admin library
# by importing firebaseutils in app, code nya di run(emang gitu cara kerja python)
cred = credentials.Certificate(fc)
# certificate = credentials.Certificate(config['FIREBASE_KEY_API'])
firebase_admin.initialize_app(cred,{
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
})
from firebase_admin import db



import globalVariable
# getData
def setDatabaseFromFirebase():
    ref = db.reference("/")
    # get ngereturn dictonary
    temp = ref.get()
    if temp == None:
        temp = {}
    globalVariable.database = temp


# updateData
def setFirebaseFromDatabase():
    ref = db.reference("/")
    # set nerima dictionary
    ref.set(globalVariable.database)

