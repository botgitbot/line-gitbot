import firebase_admin
from firebase_admin import credentials, db
import os
from globalVariable import config


import firebase_admin
from firebase_admin import credentials

# di firebase, satu buah project bisa terdiri atas beberapa app. kita cuman pake satu
# once the code below this comment is run, a new app will be created. that app doesn't have to be stored in a variable. I'm not quite sure how it works underneath, but let's assume the data is stored inside the firebase admin library
# by importing firebaseutils in app, code nya di run(emang gitu cara kerja python)
cred = credentials.Certificate("firebaseCredential.json")
# certificate = credentials.Certificate(config['FIREBASE_KEY_API'])
firebase_admin.initialize_app(cred,{
    'databaseURL': os.environ['FIREBASE_DATABASE_URL']
})


from firebase_admin import db



from globalVariable import database
# getData
def setDatabaseFromFirebase():
    global database
    ref = db.reference("/")
    # get ngereturn dictonary
    database = ref.get()

# updateData
def setFirebaseFromDatabase():
    ref = db.reference("/")
    # set nerima dictionary
    ref.set(database)

