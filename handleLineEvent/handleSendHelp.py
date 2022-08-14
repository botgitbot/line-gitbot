
from utils.lineUtils import replyFlexMessageTemplateTitleText

def handleSendHelp(reply_token):
    replyFlexMessageTemplateTitleText(reply_token,"Try sending these messages!", "!help - show help message\n!add - give a URL that can be added to your repository's webhook to track the repository\n!show - show all tracked repositories\n!manualdelete {username}/{repo} - manually remove a repository from the list (notes: the repository will still be tracked unless you remove the webhook url directly from GitHub)")

        
