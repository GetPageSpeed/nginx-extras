#!/usr/bin/env python3
import os

import pickledb
import yaml
from tabulate import tabulate

DB_FILE = "discovered.db.json"
OUTPUT_MD = "../docs/nonpackaged-modules.md"

db = pickledb.load(DB_FILE, False)

nonpackaged_modules = []
nonpackages_modules_table_entries = []
# short names of all the modules we either built or plan to build, or failed, etc.
known_modules = []

# Build up a list of known modules
for root, dirs, files in os.walk("../modules"):
    for file in files:
        if not file.endswith(".yml"):
            continue
        module_path = os.path.join(root, file)
        with open(module_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if "repo" not in data:
                # NGINX module that comes with its source, e.g. xslt
                continue
            owner, name = data["repo"].split("/")
            known_modules.append(name)

for full_repo_name in db.getall():
    repo = db.get(full_repo_name)
    if not repo["module"]:
        continue
    owner, name = full_repo_name.split("/")
    if name in known_modules:
        # Skip module we have .yml definition for
        continue

    nonpackaged_modules.append(full_repo_name)
    # Limit description length:
    description = repo["description"]
    if description:
        # remove any special characters as they mess up Markdown rendering
        # do this by keeping only ASCII characters
        description = "".join([c for c in description if ord(c) < 128])
        if len(description) > 67:
            description = description[:67] + "..."
    nonpackages_modules_table_entries.append(
        [f"https://github.com/{full_repo_name}", description, repo["stars"]]
    )

tabulated = tabulate(
    nonpackages_modules_table_entries,
    headers=["Name", "Description", "Stars"],
    tablefmt="github",
)

with open(OUTPUT_MD, "w") as nonpackages_modules_f:
    headers = ["Name", "Description", "Stars"]
    nonpackages_modules_table_entries.sort()
    nonpackages_modules_f.write("# Non-packaged NGINX modules\n\n")
    nonpackages_modules_f.write(tabulated)

# print tabulated table
print(tabulated)
