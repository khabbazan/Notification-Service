import os
import re
import subprocess
import sys

import git

COMMITID = git.Repo().head.object.hexsha[:8]

# USAGE : python3 setup/version_punch patch v b p

content = ""

if len(sys.argv) < 2:
    print("\ncommands options are: ['major', 'minor', 'patch'] [b | v | p]\n\n- b for creating build number\n- v for bumpversion\n- p for total commit and push\n")
    sys.exit()

if "v" in sys.argv and sys.argv[1] not in ["major", "minor", "patch"]:
    print("please enter version type as first argument : [major | minor | patch]")
    sys.exit()


if len(sys.argv) >= 2:
    content_new = ""
    if "v" in sys.argv:
        subprocess.call(["bumpversion", sys.argv[1]])
    if "b" in sys.argv:
        ########### setup.cfg ############
        with open(str(os.getcwd()) + "/setup.cfg") as f:
            content_setup = f.read()
        with open(str(os.getcwd()) + "/setup.cfg", "w+") as f:
            content_new = re.sub(r"build_number\s=\s\w+", f"build_number = {COMMITID}", content_setup, flags=re.M)  # noqa
            f.write(content_new)
        ########## settings.py ##########
        with open(str(os.getcwd()) + "/src/core/settings.py") as f:
            content_settings = f.read()
        with open(str(os.getcwd()) + "/src/core/settings.py", "w+") as f:
            content_new = re.sub(r'BUILD_NUMBER\s=\s"\w+"', f'BUILD_NUMBER = "{COMMITID}"', content_settings, flags=re.M)  # noqa
            f.write(content_new)
        #################################
    if "p" in sys.argv:
        subprocess.call(["git", "commit", '-am"version/build number"'], env={"SKIP": "end-of-file-fixer,trailing-whitespace,black"})
        subprocess.call(["git", "push"])
        subprocess.call(["git", "tag", "v{}".format(re.findall(r"\d+.+", content_setup)[0])])  # NOQA
        subprocess.call(["git", "push", "--tags"])
    print("versioning finished ...")
else:
    print(
        "\ncommands options are: ['major', 'minor', 'patch'] [b | v | p | --tag]\n\n- b for creating build number\n- v for bumpversion\n- p for total commit and push\n"
    )
