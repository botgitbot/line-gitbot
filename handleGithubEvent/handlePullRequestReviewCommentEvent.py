from utils.lineUtils import flexMessageWithUrlClass, sendFlexMessageToGroup


def handlePullRequestReviewCommentEvent(group_id, repo_title, author, pull_request_title, comment_body, comment_url):
    
    text_content = f"{author} commented on pull request \"{pull_request_title}\":\n\"{comment_body}\""
    flex_message = flexMessageWithUrlClass(repo_title, text_content, comment_url, "See Comment").flexMessageTemplate
    sendFlexMessageToGroup(group_id, flex_message)