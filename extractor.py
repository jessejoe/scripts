#!/usr/bin/env python 

import sys
import os
from optparse import OptionParser

usage = "usage: %prog [options] 'start' 'end'"
parser = OptionParser(usage=usage,description="This script will extract lines from a file (or stdin) between and including 'start' and 'end'")
parser.add_option("-f", dest="filename", help="input file")
parser.add_option("-m", dest="maxresults", type="int", help="maximum instances to output (default: no maximum)")
parser.add_option("-i", dest="iteration", type="int", help="only output the i'th instance found")

(options, args) = parser.parse_args()

if options.filename:
    inputdata = open(options.filename, 'rU')
else:
    inputdata = sys.stdin

inside=False
results_found=0
splitter=False
output=''
for line in inputdata:
    if args[0] in line:
        inside=True
        if splitter:
            print ('-' * 20) + ' *** ' + os.path.basename(__file__) + ' NEW RESULT #' + str(results_found + 1) + ' *** ' + ('-' * 20)
            splitter=False
    if inside:
        output+=line
    if inside and (args[1] in line):
        inside=False
        results_found+=1
        if options.iteration:
            if results_found == options.iteration:
                sys.stdout.write(output)
        else:
            sys.stdout.write(output)
            splitter=True
        output=''
    if (results_found == options.maxresults) or ((results_found == options.iteration) and inside==False):
        break
