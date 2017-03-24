"""
This program reads user input from stdin and then tells them what moves to make
in order to avoid having to purchase drinks.

Inspiration for mex function was taken from GitHub user shitikanth at:
https://github.com/shitikanth/grundy/blob/master/grundy.py

Oliver Reid - 2569385
Thomas Youngson - 7444007
Gabe Meikle - 4563079
"""
##
# Imports
##
from sys import stdin
import re

##
# Globals
##
quantities = []
rules = []
allrules = ['0 1', '1 0']
moves = []

##
# Takes a rule and checks to see if it is already in the all rules array. If it
# is not it adds it, otherwise it continues.
#
# @param rule The rule to check then add to the allrules array.
##
def addRule(rule):
    if rule not in allrules:
        allrules.append(rule)

##
# Takes the rules array and generates all permutations of each rule according
# to each rules direction character.
##
def generateRules():
    for rule in rules:
        # Pick out each part of the rule
        firsthalf, secondhalf = rule.split()
        dir1 = firsthalf[0]
        num1 = int(firsthalf[1:])
        dir2 = secondhalf[0]
        num2 = int(secondhalf[1:])
        
        # Check our base case, where we don't need to generate any more rules.
        if dir1 == '=' and dir2 == '=':
            addRule(str(num1) + ' ' + str(num2))
        else:
            if dir1 == '>':
                if dir2 == '=':
                    for i in range(num1 + 1, quantities[0] + 1):
                        addRule(str(i) + ' ' + str(num2))
                elif dir2 == '>':
                    for i in range(num1 + 1, quantities[0] + 1):
                        for j in range(num2 + 1, quantities[1] + 1):
                            addRule(str(i) + ' ' + str(j))
                elif dir2 == '<':
                    for i in range(num1 + 1, quantities[0] + 1):
                        for j in range(0, num2):
                            addRule(str(i) + ' ' + str(j))
            elif dir1 == '<':
                if dir2 == '=':
                    for i in range(0, num1):
                        addRule(str(i) + ' ' + str(num2))
                elif dir2 == '>':
                    for i in range(0, num1):
                        for j in range(num2 + 1, quantities[1] + 1):
                            addRule(str(i) + ' ' + str(j))
                elif dir2 == '<':
                    for i in range(0, num1):
                        for j in range(0, num2):
                            addRule(str(i) + ' ' + str(j))

##
# Takes a set of numbers and then finds the smallest non negative number that
# is not in the supplied set.
#
# @param s A set of numbers to exlude from in the search to find the smallest
# non negative number.
# @return lowest The lowest non negative number not in the supplied set.
##
def mex(s):
    sortedset = sorted(s)
    lowest = 0
    while(sortedset and (lowest == sortedset.pop(0))):
        lowest += 1
    return lowest

##
# Checks each rule and plays it as a rule to see if it is a winning rule. If it
# is it will add it to the moves array, otherwise it will continue to the next
# rule.
#
# @param quantities The current quantities of our peanuts and pretzels.
# @return An array of winning rules (empty if no rules win).
##
def getMove(quan, rule = 0, found = False, winning = []):
    # Call our reference to global quantities
    global quantities

    # Declare the result of applying rules arrays
    peanuts = set([])
    pretzels = set([])
    playedMoves = []

    # Iterate (not EYEterate) over the rules
    for r in allrules:
        # Apply the r to each pile and add the result to an array
        p = quan[0] - int(r.split()[0])
        z = quan[1] - int(r.split()[1])
        if p >= 0 and z >= 0:
            peanuts.add(p)
            pretzels.add(z)

    # Get the lowest non negative integer from each set of states and XOR them
    grundy = mex(peanuts) ^ mex(pretzels)

    # Check our bail out case
    if found == False and grundy == 0:
        return False

    # Check the result of our grundy number
    if found == True and grundy == 0:
        winning.append(allrules[rule - 1])

    # Check to see if we have checked all the rules
    if rule == len(allrules):
        return winning

    # We got a nonzero grundy number so have an available winning move
    num1, num2 = allrules[rule].split()
    new1 = quantities[0] - int(num1)
    new2 = quantities[1] - int(num2)

    # Recurse to the next rule
    return getMove([new1, new2], rule + 1, True, winning)


##
# Main routine
##
quantity_line = re.compile("^\d+ \d+")
rule_line = re.compile("^[=><]\d+ [=><]\d+")
for userinput in stdin:
    # Check the input and add the data to the appropriate array
    if quantity_line.match(userinput):
        quantities.append(int(userinput.split()[0]))
        quantities.append(int(userinput.split()[1]))
    elif rule_line.match(userinput):
        rules.append(userinput.strip())

# Generate the rule permutations
generateRules()

# Call our main funtion to find moves
winning = getMove(quantities)
if winning == False:
    print("0 0")
else:
    if len(winning) == 0:
        print("0 0")
    else:
        for win in winning:
            print win
