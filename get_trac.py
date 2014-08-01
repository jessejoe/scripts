#!/usr/bin/env python

import xmlrpclib
import sys
import os
import datetime

# URL to Trac xmlrpc API
trac_url = "http://user:password@trac.foo.com:8000/Trac/login/xmlrpc"

def date_diff(date):
    ''' Print dates as 'x hours/days/minutes ago' since the date is returned without any UTC offset and it's a pain to add the tzinfo stuff '''
    now = datetime.datetime.utcnow()
    diff = now - date
    output = ''
    if diff.days:
        if (diff.days/365) > 1:
            output += '%s years' % str(diff.days/365)
        elif (diff.days/7/4) > 1:
            output += '%s months' % str(diff.days/7/4)
        elif (diff.days/7) > 1:
            output += '%s weeks' % str(diff.days/7)
        else:
            output += '%s days' % str(diff.days)
    elif (diff.seconds/60/60) > 0:
        output += '%s hours' % str(diff.seconds/60/60)
    elif (diff.seconds/60) > 0:
        output += '%s minutes' % str(diff.seconds/60)
    else:
        output += '%s seconds' % str(diff.seconds)
    return '%s ago' % output

def mysort(a,b):
    ''' Sort trac changes making sure the comment is last. Trac switch it up and makes it hard to tell when a comment ends or begins. '''
    if a[0] == b[0]:
            if a[2] != 'comment':
                    return -1
            if b[2] != 'comment':
                    return 1
    return cmp(a[0], b[0])

# Get the terminal width, to display horizontal rule
rows, columns = os.popen('stty size', 'r').read().split()

# Connect to server
server = xmlrpclib.ServerProxy(trac_url, use_datetime=True)
trac = sys.argv[1]

# Combine all the calls into one multicall so it's a single HTTP request - http://trac-hacks.org/wiki/XmlRpcPlugin
multicall = xmlrpclib.MultiCall(server)
multicall.ticket.get(trac)
multicall.ticket.changeLog(trac)
multicall.ticket.getTicketFields()
basic, changes, field_map_server = multicall()

header = basic[3]

# Map field names to nice names, i.e. {'target_milestone':'Target Milestone'}
field_map = {}
for field in field_map_server:
    field_map[field['name']] = field['label']

# Make a nice "(closed defect: fixed)" type status like the GUI
in_parens = header['status'] + ' ' + header['type']
if header['resolution'] != '':
    in_parens += ': ' + header['resolution']

print 'Ticket #%s (%s)' % (basic[0], in_parens)
print 'Summary: %s\n' % header['summary']

# Print out the header fields like the GUI, print blank fields last
empty_fields = []
for field in sorted(header):
    if field != 'description' and field != 'summary' and field != '_ts':
        if header[field] != '':
            if type(header[field]) == datetime.datetime:
                print '%s: %s' % (field_map[field], date_diff(header[field]))
            else:
                print '%s: %s' % (field_map[field], str(header[field]).rstrip())
        else:
            empty_fields.append(field_map[field])
print 'Not set: %s' % (', '.join(sorted(empty_fields)))

print '\nDescription:'
print '%s' % (header['description'].rstrip())

# List for tracking field updates so we can print them after the comment number
updates = ''

# Sort the comments by date and then make sure the 'comment' is the last item since trac is not consistent
changes.sort(mysort)

# Loop through all the changes to the trac
for change in changes:
    date, author, field, oldvalue, newvalue, permanent  = change

    # If we actually get to the comment, print everything in order with the comment last
    if field == 'comment':
        # Terminal width separator
        print '-' * int(columns)
        # If there's no comment number, don't try to print it (attachments, etc.)
        if oldvalue == '':
            print 'Changed %s by %s\n' % (date_diff(date), author)
        else:
            print 'Changed %s by %s - %s:%s\n' % (date_diff(date), author, field, oldvalue)
        if newvalue != '':
            if updates != '':
                print updates
                updates = ''
            print '%s' % (newvalue.rstrip())
        else:
            print updates.rstrip()
            updates = ''
    else:
        # Try to figure out when fields were set, added, or changed
        # This prints last (unlike the GUI) so print green to stick out more
        if field in field_map.keys():
            field_label = field_map[field]
        else:
            field_label = field
        if oldvalue == '' and newvalue != '':
            # Don't print the testplan and pblic description diffs
            if field == 'public_description' or field == 'testplan':
                updates += '%s modified\n' % (field_label)
            else:
                updates += '%s set to %s\n' % (field_label, newvalue)
        elif (oldvalue != newvalue) and (newvalue != '') and ('_comment' not in field):
            # Don't print the testplan and pblic description diffs
            if field == 'public_description' or field == 'testplan':
                updates += '%s modified\n' % (field_label)
            else:
                updates += '%s changed from %s to %s\n' % (field_label, oldvalue, newvalue)
