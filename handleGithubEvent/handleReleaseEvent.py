from utils.lineUtils import sendFlexMessageToGroup, flexMessageWithUrlClass


def handleReleaseEvent(group_id, repo_title, action, is_prerelease, user, release_title, release_url, release_tag):

    text_content = f"{user} {action} release \"{release_title}\" with tag {release_tag}"
    if action == "published" and not(is_prerelease):
        flex_message = flexMessageWithUrlClass(repo_title, text_content, release_url, "See Release").flexMessageTemplate
        sendFlexMessageToGroup(group_id, flex_message)
