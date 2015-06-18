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


def create_ansible_vault():
    '''
    Create ansible vault with random passphrase and set SECRET_KEY.
    '''
    def generate_passphrase():
        import random
        import string
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(20))

    # write the ansible vault password to disk
    passphrase = generate_passphrase()
    with open('ansible/.vault_pass.txt', 'w') as vp_file:
        vp_file.write('{}\n'.format(passphrase))

    # create ansible vault
    from ansible.utils.vault import VaultEditor
    vault_path = 'ansible/group_vars/all/vault.yml'
    vault_editor = VaultEditor('AES256', passphrase, vault_path)
    data = '--- \nSECRET_KEY: {}'.format(generate_passphrase())
    vault_editor.write_data(data, vault_path)
    vault_editor.encrypt_file()


def main(args):
    fetch_ansible_roles()
    create_ansible_vault()


if __name__ == '__main__':
    main(sys.argv)
