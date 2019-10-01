def out(command):
    from subprocess import PIPE, run
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def push(file_to_transfer, message, repos):
    """ This function push one file to your github specified repository """
    
    ## Load credentials from external file
    import os
    import git_credentials as cd
    import subprocess
    outputs = []
    output = subprocess.check_output("cat /etc/services", shell=True)
    ## Message should contain escape whitespace character (to be interpreted in command)
    message = message.replace(' ', '\ ')

    origin = "https://" + cd.GIT_USERNAME + ":" + cd.GIT_PASSWORD +\
     "@github.com/" + cd.GIT_USERNAME + "/" + repos
    
    ## Adding the remote
    os.system("git remote add origin " + origin)
    ## Name of file + comment for commiting
    os.system("git add " + file_to_transfer)
    os.system("git commit " + file_to_transfer + " -m " + message)
    ## Push to Github repos
    os.system("git push origin master")
    
    # When synchronizing again (re-adding the origin)
    os.system("git remote rm origin")

def push_multiple_files(files_to_transfer, commit_messages, repos):
    """ This is an improved function to push multiple files and specify commits along with them
    Example : 
        files_to_push = ['TD2_webscrapping.ipynb', 'data', 'chromedriver', 'insta_credentials.py']
        commits       = ['Jupyter Notebook', 'Where scrapped images are', 'Chromedriver is used here by Selenium', 
                         'Credentials for the Fake account'],
        push_multiple_files(files_to_push, commits, 'TDs_ESILV.git')
    """
    if not isinstance(files_to_transfer, list) or not isinstance(commit_messages, list):
        return 'This fonction only accepts a list of files to be commited to GitHub along with a list of commit messages'
    
    if len(files_to_transfer) < len(commit_messages):
        return 'Error - there should be equal or greater number of files to be transferred than commits'
    
    import itertools
    for file, commit in itertools.zip_longest(files_to_transfer, commit_messages, fillvalue='Additional\ changes'):
        push(file, commit, repos)