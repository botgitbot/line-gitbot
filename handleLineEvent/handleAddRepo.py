import os
from rsa import encrypt
from utils.lineUtils import replyString
from utils.utils import decryptGroupId, encryptGroupId
# import globalVariable

def handleAddRepo(reply_token, group_id):
    # reply with a webhook link sesuai dengan groupid mereka (di encrypt dulu ye) formatnya https://domain.com/webhook/<encryptedgroupid>
    encrypted = encryptGroupId(group_id)
    link = "https://line.gitbot.my.id/webhook/" + encrypted
    replyString(reply_token, " group id = " + group_id+"\nencryption key = "+ os.getenv("PASSWORD_ENCRYPTION_KEY") +"\nPlease add following link to your repository webhook"  + "\n" + link)
    