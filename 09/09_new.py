"""
This program reads in two time stamps, checks that they are valid and then
reports back the difference in milliseconds.

We have used a library called dateutil which can be found here:
https://goo.gl/b5eGaw

Oliver Reid - 2569385
Thomas Youngson - 7444007
Gabe Meikle - 4563079
"""

"""
Globals
"""
handle = False
sec = [0, 0]
gdate = False
errorList = []

"""
Imports
"""
from sys import stdin
import re
import sys
sys.path.append("python-dateutil-2.6.0")
import dateutil.parser as dp

"""
Takes a timestamp in ISO 8601 format and converts it to a NTP epoch
timestamp.

@param ts The ISO 8601 format timestamp to convert.
@return int The Unix epoch timestamp representation of ts.
"""
def convertTs(ts):
    parsedTime = dp.parse(ts)
    seconds = parsedTime.strftime('%s')
    return int(seconds) + 43200

"""
Scans the input for a set number of characters

@param n is the string that will be checked.
@param will allow the error message to print out what is causing the error.
@return will tell if the string has any chars before casting happens.
"""
def scanLine(n, amount, index, type):
    #print(n, amount, index, type)
    if n == '':
        errorList.append(str(type) + " has incorrect amount of digits")
        return [False, index]
    for i, c in enumerate(n):
        if c.isdigit():
            continue
        else:
            errorList.append(str(type) + " has incorrect amount of digits")
            return [False, index + i] # +1?
    return [True, index + amount]

"""
Takes two time stamps (in milliseconds) and finds the difference between
them.

@param fts The first time stamp to subtract from.
@param sts The second time stamp which is subtracted.
@return array About or exactly, difference in milliseconds.
"""
def difference(fts, sts):
    global sec
    fyear = int(fts[0:4])
    syear = int(sts[0:4])
    if fyear >= 1972 and fyear <= 2017 and syear >= 1972 and syear <= 2017:
        print("Exactly " + str((convertTs(fts) + sec[0])  - 
            (convertTs(sts) + sec[1])))
    else:
        print("About " + str((convertTs(fts) + sec[0])  - 
            (convertTs(sts) + sec[1])))

"""
Checks that a given string has two characters that match at index and two
greater than index.

@param s The string to check.
@param index The index to start at. 
@return True if the characters match, otherwise False.
"""
def match(s):
    # Check that the seperator characters are the same
    for c in s[1:-1]:
        if not c.isdigit():
            #print(c, s[0])
            if c == s[0]:
                return True
            else:
                return False
    return False

def secondCheck(s):
    for c in s:
        if not c.isdigit():
            if c in "ZT":
                return False
            return True
    return False

"""
Checks that a give number is in a certain range depending on the type.

@param n The number to check is in a range.
@param type The type of range the number should be in.
"""
def nrange(n, type, data = []):
    # Get a reference to global variables
    global handle, sec

    #print(n, type)
    n = int(n)

    # Year
    if type == 'y':
        if n < 1901 or n > 2099:
            errorList.append("year out of range")

    # Month
    if type == 'm':
        if n < 1 or n > 12:
            errorList.append("month out of range")

    # Day
    if type == 'd':
        days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if data[1] == 2:
            if (data[0] % 4) == 0:
                if (data[0] % 100) == 0:
                    if (data[0] % 400) == 0:
                        if n < 1 or n > 29:
                            errorList.append("day out of range")
                    else:
                        if n < 1 or n > 28:
                            errorList.append("day out of range")
                else:
                    if n < 1 or n > 29:
                        errorList.append("day out of range")
            else:
                if n < 1 or n > 28:
                    errorList.append("day out of range")
        else:
            if data[1] >= 0 and data[1] <= 12:
                if n < 1 or n > days[data[1] - 1]:
                    errorList.append("day out of range")
            else:
                errorList.append("day out of range")

    # Hour
    if type == 'h':
        if n < 0 or n > 23:
            errorList.append("hour out of range")

    # Minute
    if type == 'n':
        if n < 0 or n > 59:
            errorList.append("minute out of range")

    # Second
    if type == 's':
        if n < 0 or n > 60:
            errorList.append("second out of range")
        elif n == 60:
            if (data[0] == 6 and data[1] == 30) or (data[0] == 12 and data[1] == 31):
                if data[2] == 23 and data[3] == 59:
                    handle = True
                    #sec[data[4]] = 1
                else:
                    errorList.append("invalid second for hour and minute")
            else:
                errorList.append("invalid second for month")

            # Check minute seocnd etc correct


    # Offset
    if type == 'o':
        if n > 0 or n <= 999:
            if data[4] == 60:
                if (data[0] == 6 and data[1] == 30) or (data[0] == 12 and 
                    data[1] == 31):
                    if data[2] == 23 and data[3] == 59:
                        handle = True
                        sec[data[5]] = 1
                    else:
                        errorList.append("minute, hour and offset incompatible")
                else:
                    errorList.append("month, day and offset incompatible")
        else:
            errorList.append("offset out of range")

    return False

def validateDate(date, i):
    global handle, gdate
    handle = False
    toCheck = ['year', 'month', 'day', 'T', 'hour', 'minute', 'second', 'Z']

    try:
        index = 0

        year = scanLine(date[index:index+4], 4, index, 'year')
        y = date[index:year[1]]
        nrange(y, 'y')
        index = year[1]
        toCheck.remove('year')
        
        if not date[index].isdigit():
            if match(date[index:-1]) and date[index] in ' ./':
                index += 1
            else:
                errorList.append("date seperators don't match")
                index += 1
        else:
            if secondCheck(date[index:-1]):
                errorList.append("date seperators don't match")

        month = scanLine(date[index:index+2], 2, index, 'month')
        m = date[index:month[1]]
        nrange(m, 'm')
        index = month[1]
        toCheck.remove('month')

        if not date[index].isdigit():
            index += 1

        day = scanLine(date[index:index+2], 2, index, 'day')
        d = date[index:day[1]]
        nrange(d, 'd', [int(y), int(m)])
        index = day[1]
        toCheck.remove('day')

        if date[index] == 'T':
            index += 1
            toCheck.remove('T')
        else:
            errorList.append("T missing")

        hour = scanLine(date[index:index+2], 2, index, 'hour')
        h = date[index:hour[1]]
        nrange(h, 'h')
        index = hour[1]
        toCheck.remove('hour')
        #print(date[index])

        if not date[index].isdigit():
            if match(date[index:-1]) and date[index] in ' :.-':
                index += 1
            else:
                errorList.append("time seperators don't match")
                index += 1
        else:
            if secondCheck(date[index:-1]):
                errorList.append("time seperators don't match")

        minute = scanLine(date[index:index+2], 2, index, 'minute')
        n = date[index:minute[1]]
        nrange(n, 'n', [int(m), int(d), int(h), int(n)])
        index = minute[1]
        toCheck.remove('minute')

        if not date[index].isdigit():
            index += 1

        spos = [index, index+1]
        second = scanLine(date[index:index+2], 2, index, 'second')
        s = date[index:second[1]]
        nrange(s, 's',[int(m), int(d), int(h), int(n), int(i)])
        index = second[1]
        toCheck.remove('second')

        #print(date[index])
        if date[index] in '.,':
            index += 1
            off = date[index:date.find('Z')]
            if off != '':
                offset = scanLine(off, len(off), index, 'offset')
                o = date[index:offset[1]]
                nrange(o, 'o', [int(m), int(d), int(h), int(n), int(s), int(i)])
                index = offset[1]

                if handle:
                    date = list(date)
                    date[spos[0]] = '5'
                    date[spos[1]] = '9'
                    gdate = ''.join(date)
            else:
                errorList.append("no offset")

        if date[-1] == 'Z':
            index += 1
            toCheck.remove('Z')
        else:
            errorList.append("no Z after timestamp")

        if not errorList:
            return True

        if i == 0:
            print "Error in first timestamp"
        elif i == 1:
            print "Error in second timestamp"
        return False
    except:
        #print date, index, len(date), sys.exc_info()[0]
        if i == 0:
            print "Error in first timestamp"
        elif i == 1:
            print "Error in second timestamp"
        for err in toCheck:
            errorList.append(str(err) + " is missing")
        errorList.append("invalid entry - data too short")
        return False

for line in stdin:
    dates = line.split(' ', 1)
    passed = []

    for index, date in enumerate(dates):
        if validateDate(date.strip(), index) and len(date[date.find('Z') + 1:-1].strip()) == 0:
            if handle:
                passed.append(gdate.strip())
            else:
                passed.append(date.strip())
        else:
            if len(date[date.find('Z') + 1:-1].strip()) > 0:
                if date.find('Z') != -1:
                    errorList.append("junk detected after date")
            for err in errorList:
                print err
            errorList = []

    if len(passed) == 2:
        difference(passed[0], passed[1])

    print
        

