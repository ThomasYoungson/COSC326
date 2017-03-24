"""
This program reads in data from stdin. It processes this data to fit a number
of scenarios, in order to create a matt from strips of carpet. It then reports
back the matt, depending on the rules of the scenario.

Referneces:
We are using a library called "sortedcontainers" created by Grant Jenks at
https://github.com/grantjenks/sorted_containers to provide a way to keep items
in a dictionary stored, based on their values.

Three types:
	OrderedDict to order by alphabetic
	Front to hold the most
	SortedDict to order by insertion (most and then the rest)

Oliver Reid - 2569385
Thomas Youngson - 7444004
Gabe Meikle - 4563079
-
"""
##
# Imports
##
import sys
import random
from sys import stdin
from sortedcontainers import SortedDict

##
# Globals
##
stock = SortedDict() # 'rgb' => 2 : 'strip' => quantity
criteria = sys.argv[1]
size = int(sys.argv[2])
side = 'l'

##
# This method takes a strip and updates its stock level.
#
# @param strip Strip of carpet whose stock is to be updated.
# @param quantity The current quantity of stock.
##
def updateStock(strip, quantity):
    if quantity == 1:
        del stock[strip]
    else:
        stock[strip] -= 1

##
# This method takes two pieces of strip and checks to see if they have any
# same tiles touching (matches).
#
# @param last The last strip that we added to our matt.
# @param curr The current strip that we want to add to our matt.
# @return int The number of matches between the two strips.
def checkMatch(last, curr, rev = False):
	matches = 0
	for index, tile in enumerate(curr):
		if tile == last[index]:
			matches += 1
	return matches

##
# This method attempts to find a strip to add to our matt.
#
# @param matt The matt to add the strip to.
# @param pick The index to pick the strip from.
# @param criteria The number of matches we optimally would have.
# @return matt The new matt with the added strip or False. 
##
def addStrip(matt, pick, criteria, strip = None, quantity = None, rev = False, last = False):
	#Get our global reference to side
	global side

	#Check if we still have stock
	if len(stock) == 0:
		return False

	#Check to see if we have
	if last == False:
		if side == 'l' and pick == 0:
			return addStrip(matt, pick, criteria, last = True)
		elif side == 'r' and pick == len(stock) - 1:
			return addStrip(matt, pick, criteria, last = True)

	if strip == None and quantity == None:
		#Grab our current pick from stock
		strip, quantity = list(stock.items()[pick])

	if criteria == 'n':
		matches = checkMatch(matt[-1], strip, rev)

		if matches == 0:
			#There were no matches, all good
			if rev == True:
				updateStock(strip[::-1], quantity)
			else:
				updateStock(strip, quantity)
			matt.append(strip)

			#Check which side
			if side == 'l': side = 'r'
			elif side == 'r': side = 'l'

			#Return the updated matt
			return matt
		else:
			#There were matches
			if rev == False and matches < (len(strip)/2) + 1:
				matt = addStrip(matt, pick, criteria, strip[::-1], quantity, True)
			else:
				if last == True:
					return False
				else:
					if side == 'l':
						matt = addStrip(matt, pick - 1, criteria)
					elif side == 'r':
						matt = addStrip(matt, pick + 1, criteria)
		#Return the updated matt
		return matt

##
# This method attempts to create a matt out of strips of carpet where no two
# same pieces touch.
#
# @return An array representing the matt or impossible.
##
def noMatches():
	matt = []
	pick = 0
	while len(matt) < size:
		#Check to see if the matt has any values, if not we add the first strip
		#from out stock
		if len(matt) == 0:
			#Select our strip and quantity
			strip, quantity = list(stock.items()[0])

			matt.append(strip)
			updateStock(strip, quantity)
		else:
			#Check which side we are on and udpate pick accordingly
			if side == 'l':
				pick = len(stock) - 1
			elif side == 'r':
				pick = 0

			#Call our recursive function to
			matt = addStrip(matt, pick, 'n')

			#Check to see if we added a strip
			if matt == False:
				return("not possible")
			else:
				continue

	#Return our completed matt
	return(matt)
##
# Main routine
##
def main():
	for userinput in stdin:
		userinput = userinput.strip()
		#Add the stock
		if stock.get(userinput) == None:
			stock[userinput] = 1
		else:
			stock[userinput] += 1
	print(stock)

	#Check the flags
	if criteria == '-n':
		print(noMatches())
	elif criteria == '-m':
		print("m flag")
	elif criteria == '-b':
		print("b flag")

main()