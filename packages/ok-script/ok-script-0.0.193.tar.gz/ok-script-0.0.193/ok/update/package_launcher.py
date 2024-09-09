import os.path
import sys

import git

from ok.config.Config import Config
from ok.update.GitUpdater import copy_exe_files
from ok.util.path import dir_checksum, delete_if_exists


def write_checksum_to_file(folder_path):
    # Call the dir_checksum function
    checksum = dir_checksum(folder_path)

    # Write the checksum to a file named 'md5.txt' in the same folder
    file = os.path.join(folder_path, 'md5.txt')
    with open(file, 'w') as file:
        file.write(checksum)
    print(f'write checksum {checksum} to {file}')


if __name__ == "__main__":
    try:
        # Get the folder path from the command line arguments
        tag = sys.argv[1]
        profile = sys.argv[2]

        print(f'Tag: {tag}')
        print(f'Profile: {profile}')

        build_dir = os.path.join(os.getcwd(), 'dist')
        delete_if_exists(build_dir)
        print(f'Build directory: {build_dir}')

        current_repo = git.Repo(os.getcwd())
        url = current_repo.remote('origin').url
        print(f'Repository URL: {url}')

        repo_dir = os.path.join(build_dir, 'repo', tag)
        build_repo = git.Repo.clone_from(url, repo_dir, branch=tag, depth=1)
        print(f'Cloned repository to: {repo_dir}')

        delete_if_exists(os.path.join(repo_dir, '.git'))
        print(f'Deleted .git directory in: {repo_dir}')

        copy_exe_files(repo_dir, build_dir)

        config = Config('launcher', {
            'profile_name': profile,
            'app_dependencies_installed': False,
            'app_version': tag,
            'launcher_version': tag
        }, folder=os.path.join(build_dir, 'configs'))
        print('Configuration created successfully.')

    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)
