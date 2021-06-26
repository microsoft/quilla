#!/bin/bash

DRIVER_RELEASE_API="https://api.github.com/repos/mozilla/geckodriver/releases"
JSON_FILE="release_data.json"
PLATFORM="linux64"

curl $DRIVER_RELEASE_API > $JSON_FILE

ASSET_URL=$(python3 scripts/process_release.py "$JSON_FILE" "$PLATFORM")

echo "$ASSET_URL"
wget $ASSET_URL
rm $JSON_FILE

find . -name "*.tar.gz" -exec tar -xzf {} \;
rm -rf *.tar.gz
