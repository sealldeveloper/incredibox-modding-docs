#!/bin/bash
termux-change-repo
pkg install git python3 -y
termux-setup-storage
cd storage/shared/Documents/
git clone https://github.com/sealldeveloper/incredibox-modding-docs
cd storage/shared/Documents/incredibox-modding-docs/