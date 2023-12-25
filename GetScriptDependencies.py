#!/usr/bin/env python3
import subprocess
import sys

import UpdateFunctions as upd

if __name__ == "__main__":
    # Update the package list
    upd.update_apt()

    # Install python3-pip
    upd.install_apt_package("python3-pip")

    # Install the python LSP for Helix
    upd.install_apt_package("python3-pylsp")

    # Attempt to import PIL, install it if not present
    try:
        from PIL import Image
    except ImportError:
        print("Pillow is not installed. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        # from PIL import Image  # Retry the import after installation
