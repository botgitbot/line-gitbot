
from handleLineEvent.handleAddRepo import handleAddRepo
from handleLineEvent.handleGroupJoin import handleGroupJoin
from handleLineEvent.handleGroupLeave import handleGroupLeave
from handleLineEvent.handleManualDelete import handleManualDelete
from handleLineEvent.handleShowRepo import handleShowRepo
from handleLineEvent.handleSendHelp import handleSendHelp
from utils.lineUtils import replyString
from utils.utils import addGroupIdToActive, isGroupIdRecorded, sanitizeMessage
# udah gada campur tangan sama flask

def lineEventRouter(type, event):
    if(type == "join"):
        handleGroupJoin(event.source.group_id)
    elif(type == "leave"):
        handleGroupLeave(event.source.group_id)
    elif(type == "message"):
        # 'strip down' event, to get only the data we need
        msg_from_user = event.message.text
        reply_token = event.reply_token
        source_type = event.source.type
        source_id = event.source.user_id

        if (source_type == 'user'):
            source_id = event.source.user_id
        elif (event.source.type == 'group'):
            source_id = event.source.group_id
        
        # validate event
        if msg_from_user[0] != '!':
            return
        if source_type == 'user':
            replyString(reply_token, "Line gitbot is only available for group chat.")
            return

        msg_from_user = sanitizeMessage(msg_from_user)

        # check if group id recorded
        if not isGroupIdRecorded(source_id):
            addGroupIdToActive(source_id)
        # Route event to the correct handler
        if msg_from_user == '!add':
            handleAddRepo(reply_token, source_id)
            
        elif msg_from_user == '!show':
            handleShowRepo(reply_token, source_id)

        elif msg_from_user == '!help':
            handleSendHelp(reply_token)
            
        elif msg_from_user[:14] == '!manualdelete ':
            handleManualDelete(reply_token, source_id, msg_from_user)
        else:
            # coba suruh send !help mungkin
            pass


# #    RUN FLASK APP
# import os
# if __name__ == "__main__":
#     portObject = int(os.environ.get('PORT', config.PORT))
#     app.run(host='0.0.0.0', port=portObject)