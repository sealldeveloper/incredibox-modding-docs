#!/bin/bash
termux-change-repo
pkg install git python tur-repo python-numpy -y
termux-setup-storage
read -p "Press ENTER once you've accepted the storage access for termux!" < /dev/tty
cd storage/shared/Documents
git clone https://github.com/sealldeveloper/incredibox-modding-docs
cd incredibox-modding-docs
pkg install openssl -y