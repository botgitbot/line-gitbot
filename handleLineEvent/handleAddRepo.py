from utils.firebaseUtils import setFirebaseFromDatabase
from utils.lineUtils import replyString
from utils.utils import checkIfRepoAndAccessTokenValid, createKeyFromUsernameAndRepo
import globalVariable

def handleAddRepo(reply_token, group_id):
    # reply with a webhook link sesuai dengan groupid mereka (di encrypt dulu ye) formatnya https://domain.com/webhook/<encryptedgroupid>
    pass