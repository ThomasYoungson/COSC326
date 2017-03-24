"""
Finds all anagrams from a word and dictionary.

Thomas Youngson - 7444007
Oliver Reid - 2569385
"""

"""
Imports
"""
import sys
from sys import argv
from collections import Counter
from collections import defaultdict

"""
Globals
"""
lineList = []

"""
Uses the start word (word) and parts_list words to create the anagram.

@param orig is the anagram word untouched.
@param word the start word that everything else need to be added to.
@param parts_list is the other words that can be added to the sentence.
@param letters_left is the letters left that need to be in the sentace.
@return the sentence formed from the starting word.
"""
def form_anagram(orig,word,parts_list,letters_left):
	sentence = ""
	sentence += word
	ll = ""

 	letters_left_2 = letters_left[:]
 	parts_list_2 = parts_list[:]

	for letter in word:
		if letter in letters_left_2:
			letters_left_2.remove(letter)

	if(len(letters_left_2) > 0):
		for char in letters_left_2:
			ll += char
		parts_list_2 = find_anagram_parts(parts_list_2,ll)
		for wrdd in parts_list_2:
			lineList.append(form_anagram(orig,word + " " + wrdd,parts_list,
				letters_left))
	else:
		return sentence

	return sentence


def isAnagram(w1, w2):
    w1=list(w1.upper().replace(" ",""))
    w2=list(w2.upper().replace(" ",""))
    w2.sort()
    w1.sort()
    if w1==w2:
        return True
    else:
        return False

"""
Sorts the anagram and each dict word alphabetically and checks if they are in
one another and added to a list.

@param dict is a list of dictionary words.
@param anagram is the string form of the anagram.
@return a list of all words that fit into the anagram.
"""
def find_anagram_parts(dict,anagram):
	anList = []
	for word in dict:
		A = Counter(anagram)
		B = Counter(word)
		if (B & A) == B:
			anList.append(word)			
	return anList


"""
Loads the dictionary and returns as a list.
"""
def load_dictionary():
	dictionary = []
	for word in sys.stdin:
		dictionary.append(word.strip())
	return dictionary

"""
Sorting words in each line
"""
def sorting(max):
	listing = []
	for group in lineList:
		splitted = group.split()
		if len(splitted) <= max:
			splitted.sort()
			splitted.sort(key=len,reverse=True)
			stri = ""
			for item in splitted:
				stri += item + " "
			listing.append(stri)
	return listing

"""
Main function.
"""
def main():
	words  = load_dictionary()
	max_words = int(argv[2])

	anagram = ""
	for letter in str(argv[1]):
		if letter.islower():
			anagram += letter
	parts = find_anagram_parts(words,anagram)
	orig = anagram
	letters = []

	for letter in anagram:
		letters.append(letter)

	for word in parts:
		if isAnagram(word,anagram):
			lineList.append(word)
		else:
			form_anagram(orig,word,parts,letters)

	#Sort each line of the list.
	listing = sorting(max_words)		
	
	list_2 = []
	for wd in listing:
		if wd not in list_2 and isAnagram(wd,anagram):
			list_2.append(wd)
	list_2.sort()
	list_2.sort(key=len,reverse=False)

	for i in list_2:
		print(i)

main()
