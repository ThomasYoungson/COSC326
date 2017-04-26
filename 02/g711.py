"""
This program solves the generalized 711 problem. It tries a bruteforce approach but also
checks for math like properties e.g. if a number divides by the sum num multipled.

Thomas Youngson - 7444007
"""

#Globals
solutions = 0

#Rules are that each value must be positive and an integer number of cents
def findNumber(numAdd, numTimes):
    global solutions
    solution = []
    d = 1
    while(d < (numAdd - 3)):
        if(numTimes % d == 0):
            c = 1
            while((d + c <= (numAdd - 2)) and c <= d):
                if(numTimes % c == 0):
                    b = 1
                    while(((d + c + b) <= (numAdd - 1)) and b <= c):
                        a = numAdd - (d + c + b)
                        if(a <= b):
                            if((a*b*c*d) == numTimes):
                                #Check to see if we have already found a solution
                                if len(solution) == 0:
                                    solution = [a, b, c, d]
                                else:
                                    return(None)
                        b += 1
                c += 1
        d += 1

    #Check if we had a solution
    if len(solution):
        solutions += 1
        return("$%.2f" % float(numAdd/100.0) + " = " + "$%.2f" % float(solution[0]/100.0) + " + " + "$%.2f" % float(solution[1]/100.0) + " + " + "$%.2f" % float(solution[2]/100.0) + " + " + "$%.2f" % float(solution[3]/100.0))


##
# Main routine
##
for numAdd in range(100, 1000):
    numTimes = numAdd * 1000000
    result = findNumber(numAdd, numTimes)
    if result != None:
        print(result)

print(str(solutions) + " solutions")


