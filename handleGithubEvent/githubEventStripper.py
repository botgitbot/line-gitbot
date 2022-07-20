def mergePullRequestStripper(payload):
    # ngembaliin data yang dibutuhin dari payload
    return "a", "b", "c"

def pullRequestStripper(payload):
    # ngembaliin data yang dibutuhin dari payload
    return "a", "b", "c"

def addRepoStripper(payload):
    # ngembaliin data yang dibutuhin dari payload
    # return "a", "b", "c"
    hookId = payload["hook_id"]
    username = payload["sender"]["login"]
    repo = payload["repository"]["name"]
    return hookId, username, repo