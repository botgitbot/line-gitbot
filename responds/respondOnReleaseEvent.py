from utils.lineUtils import sendStringToGroup, pushFlexMessageTemplateTitleTextToGroup


def respondOnReleaseEvent(username, repo, event, group_id):
    usernameandrepo = username + "/" + repo
    string_to_chat = f"{event['actor']['login']} released tag {event['payload']['release']['tag_name']} \"{event['payload']['release']['name']}\""
    print(string_to_chat)
    uri = event['payload']['release']['url']
    pushFlexMessageTemplateTitleTextToGroup(group_id, usernameandrepo, string_to_chat, uri)