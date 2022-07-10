from utils.lineUtils import pushFlexMessageTemplateTitleTextUrlToGroup


def respondOnPullRequestReviewCommentEvent(usernameandrepo, event, group_id):
    string_to_chat = f" {event['actor']['login']} commented on pull request \"{event['payload']['pull_request']['title']}\""
    uri = event['payload']['comment']['url']
    pushFlexMessageTemplateTitleTextUrlToGroup(group_id, usernameandrepo, string_to_chat, uri)