def mergePullRequestStripper(payload):
    # ngembaliin data yang dibutuhin dari payload
    return "a", "b", "c"

def addWebhookToRepoStripper(payload):
    # ngembaliin data yang dibutuhin dari payload

    username = payload["sender"]["login"]
    repo = payload["repository"]["name"]
    return username, repo

def pushEventStripper(payload):
    repo_title = payload["repository"]["full_name"]
    pusher = payload["pusher"]["name"]
    ref = payload["ref"]
    commits = payload["commits"]
    compare_changes_url = payload["compare"]
    return repo_title, pusher, ref, commits, compare_changes_url

def pullRequestEventStripper(payload):
    repo_title = payload["repository"]["full_name"]
    action = payload["action"]
    user = payload["pull_request"]["user"]["login"]
    pull_request_title = payload["pull_request"]["title"]
    head_ref = payload["pull_request"]["head"]["ref"]
    base_ref = payload["pull_request"]["base"]["ref"]
    requested_reviewers = payload["pull_request"]["requested_reviewers"]
    pull_request_url = payload["pull_request"]["html_url"]
    return repo_title, action, user, pull_request_title, head_ref, base_ref, requested_reviewers, pull_request_url

def releaseEventStripper(payload):
    repo_title = payload["repository"]["full_name"]
    action = payload["action"]
    is_prerelease = payload["release"]["prerelease"]
    user = payload["release"]["author"]["login"]
    release_title = payload["release"]["name"]
    release_url = payload["release"]["html_url"]
    release_tag = payload["release"]["tag_name"]
    return repo_title, action, is_prerelease, user, release_title, release_url, release_tag

def pullRequestReviewCommentEventStripper(payload):
    repo_title = payload["repository"]["full_name"]
    author = payload["comment"]["user"]["login"]
    pull_request_title = payload["pull_request"]["title"]
    comment_body = payload["comment"]["body"]
    comment_url = payload["comment"]["url"]
    return repo_title, author, pull_request_title, comment_body, comment_url

def deleteRepoStripper(payload):
    username = payload["repository"]["owner"]["login"]
    repo = payload["repository"]["name"]

    return username, repo