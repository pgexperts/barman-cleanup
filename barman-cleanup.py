#!/usr/local/bin/python2.7

from subprocess import Popen, PIPE
import sys
import re

dbserver = sys.argv[1]

backuplist = Popen(["barman", "list-backup", dbserver], stdout=PIPE)

i = 0

for line in backuplist.stdout:
    if re.search("FAILED", line):
        try:
            backup, status = line.split(' - ')
            server, backupid = backup.split()
            # We delete delete FAILED backups with impunity and
            # don't
            # count them toward the 2 saved backups
            deleteit = Popen(["barman", "delete", server, backupid])
        except:
            sys.stderr.write("Unable to split line due to incorrect number of values.\n")
            sys.stderr.write(line + "\n")

    else:
        try:
            backup, date, size, wsize = line.split(' - ')
            i += 1
            if i > 2:
                #print "Deleting " + backup
                server, backupid = backup.split()
                deleteit = Popen(["barman", "delete", server, backupid])
        except:
            sys.stderr.write("Unable to split line due to incorrect number of values.\n")
            sys.stderr.write(line + "\n")

