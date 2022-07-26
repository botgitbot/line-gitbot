from utils.lineUtils import sendFlexMessageToGroup, standardFlexMessageClass, flexMessageWithUrlClass


def handlePullRequestEvent(group_id, repo_title, payload):
    action = payload["action"]
    user = payload["pull_request"]["user"]["login"]
    pull_request_title = payload["pull_request"]["title"]
    head_ref = payload["pull_request"]["head"]["ref"]
    base_ref = payload["pull_request"]["base"]["ref"]
    requested_reviewers = payload["pull_request"]["requested_reviewers"]
    
    text_content = f"{user} {action} pull request \"{pull_request_title}\" from {head_ref} to {base_ref}"
    if len(requested_reviewers) > 0:
        text_content += f"\n  - With request review from:"
        for reviewer in requested_reviewers:
            text_content += f"\n    - {reviewer['login']}"
    
    if action == "opened" or action == "reopened":
        pull_request_url = payload["pull_request"]["url"]
        flex_message = flexMessageWithUrlClass(repo_title, text_content, pull_request_url, "See Pull Request").flexMessageTemplate
        sendFlexMessageToGroup(group_id, flex_message)
    elif action == "closed":
        flex_message = standardFlexMessageClass(repo_title, text_content).flexMessageTemplate
        sendFlexMessageToGroup(group_id, flex_message)