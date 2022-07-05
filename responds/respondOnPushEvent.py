from utils.lineUtils import sendStringToGroup


def respondOnPushEvent(username, repo, event, group_id):
    usernameandrepo  = username + "/" + repo
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} pushed to branch {event['payload']['ref']} with {event['payload']['size']} commits:"
    print(string_to_chat)
    for commit in event["payload"]["commits"]:
        string_to_chat += f"\n  - {commit['message']}"
    sendStringToGroup(group_id, string_to_chat)