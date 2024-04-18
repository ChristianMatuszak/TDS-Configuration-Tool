import versiontag

current_version = versiontag.get_version()

print("Embedding version: ", current_version)

with open("version.py", "w") as f:
    f.write(f'VERSION = "{current_version}"')
