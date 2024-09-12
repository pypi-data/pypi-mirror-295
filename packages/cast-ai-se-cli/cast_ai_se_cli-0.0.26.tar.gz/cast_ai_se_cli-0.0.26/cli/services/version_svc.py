import requests
from typing import Optional
from packaging import version
import os
from pkg_resources import get_distribution

from cli.constants import PACKAGE_NAME


def get_current_version() -> str:
    current_file_path = os.path.abspath(__file__)  # Get absolute path of the current file
    grandparent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))  # Go 3 levels up
    version_file_path = os.path.join(grandparent_dir_path, 'version.txt')  # Construct the full path

    if os.path.exists(version_file_path):
        with open(version_file_path, 'r') as file:
            pkg_version = file.read().strip()
    else:
        try:
            pkg_version = get_distribution(PACKAGE_NAME).version
        except:
            return ""
    return pkg_version


def get_latest_version(package_name: str = PACKAGE_NAME) -> Optional[str]:
    try:
        response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
        response.raise_for_status()
        data = response.json()
        latest_version = data['info']['version']
        return latest_version
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def check_if_latest_version():
    l_version = get_latest_version()
    c_version = get_current_version()
    if not l_version or not c_version:
        return
    latest_version = version.parse(l_version)
    current_version = version.parse(c_version)
    if latest_version > current_version:
        print(f"New version ({latest_version}) is out! Please consider upgrading.\n")
    else:
        print(f"You are using latest version ({latest_version})...Respect!")
