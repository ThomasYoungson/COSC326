"""
Finds all anagrams from a word and dictionary.

Thomas Youngson - 7444007
Oliver Reid - 2569385
"""

##
# Imports
##
import sys
from sys import argv

##
# Uses the start word (word) and parts_list words to create the anagram.
#
# @param word the start word that everything else need to be added to.
# @param parts_list is the other words that can be added to the sentence.
# @param letters_left is the letters left that need to be in the sentace.
# @param size the size of the amount of words that should be in the sentence. 
# @return the sentence formed from the starting word.
##
def form_anagram(word, parts_list, letters_left, size):
	sentence = word
	#use the find_anagram_parts to see what could be added in. By sending parts_list as the dict and letters_left turned into a string as the anagram

	return sentence

##
# Sorts the anagram and each dict word alphabetically and checks if they are in
# one another and added to a list.
#
# @param dict is a list of dictionary words.
# @param anagram is the string form of the anagram.
# @return a list of all words that fit into the anagram.
##
def find_anagram_parts(dict, anagram):
	anList = []
	b = ''.join(sorted(anagram))

	for word in dict:
		a = ''.join(sorted(word))
		if word == anagram:
			anList.append(word)
		elif a in b:
			anList.append(word)
	return anList


##
# Loads the dictionary and returns as a list.
#
# @return a list containing the dictionary.
##
def load_dictionary():
	dictionary = []
	for word in sys.stdin:
		dictionary.append(word.strip())
	return dictionary

##
# Main function.
##
def main():
	words  = load_dictionary()
	# Argv 1 is the anagram.
	anagram = str(argv[1])

	# Argv 2 is the most words used from dict.
	max_words = int(argv[2])

	# Reads in the anagram and splits into a list of chars.
	letters = []
	for letter in anagram:
		letters.append(letter)

	# Sends the current dict and letters
	parts = find_anagram_parts(words, anagram)

	size = len(anagram)
	anagram_list = []
	for word in parts:
		anagram_list.append(form_anagram(word,parts,letters,size))

	print("Returned List")
	print(anagram_list)

	# Sort the returned anagrams in the correct order to be printed
	# Also check that the anagram sentace is only max_words or less. 

main()