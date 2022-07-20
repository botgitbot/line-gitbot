
from handleGithubEvent.githubEventStripper import addRepoStripper
from handleGithubEvent.handleAddRepo import handleAddRepo
from utils.lineUtils import sendStringToGroup


def githubEventRouter(payload, group_id):
    # nge strip informasi yang dibutuhkan dari payload, tros manggil fungsi2 lainnya.
    # tiap handler punya stripper sendiri yang ada di file githubEventStripper
    if("zen" in payload.keys()):
        sendStringToGroup(group_id, "ada webhook baru")
        hookId, username, repo = addRepoStripper(payload)
        handleAddRepo(group_id, hookId, username, repo)
    elif("action" in payload.keys()):
        sendStringToGroup(group_id, "ada action " + str(payload["action"]))
    else:
        sendStringToGroup(group_id, "ada push atau merge")


        
