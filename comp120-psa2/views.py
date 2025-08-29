"""
Module: views

Code related to the View of our Wordy application.

Authors:
- Sawyer Dentz - sdentz@sandiego.edu
- Cavin Nguyen - cavinnguyen@sandiego.edu
"""
from typing import Optional, Union, Callable, Any
import string, time
import tkinter as tk
import tkinter.font as font
from models import LetterState

class GuessLetter(tk.Frame):

    # instance variables
    settings: dict  # the dictionary with all the UI settings
    label: tk.Label  # the label containing the text for this frame

    def __init__(self, parent: Union[tk.Tk, tk.Frame], row: int, col: int, settings: dict) -> None:
        super().__init__(parent)

        self.settings = settings

        # set the "width" and "height" properties of this frame based on the given
        # settings.
        self['width'] = settings['ui']['guesses']['letter_box_size']
        self['height'] = settings['ui']['guesses']['letter_box_size']

        # set the "bg" property of this frame based on the given settings
        self['bg'] = settings['ui']['guesses']['initial_bg_color']

        # set the location of this letter based on the row and ocl parameters. set padx and pady based on settings
        self.grid(row= row, column= col, padx= settings['ui']['guesses']['letter_padding'], pady= settings['ui']['guesses']['letter_padding'])

        # Tell this frame to use the exact width/height set above instead of
        # resizing to fit its contents.
        self.grid_propagate(False)

        # Set the type of font used
        font_style = font.Font(family=settings['ui']['font_family'])

        # create a tk.Label and set "bg", "fg", and "font" based on settings
        self.label = tk.Label(self, 
                              bg= settings['ui']['guesses']['initial_bg_color'], 
                              fg= settings['ui']['guesses']['initial_text_color'],
                              font= (font_style, settings['ui']['guesses']['letter_font_size']))


        # WARNING: don't change anything below here in this method

        # Place the label inside of this frame using grid
        self.label.grid(row=1, column=1, sticky='ewns')

        # Somewhat mystifying code to ensure that the label is centered
        # within the frame.
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


    def set_letter(self, letter: str) -> None:
        """ Sets the self.label's text to the given letter.

        Precondition: letter is only a single character.

        Parameter:
            letter: (str) The letter to set this to.
        """
        # precondition: letter is only a single character
        assert len(letter) == 1, "letter must be a single character"

        # set label to given character
        self.label.config(text= letter)


    def set_status(self, state: LetterState) -> None:
        """ Updates the background color based on the LetterState (using the
        colors defined in settings) and the text/fg color (also based on
        settings).

        Parameters:
            state (LetterState): The state used to determine the color of the background and foreground (text)
        """

        # update "bg" for label and frame depending on what the letter state is. "bg" is updated based on settings
        if state == LetterState.CORRECT:
            self.label.config(bg= self.settings['ui']['correct_color'])
            self.config(bg= self.settings['ui']['correct_color'])
        elif state == LetterState.MISPLACED:
            self.label.config(bg = self.settings['ui']['misplaced_color'])
            self.config(bg = self.settings['ui']['misplaced_color'])
        else:
            self.label.config(bg= self.settings['ui']['incorrect_color'])
            self.config(bg = self.settings['ui']['incorrect_color'])

        # update "fg" based on settings
        self.label.config(fg= self.settings['ui']['guesses']['updated_text_color'])


class GuessesFrame(tk.Frame):
    """ A Tk Frame used to display the guesses that user has made. """

    # instance variables
    settings: dict  # the dictionary with all the UI settings
    guess_letters: list[list[GuessLetter]] # 2D list of letters (i.e. the matrix of guess letter)

    def __init__(self, parent: Union[tk.Tk, tk.Frame], settings: dict) -> None:
        super().__init__(parent)

        self.settings = settings

        self['height'] = settings['ui']['guesses']['frame_height']
        self['width'] = settings['ui']['window_width']

        # place this frame into the parent using the pack layout manager
        self.pack(pady=(20, 0))
        self.pack_propagate(False)

        self.guess_letters = []

        # loop through num_guesses and word_size. create a GuessLetter for each x,y value in a matrix
        for y in range(settings['num_guesses']):
            self.guess_letters.append([])
            for x in range(settings['word_size']):
                self.guess_letters[y].append(GuessLetter(self, y, x, self.settings))

        # Do not modify any of this method's code below this point.

        # The following code ensures that the guesses are centered both
        # horizontally and vertically within this frame.
        self.columnconfigure(0, weight=1)
        self.columnconfigure(settings['word_size']+1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(settings['num_guesses']+1, weight=1)


    def set_letter(self, letter: str, guess_num: int, letter_index: int) -> None:
        """ Sets the guess letter at the <letter_index> in the specified <guess_num> to <letter>.

        Preconditions:
            guess_num is between 0 and num guesses
            col is between 0 and word size

        Parameters:
            letter: (str) The letter (duh?)
            guess_num: (int) The number of the guess to update
            letter_index: (int) The index in the guess that will be updated
        """

        # preconditions:
        assert 0 <= guess_num < self.settings['num_guesses']
        assert 0 <= letter_index <= self.settings['word_size']

        # set the letter of the GuessLetter at the given guess_num and letter_index
        self.guess_letters[guess_num][letter_index].set_letter(letter)


    def show_guess_result(self, guess_num: int, results: list[LetterState]) -> None:
        """ Updates the specific guess based on the given results.

        Note that there should be a delay between the update of each letter in
        the guess; this delay time is located in self.settings.

        Preconditon: len(results) == word size

        Parameters:
            guess_num: (int) The number of the guess to update
            results: (list[LetterState]) The state of each letter in the guess.

        """
        # precondition
        assert len(results) == self.settings['word_size']

        # loop through each GuessLetter in the current guess, updating the color depending on the given result list
        for i in range(len(self.guess_letters[guess_num])):
            self.update()
            time.sleep(self.settings['ui']['guesses']['process_wait_time'])
            self.guess_letters[guess_num][i].set_status(results[i])



class MessageFrame(tk.Frame):
    """ A Tk Frame used to display a message to the user. """

    # instance variables
    settings: dict  # the dictionary with all the UI settings
    message_str: tk.StringVar  # the message being displayed
    message_timer: Optional[Any]

    def __init__(self, parent, settings: dict) -> None:
        super().__init__(parent)

        self['height'] = settings['ui']['messages']['frame_height']

        # place this frame into its parent using the pack layout manager
        self.pack(pady=20, fill=tk.X)

        self.pack_propagate(False)

        self.message_str = tk.StringVar()
        f = font.Font(family=settings['ui']['font_family'])
        message_label = tk.Label(self, textvariable=self.message_str,
                                 font=(f, settings['ui']['messages']['font_size']))
        message_label.place(relx=.5, rely=.5, anchor="center")

        self.message_timer = None
        self.set_message("It's Wordy time. Let's GO!!!")


    def set_message(self, message: str, time: int = 0):
        """ Sets the message, clearing it after the specified amount of time.

        Note that the unit of <time> will be seconds. If <time> is zero

        Precondition: time is non-negative

        Parameters:
            message: (str) The message to use
            time: (int) The length of time (in seconds) before the message will be cleared.
        """
        assert time >= 0

        if self.message_timer is not None:
            self.after_cancel(self.message_timer)
            self.message_timer = None

        self.message_str.set(message)

        if time > 0:
            self.message_timer = self.after(time * 1000, self.clear_message)

    def clear_message(self):
        """ Clears the message. """
        self.message_str.set("")
        self.message_timer = None



class KeyboardFrame(tk.Frame):
    """ A Tk Frame used to display a keyboard to the user. """

    # instance variables
    settings: dict  # the dictionary with all the UI settings
    keyboard_buttons: dict[str, tk.Button]  # associates a letter ("A") with the corresponding Button

    def __init__(self, parent, settings: dict) -> None:
        super().__init__(parent)

        self.settings = settings

        self['height'] = settings['ui']['keyboard']['frame_height']
        self['width'] = settings['ui']['window_width']

        # put solid border around keyboard to really make it POP!
        self['borderwidth'] = 1
        self['relief'] = 'solid'

        self.pack(fill=tk.X, ipadx=10, ipady=20)
        self.pack_propagate(False)

        self.keyboard_buttons = {}
        self.add_keyboard_buttons()


    def add_keyboard_buttons(self) -> None:
        """ Creates and places keyboard buttons. """

        # Create frames for the rows of keyboard buttons
        keyboard_button_frames = []

        for i in range(3):
            frame = tk.Frame(self)
            frame.grid(row=i+1, column=1)
            keyboard_button_frames.append(frame)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        layout = self.settings['ui']['keyboard']['key_layout']

        f = font.Font(family=self.settings['ui']['font_family'])

        # Create keyboard buttons
        for r in range(3):
            for c in range(len(layout[r])):
                if layout[r][c] == 'ENTER':
                    button = tk.Button(keyboard_button_frames[r],
                                       width=self.settings['ui']['keyboard']['key_width_long'],
                                       text=layout[r][c],
                                       fg=self.settings['ui']['keyboard']['text_color'],
                                       font=f)

                elif layout[r][c] == "BACK":
                    button = tk.Button(keyboard_button_frames[r],
                                       width=self.settings['ui']['keyboard']['key_width_long'],
                                       text=layout[r][c],
                                       fg=self.settings['ui']['keyboard']['text_color'],
                                       font=f)
                else:
                    button = tk.Button(keyboard_button_frames[r],
                                       width=self.settings['ui']['keyboard']['key_width'],
                                       text=layout[r][c],
                                       fg=self.settings['ui']['keyboard']['text_color'],
                                       font=f)

                button.grid(row=r, column=c)

                self.keyboard_buttons[layout[r][c].lower()] = button

    def set_key_colors(self, key_states: dict[str, LetterState]) -> None:
        """ Updates the colors of keys based on their states.

        Parameters:
            key_states (dict[str, LetterState]): Dictionary mapping key to its state
        """
        for letter, state in key_states.items():
            if state == LetterState.CORRECT:
                text_color = self.settings["ui"]["correct_color"]
            elif state == LetterState.INCORRECT:
                text_color = self.settings["ui"]["incorrect_color"]
            else:
                text_color = self.settings["ui"]["misplaced_color"]

            self.keyboard_buttons[letter]['fg'] = text_color


    def disable(self):
        """ Disables the keyboard by setting the state of all buttons to 'disabled'. """
        for button in self.keyboard_buttons.values():
            button['state'] = "disabled"


    def set_key_handler(self, key: str, handler: Callable[[], None]) -> None:
        """ Sets the handler for the given keyboard key.

        Precondition: key is a valid keyboard key (i.e. A-Z, "ENTER", or "BACK")

        Parameters:
            key: (str) The keyboard key to set the handler for.
            handler: Callable[[], None]) The handler function to call when the key is pressed.
        """

        # precondition
        assert key in self.keyboard_buttons

        # set keyboard button command to handler
        self.keyboard_buttons[key].config(command= handler)


class WordyView:
    """ Class that creates represents the Tk application. """

    # instance variables
    settings: dict  # the dictionary with all the UI settings
    window: tk.Tk  # the top-level application window

    guesses_frame: GuessesFrame  # the frame for holding the guesses
    message_frame: MessageFrame  # the frame for displaying a message
    keyboard_frame: KeyboardFrame  # the frame for holding the keyboard

    def __init__(self, settings: dict) -> None:

        self.settings = settings

        # Create window and set title
        self.window = tk.Tk()
        self.window.title("Wordy")

        # Create three primary window frames: guesses, messages, and keyboard

        self.guesses_frame = GuessesFrame(self.window, settings)
        self.message_frame = MessageFrame(self.window, settings)
        self.keyboard_frame = KeyboardFrame(self.window, settings)


    def set_letter(self, letter: str, guess_num: int, letter_index: int) -> None:
        """ Sets the guess letter at the <letter_index> in the specified <guess_num> to <letter>.

        Preconditions:
            guess_num is between 0 and num guesses
            col is between 0 and word size

        Parameters:
            letter: (str) The letter (duh?)
            guess_num: (int) The number of the guess to update
            letter_index: (int) The index in the guess that will be updated
        """

        # precondition:
        assert 0 <= guess_num < self.settings['num_guesses']
        assert 0 <= letter_index <= self.settings['word_size']

        # set letter using function from GuessesFrame
        self.guesses_frame.set_letter(letter, guess_num, letter_index)


    def start_gui(self) -> None:
        """ Starts the GUI. """
        self.window.mainloop()


    def quit_program(self) -> None:
        """ Quits the program by shutting down the Tk window. """
        self.window.destroy()


    def display_guess_result(self, guess_num: int, guess_results: list[LetterState], letter_states: dict[str, LetterState]) -> None:
        """ Updates the guesses frame to show the results for the given guess number.

        Parameters:
             guess_num: (int) The number of the guess to update.
             guess_results: (list[LetterState]) The state of each letter in the guess.
             letter_states: (dict[str, LetterState]) The state of each letter in the guess.
        """
        # display guess result using show_guess_result function from GuessesFrame
        self.guesses_frame.show_guess_result(guess_num, guess_results)


    def display_message(self, msg: str) -> None:
        """ Displays the given message in the message frame.

        Parameters:
            msg: (str) The message to use.
        """
        self.message_frame.set_message(msg)


    def game_over(self) -> None:
        """ Ends the game by disabling all further keyboard input. """
        self.keyboard_frame.disable()

    def set_key_handler(self, key: str, handler: Callable[[], None]) -> None:
        """ Sets the handler using the keyboard frame's set_key_handler.

        Parameters:
            key: (str) The keyboard key to set the handler for.
            handler: Callable[[], None]) The handler function to call when the key is pressed.
        """
        self.keyboard_frame.set_key_handler(key, handler)

