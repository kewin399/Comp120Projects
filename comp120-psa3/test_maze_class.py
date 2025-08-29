"""
Module: test_maze_class

pytest module for the Maze classes.
"""
import pytest
from maze_solver import Maze, Square, SquareType, BadMazeFileFormat


def test_maze_init_ok():
    """ Tests that the Maze.__init__ method works when given a maze file with
    the correct format. """
    m = Maze('maze1.txt')

    assert m.width == 7, "width instance variable not correctly set"
    assert m.height == 4, "height instance variable not correctly set"

    # check that upper left corner is a WALL square
    first_square = m._locations[0][0]
    assert isinstance(first_square, Square)
    assert first_square.location == (0, 0)
    assert first_square.type == SquareType.WALL

    # check that upper left corner is the START square
    start_square = m._locations[1][5]
    assert isinstance(start_square, Square)
    assert start_square.location == (5, 1)
    assert start_square.type == SquareType.START

def test_maze_init_bad():
    """ Tests that the Maze.__init__ method properly raises an exception if
    given a maze file with an incorrect format. """

    # check that each of the "bad_maze" files raises a BadMazeFileFormat
    # exception
    with pytest.raises(BadMazeFileFormat):
        m = Maze('bad_maze1.txt')

    with pytest.raises(BadMazeFileFormat):
        m = Maze('bad_maze2.txt')

    with pytest.raises(BadMazeFileFormat):
        m = Maze('bad_maze3.txt')

def test_maze_str():
    """ Tests the correctness of the Maze.__str__ method. """

    m = Maze('tester_maze3.txt')
    assert str(m) == "o#*\n...\n"

def test_maze_starting_square():
    """ Tests the correctness of the Maze.starting_square method. """

    m = Maze('tester_maze1.txt')
    start = m.starting_square()
    assert isinstance(start, Square)
    assert start.location == (0, 0)
    assert start.type == SquareType.START

    # make sure it works with non (0,0) start square
    m = Maze('maze1.txt')
    start = m.starting_square()
    assert isinstance(start, Square)
    assert start.location == (5, 1)
    assert start.type == SquareType.START

def test_maze_get_square():
    """ Tests the correctness of the Maze.get_square method. """
    m = Maze('tester_maze1.txt')
    sq = m.get_square(2,0)
    assert isinstance(sq, Square)
    assert sq.location == (2, 0)
    assert sq.type == SquareType.FINISH

    m = Maze('tester_maze3.txt')
    sq = m.get_square(0,1)
    assert isinstance(sq, Square)
    assert sq.location == (0, 1)
    assert sq.type == SquareType.OPEN_SPACE


# TODO: Write your test_maze_get_neighbors test case below this line.

def test_get_neighbors():
    m = Maze("small_maze.txt")
    x = 1
    y = 1
    expected = ["#", "*", ".", "o"]
    list_got = []
    neighbors = m.get_neighbors(x,y)
    assert len(neighbors) == 4
    for i in neighbors:
        list_got.append(i.type.value)
    assert (list_got[0] in expected) and (list_got[1] in expected) and (list_got[2] in expected) and (list_got[3] in expected)


    # Tests No value in the South and no value in the East
    m = Maze("small_maze.txt")
    x = 3
    y = 2
    print(m.get_square(x,y))
    expected = ["#", "."]
    list_got = []
    neighbors = m.get_neighbors(x,y)
    assert len(neighbors) == 2
    for i in neighbors:
        list_got.append(i.type.value)
    assert (list_got[0] in expected) and (list_got[1] in expected)

    # tests no Value in the North and no value in the west
    m = Maze("small_maze.txt")
    x = 0
    y = 0
    print(m.get_square(x,y))
    expected = ["o", "."]
    list_got = []
    neighbors = m.get_neighbors(x,y)
    assert len(neighbors) == 2
    for i in neighbors:
        list_got.append(i.type.value)
    assert (list_got[0] in expected) and (list_got[1] in expected)






# WARNING: Don't change anything below here.
if __name__ == "__main__":
    pytest.main(['test_maze_class.py'])
