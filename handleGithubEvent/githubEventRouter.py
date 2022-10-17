
from handleGithubEvent.githubEventStripper import addWebhookToRepoStripper, deleteRepoStripper, pullRequestEventStripper, pullRequestReviewCommentEventStripper, pushEventStripper, releaseEventStripper
from handleGithubEvent.handleAddWebhookToRepo import handleAddWebhookToRepo
from handleGithubEvent.handleDeleteRepo import handleDeleteRepoEvent
from utils.lineUtils import sendStringToGroup
from handleGithubEvent.handlePushEvent import handlePushEvent
from handleGithubEvent.handlePullRequesteEvent import handlePullRequestEvent
from handleGithubEvent.handleReleaseEvent import handleReleaseEvent
from handleGithubEvent.handlePullRequestReviewCommentEvent import handlePullRequestReviewCommentEvent
from utils.utils import addWebhookToDatabase, isWebhookRecorded
def githubEventRouter(payload, group_id):
    # nge strip informasi yang dibutuhkan dari payload, tros manggil fungsi2 lainnya.
    # tiap handler punya stripper sendiri yang ada di file githubEventStripper
    if("zen" in payload.keys()):
        # add webhook to repo
        username, repo = addWebhookToRepoStripper(payload)
        handleAddWebhookToRepo(group_id, username, repo)
    else:
        # check apakah webhook udah ada di datatase
        if not isWebhookRecorded(group_id, payload["repository"]["owner"]["login"], payload["repository"]["name"]):
            addWebhookToDatabase(group_id, payload["repository"]["owner"]["login"], payload["repository"]["name"])

        if("pusher" in payload.keys()):
            # push or merge
            repo_title, pusher, ref, commits, compare_changes_url = pushEventStripper(payload)
            handlePushEvent(group_id, repo_title, pusher, ref, commits, compare_changes_url)

        elif("action" in payload.keys()):
            if ("pull_request" in payload.keys()):
                if(payload["action"] == "opened"):
                    repo_title, action, user, pull_request_title, head_ref, base_ref, requested_reviewers, pull_request_url = pullRequestEventStripper(payload)
                    handlePullRequestEvent(group_id, repo_title, action, user, pull_request_title, head_ref, base_ref, requested_reviewers, pull_request_url)
                if("comment" in payload.keys() and payload["action"] == "created"):
                    repo_title, author, pull_request_title, comment_body, comment_url = pullRequestReviewCommentEventStripper(payload)
                    handlePullRequestReviewCommentEvent(group_id, repo_title, author, pull_request_title, comment_body, comment_url) 

            elif ("release" in payload.keys()):
                if(payload["action"] == "published"):
                    repo_title, action, is_prerelease, user, release_title, release_url, release_tag = releaseEventStripper(payload)
                    handleReleaseEvent(group_id,repo_title, action, is_prerelease, user, release_title, release_url, release_tag)

            elif(payload["action"] == "deleted"):
                username, repo = deleteRepoStripper(payload)
                handleDeleteRepoEvent(group_id, username, repo)


        
