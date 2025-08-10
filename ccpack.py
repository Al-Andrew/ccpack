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

If you have dependencies, add them as a submodule in your git repository.
If they have a ccpack.json file, it will be used to create the baked_manifest.json file. (the author, name and version will be used from the ccpack.json file)
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

    # Walk through the current directory recursively, ignore the ccpack directory itself
    current_ccpack_data = ccpack_data.copy()
    ccpack_data_relative_dir = '.'
    for root, dirs, files in os.walk('.'):
        # Ignore the ccpack directory itself
        if 'ccpack' in dirs:
            dirs.remove('ccpack')

        # ignore .git directory
        if '.git' in dirs:
            dirs.remove('.git')

        print(f"entering directory: {root}")

        # Check for ccpack.json in the current directory
        if 'ccpack.json' in files:
            with open(os.path.join(root, 'ccpack.json'), 'r') as ccpack_file:
                current_ccpack_data = json.load(ccpack_file)
            ccpack_data_relative_dir = os.path.relpath(root, start='.')
            print("Found ccpack.json, using its data: ", current_ccpack_data)

        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, start=ccpack_data_relative_dir)

                baked_file = {
                    "path": relative_path,
                    "url": "https://raw.githubusercontent.com/" + current_ccpack_data["author"] + "/" + current_ccpack_data["name"] + "/refs/heads/main/" + relative_path
                }
                print(f"Adding file to baked_manifest: {baked_file}")

                # Add the file to the baked_manifest
                baked_manifest["files"].append(baked_file)
        

    # Write the baked_manifest.json file
    with open('baked_manifest.json', 'w') as f:
        json.dump(baked_manifest, f, indent=4)

if __name__ == "__main__":
    create_baked_manifest()
    print("baked_manifest.json created successfully.")