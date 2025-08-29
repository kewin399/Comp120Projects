"""
module: maze_solver

Implementation of the SquareType, Square, and Maze classes as well as the
maze_solver function.
"""

from enum import Enum
from agenda import Agenda
from agenda import QueueAgenda
from agenda import StackAgenda

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
    pass


class Maze():

    _location: list[list[Square]]
    width: int
    height: int

    def __init__(self, filename: str) -> None:
        possibles = ["#", ".", "o", "*"]
        start_point = False
        end_point = False
        x = 0
        y = 0

        self._location = []
        with open(filename) as file:
            dimensions = file.readline().strip()
            dimensions = list(dimensions)
            try:
                self.width = int(dimensions[0])
                self.height = int(dimensions[2])
            except:
                raise BadMazeFileFormat
            
            for line in file:
                test = line.strip()
                stuff = []
                x = 0
                for square in test:
                    if square not in possibles:
                        raise BadMazeFileFormat
                    current_square = Square(square,x,y)
                    if current_square.type == SquareType.START:
                        start_point = True
                    if current_square.type == SquareType.FINISH:
                        end_point = True
                    stuff.append(current_square)
                    x += 1
                self._location.append(stuff)
                # print(self._location)

                y += 1
            if start_point and end_point and x== self.width and y == self.height:
                # good file format 
                pass
            else:
                raise BadMazeFileFormat
    
    def __str__(self) -> str:
        running_maze = ""
        for line in self._location:
            for square in line:
                running_maze = running_maze + str(square)
            running_maze += "\n"
        return running_maze
        
    def starting_square(self) -> Square:
        for line in self._location:
            for square in line:
                if square.type.value == "o":
                    return square
    
    def get_square(self, x: int, y: int) -> Square:
        return self._location[y][x]
 
    # def get_neightbors(self, x: int, y: int) -> list[Square]:
    #     neighbors = []
    #     if x-1 >= 0:
    #         north = self.get_square(y, x-1)
    #         neighbors.append(north)
    #     if x+1 <= self.height:
    #         south = self.get_square(y, x+1)
    #         neighbors.append(south)
    #     if y-1 >= 0:
    #         west = self.get_square(y-1, x)
    #         neighbors.append(west)
    #     if y+1 <= self.width:
    #         east = self.get_square(y+1, x)
    #         neighbors.append(east)
    #     return neighbors



    def get_neighbors(self, x: int, y: int):
        print(x)
        print(y)

        if self.height == 1:
            if x == 0:
                east = self.get_square(x+1, y)
                return [east]
            elif x == self.width:
                west = self.get_square(x-1, y)
            else:
                east = self.get_square(x+1, y)
                west = self.get_square(x-1, y)
                return [east, west]
                
        elif x == 0:
            if y == 0:
                east = self.get_square(x+1, y)
                south = self.get_square(x,y+1)
                return [east, south]
            elif y == self.height - 1:
                north = self.get_square(x, y-1)
                east = self.get_square(x+1, y)
                return [north, east]
            else:
                east = self.get_square(x+1, y)
                south = self.get_square(x,y+1)
                north = self.get_square(x, y-1)
                return [east, north, south]
    
        elif y==0:
            if x==0:
                east = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                return[east, south]
            elif x == self.width - 1:
                west = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                return [west,south]
            else:
                west = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                east = self.get_square(x+1, y)
                return [west, south, east]

        elif x==self.width - 1:
            if y == 0:
                west = self.get_square(x-1, y)
                south = self.get_square(x,y+1)
                return[west,south]
            elif y == self.height - 1:
                north = self.get_square(x, y-1)
                west = self.get_square(x-1, y)
                return [north, west]
            else:
                north =self.get_square(x, y-1)
                south = self.get_square(x,y+1)
                west = self.get_square(x-1, y)
                return [north, south, west]

        elif y == self.height - 1:
            if x ==0:
                north = self.get_square(x, y-1)
                east = self.get_square(x+1, y)
                return [north, east]
            elif x == self.width - 1:
                north = self.get_square(x, y-1)
                west = self.get_square(x-1, y)
                return [north , west]
            else:
                north = self.get_square(x, y-1)
                west = self.get_square(x-1, y)
                east = self.get_square(x+1, y)
                return [north, west ,east]
        else:
            north = self.get_square(x, y-1)
            south = self.get_square(x, y+1)
            west = self.get_square(x-1, y)
            east = self.get_square(x+1, y)
            return [north, south, west, east]
        



# testMaze = Maze("tester_maze1.txt")
# testMaze1 = Maze("bad_maze2.txt")




def maze_solver(maze: Maze, agenda: Agenda, wait_for_user: bool=True) -> bool:

    print(maze)
    if wait_for_user:
        input("Press Enter To Continue")

    while not agenda.is_empty():
        agenda.remove()
    
    starting: Square = maze.starting_square()
    print(starting.type.value)
    agenda.add(starting)

    while not agenda.is_empty():
        print(maze)
        current_square: Square = agenda.remove()
        print()
        print(current_square.type.value)

        if current_square.visited:
            # do nothing  we dont have to re-explore
            pass
        if current_square.type == SquareType.FINISH:
            print(current_square.type.value)
            # end, you are at the finish
            return True
        
        for neighbor in maze.get_neighbors(current_square.location[0], current_square.location[1]):
            if neighbor.type != SquareType.WALL and not neighbor.visited:
                agenda.add(neighbor)
        
        current_square.visited = True
    return False


maze = Maze("maze2.txt")

