"""
Module: dna_profiler

A program to use short tandem repeats (STRs) to identify a person using their
DNA.

Authors:
    1) Cavin Nguyen - cavinnguyen@sandiego.edu
    2) Sawyer Dentz - sdentz@sandiego.edu
"""

from typing import Tuple, List, Dict
from sys import argv

# Write your new functions below this point.
# Recall that all functions need type hints for all parameters and the return,
# AND must have docstrings in the correct format.


def read_dna_sequence(sequence_filename: str) -> str:
    """
    Reads into a file and returns a string of DNA sequence.
    
    Parameters: sequence_filename (str) - Name of file containing DNA sequence

    Returns: (str) String of DNA sequence

    >>> read_dna_sequence("alice.txt")
    'AGACGGGTTACCATGACTATCTATCTATCTATCTATCTATCTATCTATCACGTACGTACGTATCGAGATAGATAGATAGATAGATCCTCGACTTCGATCGCAATGAATGCCAATAGACAAAA'

    >>> read_dna_sequence("bob.txt")
    'AACCCTGCGCGCGCGCGATCTATCTATCTATCTATCCAGCATTAGCTAGCATCAAGATAGATAGATGAATTTCGAAATGAATGAATGAATGAATGAATGAATG'

    >>> read_dna_sequence("charlie.txt")
    'CCAGATAGATAGATAGATAGATAGATGTCACAGGGATGCTGAGGGCTGCTTCGTACGTACTCCTGATTTCGGGGATCGCTGACACTAATGCGTGCGAGCGGATCGATCTCTATCTATCTATCTATCTATCCTATAGCATAGACATCCAGATAGATAGATC'

    >>> read_dna_sequence("nomatch.txt")
    'GGTACAGATGCAAAGATAGATAGATGTCGTCGAGCAATCGTTTCGATAATGAATGAATGAATGAATGAATGAATGACACACGTCGATGCTAGCGGCGGATCGTATATCTATCTATCTATCTATCAACCCCTAG'

    """
    # open file and return first line as a string
    with open(sequence_filename, "r") as in_f:
        return in_f.readline().strip()
    

def create_dna_profiles(profiles_filename: str) -> dict[str, dict[str, int]]:
    """
    This function creates multiple dna profiles.

    Parameters: profiles_filename (str) - reads in the dna data of multiple profiles

    Returns: (dict) A dictionary of subdictionaries. In the dictionary the STRS are the key, and the 
    value is the subdictionary with the person's name as the key and repetition amount as the value.

    >>> create_dna_profiles("dna_database.csv")
    {'AGAT': {'Alice': 5, 'Bob': 3, 'Charlie': 6}, 'AATG': {'Alice': 2, 'Bob': 7, 'Charlie': 1}, 'TATC': {'Alice': 8, 'Bob': 4, 'Charlie': 5}}
    """
    profile = {} # dna profile to be created

    # open file containing profile data
    with open(profiles_filename, "r") as in_f:

        # read header and save STRs as a list and add a subdictionary for each STR
        strs = in_f.readline().strip().split(",")[1:]
        for i in strs:
            profile[i] = {}
        
        # loop through remaining line in file and add name and length of sequence to subdictionary
        for line in in_f:
            split_line = line.strip().split(",")
            for i in range(len(strs)):
                profile[strs[i]][split_line[0]] = int(split_line[i + 1])
    # return completed dna profile
    return profile


def find_max_consecutive(dna: str, target: str) -> int:
    """
    This function finds the maximum number of times the target STR shows up consecutively in the given DNA sequence.

    Parameters: dna (str) - The DNA strand to search for the STRs in.
    target (str) - The STR the function is searching for.

    Returns: (int) Returns an integer of the maximum number of times the target STR shows up consecutively.

    >>> find_max_consecutive("AACCCTGCGCGCGCGCGATCTATCTATCTATCTATCCAGCATTAGCTAGCATCAAGATAGATAGATGAATTTCGAAATGAATGAATGAATGAATGAATGAATG", "AGAT")
    3

    >>> find_max_consecutive("ATAACACTT", "AC")
    2

    >>> find_max_consecutive("AACACATTCACACACGT", "AC")
    3
    """
    max = 0 # maximum consecutive STR sequence
    count = 0 # current length of sequence
    position = 0 # current position in dna sequence

    # loop through all characters in string
    while position < len(dna):

        # if the current four characters match with the target, increase count and advance loop 4 characters
        if dna[position:position+len(target)] == target:
            count +=1
            position += len(target)
            if count > max:
                max = count

        # if the current four characters do not match, reset count and advance loop 1 character
        else:
            position += 1
            if count > max:
                max = count
            count = 0

    return max


def identify_dna(mystery_dna: str, dna_profiles: dict[str, dict[str, int]],) -> str:
    """
    This function finds which person is associated with the given dna sequence.

    Parameters: mystery_dna (str) - The dna sequence to be identified.
    dna_profiles (dict) - The dictionary containing the STR sequence length of each person.

    Returns (str): The name of the person associated with the mystery dna sequence.

    >>> identify_dna(read_dna_sequence("bob.txt"), create_dna_profiles("dna_database.csv"))
    'Bob'
    >>> identify_dna(read_dna_sequence("alice.txt"), create_dna_profiles("dna_database.csv"))
    'Alice'
    >>> identify_dna(read_dna_sequence("charlie.txt"), create_dna_profiles("dna_database.csv"))
    'Charlie'
    >>> identify_dna(read_dna_sequence("nomatch.txt"), create_dna_profiles("dna_database.csv"))
    'No match'
    """
    mystery_profile = {} # dna profile for unkown person
    names = [] # list of possible names that match the unkown profile

    # loop through STRs in the dna_profiles dictionary
    for str in dna_profiles:

        # create mystery dna profile
        mystery_profile[str] = find_max_consecutive(mystery_dna, str)

    # loop through dna_profile and add all names to list
    for strs in dna_profiles:
        for name in dna_profiles[strs]:
            if name not in names:
                names.append(name)
    
    # if STRs associated with a name does not match mystery_profile, remove the name from the list
    for (strs, reps) in dna_profiles.items():
        for name in names:
            if reps[name] != mystery_profile[strs]:
                names.remove(name)
    
    # if there is only 1 possible name, return it, otherwise return "No match"
    if len(names) == 1:
        return names[0]
    else:
        return "No match"

# keep the following code at the END of your file, as per convention
def main(sequence_filename: str, profiles_filename: str) -> None:
    """
    This function executes identify_dna() which calls the other functions and prints out the name of the mystery person.

    Parameters: sequence_filename (str) - filename of the person's DNA sequence
    profiles_filename (str) - filename of the dna database

    >>> main("bob.txt", "dna_database.csv")
    Bob
    >>> main("alice.txt", "dna_database.csv")
    Alice
    >>> main("charlie.txt", "dna_database.csv")
    Charlie
    >>> main("nomatch.txt", "dna_database.csv")
    No match
    """
    # Identifies and prints the names of the person corresponding to the DNA sequence given.
    print(identify_dna(read_dna_sequence(sequence_filename), create_dna_profiles(profiles_filename)))

if __name__ == "__main__":
    if len(argv) >= 3:
        main(argv[1],argv[2])
    else:
        print("Error: not enough terminal arguments specified.")
