import os
import sys
import shutil

from pprint import pformat
from cookiecutter.vcs import clone
from cookiecutter.utils import make_sure_path_exists


def fetch_ansible_roles():
    roles = []
    with open('requirements.ansible_roles', 'r') as rfile:
        my_roles = rfile.read().rstrip().split(',')
        if len(my_roles) > 0:
            roles = my_roles
        
    roles_dir = 'ansible/roles'
    make_sure_path_exists(roles_dir)
    for role in roles:
        repo_url = 'git@github.com:ephes/ansible_{}.git'.format(role)
        role_dir = os.path.join(roles_dir, role)
        if not os.path.exists(role_dir):
            cloned_dir = clone(repo_url, checkout='master', clone_to_dir=roles_dir)
            shutil.move(cloned_dir, os.path.join(roles_dir, role))
        

def main(args):
    fetch_ansible_roles()

if __name__ == '__main__':
    main(sys.argv)
