"""
This program reads in two time stamps, checks that they are valid and then
reports back the difference in milliseconds.

We have used a library called dateutil which can be found here:
https://goo.gl/b5eGaw

Oliver Reid - 2569385
Thomas Youngson - 7444007
Gabe Meikle - 4563079
"""

##
# Imports
##
from sys import stdin
import re
import sys
sys.path.append("python-dateutil-2.6.0")
import dateutil.parser as dp

##
# Takes a timestamp in ISO 8601 format and converts it to a NTP epoch
# timestamp.
#
# @param ts The ISO 8601 format timestamp to convert.
# @return int The Unix epoch timestamp representation of ts.
##
def convertTs(ts):
    parsedTime = dp.parse(ts)
    seconds = parsedTime.strftime('%s')
    return int(seconds) + 43200

##
# Takes two time stamps (in milliseconds) and finds the difference between
# them.
#
# @param fts The first time stamp to subtract from.
# @param sts The second time stamp which is subtracted.
# @return array About or exactly, difference in milliseconds.
##
def difference(fts, sts):
    fyear = int(fts[0:4])
    syear = int(sts[0:4])
    if fyear >= 1972 and fyear <= 2017 and syear >= 1972 and syear <= 2017:
        print("Exactly " + str(convertTs(fts) - convertTs(sts)))
    else:
        print("About " + str(convertTs(fts) - convertTs(sts)))


##
# Main routine
##
valid_timestamp = re.compile('(190[1-9]|19[1-9][0-9]|20[0-9][0-9])(?P<datesep>'
                            '[ ./]*)'
                            '(0[1-9]|1[0-2])(?P=datesep)([0-2][1-9]|3[0-1])T'
                            '([0-1][0-9]|2[0-3])(?P<timesep>[:.-]*)'
                            '([0-5][0-9])(?P=timesep)'
                            '([0-5][0-9]|[0-5][0-9][.,][0-9]{1,3}|60[.,][0-9]'
                            '{1,3})Z\s(190[1-9]|19[1-9][0-9]|20[0-9][0-9])'
                            '(?P<datesep1>'
                            '[ ./]*)(0[1-9]|1[0-2])(?P=datesep1)([0-2][1-9]'
                            '|3[0-1])T([0-1][0-9]|2[0-3])(?P<timesep1>[:.-]*)'
                            '([0-5][0-9])(?P=timesep1)([0-5][0-9]|[0-5][0-9]'
                            '[.,][0-9]{1,3}|60[.,][0-9]{1,3})Z')
for line in stdin:
    if valid_timestamp.match(line):
        difference(line.split()[0], line.split()[1])
    else:
        print("Error")
