#!/usr/bin/env python
from optparse import OptionParser
import sys
import psycopg2

usage = "usage: %prog [options] arg1 arg2"
description = "A simple script to search synology's indexed files for a string argument. Requires at least one argument to search for."
parser = OptionParser(usage=usage,description=description)
parser.add_option("-i",action="store_true",dest="insensitive",help="Case insensitive search")
parser.add_option("-v",action="store_true",dest="videos",help="Search videos only")
parser.add_option("-m",action="store_true",dest="music",help="Search music only")
(options, args) = parser.parse_args()

if not args:
    parser.print_help()
    sys.exit()

tables=[]

if options.music or options.videos:
    if options.music:
        tables.append('music')
    if options.videos:
        tables.append('video')
else:
    tables = ['video','music']

def db_query(search_path):
    if options.insensitive:
        like = 'ILIKE'
    else:
        like = 'LIKE'
    # Query the database and obtain data as Python objects
    for table in tables:
        sql_command = "SELECT path FROM " + table + " WHERE path " + like + " '%" + search_path + "%';"
        cur.execute(sql_command)
        results=cur.fetchall()

        for result in results:
            print result[0]

conn = psycopg2.connect("dbname=mediaserver user=admin")
cur = conn.cursor()

for arg in args:
    db_query(arg)

cur.close()
conn.close()
