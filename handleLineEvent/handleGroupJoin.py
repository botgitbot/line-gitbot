import globalVariable
from config import placeholderWebhook 
from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import sendStringToGroup
def handleGroupJoin(group_id):
    # kalo diinvite, cek apakah group id ada di database bagian inactive. kalo ada, pindah ke active. kalo gada, brarti group baru, buat key baru di bagian active. valuenya kasih sembarang, misal true dulu(dia cuman jadi placeholder yang bakal ditindih, kalo akhirnya group tersebut make webhook). jangan lupa update fireabase setiap kali ada perubahan database
    if(group_id in globalVariable.database["inactive"].keys()):
        sendStringToGroup(group_id, "Hi there!")
        globalVariable.database["active"][group_id] = globalVariable.database["inactive"][group_id]
        del globalVariable.database["inactive"][group_id]
        setFirebaseFromDatabase()
    else:
        sendStringToGroup(group_id, "try !help")
        globalVariable.database["active"][group_id] = placeholderWebhook
        setFirebaseFromDatabase()