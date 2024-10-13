#!/usr/bin/env python3
import argparse
import os
import json
from github import Github
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException, GithubException
from github.Repository import Repository
import logging as log

DB_FILE = "discovered.db.json"

log.basicConfig(level=log.INFO)
g = Github(os.getenv("GITHUB_API_TOKEN"))
db = {}
# Load the database
try:
    with open(DB_FILE) as f:
        db = json.load(f)
except FileNotFoundError:
    pass

# Set up argparse
parser = argparse.ArgumentParser(description="Discover NGINX modules")
parser.add_argument("--stars", type=int, default=100, help="Minimum number of stars")
args = parser.parse_args()

queries = [
    f"ngx_ in:name stars:>={args.stars} archived:false",
    f"nginx in:name stars:>={args.stars} archived:false",
]

for q in queries:
    repositories = g.search_repositories(query=q, sort="stars")

    repo: Repository

    for repo in repositories:
        log.info(f"================= {repo.full_name} =================")
        known = db.get(repo.full_name)
        if known:
            log.info("Already known")
            continue
        is_nginx_module = False
        try:
            config_contents = repo.get_contents("config")
            if isinstance(config_contents, ContentFile):
                log.info("Config file detected in the root directory")
                if "ngx_addon_name" in config_contents.decoded_content.decode("utf-8"):
                    log.info("Config file has ngx_addon_name, so it is an NGINX module")
                    is_nginx_module = True
            log.info("NGINX module detected")
        except (UnknownObjectException, GithubException):
            log.warning(f"Has no config. Likely not a module")

        db[repo.full_name] = {
            "module": is_nginx_module,
            "description": repo.description,
            "stars": repo.stargazers_count,
        }

        # Save the database
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=2)
