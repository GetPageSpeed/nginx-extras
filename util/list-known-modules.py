#!/usr/bin/env python3
import os

import pickledb
import yaml

db = pickledb.load('known.db.json', False)

all = []
for k in db.getall():
    repo = db.get(k)
    if repo['module']:
        # check if .yml definition for it exists in our system
        # iterate over modules/*.yml and see repo: key
        # if found, skip
        # if not found, print
        exists = False
        for module in os.listdir('../modules'):
            if module in ['bad', 'internal', 'others', 'upcoming']:
                continue
            module = os.path.join('../modules', module)
            # read as yaml
            # check if repo: is in it
            # if not, print
            with open(module) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if data['repo'] == k:
                    exists = True
                    break
                owner, name = k.split('/')
                yml_owner, yml_name = data['repo'].split('/')
                if name == yml_name:
                    exists = True
                    break
        if not exists:
            all.append(k)
            print(f"https://github.com/{k}")
