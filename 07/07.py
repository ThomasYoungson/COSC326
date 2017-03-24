#!/usr/bin/python

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
states = {}
ori = ()
final = []

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
# Checks whether the state is a winning state or a losing state
#
# @params takes the Peanuts & Pretzels quanitities
##                            
def checkState(quantities):
    global final, ori
    peanuts, pretzels = quantities[0], quantities[1]
    # Check whether quantities are already in states
    if tuple(quantities) in states:
        return states[tuple(quantities)]
    else:
        found = False    
        for rule in allrules:
            rule1, rule2 = rule.split()
            p, z = peanuts - int(rule1), pretzels - int(rule2)
            if p < 0 or z < 0:
                continue
            newQuant = (p,z)
            
            if newQuant not in states.keys():
                if not checkState(newQuant):
                    found = True
                    
            if newQuant == (0,0) or (newQuant in states.keys() and states[newQuant] == False):
                found = True
                if (peanuts,pretzels) == ori:
                    final.append(rule)
                    
    states[peanuts,pretzels] = found
    return found
        
##
# Main routine
##
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
        generateRules()
        ori = tuple(quantities)
        checkState(quantities)

        if not final:
            print "0 0"
        else:
            for i in final:
                print i
        print

        # Reset our scenario variables
        quantities = []
        rules = []
        allrules = ['0 1', '1 0']
        states = {}
        ori = ()
        final = []

# Generate the final scenario
generateRules()
ori = tuple(quantities)
checkState(quantities)
if not final:
    print "0 0"
else:
    for i in final:
        print i
