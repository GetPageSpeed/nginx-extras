#!/usr/bin/env python3
import os
import pickledb
from github import Github
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException, GithubException
from github.Repository import Repository
import logging as log

log.basicConfig(level=log.INFO)
g = Github(os.getenv("GITHUB_API_TOKEN"))
db = pickledb.load('known.db.json', False)
repositories = g.search_repositories(query='nginx in:name stars:>=100 archived:false', sort='stars')

repo: Repository
i = 0
for repo in repositories:
    log.info(f'================= {repo.full_name} =================')
    known = db.get(repo.full_name)
    if known:
        log.info('Already known')
        continue
    is_nginx_module = False
    try:
        config_contents = repo.get_contents('config')
        if isinstance(config_contents, ContentFile):
            log.info('Config file detected in the root directory')
            if 'ngx_addon_name' in config_contents.decoded_content.decode("utf-8"):
                log.info('Config file has ngx_addon_name, so it is an NGINX module')
                is_nginx_module = True
        log.info('NGINX module detected')
    except (UnknownObjectException, GithubException):
        log.warning(f"Has no config. Likely not a module")

    db.set(repo.full_name, {'module': is_nginx_module})
    db.dump()

