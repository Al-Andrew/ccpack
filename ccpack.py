"""
This is the local component for ccpack.
You can use this to create the baked_manifest.json file needed for ccpack to work.

This requries a local file with the name ccpack.json to be present in the same directory as this file.
This file should contain a JSON object with the following structure:
{
    "name": "ccpack",
    "version": "1.0.0",
    "author": "Your Name",
}

This script will look through the current directory recursively and create a baked_manifest.json file
with all the lua files found.
"""

import os
import json


def create_baked_manifest():
    # Load the ccpack.json file
    with open('ccpack.json', 'r') as f:
        ccpack_data = json.load(f)

    # Create the baked_manifest.json structure
    baked_manifest = {
        "name": ccpack_data["name"],
        "version": ccpack_data["version"],
        "url": "https://github.com/" + ccpack_data["author"],
        "files": []
    }

    # Walk through the current directory recursively
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.relpath(os.path.join(root, file), start='.')
                baked_file = {
                    "path": file_path,
                    "url": "https://raw.githubusercontent.com/" + ccpack_data["author"] + "/" + ccpack_data["name"] + "/main/" + file_path, # TODO: Support versioning
                }
                baked_manifest["files"].append(baked_file)

    # Write the baked_manifest.json file
    with open('baked_manifest.json', 'w') as f:
        json.dump(baked_manifest, f, indent=4)

if __name__ == "__main__":
    create_baked_manifest()
    print("baked_manifest.json created successfully.")