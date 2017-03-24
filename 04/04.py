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
from sys import stdin
sys.path.append("../sortedcontainers")
from sortedcontainers import SortedDict
import collections
import copy

##
# Globals
##
data = SortedDict()
criteria = sys.argv[1]
size = int(sys.argv[2])
side = 'l'

##
# This function takes a strip and updates its stock level.
#
# @param strip Strip of carpet whose stock is to be updated.
# @param quantity The current quantity of stock.
##
def updateStock(stock, strip, quantity):
    if quantity == 1:
        del stock[strip]
    else:
        stock[strip] -= 1
    return stock

##
# This function takes two pieces of strip and checks to see if they have any
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
# This function uses all of the quantity of a strip and adds it to the matt for
# max matches.
#
# @param stock The current stock of strips we have.
# @param matt The current state of the matt.
# @param strip The strip that we are using from stock.
# @param quantity The amount of the strip that we have.
# @return The updated matt.
##
def useAll(stock, matt, strip, quantity, rev = False):
    q = quantity
    while q > 0:
        matt.append(strip)
        if rev == True:
            stock = updateStock(stock, strip[::-1], q)
        else:
            stock = updateStock(stock, strip, q)
        q -= 1
    matches = (quantity - 1) * len(strip)
    return [matt, stock, matches]

##
# This function attempts to find a strip to add to our matt.
#
# @param matt The matt to add the strip to.
# @param pick The index to pick the strip from.
# @param criteria The number of matches we optimally would have.
# @return matt The new matt with the added strip or False. 
##
def addStrip(stock, matt, pick, criteria, strip = None, quantity = None, rev = False, last = False):
    if criteria == 'n':
        # Get our global reference to side
        global side

        # Check if we still have stock
        if len(stock) == 0:
            return False

        # Check to see if we have
        if last == False:
            if side == 'l' and pick == 0:
                return addStrip(stock, matt, pick, criteria, rev=rev, last=True)
            elif side == 'r' and pick == len(stock) - 1:
                return addStrip(stock, matt, pick, criteria, rev=rev, last=True)

        if strip == None and quantity == None:
            # Grab our current pick from stock
            strip, quantity = list(stock.items()[pick])

        matches = checkMatch(matt[-1], strip, rev)

        if matches == 0:
            # There were no matches, all good
            if rev == True:
                stock = updateStock(stock, strip[::-1], quantity)
            else:
                stock = updateStock(stock, strip, quantity)
            matt.append(strip)

            # Check which side
            if side == 'l': side = 'r'
            elif side == 'r': side = 'l'

            # Return the updated matt
            return matt
        else:
            # There were matches
            if rev == False:
                matt = addStrip(stock, matt, pick, criteria, strip[::-1], quantity, rev = True, last = last)
            else:
                if last == True and rev == True:
                    return False
                elif last == True and matches < (len(strip)/2) + 1:
                    return False
                else:
                    if side == 'l':
                        matt = addStrip(stock, matt, pick - 1, criteria)
                    elif side == 'r':
                        matt = addStrip(stock, matt, pick + 1, criteria)
        # Return the updated matt
        return matt
    elif criteria == 'm':
        pass


##
# This method attempts to create a matt out of strips of carpet where no two
# same pieces touch.
#
# @return An array representing the matt or impossible.
##
def noMatches():
    stock = collections.OrderedDict() # 'rgb' => 2 : 'strip' => quantity
    
    # Create the stock dictionary
    highestkey = None
    highest = 0
    for key, value in data.items():
        if value > highest:
            highestkey = key
            highest = value

    # Remove the highest value
    del data[highestkey]

    # Add the highest first
    stock[highestkey] = highest

    # Add the rest of the values
    for key, value in data.items():
        stock[key] = value

    matt = []
    pick = 0
    while len(matt) < size:
        # Check to see if the matt has any values, if not we add the first strip
        # from out stock
        if len(matt) == 0:
            # Select our strip and quantity
            strip, quantity = list(stock.items()[0])

            matt.append(strip)
            stock = updateStock(stock, strip, quantity) #WE CHANGED THIS LINE *********************************************
        else:
            # Check which side we are on and udpate pick accordingly
            if side == 'l':
                pick = len(stock) - 1
            elif side == 'r':
                pick = 0

            # Call our recursive function to
            matt = addStrip(stock, matt, pick, 'n')

            # Check to see if we added a strip
            if matt == False:
                return("Not possible")
            else:
                continue

    # Return our completed matt
    return(matt)

def mostMatches():
    # Do stuff
    stock = data
    matt = []
    totalmatches = 0
    rev = False

    while len(matt) < size:
        # Start building the matt
        if len(matt) == 0:
            # Select the first strip
            strip, quantity = list(stock.items()[0])

            # Add to the matt and update our stock
            updates = useAll(stock, matt, strip, quantity)
            matt = updates[0]
            stock = updates[1]
            totalmatches += updates[2]
        else:
            # Get the last value added to the matt so we can get the next best match
            check = matt[-1]

            # Declare our data to record the highest match
            highestmatches = 0
            higheststrip = None
            highestquantity = 0

            # Check our last matt strip against all other strips to see which has the highest matches
            for strip, quantity in stock.items():
                # Try regular and reversed
                matches = checkMatch(check, strip)
                revmatches = checkMatch(check, strip[::-1])

                if matches > highestmatches:
                    highestmatches = matches
                    if matches < revmatches:
                        rev = True
                        highestmatches = revmatches
                    higheststrip = strip
                    highestquantity = quantity

            # Add the matches between the two groups
            totalmatches += highestmatches

            # Ensure that we set our values to add to the matt
            if higheststrip == None:
                higheststrip, highestquantity = stock.items()[0]

            # Add to the matt and update our stock
            if rev == True:
                updates = useAll(stock, matt, higheststrip[::-1], highestquantity, rev)
            else:
                updates = useAll(stock, matt, higheststrip, highestquantity)
            matt = updates[0]
            stock = updates[1]
            totalmatches += updates[2]

    return(matt, totalmatches)


def balanceMatches():
    # Do stuff
    stock = data
    matt = []
    totalmatches = 0
    totalnonmatches = 0
    rev = False
    mode = True

    while len(matt) < size:
        if len(matt) == 0:
            # Select the first strip
            strip, quantity = list(stock.items()[0])

            # Add to the matt and update our stock
            matt.append(strip)
            updateStock(stock, strip, quantity)
        else:

            check = matt[-1]

            #Lets find matches
            if mode:
                #Reset rev
                rev = False

                # Declare our data to record the highest match
                highestmatches = 0
                higheststrip = None
                highestquantity = 0

                # Check our last matt strip against all other strips to see which has the highest matches
                for strip, quantity in stock.items():
                    # Try regular and reversed
                    matches = checkMatch(check, strip)
                    revmatches = checkMatch(check, strip[::-1])

                    if matches > highestmatches:
                        highestmatches = matches
                        if matches < revmatches:
                            rev = True
                            highestmatches = revmatches
                        higheststrip = strip
                        highestquantity = quantity

                totalmatches += highestmatches
                totalnonmatches += len(strip) - highestmatches

                # Ensure that we set our values to add to the matt
                if higheststrip == None:
                    higheststrip, highestquantity = stock.items()[0]

                if rev:
                    matt.append(higheststrip[::-1])
                else:
                    matt.append(higheststrip)
                stock = updateStock(stock, higheststrip, highestquantity)
                mode = False

            else:
                #Reset rev
                rev = False

                # Declare our data to record the lowest match
                lowestmatches = len(strip) + 1
                loweststrip = None
                lowestquantity = 0

                # Check our last matt strip against all other strips to see which has the highest matches
                for strip, quantity in stock.items():
                    # Try regular and reversed
                    matches = checkMatch(check, strip)
                    revmatches = checkMatch(check, strip[::-1])

                    if matches < lowestmatches:
                        lowestmatches = matches
                        if revmatches < matches:
                            rev = True
                            lowestmatches = revmatches
                        loweststrip = strip
                        lowestquantity = quantity

                totalmatches += lowestmatches
                totalnonmatches += len(strip) - lowestmatches

                # Ensure that we set our values to add to the matt
                if loweststrip == None:
                    loweststrip, lowestquantity = stock.items()[0]

                matt.append(loweststrip)
                stock = updateStock(stock, loweststrip, lowestquantity)
                mode = True

    return [matt, totalmatches, totalnonmatches]

def giveAnswer(matt): 
    for strip in matt:
        print(strip)
                    
##
# Main routine
##
def main():
    for userinput in stdin:
        userinput = userinput.strip()
        #Add the stock
        if data.get(userinput) == None:
            data[userinput] = 1
        else:
            data[userinput] += 1

    #Check the flags
    if criteria == '-n':
        nm = noMatches()
        if type(nm) is str:
            print(nm)
        else:
            giveAnswer(nm)
    elif criteria == '-m':
        mm = mostMatches()
        giveAnswer(mm[0])
        print("Matches: " + str(mm[1]))
    elif criteria == '-b':
        bm = balanceMatches()
        giveAnswer(bm[0])
        print("Matches: " +  str(bm[1]))
        print("Non matches: " + str(bm[2]))
main()