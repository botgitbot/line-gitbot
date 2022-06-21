
from dotenv import load_dotenv


# SETUP ENV
load_dotenv()
# now you can use value from .env with from `os.environ` or
# `os.getenv`

from firebaseUtils import setDatabaseFromFirebase, setFirebaseFromDatabase
import globalVariable

globalVariable.initialize()

setDatabaseFromFirebase()
print("database sekarang")
print(globalVariable.database)
print(type(globalVariable.database))

print("coba diganti")
globalVariable.database = {"DIGANTI": {"asdf": {"access_token": "asdf"}}}

setFirebaseFromDatabase()
