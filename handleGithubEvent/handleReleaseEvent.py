from utils.lineUtils import sendFlexMessageToGroup, flexMessageWithUrlClass


def handleReleaseEvent(group_id, repo_title, payload):
    action = payload["action"]
    is_prerelease = payload["release"]["prerelease"]
    user = payload["release"]["author"]["login"]
    release_title = payload["release"]["name"]
    release_url = payload["release"]["html_url"]
    release_tag = payload["release"]["tag_name"]

    text_content = f"{user} {action} release \"{release_title}\" with tag {release_tag}"
    if action == "published" and not(is_prerelease):
        flex_message = flexMessageWithUrlClass(repo_title, text_content, release_url, "See Release").flexMessageTemplate
        sendFlexMessageToGroup(group_id, flex_message)
