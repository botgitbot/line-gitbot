import os
from rsa import encrypt
from utils.lineUtils import replyString
from utils.utils import decryptGroupId, encryptGroupId
# import globalVariable

def handleAddRepo(reply_token, group_id):
    # reply with a webhook link sesuai dengan groupid mereka (di encrypt dulu ye) formatnya https://domain.com/webhook/<encryptedgroupid>
    encrypted = encryptGroupId(group_id)
    link = "https://line.gitbot.my.id/webhook/" + encrypted
    replyString(reply_token, "Please add following URL to your repository webhook (Repository page > Settings > Webhooks > Add webhook):"  + "\n" + link)
    
