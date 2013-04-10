#!/usr/bin/env python

# Just a stupid simple script to look for available reddit usernames.
# Searches for 3 letter names only (the shortest possible) and only
# names in the format consonant-vowel-consonant (easy to remember).

import time
import urllib2
import itertools

consonants = "bcdfghjklmnpqrstvwxyz"
vowels = "aeiou"

for word in list(itertools.product(consonants, vowels, consonants)):
    handle = urllib2.Request('http://www.reddit.com/api/username_available.json?user=' + str(word[0]) + str(word[1]) + str(word[2]))
    opener = urllib2.build_opener()
    handle.add_header('User-Agent','username checker v0.1')
    response = opener.open(handle).read()
    if response == 'true':
            print str(word[0]) + str(word[1]) + str(word[2]) + ' is available!'
    else:
            print str(word[0]) + str(word[1]) + str(word[2]) + ' == ' + response
    time.sleep(1)
