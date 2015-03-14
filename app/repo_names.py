"""Required modules"""
import requests
import pprint
import json

#--------------------------------------Globals---------------------------------------
PROFILE_URL = "https://api.github.com/users/%s"
REPOS_URL = "https://api.github.com/users/%s/repos"
EVENTS_URL = "https://api.github.com/users/%s/events"
ISSUES_URL = "https://api.github.com/search/issues?q=type:pr+state:closed+author:%s"
STARRED_URL = "https://api.github.com/users/%s/starred"
SUBSCRIPTION_URL = "https://api.github.com/users/%s/subscriptions"
ORGS_URL = "https://api.github.com/users/%s/orgs"
ORG_REPOS = "https://api.github.com/orgs/%s/repos"

TOKEN = "659831a631db1e1a8a17c3cee54d15cc0a26d64f"
params = {"per_page" : 100, "page" : 3}
headers = {"Content-Type": "application/json",
           "Authorization":"token %s" % TOKEN,
           "X-Github-Event":"push"}
REPOS = {}
INDEX = 0
username = "swati-jaiswal"

#-----------------------------------------------------------------------------------
def get_repo_names(username):
    """
    (username) -> list_of_repos
    
    This function takes a username as input and returns 
    the name of all the repositories the user owns or have contributed to.
    
    >>>get_repos_name("swati-jaiswal")
    Gitoscope
    swati-jaiswal.github.io
    blog
    MyScripts
    SJdownloader
    Code_chef_practice
    Algorithms
    Project1
    mojombo.github.io
    """
    #--------------------------Listing Public repos--------------------------------
    r = requests.get(REPOS_URL % username)
    data = r.json()
    INDEX = 0

    for repo in data:
        content = repo['owner']['login'], repo['name']
        REPOS[INDEX] = content
        INDEX += 1

    #-------------------Using events to fetch contributions------------------------
    page = 1

    while True:
        params['page'] = page
        r = requests.get(EVENTS_URL % username, params=params, headers=headers)
        data = r.json()
        if not data:
            break

        for item in data:
            repo = item[u'repo'][u'name'].split('/')
            owner = repo[0]
            name = repo[1]
            entry = owner, name
            if entry not in REPOS.values():
                REPOS[INDEX] = entry
                INDEX += 1
        page += 1

    #------------------Fetching contributions using issues-------------------------
    r = requests.get(ISSUES_URL % username)
    data = r.json()

    items = data[u'items']
    for item in items:
        repo = item[u'html_url']
        if repo not in REPOS.values():
            REPOS[INDEX] = repo
            INDEX += 1

    #-----------------------Fetching subscribed repos------------------------------
    r = requests.get(SUBSCRIPTION_URL % username)
    data = r.json()

    for repo in data:
        content = repo['owner']['login'], repo['name']
        if content not in REPOS.values():
            REPOS[INDEX] = content
            INDEX += 1

    #-------------------------Fetching starred repos-------------------------------
    r = requests.get(STARRED_URL % username )
    data = r.json()

    for repo in data:
        owner = repo[u'owner'][u'login']
        name = repo[u'name']
        entry = owner, name
        if entry not in REPOS.values():
            REPOS[INDEX] = entry
            INDEX += 1

    #---------------showing the fetched names of the repositories.-----------------
    for repo in REPOS:
        print repo, REPOS[repo]

#Calling the function
get_repo_names("swati-jaiswal")