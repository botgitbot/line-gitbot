
from handleGithubEvent.githubEventStripper import addRepoStripper
from handleGithubEvent.handleAddWebhookToRepo import handleAddWebhookToRepo
from utils.lineUtils import sendStringToGroup
from handleGithubEvent.handlePushEvent import handlePushEvent
from handleGithubEvent.handlePullRequesteEvent import handlePullRequestEvent
from handleGithubEvent.handleReleaseEvent import handleReleaseEvent
from handleGithubEvent.handlePullRequestReviewCommentEvent import handlePullRequestReviewCommentEvent
def githubEventRouter(payload, group_id):
    # nge strip informasi yang dibutuhkan dari payload, tros manggil fungsi2 lainnya.
    # tiap handler punya stripper sendiri yang ada di file githubEventStripper
    if("zen" in payload.keys()):
        sendStringToGroup(group_id, "ada webhook baru")
        hookId, username, repo = addRepoStripper(payload)
        handleAddWebhookToRepo(group_id, hookId, username, repo)
    else:
        # sendStringToGroup(group_id, "ada action " + str(payload["action"]))
        repo_title = payload["repository"]["full_name"]
        if ("pusher" in payload.keys()):
            handlePushEvent(group_id, repo_title, payload)
        elif("comment" in payload.keys()):
            handlePullRequestReviewCommentEvent(group_id, repo_title, payload)
        elif ("pull_request" in payload.keys()):
            handlePullRequestEvent(group_id, repo_title, payload)
        elif ("release" in payload.keys()):
            handleReleaseEvent(group_id, repo_title, payload)



        
