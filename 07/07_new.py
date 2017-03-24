 ##
# Imports
##
from sys import stdin
import re
import collections
import sys

sys.setrecursionlimit(10000)

##
# Globals
##
quantities = []
rules = []
allrules = ['0 1', '1 0']
states = {}
final = []
grid = {}

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
            elif dir1 == '=':
                if dir2 == '>':
                    for i in range(num2 + 1, quantities[1] + 1):
                        addRule(str(num1) + ' ' + str(i))
                elif dir2 == '<':
                    for i in range(0, num2):
                        addRule(str(num1) + ' ' + str(i))

def buildGrid():
    for rule in allrules:
        # If we play a first move that leaves us at at the quantities of any
        # available move, then we know that that move is a bad move (will lose)
        grid[int(rule.split()[0]), int(rule.split()[1])] = [0]
    for rule in allrules:
        recurseAdd([int(rule.split()[0]), int(rule.split()[1])], 1)

def recurseAdd(last, i):
    for rule in allrules:
        state = i % 2
        p = last[0] + int(rule.split()[0])
        z = last[1] + int(rule.split()[1])

        if p <= quantities[0] and z <= quantities[1]:

            # Checks to see if we already have something at grid[p, z]
            try:
                # Just becuase current fails, doesn't mean a state off this
                # will also fail
                if 0 in grid[p, z]:
                    break
                grid[p, z].append(state)
            except KeyError:
                grid[p, z] = [state]


            recurseAdd([p, z], i + 1)
    return

quantity_line = re.compile("^\d+ \d+")
rule_line = re.compile("^[=><]\d+ [=><]\d+")
blank_line = re.compile("\n")
for userinput in stdin:
    # Check the input and add the data to the appropriate array
    if quantity_line.match(userinput):
        quantities.append(int(userinput.split()[0]))
        quantities.append(int(userinput.split()[1]))
    elif rule_line.match(userinput):
        rules.append(userinput.strip())
    elif blank_line.match(userinput):
        # Generate the rule permutations
        grid = {}
        generateRules()
        buildGrid()

        for rule in allrules:
            rule1 = int(quantities[0]) - int(rule.split()[0])
            rule2 = int(quantities[1]) - int(rule.split()[1])

            try:
                if sum(grid[rule1, rule2]) == len(grid[rule1, rule2]):
                    final.append((quantities[0] - rule1, quantities[1] - rule2))
            except:
                pass

        if not final:
            print "0 0"
        else:
            for fin in final:
                print str(fin[0]) + " " + str(fin[1])

        print # Remove this to remove spaces between printouts

        quantities = []
        rules = []
        allrules = ['0 1', '1 0']
        states = {}
        final = []
        grid = {}

generateRules()
grid = {}
buildGrid()

for rule in allrules:
    rule1 = int(quantities[0]) - int(rule.split()[0])
    rule2 = int(quantities[1]) - int(rule.split()[1])

    try:
        if sum(grid[rule1, rule2]) == len(grid[rule1, rule2]):
            final.append((quantities[0] - rule1, quantities[1] - rule2))
    except:
        pass

if not final:
    print "0 0"
else:
    for fin in final:
        print str(fin[0]) + " " + str(fin[1])