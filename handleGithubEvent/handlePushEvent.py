from utils.lineUtils import flexMessageWithUrlClass, sendFlexMessageToGroup


def handlePushEvent(group_id, repo_title, pusher, ref, commits, compare_changes_url):
    text_content = f"{pusher} pushed to branch {ref}"
    if len(commits) > 0:
        text_content += f" with {len(commits)} commits:"
        for commit in commits:
            text_content += f"\n  - {commit['message']}"
    flex_message = flexMessageWithUrlClass(repo_title, text_content, compare_changes_url, "Compare Changes").flexMessageTemplate
    sendFlexMessageToGroup(group_id, flex_message)