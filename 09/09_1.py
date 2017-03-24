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
    for i, c in enumerate(n):
        if c.isdigit():
            continue
        else:
            errorList.append(str(type) + " has incorrect amount of digits")
            return [False, (index + 1) + i]
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
Checks that a given input is a number.

@param n The input to check is a number.
@return True if the input is a number, otherwise False.
"""
def digits(n, type, index, jump = 0, data = []):
    # Check that the input is valid digits

    print(n, type, index)
    if type == 'c':
        if n.isdigit():
            return False
    else:
        dots = scanLine(n, type)

        if dots[0]:
            n = int(n)
            return nrange(n, type, index, jump, data)
        else:
            return index + dots[1]

"""
Checks that a given string has two characters that match at index and two
greater than index.

@param s The string to check.
@param index The index to start at. 
@return True if the characters match, otherwise False.
"""
def match(s, index):
    # Check that the seperator characters are the same
    if s[index] == s[index + 3]:
        return True


"""
Checks that a give number is in a certain range depending on the type.

@param n The number to check is in a range.
@param type The type of range the number should be in.
"""
def nrange(n, type, index, jump = 0, data = []):
    # Get a reference to global variables
    global handle, sec

   # print(n, type)

    # Year
    if type == 'y':
        if n >= 1901 and n <= 2099:
            return index + 4
        else:
            errorList.append("year out of range")
            return index + 4

    # Month
    if type == 'm':
        if n >= 01 and n <= 12:
            return index + 2
        else:
            errorList.append("month out of range")
            return index + 2

    # Day
    if type == 'd':
        days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if data[1] == 02:
            if (data[0] % 4) == 0:
                if (data[0] % 100) == 0:
                    if (data[0] % 400) == 0:
                        if n >= 01 and n <= 29:
                            return index + 2
                        else:
                            errorList.append("day out of range")
                            return index + 2
                    else:
                        if n >= 01 and n <= 28:
                            return index + 2
                        else:
                            errorList.append("day out of range")
                            return index + 2
                else:
                    if n >= 01 and n <= 29:
                        return index + 2
                    else:
                        errorList.append("day out of range")
                        return index + 2
            else:
                if n >= 01 and n <= 28:
                    return index + 2
                else:
                    errorList.append("day out of range")
                    return index + 2
        else:
            if data[1] >= 0 and data[1] <= 12:
                if n >= 01 and n <= days[data[1] - 1]:
                    return index + 2
                else:
                    errorList.append("day out of range")
                    return index + 2
            else:
                errorList.append("day out of range")
                return index + 2

    # Hour
    if type == 'h':
        if n >= 00 and n <= 23:
            return index + 2
        else:
            errorList.append("hour out of range")
            return index + 2

    # Minute
    if type == 'n':
        if n >= 00 and n <= 59:
            return index + 2
        else:
            errorList.append("minute out of range")
            return index + 2

    # Second
    if type == 's':
        if n >= 00 and n <= 60:
            return index + 2
        else:
            errorList.append("second out of range")
            return index + 2

    # Offset
    if type == 'o':
        if n >= 000 and n <= 999:
            if data[4] != 60:
                return index + jump
            else:
                if (data[0] == 06 and data[1] == 30) or (data[0] == 12 and 
                    data[1] == 31):
                    if data[2] == 23 and data[3] == 59:
                        handle = True
                        sec[data[5]] = 1
                        return index + jump
        else:
            errorList.append("offset out of range")
            return index + jump

    return False

def validateDate(date, i):
    global handle, gdate
    handle = False

    try:
        index = 0

        y = date[index:index+4]
        index = digits(date[index:index+4], 'y', index)
        
        if not date[index].isdigit():
            if match(date, index) and date[index] in ' ./':
                index += 1
            else:
                errorList.append("date seperators don't match")
                index += 1

        m = date[index:index+2]
        index = digits(date[index:index+2], 'm', index)

        if not date[index].isdigit():
            index += 1

        d = date[index:index+2]
        index = digits(date[index:index+2], 'd', index, data = [int(y), int(m)])

        #print(index)

        if date[index] == 'T':
            index += 1
        else:
            errorList.append("T missing")

        h = date[index:index+2]
        index = digits(date[index:index+2], 'h', index)

        if not date[index].isdigit():
            if match(date, index) and date[index] in ' :.-':
                index += 1
            else:
                errorList.append("time seperators don't match")
                index += 1


        n = date[index:index+2]
        index = digits(date[index:index+2], 'n', index)

        if not date[index].isdigit():
            index += 1

        s = date[index:index+2]
        spos = [index, index+1]
        index = digits(date[index:index+2], 's', index)

        if date[index] in '.,':
            index += 1
            index = digits(date[index:-1], 'o', index, len(str(date[:-1])) 
                - index, [int(m), int(d), int(h), int(n), int(s), int(i)])

            if handle:
                date = list(date)
                date[spos[0]] = '5'
                date[spos[1]] = '9'
                gdate = ''.join(date)

        if date[index] == 'Z':
            index += 1
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
        print index, date[index], sys.exc_info()[0]
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
            for err in errorList:
                print err
            errorList = []

    print(passed)
    if len(passed) == 2:
        difference(passed[0], passed[1])

    print
        

