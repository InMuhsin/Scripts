#!/usr/bin/env python3
import subprocess
import re

import MyUtils as utils

def update_apt():
    subprocess.check_call(["sudo", "apt", "update"])

def upgrade_apt(update_first = True):
    if update_first:
        update_apt()
    # subprocess.check_call(["sudo", "apt", "upgrade"])
    subprocess.check_call(["sudo", "apt", "full-upgrade"])
    subprocess.check_call(["flatpak", "upgrade"])

def package_name_is_valid(package_name):
    package_name = utils.is_none(package_name, "")

    if package_name.strip() == "":
        return False
    
    if ("\r" in package_name) or ("\n" in package_name):
        return False
    
    # will match if not alphanumeric, -, or _
    matches = re.findall("[^a-z0-9\-\_]", package_name.lower())
    
    return (len(matches) == 0)

def apt_package_is_installed(package_name):
    package_name = package_name.strip()

    if ((package_name == "") or (" " in package_name) or not(package_name_is_valid(package_name))):
        return None
    
    try:
        # Run 'dpkg -l' command to check for the package
        subprocess.check_call(["dpkg", "-l", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        # The package is not installed
        return False

def install_apt_package(package_name):
    package_name = package_name.strip()

    if ((package_name == "") or (" " in package_name) or not(package_name_is_valid(package_name))):
        return
    
    already_installed = apt_package_is_installed(package_name)
    if already_installed is None:
        return
    elif not(already_installed):
        subprocess.check_call(["sudo", "apt", "install", "-y", package_name])
