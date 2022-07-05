from utils.lineUtils import sendStringToGroup


def respondOnReleaseEvent(username, repo, event, group_id):
    usernameandrepo = username + "/" + repo
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} released tag {event['payload']['release']['tag_name']} \"{event['payload']['release']['name']}\""
    print(string_to_chat)
    sendStringToGroup(group_id, string_to_chat)