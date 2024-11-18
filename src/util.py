def getGitandEventType(request):
    if request.headers.get('x-gitea-event') is not None:
        git = 'Gitea'
        eventType = request.headers.get('x-gitea-event')
    else:
        git = 'GitHub'
        eventType = request.headers.get('X-GitHub-Event')

    return git, eventType
