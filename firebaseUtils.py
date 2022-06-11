import firebase_admin
from firebase_admin import credentials, db
import os

certificate = credentials.Certificate(os.environ.get('FIREBASE_API_KEY'))
firebaseApp = firebase_admin.initialize_app(certificate, {'databaseURL': os.environ['FIREBASE_DATABASE_URL']})