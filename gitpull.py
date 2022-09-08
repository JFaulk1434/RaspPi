import subprocess
from os.path import exists as file_exists

ACCOUNT_NAME = "Admin"
GIT_USER = "JFaulk1434"
GIT_REPO = "https://github.com/JFaulk1434/RaspPi.git"
FPATH = f'/home/{ACCOUNT_NAME}/Documents/RaspPi'
FNAME = "gitpull.py"


def run(*args):
    return subprocess.check_call(['git'] + list(args))


def clone():
    if file_exists(f'{FPATH}/{FNAME}') == False:
        subprocess.Popen(['git', 'clone', GIT_REPO])
        print(f'file not located...')
        print(f'pulling from github...')
        print(f'adding {FNAME} to {FPATH}')
    else:
        subprocess.Popen(f'git reset --hard')
        subprocess.Popen(f'git pull')
        print(f'Files already detected...')

# def clone():
#     subprocess.Popen(['git', 'clone', GIT_REPO])
#     print("Cloning new files")


clone()
