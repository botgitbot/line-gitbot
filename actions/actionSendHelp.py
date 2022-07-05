
from utils.lineUtils import replyString


def actionSendHelp(reply_token):
    replyString(reply_token, """
    add first repo with
    `!add [owner]/[repo]:[access_token]`

    help with
    `!help` 

    show repo list with
    `!show`

    delete repo with
    `!delete [owner]/[repo]`
    """)


           