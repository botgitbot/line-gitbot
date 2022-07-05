from utils.lineUtils import sendStringToGroup, pushFlexMessageTemplateTitleTextUrlToGroup


def respondOnPullRequestEvent(username, repo, event, group_id):
    usernameandrepo = username + "/" + repo
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} {event['payload']['action']} pull request \"{event['payload']['pull_request']['title']}\" from {event['payload']['pull_request']['head']['ref']} to {event['payload']['pull_request']['base']['ref']}"
    print(string_to_chat)
    sendStringToGroup(group_id, string_to_chat)
    if event['actor']['login'] == "opened" and event['payload']['pull_request']['requested_reviewers']:
        string_to_chat += " with request to review from: "
        for reviewer in event['payload']['pull_request']['requested_reviewers']:
            string_to_chat += f"\n - {reviewer['login']} "
    uri = event['payload']['pull_request']['url']
    print(string_to_chat)
    sendStringToGroup(group_id, string_to_chat)
    pushFlexMessageTemplateTitleTextUrlToGroup(group_id, "Pull request event", string_to_chat, uri)