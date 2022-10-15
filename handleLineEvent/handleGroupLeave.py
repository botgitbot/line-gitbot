import globalVariable
from utils.firebaseUtils import setFirebaseFromDatabase

def handleGroupLeave(group_id):
    # kalo leave group, pindah data group dari active ke inactive. jangan lupa update firebase setiap kali update database.
    if(group_id in globalVariable.database["active"].keys()):
        globalVariable.database["inactive"][group_id] = globalVariable.database["active"][group_id]
        del globalVariable.database["active"][group_id]
        setFirebaseFromDatabase()
    pass