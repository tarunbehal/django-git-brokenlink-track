# DJANGO GIT BROKENLINK TRACKING

DJANGO GIT BROKENLINK TRACKING is a Django app which provides a middleware which can be used to generate Git Issue whenever the application encounters 404 page.

## Quick start

1. Add "git_brokenlink_track" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'git_brokenlink_track',
    ]

2. Include "git_brokenlink_track.middleware.GitIssueTrackMiddleware" in the MIDDLEWARE_CLASSES like this::

    MIDDLEWARE_CLASSES = [
        ...
        'git_brokenlink_track.middleware.GitIssueTrackMiddleware',
    ]

3. Add DJANGO GIT BROKENLINK TRACKING settings in your settings file:
	GBT_ENABLED = True # default to False. This flag must be enabled for the broken link tracking to work
	GBT_DEBUG_MODE = True # If set to true issues will be logged in debug mode as well, default False
	GBT_REPO_OWNER = 'repo_owner'
	GBT_REPO_NAME = 'repo_name'
	GBT_ACCESS_TOKEN = 'user_access_token'
	GBT_ISSUE_LABEL = [] # multiple labels can be specified in an array ['broken-link', '404']

4. Restart your development server