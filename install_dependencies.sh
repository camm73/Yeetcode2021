#! /bin/bash

echo "Installing Spotify Smash libraries..."

python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install libraries!"
    exit 1
fi

echo "Done installing!"

exit 0