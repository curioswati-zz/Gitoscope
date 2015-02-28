import requests

def get_user_info(username):
    """ Getting basic user infos: Step 1 
        
        username : u'login'
        real name: u'name'
        gravtar : u'avatar_url' 
        numbre of public repos
        email: u'email'
        github url: u'url'
    """
    
    url = "https://api.github.com/users/"+username
    r = requests.get(url).json()
    
    print('username: {username} \n Real Name: {real_name} \n \
          gravtar_url: {avatar_url} \n email address: {email} \n \
          github url: {github_url} \n Number of Public repos: \
          {public_repos}'.format(username=username, real_name=r[u'name'],
          avatar_url= r[u'avatar_url'], email= r[u'email'], github_url=r[u'url'],
          public_repos= r[u'public_repos']))
    
    return r

def get_repos_info(username, url):
    
    '''
    Step 2
    url = url of all public repo list.
    
    for each repo get:
        name: u'name'
        repo url :u'url', u'html_url', u'clone_url'
        Number of contributors: u'contributors_url'
        Number of total commits : https://api.github.com/repos/exploreshaifali/bonafidePro/commits
        Number of commits made by given user
        start date : u'created_at'
        last updated date : u'updated_at'
        number of issues, milestones
        description: u'description'
    '''
    r = requests.get(url).json()
    number_of_repo = len(r)
    for i in range(number_of_repo):
        _repo_name = r[i][u'name']
        print('for repo: '+_repo_name)
        _repo_url = r[i][u'url']
        _repo_description = r[i][u'description']
        _number_of_contributors = get_number_of_contibutors_of_repo(r[i][u'contributors_url'])
        
        _commits_url = _repo_url+'/commits'
        _total_commits = get_total_number_of_commits(_commits_url)
        _commits_by_given_user = get_number_of_commits_made_by_given_user(_commits_url, username)

        _issues_url = _repo_url+'/issues'
        _issues = get_total_issues_by_user_in_a_repo(username, _issues_url)
                       
        print('repo name: {name} \n repo url {repo_url} \n Description:{description}\n number of contributors:{number_of_contributors}\n total number of commits: {total_commits}\n Commits made by {username}:{number_of_commits_by_given_user}\n issues: {issues}\n'.format(name=_repo_name,
            repo_url=_repo_url, number_of_contributors=_number_of_contributors,
            total_commits=_total_commits,
            description=_repo_description, username=username,
            number_of_commits_by_given_user=_commits_by_given_user,
            issues=_issues))   
        
def get_number_of_contibutors_of_repo(url):
    """ Step 2.b """
    r = requests.get(url).json()
    return len(r)     
    
def get_total_number_of_commits(url):
    """ Step 2.c """
    r = requests.get(url).json()
    return len(r)    

def get_number_of_commits_made_by_given_user(url, username):
    """ Step 2.d
        url: repo commits api url
        Return Number of commits made by a contributor in a particular repo.
    """
    r = requests.get(url).json()
   
    number_of_commits = 0
    for i in range(len(r)):  
        '''
            Though at present 'committer' key is used but many times committer and
            author keys are none, so would be more better to get this info from 'commit' key. Need to 
            think more on how to get value using commit key.
        '''
        if r[i].get('committer', None) != None:
            if r[i]['committer'][u'login'] == username:
                number_of_commits += 1
                
    return number_of_commits

#get issues for given repo and given username
def get_total_issues_by_user_in_a_repo(username, url):
    """ return dict{'total_issues': value,
        'issues_created_by_given_user': value}
        
        :param username: github handler
        :param url: url of repo
    """
    r = requests.get(url).json()
    total_issues = len(r)
    issues_created_by_given_user = 0
    total_open_issues=0
    user_open_issues=0
    for issue in r:
        if issue[u'user'][u'login'] == username:
            issues_created_by_given_user += 1 
            if issue[u'state'] == 'open':
                user_open_issues += 1 
        if issue[u'state'] == 'open':
            total_open_issues += 1 
    _dict = {'total_issues':total_issues, 'issues_created_by_given_user':issues_created_by_given_user,
             'total_open_issues':total_open_issues, 'user_open_issues':user_open_issues}
    return _dict

if __name__ == '__main__':
	username = input("Enter github handler: ")
	#get user's basic info
	user_info = get_user_info(username)
	# get user's repos info:
	get_repos_info(username, user_info[u'repos_url'])
	print("Done!!!")