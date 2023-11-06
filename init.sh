#!/bin/bash
termux-change-repo
apt update
pkg install git python tur-repo build-essential cmake ninja libandroid-execinfo python-numpy libcrypt zlib python-pillow -y
termux-setup-storage
read -p "Press ENTER once you've accepted the storage access for termux!" < /dev/tty
cd storage/shared/Documents
git clone https://github.com/sealldeveloper/incredibox-modding-docs
cd incredibox-modding-docs
apt full-upgrade
python3 -m pip install setuptools wheel packaging pyproject_metaddata cython