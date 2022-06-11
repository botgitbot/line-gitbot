# semua file gaboleh nyentuh firebase module secara langsung, harus pake fungsi yang ada di file ini


import firebase_admin
from firebase_admin import credentials

# di firebase, satu buah project bisa terdiri atas beberapa app. kita cuman pake satu
# once the code below this comment is run, a new app will be created. that app doesn't have to be stored in a variable. I'm not quite sure how it works underneath, but let's assume the data is stored inside the firebase admin library
cred = credentials.Certificate("firebaseCredential.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://line-github-bot-default-rtdb.asia-southeast1.firebasedatabase.app/'
})



from firebase_admin import db

ref = db.reference("/")

import json
with open("book_info.json", "r") as f:
	file_contents = json.load(f)
ref.set(file_contents)

from globalVariable import database
# getData
def setDatabaseFromFirebase():
    global database
    ref = db.reference("/")
    # i still need to check if the return of ref.get is json or any other data structure, and then need to be converted to python dictionary
    database = ref.get()

# updateData
def setFirebaseFromDatabase():
    ref = db.reference("/")
    ref.set(database)