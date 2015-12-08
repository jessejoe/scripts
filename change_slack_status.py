#!/usr/bin/env python
"""
Script to change Slack last name to include an away message.

Slack doesn't support away messages currently, and it takes too many clicks to
change a profile.

Simply set last_name and api_token, and provide a message on the CLI. If no
message is provided, it will set it back to last_name.
"""

import sys
import requests

# Used to concatenate with status
last_name = 'Smith'
# Get this from https://api.slack.com/web
api_token = 'xoxp-'

# Assume all arguments make up the message
message = ' '.join(sys.argv[1:])
if message:
    status = "{} - {}".format(last_name, message)
else:
    # If no message provided, (re)set last name
    status = last_name

# Double brackets required for python strings to be literal brackets
# 'profile' must be a string, not a dict/object
payload = {'profile': '{{"last_name":"{}"}}'.format(status),
           'token': api_token}

r = requests.post('https://slack.com/api/users.profile.set', data=payload)
# Check for HTTP response errors
r.raise_for_status()
resp_json = r.json()
# Check for error from Slack
if resp_json['ok'] is not True:
    raise Exception('Error in Slack reponse: {}'.format(resp_json['error']))
