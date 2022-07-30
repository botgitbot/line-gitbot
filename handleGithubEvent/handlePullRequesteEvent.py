from utils.lineUtils import sendFlexMessageToGroup, standardFlexMessageClass, flexMessageWithUrlClass


def handlePullRequestEvent(group_id, repo_title, action, user, pull_request_title, head_ref, base_ref, requested_reviewers, pull_request_url):
  
    
    text_content = f"{user} {action} pull request \"{pull_request_title}\" from {head_ref} to {base_ref}"
    if len(requested_reviewers) > 0:
        text_content += f"\n  - With request review from:"
        for reviewer in requested_reviewers:
            text_content += f"\n    - {reviewer['login']}"
    
    if action == "opened" or action == "reopened":
        flex_message = flexMessageWithUrlClass(repo_title, text_content, pull_request_url, "See Pull Request").flexMessageTemplate
        sendFlexMessageToGroup(group_id, flex_message)
    elif action == "closed":
        flex_message = standardFlexMessageClass(repo_title, text_content).flexMessageTemplate
        sendFlexMessageToGroup(group_id, flex_message)