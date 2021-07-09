import json
import sys
import re

release_json = sys.argv[1]
platform = sys.argv[2]

asset_regex = re.compile(f'{platform}.tar.gz$')

with open(release_json) as f:
    release_data = json.load(f)
release = None

for data in release_data:
    # Get latest actual release
    if not data['draft'] and not data['prerelease']:
        release = data
        break

if release is None:
    print('')
    sys.exit(1)

for asset in release['assets']:
    if asset_regex.search(asset['name']):
        print(asset['browser_download_url'])
        sys.exit(0)

sys.exit(1)
