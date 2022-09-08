import subprocess
from os.path import exists as file_exists

ACCOUNT_NAME = "Admin"
GIT_USER = "JFaulk1434"
GIT_REPO = "https://github.com/JFaulk1434/RaspPi.git"
FPATH = f'/home/{ACCOUNT_NAME}/Documents/pyControl'
FNAME = "gitpull.py"


def run(*args):
    return subprocess.check_call(['git'] + list(args))


def clone():
    subprocess.Popen(['git', 'clone', GIT_REPO])
    print("Cloning new files")


clone()
