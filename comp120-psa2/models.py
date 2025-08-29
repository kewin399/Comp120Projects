"""
Modules: models

Classes associated with the models used by the Wordy application.

Authors:
- Sawyer Dentz - sdentz@sandiego.edu
- Cavin Nguyen - cavinnguyen@sandiego.edu
"""

import random
from enum import Enum, auto
from typing import Optional

class LetterState(Enum):
    CORRECT = 1
    INCORRECT = 2
    MISPLACED = 3


# DO NO MODIFY THIS CLASS
class NotAWordError(ValueError):
    pass

class WordyModel:
    """ Representation of the model used by the Wordy application. """

    # instance variables
    word_size: int  # size of the word
    word_list: list[str]  # list of valid words
    hidden_word: str  # the "hidden" word

    # the following is a "private" variable that the outside world shouldn't
    # know about or mess with.
    # It is dictionary that associates each letter in the hidden word with the
    # list of indices where that letter appears. If you are interested, check
    # out the _letter_positions method to see how this is generated.
    _hidden_word_letter_positions: dict[str, list[int]]

    def __init__(self, word_size: int, word_list_filename: str, preselected_word: Optional[str]=None) -> None:
        self.word_size = word_size

        self.word_list = []
        self.set_word_list(word_list_filename)

        self.hidden_word = ""
        self.set_word(preselected_word)

        self._hidden_word_letter_positions = self._letter_positions(self.hidden_word)


    def set_word_list(self, filename: str) -> None:
        """ Sets the word_list instance variable based on all the words of the
        given size (self.word_size) in the word file with name <filename>.

        Parameters:
            self (WordyModel): The object being modified.
            filename (str): name of the file containing a list of valid words.
        """
        self.word_list = []

        with open(filename, 'r') as f:
            for word in f:
                word = word.strip()
                if len(word) == self.word_size:
                    self.word_list.append(word)

        if len(self.word_list) == 0:
            raise RuntimeError(f"No words of length {self.word_size} found in {filename}")


    def set_word(self, preselected_word: Optional[str]) -> None:
        """ Sets the hidden_word, either to the preselected word or a random one from
        the word list if <preselected_word> is None.

        Parameters:
            preselected_word (str): The word to use for this round of the
                game, or None if a random word is to be selected.

        Raises:
            ValueError: When preselected_word isn't the proper size.
            NotAWordError: When preselected_word is not a valid word.
        """
        if preselected_word is None:
            self.hidden_word = random.choice(self.word_list)
        else:
            if len(preselected_word) != self.word_size:
                raise ValueError("preselected word isn't of the correct size")
            elif preselected_word not in self.word_list:
                raise NotAWordError("preselected word is not in the word list")
            else:
                self.hidden_word = preselected_word


    def check_guess(self, guess: str) -> tuple[bool, list[LetterState], dict[str, LetterState]]:
        """ Logs the guess to a file named guess_log.csv, then checks the
        given <guess> against the hidden word, returning three things.

        (1) Whether the guess was correct
        (2) A list of LetterState to indicate for each letter in the guess
        whether it was correct, incorrect, or a misplaced letter.
        (3) A dictionary that associates each letter in the guess with its
        state.

        Parameters:
            guess: (str) The guess to check.

        Return (type: tuple[bool, list[LetterState], dict[str, LetterState]]): if the guess was correct, 
        a list of letter states for each guessed letter, and a dictionary that associates each letter with its state

        """
        # open "guess_log.csv" and append hidden word and guessed word
        with open("guess_log.csv", "a") as out_file:
            out_file.write(f"{self.hidden_word}, {guess}\n")

        # raise NotAWordError if guess not in word list
        if guess not in self.word_list:

            raise NotAWordError
        
        # create variable to be returned
        correct = False
        letter_state_list = []
        letter_state_dict = {}

        # if guess is correct, return variable set to correct
        if guess == self.hidden_word:
            correct = True

        # loop through guess by index
        for i in range(len(guess)):
            # if guess is in the right position, append CORRECT
            if guess[i] == self.hidden_word[i]:
                letter_state_list.append(LetterState.CORRECT)
            # if letter not in correct position:
            elif guess[i] in self.hidden_word:
                # count how many duplicates have appeared before. If count exceeds the count in the hidden word, append INCORRECT
                if guess[0:i].count(guess[i]) >= self.hidden_word.count(guess[i]):
                    letter_state_list.append(LetterState.INCORRECT)
                    # if count does not exceed, append MISPLACED
                else:
                    letter_state_list.append(LetterState.MISPLACED)
            # if guess is not in word, append INCORRECT
            else:
                letter_state_list.append(LetterState.INCORRECT)



        # loop through guess by index
        for i in range(len(guess)):
            # initializes dictionary to avoid errors
            letter_state_dict[guess[i]] = None

            # if the current guess letter is at the same position as the current hidden word letter, set letterstate to correct
            if guess[i] == self.hidden_word[i]:
                letter_state_dict[guess[i]] = LetterState.CORRECT

            # if current guess letter not in correct position:
            elif guess[i] in self.hidden_word:
                if letter_state_dict[guess[i]] != LetterState.CORRECT: # set to correct if another letter in correct position
                    letter_state_dict[guess[i]] = LetterState.MISPLACED # set to incorrect if no other letter in correct position
            else:
                letter_state_dict[guess[i]] = LetterState.INCORRECT # otherwise set to incorrect

        return correct, letter_state_list, letter_state_dict


    def _letter_positions(self, word: str) -> dict[str, list[int]]:
        """ Returns a mapping between letters and the indexes at which the
        letter appears in the word.

        Parameters:
            word: (str) The word to analyze.

        Returns:
            (dict[str, list[int]]) Dictionary mapping character to its
            positions (i.e. indexes) in the given word.
        """
        letter_positions: dict[str, list[int]] = {}
        for i in range(len(word)):
            letter = word[i]
            letter_positions.setdefault(letter, []).append(i)
        return letter_positions
