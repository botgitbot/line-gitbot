
from handleGithubEvent.githubEventStripper import addWebhookToRepoStripper, deleteRepoStripper, pullRequestEventStripper, pullRequestReviewCommentEventStripper, pushEventStripper, releaseEventStripper
from handleGithubEvent.handleAddWebhookToRepo import handleAddWebhookToRepo
from handleGithubEvent.handleDeleteRepo import handleDeleteRepoEvent
from utils.lineUtils import sendStringToGroup
from handleGithubEvent.handlePushEvent import handlePushEvent
from handleGithubEvent.handlePullRequesteEvent import handlePullRequestEvent
from handleGithubEvent.handleReleaseEvent import handleReleaseEvent
from handleGithubEvent.handlePullRequestReviewCommentEvent import handlePullRequestReviewCommentEvent
def githubEventRouter(payload, group_id):
    # nge strip informasi yang dibutuhkan dari payload, tros manggil fungsi2 lainnya.
    # tiap handler punya stripper sendiri yang ada di file githubEventStripper
    if("zen" in payload.keys()):
        # add webhook to repo
        hook_id, username, repo = addWebhookToRepoStripper(payload)
        handleAddWebhookToRepo(group_id, hook_id, username, repo)
    elif("ref" in payload.keys()):
        # push or merge
        repo_title, pusher, ref, commits, compare_changes_url = pushEventStripper(payload)
        handlePushEvent(group_id, repo_title, pusher, ref, commits, compare_changes_url)

    elif("action" in payload.keys()):
        print("ada action " + str(payload["action"]))
        if(payload["action"] == "opened"):
            repo_title, action, user, pull_request_title, head_ref, base_ref, requested_reviewers, pull_request_url = pullRequestEventStripper(payload)
            handlePullRequestEvent(group_id, repo_title, action, user, pull_request_title, head_ref, base_ref, requested_reviewers, pull_request_url)

        if(payload["action"] == "deleted"):
            webhook_id, username, repo = deleteRepoStripper(payload)
            handleDeleteRepoEvent(group_id, webhook_id, username, repo)
            
        if(payload["action"] == "created"):
            repo_title, author, pull_request_title, comment_body, comment_url = pullRequestReviewCommentEventStripper(payload)
            handlePullRequestReviewCommentEvent(group_id, repo_title, author, pull_request_title, comment_body, comment_url)

        if(payload["action"] == "published"):
            repo_title, action, is_prerelease, user, release_title, release_url, release_tag = releaseEventStripper(payload)
            handleReleaseEvent(group_id,repo_title, action, is_prerelease, user, release_title, release_url, release_tag)



        
