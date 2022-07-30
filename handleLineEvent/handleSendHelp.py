
from utils.lineUtils import replyFlexMessageTemplateTitleText

def handleSendHelp(reply_token):
    replyFlexMessageTemplateTitleText(reply_token,"try sending these message!", "!help - show this message\n!add - give a link that you can add to repo's webhook to be tracked\n!show - show all repo's that you are tracking")

        