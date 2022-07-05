from utils.lineUtils import sendStringToGroup


def respondOnPullRequestReviewCommentEvent(usernameandrepo, event, group_id):
    string_to_chat = f"[{usernameandrepo}] {event['actor']['login']} commented on pull request \"{event['payload']['pull_request']['title']}\""
    sendStringToGroup(group_id, string_to_chat)
