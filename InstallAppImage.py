#!/usr/bin/env python3
import os
import subprocess
import shutil
import tempfile
import argparse
import sys
from pathlib import Path
from PIL import Image

import MyUtils as utils

def extract_appimage(appimage_path: Path, temp_dir: Path):
    subprocess.run([appimage_path.expanduser(), "--appimage-extract"], cwd=temp_dir.expanduser())
    extract_folder = temp_dir.joinpath("squashfs-root").expanduser().resolve()

    if not(extract_folder.exists() and extract_folder.is_dir()):
        raise FileNotFoundError(f"Problem with extraction directory.")

    return extract_folder

def is_correct_size(image_path: Path, size):
    with Image.open(image_path.expanduser()) as img:
        width, height = img.size
        return width == size or height == size

def find_icon(extracted_path: Path):
    preferred_sizes = [128, 96, 64, 256, 32]
    for root, dirs, files in os.walk(extracted_path.expanduser()):
        if "icons" in root or "icon" in root:
            for size in preferred_sizes:
                for file in files:
                    file_path = Path(root).joinpath(file)
                    if (file.endswith(".png") or file.endswith(".svg")) and is_correct_size(file_path, size):
                        return file_path
    return None

def move_icon(icon_path: Path, destination: Path, filename_no_ext):
    destination = destination.expanduser()
    if not(destination.exists()):
        os.makedirs(destination)
    
    destination = destination.joinpath(f"{filename_no_ext}{icon_path.suffix}")

    if destination.exists():
        raise FileExistsError(f"Output file {destination} already exists.")

    shutil.move(icon_path, destination)

    return destination

def install_desktop_file(name: str, exec_path: Path, icon_path: Path, destination: Path):
    desktop_file_path = destination.expanduser().joinpath(f"{name}.desktop")
    
    if desktop_file_path.exists():
        raise FileExistsError(f"Output file {desktop_file_path} already exists.")

    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={name}
Exec={exec_path.expanduser()}
Icon={icon_path.expanduser()}
Categories=Utility;
"""

    with open(desktop_file_path, "w") as desktop_file:
        desktop_file.write(content)

    return desktop_file_path

def move_appimage(appimage_path: Path, destination: Path):
    destination = destination.expanduser()
    if not destination.exists():
        os.makedirs(destination)
    
    destination = destination.joinpath(appimage_path.name)

    shutil.move(appimage_path, destination)

    return destination

def install_appimage(appimage_path: Path, app_name):
    temp_dir = Path(tempfile.mkdtemp().strip()).expanduser().resolve()

    if not(temp_dir.exists() and temp_dir.is_dir()):
        raise FileNotFoundError(f"Problem with temporary directory.")
    else:
        try:
            # Add execute permission on user, needed for extraction + to be able to use as a program later
            subprocess.run(["chmod", "u+x", appimage_path.expanduser()])

            extracted_path = extract_appimage(appimage_path, temp_dir)
            icon_path = find_icon(extracted_path)
            if icon_path is None:
                raise FileNotFoundError("Suitable icon not found.")

            icon_path = move_icon(icon_path, Path("~/.local/share/applications/"), app_name)
            appimage_path = move_appimage(appimage_path, Path("~/.apps"))

            desktop_file_path = install_desktop_file(app_name, appimage_path, icon_path, Path("~/.local/share/applications/"))
            print(f"{app_name} installed successfully.")

        except (FileExistsError, FileNotFoundError) as e:
            print(f"Error: {e}", file=sys.stderr)

        finally:
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a desktop entry for an AppImage.")
    parser.add_argument("appimage", type=Path, help="Path to the AppImage file")
    parser.add_argument("--name", help="Name of the application")
    args = parser.parse_args()

    appimage_path = args.appimage.expanduser().resolve()
    app_name = utils.is_none(args.name, "").strip()

    app_name = utils.filename_make_safe(app_name if app_name != "" else appimage_path.stem)

    if not(appimage_path.exists() and appimage_path.is_file()):
        print("AppImage doesn't exist!")
    elif not(utils.filename_is_safe(app_name)):
        print("Filename is invalid!")
    else:
        install_appimage(appimage_path, app_name)
