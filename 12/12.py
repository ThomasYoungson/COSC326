
"""
This program supersizes the idea behind the 711 problem and finds all solutions
between 1 dollar and 1000 dollars.

Group Members
Oliver Reid - 2569385
Thomas Youngson - 7444007
Gabe Meikle - 4563079
"""

"""
Imports
"""
import sys

"""
Globals
"""
factorCache = {}

"""
Helper function that prints our answer in the required format.

@param low The value that the other parts of the transaction sum to.
@param a The first part of the transaction.
@param b The second part of the transaction.
@param c The third part of the transaction.
@param d The fourth part of the transaction.
"""
def giveAnswer(low, a, b, c ,d):
    print "$"+"{0:.2f}".format((float(low))/100),
    print "=",
    print "$"+"{0:.2f}".format((float(a))/100),
    print "+",
    print "$"+"{0:.2f}".format((float(b))/100),
    print "+",
    print "$"+"{0:.2f}".format((float(c))/100),
    print "+",
    print "$"+"{0:.2f}".format((float(d))/100)

"""
Gets a list of the factors for a number n. Memoize's the factors so that we
aren't repeating work.

@param n The number to find the factors of.
@return 
"""
def getFactors(n):
    # Find the factors of n
    factorList = []
    for i in range(1, n/1000000):
        if n % i == 0:
            factorList.append(i)

    return factorList

def findNumber(low, high):
    solutions = []
    divs = getFactors(high)

    a = 0
    aDivs = divs[a]
    while a < len(divs):
        b = 0
        bDivs = divs[b]
        while aDivs + bDivs <= low - 2 and b <= a:
            c = 0
            cDivs = divs[c]
            while aDivs + bDivs + cDivs <= low - 1 and c <= b:
                dDivs = low - (aDivs + bDivs + cDivs)
                if dDivs <= cDivs:
                    if (aDivs * bDivs * cDivs * dDivs) == high:
                        solutions.append([low, dDivs, cDivs, bDivs, aDivs])
                cDivs = divs[c]
                c += 1
            bDivs = divs[b]
            b += 1
        aDivs = divs[a]
        a += 1

    # Check that we only have one unique solution
    if len(solutions) == 1:
        return solutions[0]

    return False
    
"""
Main routine
"""
def main():
    unique = []
    for i in reversed(range(100, int(sys.argv[1]))):
        solution = findNumber(i, i * 1000000)
        if solution:
            unique.append(solution)
        
    #Prints the final number of unique solutions
    solutions = len(unique)
    while unique:
        low, a, b, c ,d = unique.pop()
        giveAnswer(low, a, b, c, d)

    print str(solutions) + " solutions"

main()