"""
This program reads in data from stdin which determines a set of "moves" for our
ant to take. The program ends and reports back the location of the ant.

Group members

Oliver Reid - 2569385
Thomas Youngson - 7444007
"""

#Imports
from sys import stdin
import collections
import re

#Globals
directions = collections.OrderedDict()
changes = collections.OrderedDict()
steps = 0
face = 0
orig = False

##
# addData takes a line of input from stdin and stores it in our rules
# dictionary.
#
# @param userinput A line of user input.
##
def addData(userinput):
    #Use the global variable orig
    global orig
    
    #Break the userinput up
    state = userinput[0]
    direction = userinput[2:6]
    colour = userinput[7:11]
    
    #Check to see if the original state is set
    if orig == False:
        orig = state
        
    #Add it to the rules array
    directions[state] = direction
    changes[state] = colour


##
# moveAnt sets up the grid and then begins making the appropriate moves based on
# the rules dictionary. At the end of this cycle, it calls the giveAnswer
# function.
##
def moveAnt():
    #Get a reference to our global face
    global face, directions, changes, orig
    
    #Create our ant parameters
    visited = {}
    y = 0
    x = 0
    
    #Update current grid, move in direction according to rules
    for i in range(steps):
        #Get information from our current location
        tile = visited.get((y, x))
        
        if(tile == None):
            tile = orig
                    
        #Get our sequence of moves and replaces
        dirs = directions.get(tile)
        replace = changes.get(tile)
       
        
        #Update current cell on grid
        visited[(y, x)] = replace[face]
        
        
        #Get the move and make it
        move = dirs[face]
        
        #Update our face and coordinant
        if(move == 'N'):
            y = y + 1
            face = 0
        elif(move == 'E'):
            x = x + 1
            face = 1
        elif(move == 'S'):
            y = y - 1
            face = 2
        elif(move == 'W'):
            x = x - 1
            face = 3

    #Report our answer back
    print("# " + str(x) + " " + str(y))
    
    #Clean up for the next scenario
    directions = collections.OrderedDict()
    changes = collections.OrderedDict()
    face = 0
    orig = False

##
# Main routine
##
all_digits = re.compile("^\\d+$")
dna_line   = re.compile("^. [NEWS][NEWS][NEWS][NEWS] ....")
for userinput in stdin:
    #Check for comments
    if(userinput.startswith("#")):
        continue
    
    #Print the user input
    print(userinput.strip())
    
    #Check if the userinput is an integer
    if all_digits.match(userinput):
        steps = int(userinput)
        moveAnt()
    elif dna_line.match(userinput):
        addData(userinput)

