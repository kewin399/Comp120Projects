"""
Module: test_maze_solver

pytest module for the maze_solver function.
"""

import pytest

from maze_solver import maze_solver, Maze
from agenda import StackAgenda, QueueAgenda

def test_maze1():
    m = Maze('tester_maze1.txt')

    # test that we get the correct result with the stack agenda
    sa = StackAgenda()
    result = maze_solver(m, sa, wait_for_user=False)
    assert result == True

    # test that we get the correct result with the queue agenda
    m = Maze('tester_maze1.txt') # create a new maze since the old one was changed by maze_solver

    qa = QueueAgenda()
    result = maze_solver(m, qa, wait_for_user=False)
    assert result == True



def test_maze2():
    m = Maze('tester_maze2.txt')

    # test that we get the correct result with the stack agenda
    sa = StackAgenda()
    result = maze_solver(m, sa, wait_for_user=False)
    assert result == False

    # test that we get the correct result with the queue agenda
    m = Maze('tester_maze2.txt') # create a new maze since the old one was changed by maze_solver

    qa = QueueAgenda()
    result = maze_solver(m, qa, wait_for_user=False)
    assert result == False


def test_maze3():
    m = Maze('tester_maze3.txt')

    # test that we get the correct result with the stack agenda
    sa = StackAgenda()
    result = maze_solver(m, sa, wait_for_user=False)
    assert result == True

    # test that we get the correct result with the queue agenda
    m = Maze('tester_maze3.txt') # create a new maze since the old one was changed by maze_solver

    qa = QueueAgenda()
    result = maze_solver(m, qa, wait_for_user=False)
    assert result == True

def test_maze4():
    m = Maze('tester_maze4.txt')

    # test that we get the correct result with the stack agenda
    sa = StackAgenda()
    result = maze_solver(m, sa, wait_for_user=False)
    assert result == False

    # test that we get the correct result with the queue agenda
    m = Maze('tester_maze4.txt') # create a new maze since the old one was changed by maze_solver

    qa = QueueAgenda()
    result = maze_solver(m, qa, wait_for_user=False)
    assert result == False

def test_maze5():
    m = Maze('tester_maze5.txt')

    # test that we get the correct result with the stack agenda
    sa = StackAgenda()
    result = maze_solver(m, sa, wait_for_user=False)
    assert result == True

    # test that we get the correct result with the queue agenda
    m = Maze('tester_maze5.txt') # create a new maze since the old one was changed by maze_solver

    qa = QueueAgenda()
    result = maze_solver(m, qa, wait_for_user=False)
    assert result == True




# DO NOT change anything below this line
if __name__ == "__main__":
    pytest.main(['test_maze_solver.py'])
