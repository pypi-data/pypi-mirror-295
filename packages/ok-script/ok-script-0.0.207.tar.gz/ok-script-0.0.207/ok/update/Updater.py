import importlib
import math
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime

import psutil
import py7zr
import requests

import ok
from ok.gui.Communicate import communicate
from ok.logging.Logger import get_logger
from ok.update.GithubMultiDownloader import GithubMultiDownloader
from ok.util.Handler import Handler
from ok.util.path import get_path_relative_to_exe, ensure_dir, dir_checksum, find_folder_with_file, clear_folder

logger = get_logger(__name__)


class Updater:
    def __init__(self, app_config, exit_event):
        self.config = app_config.get('update')
        self.version = app_config.get('version')
        self.debug = app_config.get('debug')
        self.latest_release = None
        self.stable_release = None
        self.to_update = None
        self.downloading = False
        self.exe_name = self.config.get('exe_name')
        if self.config is None:
            return
        self.update_url = self.config.get('releases_url')
        self.proxy_url = self.config.get('proxy_url')
        self.use_proxy = self.config.get('use_proxy')
        self.update_dir = get_path_relative_to_exe('updates')
        self.exit_event = exit_event
        self.handler = Handler(exit_event, self.__class__.__name__)
        self.downloader = GithubMultiDownloader(app_config, exit_event)
        self.handler.post(self.do_check_for_updates, 50)

    def get_proxy_url(self, url):
        if self.use_proxy:
            url = self.proxy_url + url
            logger.info(f'get_url: {url}')
            return url

    def check_for_updates(self):
        self.handler.post(self.do_check_for_updates, remove_existing=True)

    def do_check_for_updates(self, proxied_url=None):

        try:
            url = proxied_url or self.update_url
            logger.info(f'do_check_for_updates: {url}')
            # Send GET request to the API endpoint
            response = requests.get(url, timeout=10, verify=proxied_url is None)

            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            # Parse the JSON response to a dictionary
            releases = response.json()

            # Extract useful information from each release
            self.latest_release = None
            self.stable_release = None

            for release in releases:
                try:
                    release = self.parse_data(release)
                    if not release:
                        continue

                    if not release.get('draft'):
                        if self.latest_release is None:
                            self.latest_release = release
                        if not release.get('prerelease') and self.stable_release is None:
                            self.stable_release = release

                        if self.latest_release and self.stable_release:
                            break
                except Exception as e:
                    logger.error(f'parse data error {release}', e)

            if self.latest_release == self.stable_release:
                self.latest_release = None

            if self.stable_release is not None and self.stable_release.get('version') != self.version:
                communicate.notification.emit(
                    ok.gui.app.app.translate('@default',
                                             'Start downloading latest release version {version}'.format(
                                                 version=self.stable_release.get('version'))),
                    ok.gui.app.app.translate('@default', 'Version Update'),
                    False, False)
                self.download(self.stable_release, False)
            if not self.latest_release and not self.stable_release:
                logger.info(f"check update newest version clear update folder {self.update_dir}")
                clear_folder(self.update_dir)
            communicate.check_update.emit(None)
        except Exception as e:
            logger.error(f'check_update http error, retry with proxy', e)
            proxy = self.get_proxy_url(self.update_url)
            if proxied_url is None and proxy:
                self.do_check_for_updates(proxy)
                return
            logger.error(f'check_update_error: ', e)
            communicate.check_update.emit(str(e))

    def async_run(self, task):
        self.handler.post(task)

    def download(self, release, debug):
        try:
            ensure_dir(self.update_dir)
            asset = release.get('debug_asset') if debug else release.get('release_asset')
            file = os.path.join(self.update_dir, release.get('version') + '.' + asset.get('type'))
            size = asset.get('size')
            if os.path.exists(file):
                downloaded = os.path.getsize(file)
                if downloaded == size:
                    logger.info(f'File {file} already downloaded')
                    self.extract(file, release, debug)
                    return
                else:
                    logger.warning(f'File size error {file} {downloaded} != {size}')
                    os.remove(file)
            self.downloading = True
            success = self.downloader.download(self.update_dir, asset)
            self.downloading = False
            if success:
                logger.info(f'download success: {file}')
                self.extract(file, release, debug)
            return

        except Exception as e:
            logger.error('download error occurred', e)
            self.downloading = False
            communicate.download_update.emit(0, "", True, "download error")

    def extract(self, file, release, debug):
        version = release.get('version')
        communicate.download_update.emit(100, "Extracting", False, None)
        folder, extension = file.rsplit('.', 1)
        ensure_dir(folder)
        try:
            if extension == '7z':
                with py7zr.SevenZipFile(file, mode='r') as z:
                    z.extractall(folder)
            elif extension == 'zip':
                with zipfile.ZipFile(file, 'r') as z:
                    z.extractall(folder)
        except Exception as e:
            logger.error('extract error occurred', e)
            self.check_package_error()
            return

        update_package_folder = find_folder_with_file(folder, 'md5.txt')

        if update_package_folder is None:
            logger.error('check_package_error no md5.txt found')
            self.check_package_error()
            return
        correct_md5_file = os.path.join(update_package_folder, 'md5.txt')
        try:
            with open(correct_md5_file, 'r') as file:
                # Read the content of the file
                correct_md5 = file.read()
        except Exception as e:
            logger.error(f'check_package_error md5.txt not found {correct_md5_file}', e)
            self.check_package_error()
            return

        md5 = dir_checksum(update_package_folder, ['md5.txt'])
        if md5 != correct_md5:
            logger.error(f'check_package_error md5.txt mismatch {correct_md5_file} != {md5}')
            self.check_package_error()
            return
        logger.info(f'extract md5: {md5}')

        # Open the file in write mode ('w')
        try:
            updater_exe = os.path.join(update_package_folder, '_internal', 'ok', 'binaries',
                                       'updater.exe')
            if not os.path.exists(updater_exe):
                communicate.download_update.emit(100, "", True, "can't find updater.exe!")
                return
            move_file(updater_exe, self.update_dir)

            updater_exe = os.path.join(self.update_dir, 'updater.exe')

        except Exception as e:
            logger.error(f'write updater_exe error', e)
            self.check_package_error()
            return

        # Now, 'Hello, World!' is written to 'filename.txt'
        self.to_update = {'version': version, 'update_package_folder': update_package_folder, 'debug': debug,
                          'updater_exe': updater_exe, 'notes': release.get('notes'), 'release': release}
        communicate.download_update.emit(100, "", True, None)
        return True

    def update(self):
        ok.gui.device_manager.adb_kill_server()
        exe_folder = get_path_relative_to_exe()
        batch_command = [self.to_update.get("updater_exe"), self.to_update.get("update_package_folder"), exe_folder,
                         self.exe_name]
        pids = [os.getpid()]
        if ok.gui.device_manager.adb:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] == 'adb.exe' and os.path.normpath(proc.info['exe']).startswith(
                        os.path.normpath(exe_folder)):
                    try:
                        logger.info(f'try kill the adb process {proc.info}')
                        proc.kill()
                    except Exception as e:
                        logger.error(f'kill process error', e)
                    pids.append(proc.info['pid'])

        batch_command.append(','.join(str(i) for i in pids))

        logger.info(f'execute update {batch_command}')

        subprocess.Popen(batch_command, close_fds=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        ok.gui.ok.quit()

    def check_package_error(self):
        clear_folder(self.update_dir)
        communicate.download_update.emit(100, "", True, "Update Package CheckSum Error!")

    def enabled(self):
        return self.config is not None

    def parse_data(self, release):
        version = release.get('tag_name')
        if not release.get('assets'):
            return None
        if not is_newer_or_eq_version(self.version, version):
            return None
        date = datetime.strptime(release.get('published_at'), "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d')
        release_asset = None
        debug_asset = None
        for asset in release.get('assets'):
            asset = {
                'name': asset.get('name'),
                'url': asset.get('browser_download_url'),
                'size': asset.get('size'),
                'readable_size': convert_size(asset.get('size')),
                'version': version
            }
            asset['type'] = asset['url'].rsplit('.', 1)[1]
            url = asset.get('url')
            if version in url:
                if 'debug' in url:
                    debug_asset = asset
                elif 'release' in url:
                    release_asset = asset
            if version == self.version:
                if self.debug:
                    debug_asset = None
                else:
                    release_asset = None
        if not release_asset and not debug_asset:
            return None
        return {
            'version': version,
            'notes': release.get('body'),
            'date': date,
            'draft': release.get('draft'),
            'prerelease': release.get('prerelease'),
            'release_asset': release_asset,
            'debug_asset': debug_asset
        }


def move_file(src, dst_folder):
    # Get the file name from the source path
    file_name = os.path.basename(src)
    # Construct the full destination path
    dst = os.path.join(dst_folder, file_name)

    # Check if the destination file already exists
    if os.path.exists(dst):
        os.remove(dst)  # Remove the existing file
    shutil.move(src, dst)  # Move the file


def is_newer_or_eq_version(base_version, target_version):
    try:
        base_version = list(map(int, base_version[1:].split('.')))
        target_version = list(map(int, target_version[1:].split('.')))
        # Compare the versions
        return base_version <= target_version
    except Exception as e:
        logger.error(f'is_newer_or_eq_version error {base_version} {target_version}', e)
        return False


def get_updater_exe_local():
    if sys.version_info < (3, 9):
        context = importlib.resources.path("ok.binaries", "__init__.py")
    else:
        ref = importlib.resources.files("ok.binaries") / "__init__.py"
        context = importlib.resources.as_file(ref)
    with context as path:
        pass
    # Return the dir. We assume that the data files are on a normal dir on the fs.
    return str(path.parent) + '.exe'


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


if __name__ == '__main__':
    print(get_updater_exe_local())
