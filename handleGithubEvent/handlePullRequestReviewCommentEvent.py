from utils.lineUtils import flexMessageWithUrlClass, sendFlexMessageToGroup


def handlePullRequestReviewCommentEvent(group_id, repo_title, payload):
    author = payload["comment"]["user"]["login"]
    pull_request_title = payload["pull_request"]["title"]
    comment_body = payload["comment"]["body"]
    comment_url = payload["comment"]["url"]
    text_content = f"{author} commented on pull request \"{pull_request_title}\":\n\"{comment_body}\""
    flex_message = flexMessageWithUrlClass(repo_title, text_content, comment_url, "See Comment").flexMessageTemplate
    sendFlexMessageToGroup(group_id, flex_message)