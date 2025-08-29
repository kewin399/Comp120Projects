"""
Program to try to escape from a customize labyrinth.

Author:
Cavin Nguyen - cavinnguyen@sandiego.edu
"""
import labyrinth
from labyrinth import MazeCell, Item

# Change the following variable (YOUR_NAME) to contain your FULL name.

"""
!!!WARNING!!!

Once you've set set this constant and started exploring your maze,
do NOT edit the value of YOUR_NAME. Changing YOUR_NAME will change which
maze you get back, which might invalidate all your hard work!
"""

YOUR_NAME = "Cavin Nguyen"

# Change these following two constants to contain the paths out of your mazes.
# You'll need to use the debugger to help you out!

PATH_OUT_OF_MAZE        = "SWSESNWNENWWWSEWSESW"
PATH_OUT_OF_TWISTY_MAZE = "SSWEEWENNWSE"

def is_path_to_freedom(start: MazeCell, moves: str) -> bool:
    """
    Given a location in a maze, returns whether the given sequence of
    steps will let you escape the maze. The steps should be given as
    a string made from N, S, E, and W for north/south/east/west without
    spaces or other punctuation symbols, such as "WESNNNS"

    To escape the maze, you need to find the Potion, the Spellbook, and
    the Wand. You can only take steps in the four cardinal directions,
    and you can't move in directions that don't exist in the maze.

    Precondition: start is not None

    Args:
        start (MazeCell): The start location in the maze.
        moves (str): The sequence of moves.

    Raises:
        ValueError: If <moves> contains any character other than N, S, E, or W

    Returns:
        (bool) Whether that sequence of moves picks up the needed items
               without making any illegal moves.
    """
    # Syntax reminders:
    # start.north/east/south/west
    # start.whats_here
    # moves good example: NWSSW
    # moves bad example: NWEKSW
    # Item.NOTHING
    # Item.POTION
    # Item.SPELLBOOK
    # Item.WAND

    assert start != None
    # create variables 
    direction_list = ["N", "E", "S", "W"]
    current = start

    # boolean variables for final check if maze was solved.
    check_potion = False
    check_spellbook = False
    check_wand = False

    # loops through the string moveset and assigns char to dir.
    for dir in moves:
        # checks if the char is N, E, S, or W.
        if dir in direction_list:
            
            # processes the string representation of direction to check if the MazeCell move is legal. Returns False otherwise.
            if dir == "N":
                if current.north != None:
                    current = current.north
                else:
                    return False
            elif dir == "E":
                if current.east != None:
                    current = current.east
                else:
                    return False
            elif dir == "S":
                if current.south != None:
                    current = current.south
                else: 
                    return False
            else: #west
                if current.west != None:
                    current = current.west
                else:
                    return False
            
            # after changing MazeCell, checks if potion, spellbook, or wand is in the cell. If found, change our check to true.
            # match current.whats_here:
            #     case Item.POTION:
            #         check_potion = True
            #     case Item.SPELLBOOK:
            #         check_spellbook = True
            #     case Item.WAND:
            #         check_wand = True
            # ^ I would prefer using this
            
            if current.whats_here == Item.POTION:
                check_potion = True
            elif current.whats_here == Item.SPELLBOOK:
                check_spellbook = True
            elif current.whats_here == Item.WAND:
                check_wand = True

        else:
            raise ValueError
    
    # final check to determine if the maze was solved (all items are picked up)
    if check_potion and check_spellbook and check_wand:
        return True
        
    return False



def main() -> None:
    """ Generates two types of labyrinths and checks whether the user has
    successfully found the path out of them.

    DO NOT MODIFY THIS CODE IN ANY WAY!!!
    """
    start_location = labyrinth.maze_for(YOUR_NAME)

    print("Ready to explore the labyrinth!")
    # Set a breakpoint here to explore your personal labyrinth!

    if is_path_to_freedom(start_location, PATH_OUT_OF_MAZE):
        print("Congratulations! You've found a way out of your labyrinth.")
    else:
        print("Sorry, but you're still stuck in your labyrinth.")


    twisty_start_location = labyrinth.twisty_maze_for(YOUR_NAME)

    print("Ready to explore the twisty labyrinth!")
    # Set a breakpoint here to explore your personal TWISTY labyrinth!

    if is_path_to_freedom(twisty_start_location, PATH_OUT_OF_TWISTY_MAZE):
        print("Congratulations! You've found a way out of your twisty labyrinth.")
    else:
        print("Sorry, but you're still stuck in your twisty labyrinth.")



if __name__ == "__main__":
    main()
