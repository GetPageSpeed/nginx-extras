#!/usr/bin/env python3
import os
import pickledb
from github import Github
from github.GithubException import UnknownObjectException, GithubException
from github.Repository import Repository
import logging as log

log.basicConfig(level=log.INFO)
g = Github(os.getenv("GITHUB_API_TOKEN"))
db = pickledb.load('known.db', False)
repositories = g.search_repositories(query='nginx in:name stars:>=1 archived:false', sort='stars')

repo: Repository
i = 0
for repo in repositories:
    log.info(f'================= {repo.full_name} =================')
    known = db.get(repo.full_name)
    if known:
        log.info('Already known')
        continue
    try:
        contents = repo.get_contents('config')
        log.info('NGINX module detected')
        db.set(repo.full_name, {'module': True})
    except (UnknownObjectException, GithubException):
        log.warning(f"Has no config. Likely not a module")
        db.set(repo.full_name, {'module': False})
    db.dump()

