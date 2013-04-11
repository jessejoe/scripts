#!/usr/bin/env python

# A simple script to use praw to download all saved links for a reddit user
# Download praw here - https://github.com/praw-dev/praw/wiki

# Note: by default the script has no result limit, however the reddit API may limit the results to ~1000

import praw

r = praw.Reddit(user_agent='saved links downloader v0.1')
r.login()
print

for counter,link in enumerate(r.user.get_saved(limit=None), 1):
    print 'Saved link #' + str(counter)
    print 'Title: '+ link.title.strip()
    print 'URL: ' + link.url
    print 'Comments: ' + link.permalink
    print
