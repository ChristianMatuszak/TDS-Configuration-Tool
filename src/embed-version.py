import versiontag

current_version = versiontag.get_version()

with open("version.py", "w") as f:
    f.write(f'VERSION = "{current_version}"')
