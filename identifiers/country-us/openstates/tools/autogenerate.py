#!/usr/bin/env python3
import re
import os
import csv

# In case you've not guessed, this is a one-off to help.
OPENSTATES_CSV_ROOT = "/home/tag/dev/sunlight/openstates/manual_data/districts"
DISTRICT_INFO = re.compile("(?P<flavor>.*)/(?P<state>.*)-(?P<district>.*)")

STATES = ["ma.csv",
          "vt.csv",
          "sc.csv",
          "nh.csv",
          "md.csv",]
# STATES = os.listdir(OPENSTATES_CSV_ROOT)

for state in STATES:
    state_, _ = state.split(".", 1)
    with open("state-%s-openstates.csv" % (state_), 'w') as wfd:
        wfd.write("id,openstates_district\n")

        with open("%s/%s" % (OPENSTATES_CSV_ROOT, state)) as fd:
            r = csv.reader(fd)
            next(r)  # Mapping row.
            for line in r:
                abbr, chamber, name, num_seats, boundary_id = line
                if boundary_id == "unknown":
                    continue

                info = DISTRICT_INFO.match(boundary_id).groupdict()
                print(info)

                gid = "ocd-division/country:us/state:%s/%s:%s" % (
                    abbr, info['flavor'], info['district'],)

                wfd.write("%s,%s\n" % (gid, "%s-%s-%s" % (
                    abbr, chamber, info['district'])))
