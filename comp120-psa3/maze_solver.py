"""
module: maze_solver

Implementation of the SquareType, Square, and Maze classes as well as the
maze_solver function.
"""

from agenda import Agenda
from agenda import QueueAgenda
from agenda import StackAgenda
import sys

from agenda import Stack
from enum import Enum
class SquareType(Enum):
    '''
        This class assigns the character for each spot in the maze
    '''

    WALL = '#'
    OPEN_SPACE = '.'
    START = 'o'
    FINISH = '*'


class Square():
    '''
        This is the square class, which represents a location in the maze
        >>> Square("G", 2, 3)
        Traceback (most recent call last):
        ValueError: Invalid value given
        >>> a = Square("#", 1,1)
        >>> a.location[0]
        1
        >>> print(a)
        #
        >>> a.location = (7,5)
        >>> a.location
        (7, 5)
    '''

    # instance variables
    type: SquareType
    visited: bool
    location: tuple[int, int]

    def __init__(self, rep: str, x: int, y: int) -> None:
        '''
            The constructor method.

            Parameters:
                rep (type: str) = String representation 
                x (type: int) = x-coordinate on the maze
                y (type: int) = y-coordinate on the maze

            Return:
            None

            >>> a = Square("#", 100,2)
            >>> a.location[1]
            2

        '''

        # the list to check and make sure values are within, and do the chec
        check_values = ["#", ".", "o", "*"]
        if rep not in check_values:
            raise ValueError("Invalid value given")


        # Set the values of the instance vars. 
        if rep == "#":
            self.type = SquareType.WALL
        if rep == ".":
            self.type = SquareType.OPEN_SPACE
        if rep == "o":
            self.type = SquareType.START
        if rep == "*":
            self.type = SquareType.FINISH

        
        self.visited = False
        self.location = (x,y)

    def __str__(self) ->  str:
        '''
            The string class, allows for print()

            >>> a = Square(".", 100,2)
            >>> print(a)
            .

        '''

        if self.type == SquareType.OPEN_SPACE:
    
            if self.visited:
                return  "x"
            else:
                return  "."

        return f"{self.type.value}"







class BadMazeFileFormat(Exception):
    """
    An exception class to associate with a bad maze file format.
    """
    pass


class Maze():
    """
    This is the maze class, which ensures that the maze is formatted correctly
    """

    _locations: list[list[Square]]
    width: int
    height: int

    def __init__(self, filename: str) -> None:
        possibles = ["#", ".", "o", "*"]
        start_point = False
        end_point = False
        x = 0
        y = 0

        self._locations = []
        with open(filename, 'r') as file:
            dimensions = file.readline().strip()
            dimensions = dimensions.split()
            
            # Try to convert str data type to int. 
            # If first line does not exist or its formatted incorrectly, raise custom BadMazeFileFormat error.
            try:
                self.width = int(dimensions[0])
                self.height = int(dimensions[1])
            except:
                raise BadMazeFileFormat
            
            # Iterate through the maze to check for formatting errors.
            for line in file:
                test = line.strip()
                maze_row = []
                x = 0

                for square in test:
                    if square not in possibles: # checks if character is not valid
                        raise BadMazeFileFormat
                    current_square = Square(square,x,y)
                    # checks if a start and finish exist 
                    if current_square.type == SquareType.START:
                        start_point = True
                    if current_square.type == SquareType.FINISH:
                        end_point = True
                # append square to maze_row to create list representation of the maze row.
                    maze_row.append(current_square)
                    x += 1
                # append to self._locations to create 2D array.
                self._locations.append(maze_row)

                y += 1
            # checks if SquareType.START and SquareType.FINISh exist, as well as if the rows and columns match with the header.
            if start_point and end_point and x == self.width and y == self.height:
                # good file format 
                pass
            else:
                raise BadMazeFileFormat
    

    def __str__(self) -> str:
        """
        This method will return a string of the current maze

        Inputs:
        None

        Returns:
        running_maze(str): A string representation of the maze
        """
        running_maze = ""
        for line in self._locations:
            for square in line:
                running_maze = running_maze + str(square)
            running_maze += "\n"
        return running_maze
                


    def starting_square(self) -> Square:
        """
        This method returns the square containing the information with the starting square

        Inputs:
        None

        Returns:
        square(Square): A square object containing the information for the starting square
        """
        for line in self._locations:
            for square in line:
                if square.type.value == "o":
                    return square
            
    def get_square(self, x: int, y: int) -> Square:
        """
        This method takes and returns the square at a given coordinate.

        Inputs:
        x(int): The x coordinate of the square's location.
        y(int): The y coordinate of the square's location.

        Returns:
        (Square): Returns the square object derived from the location x,y.
        """
        return self._locations[y][x]
    


    def get_neighbors(self, x: int, y: int) -> list[Square]:
        """
        This method checks the four cardinal squares adjacent to the square at the given location, and returns them if they exist.

        Inputs:
        x(int): The x-coordinate of the location we want the neighbors for
        y(int): The y-coordinate of the location we want the neighbors for

        Returns:
        A list containing the the neighbor information for north, east, south, and west, which are all square objects, skipping over a direction if it doesn't exist.
        """
        # checks that the height is equal to 1
        if self.height == 1:
            # If x is 0, then only east will exist
            if x == 0:
                east = self.get_square(x+1, y)
                return [east]
            elif x == self.width:
            # If x is equal to the width, then only west exists
                west = self.get_square(x-1, y)
            else:
            # Otherwise, east and west exist
                east = self.get_square(x+1, y)
                west = self.get_square(x-1, y)
                return [east, west]
                
        elif x == 0:
            if y == 0:
                # If and y are both 0, then only east and south neighbors exist
                east = self.get_square(x+1, y)
                south = self.get_square(x,y+1)
                return [east, south]
            elif y == self.height - 1:
                # If y is at one less than the hiehgt, then only north and east exist
                north = self.get_square(x, y-1)
                east = self.get_square(x+1, y)
                return [north, east]
            else:
                # Otherwise, east north and south exist
                east = self.get_square(x+1, y)
                south = self.get_square(x,y+1)
                north = self.get_square(x, y-1)
                return [east, north, south]
    
        elif y==0:
            # If y is 0, then north will not exist
            if x==0:
                # If x is 0, then only east and south exist
                east = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                return[east, south]
            elif x == self.width - 1:
                # If x is width-1, then only west and south exist
                west = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                return [west,south]
            else:
                # Otherwise, west south and east exist
                west = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                east = self.get_square(x+1, y)
                return [west, south, east]

        elif x==self.width - 1:
            # If x is 1 less than the width, then east will not exist
            if y == 0:
                # If y is 0, then only west and south exist
                west = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                return[west,south]
            elif y == self.height - 1:
                # If y is 1 less than the height, then only north and west exist
                north = self.get_square(x, y-1)
                west = self.get_square(x-1, y)
                return [north, west]
            else:
                # Otherwise, north south and west will exist
                north =self.get_square(x, y-1)
                south = self.get_square(x,y+1)
                west = self.get_square(x-1, y)
                return [north, south, west]

        elif y == self.height - 1:
            # If y is 1 less than the height, then south will not exist
            if x ==0:
                # If x is 0, then only north and east exist
                north = self.get_square(x, y-1)
                east = self.get_square(x+1, y)
                return [north, east]
            elif x == self.width - 1:
                # If x is 1 less than the width, then only north and west exist
                north = self.get_square(x, y-1)
                west = self.get_square(x-1, y)
                return [north , west]
            else:
                # Otherwise, north west and east exist
                north = self.get_square(x, y-1)
                west = self.get_square(x-1, y)
                east = self.get_square(x+1, y)
                return [north, west ,east]
        else:
            # If none of the above are true, then all 4 neighbors exist
            north = self.get_square(x, y-1)
            south = self.get_square(x, y+1)
            west = self.get_square(x-1, y)
            east = self.get_square(x+1, y)
            return [north, south, west, east]
        






def maze_solver(maze: Maze, agenda: Agenda, wait_for_user: bool=True) -> bool:
    """
    This method takes a given maze input and agenda type, and attempts to check and see if the given maze is solvable.

    Inputs:
    maze(Maze): The maze that we are trying to check
    agenda(Agenda): This is the agenda type we are utilizing, either a StackAgenda or a QueueAgenda
    wait_for_user(boolean): this is a variable which will ensure that the code will only run after the user allows it to

    Returns:
    A boolean value representing whether or not the maze is solvable, returning True if the maze is solvable and False if the maze is not solvable
    """
    # clear out the entire agenda before solving
    while not agenda.is_empty():
        agenda.remove()
    
    # finding the starting square and adding to the agenda
    starting: Square = maze.starting_square()

    agenda.add(starting)

    # loops until agenda is empty
    while not agenda.is_empty():
        # conditional to check if function will wait for user or not.
        if wait_for_user:
            print(maze)
            input("Press Enter To Continue")

        # use agenda.remove() method to remove square from agenda AND move on to current square.
        current_square: Square = agenda.remove()

        if current_square.visited:
            # do nothing  we dont have to re-explore
            pass
        if current_square.type == SquareType.FINISH:
            # end, you are at the finish
            return True
        
        # uses get_neighbors() method to get neighbors of the square and checks if type is not a wall, and if not visited.
        for neighbor in maze.get_neighbors(current_square.location[0], current_square.location[1]):
            if neighbor.type != SquareType.WALL and not neighbor.visited:
                agenda.add(neighbor)
        
        # updates the square so that it is visited.
        current_square.visited = True
    # if loop ends, no solution was found
    return False
        










def main(maze_filename: str, agenda_type: str) -> None:
    """
    The main method, which takes the user input maze and agenda type and deetermines if the maze is possible to solve or not

    Inputs:
    maze_filename(str): The name of the maze file in which we are checking to see if it is possible
    agenda_type(str): The agenda type that we want to utilize, either stack or queue

    Returns:
    None

    Preconditions:
    agenda_type is "stack" or "queue"
    """
    assert agenda_type == "stack" or agenda_type == "queue", "The type for agenda was not a stack or queue"

    maze = Maze(maze_filename)
    if agenda_type == "stack":
        agenda = StackAgenda()
    elif agenda_type == "queue":
        agenda = QueueAgenda()
    solvable = maze_solver(maze, agenda)

    if solvable == True:
        print("Maze solution found")
    else:
        print("Maze solution does not exist")







# Keep this conditional at the bottom of the file.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid amount of arguments provided")
    m_name = sys.argv[1]
    a_type = sys.argv[2]
    if a_type not in ["stack", "queue"]:
        print("Error: The agenda type must be either 'stack' or 'queue'.")

    main(m_name, a_type)

