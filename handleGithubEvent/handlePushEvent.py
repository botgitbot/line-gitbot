from utils.lineUtils import pushFlexMessageTemplateTitleTextToGroup


def handlePushEvent(username, repo, event, group_id):
    usernameandrepo  = username + "/" + repo
    string_to_chat = f"{event['actor']['login']} pushed to branch {event['payload']['ref']} with {event['payload']['size']} commits:"
    print(string_to_chat)
    for commit in event["payload"]["commits"]:
        string_to_chat += f"\n  - {commit['message']}"
    pushFlexMessageTemplateTitleTextToGroup(group_id, usernameandrepo, string_to_chat)