#!/usr/bin/env python3
import pickledb

db = pickledb.load('known.db', False)

all = []
for k in db.getall():
    repo = db.get(k)
    if repo['module']:
        all.append(k)
        print(f"https://github.com/{k}")

