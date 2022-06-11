import firebase_admin
from firebase_admin import credentials, db
import os
from globalVariable import config

certificate = credentials.Certificate(config['FIREBASE_KEY_API'])
firebaseApp = firebase_admin.initialize_app(certificate, {'databaseURL': os.environ['FIREBASE_DATABASE_URL']})