"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    if len(list1) > 0:
        new_list.append(list1[0])
        for element in list1[1:]:
            if element != new_list[-1]:
                new_list.append(element)

    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    idx1, idx2 = 0, 0

    for dummy_idx in range(len(list1)+len(list2)):
        if idx1 > len(list1) - 1:
            break
        elif idx2 > len(list2) - 1 :
            break            
        elif list1[idx1] < list2[idx2]:
            idx1 += 1
        elif list1[idx1] > list2[idx2]:
            idx2 += 1
        else:
            new_list.append(list2[idx2])
            idx1 += 1
            idx2 += 1
    
    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    new_list = []
    idx1, idx2 = 0, 0

    for dummy_idx in range(len(list1)+len(list2)):
        if idx1 > len(list1) - 1:
            new_list.append(list2[idx2])
            idx2 += 1
        elif idx2 > len(list2) - 1 :
            new_list.append(list1[idx1])
            idx1 += 1
            
        elif list1[idx1] <= list2[idx2]:
            new_list.append(list1[idx1])
            idx1 += 1
        else:
            new_list.append(list2[idx2])
            idx2 += 1
    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    mid = len(list1)/2
    list2 = merge_sort(list1[:mid])
    list3 = merge_sort(list1[mid:])
    return merge(list2, list3)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    new_strings = []
    if len(word) == 0:
        return [""]
    
    if len(word) == 1:
        return ["", word]
    else:
        first = word[0]
        rest = word[1:]

        new_strings = []
        rest_strings = gen_all_strings(rest)

        for dummy_str in rest_strings:
            for dummy_idx in range(len(dummy_str)):
                new_strings.append(dummy_str[:dummy_idx]+first+dummy_str[dummy_idx:])
            new_strings.append(dummy_str+first)
            
        new_strings += rest_strings
    return new_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_file = urllib2.urlopen(filename)
    word_list = []
    for dummy_word in word_file:
        word_list.append(dummy_word.strip())
    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
