from rsa import encrypt
from utils.lineUtils import replyString
from utils.utils import decryptGroupId, encryptGroupId
# import globalVariable

def handleAddRepo(reply_token, group_id):
    # reply with a webhook link sesuai dengan groupid mereka (di encrypt dulu ye) formatnya https://domain.com/webhook/<encryptedgroupid>
    encrypted = encryptGroupId(group_id)
    link = "https://domain.com/webhook/" + encrypted
    decrypted = decryptGroupId(encrypted)
    replyString(reply_token, "addrepo is not yet implemented"  + "\n" + link + "\nkalo di decrypt jadi" + decrypted)
    