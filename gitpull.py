import subprocess
from os.path import exists as file_exists

ACCOUNT_NAME = "Admin"
GIT_USER = "JFaulk1434"
GIT_REPO = "https://github.com/JFaulk1434/RaspPi.git"
FPATH = f'/home/{ACCOUNT_NAME}/Documents/pyControl'
FPATH2 = f'/Users/justinfaulk/Documents/pyControl/RaspPi'
FNAME = "gitpull.py"


def run(*args):
    return subprocess.check_call(['git'] + list(args))


def clone():
    if file_exists(f'{FPATH2}/{FNAME}') == False:
        subprocess.Popen(['git', 'clone', GIT_REPO])
        print(f'file not located...')
        print(f'pulling from github...')
        print(f'adding {FNAME} to {FPATH}')
    else:
        subprocess.Popen(['git', 'pull --prune', GIT_REPO])
        print(f'Files already detected...')
        print(f'ignoring')
# def clone():
#     subprocess.Popen(['git', 'clone', GIT_REPO])
#     print("Cloning new files")


clone()
