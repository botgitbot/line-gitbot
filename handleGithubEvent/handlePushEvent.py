from utils.lineUtils import flexMessageWithUrlClass, sendFlexMessageToGroup


def handlePushEvent(group_id, repo_title, pusher, ref, commits, compare_changes_url):
    text_content = f"{pusher} pushed to branch {ref}"
    if len(commits) > 0:
        text_content += f" with {len(commits)} commits:"
        for commit in commits:
            commit_message = commit['message'].rpartition('\n')[0] if '\n' in commit['message'] else commit['message']
            text_content += f"\n  - {commit_message}"
    flex_message = flexMessageWithUrlClass(repo_title, text_content, compare_changes_url, "Compare Changes").flexMessageTemplate
    sendFlexMessageToGroup(group_id, flex_message)