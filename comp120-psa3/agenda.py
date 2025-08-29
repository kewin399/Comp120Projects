"""
Module: agenda

Implementations of the Agenda ADT
"""

from abc import ABC, abstractmethod
from typing import Any
from comp120 import Stack
from comp120 import Queue

class Agenda(ABC):
    """Parent/base class for all classes that will implement the Agenda ADT.

    DO NOT MODIFY THIS CLASS IN ANY WAY."""

    @abstractmethod
    def add(self, item: Any) -> None:
        """Adds an item to the agenda."""
        return

    @abstractmethod
    def remove(self) -> Any:
        """Removes and returns an next item on the agenda."""
        return

    @abstractmethod
    def next(self) -> Any:
        """Returns an next item on the agenda."""
        return

    @abstractmethod
    def size(self) -> int:
        """Returns the number of items on the agenda."""
        return 0

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the agenda has no items, and False otherwise."""
        return False



class AgendaEmpty(Exception):
    """
    An exception class associated if the agenda is empty.
    """
    pass


class StackAgenda(Agenda):
    """
    A child class that inherits from the Agenda class, which provides functionality for Stack type Agenda
    """
    
    def __init__(self):
        self.stack_list = Stack()

    def add(self, item: Any) -> None:
        """Adds an item to the agenda."""
        self.stack_list.push(item)
        
    
    def remove(self) -> Any:
        """Removes and returns an next item on the agenda."""
        if self.is_empty():
            raise AgendaEmpty()
        temp = self.stack_list.pop()
        return temp

    
    def next(self) -> Any:
        """Returns an next item on the agenda."""
        if self.is_empty():
            raise AgendaEmpty()
        temp = self.stack_list.peek()
        return temp


    
    def size(self) -> int:
        """Returns the number of items on the agenda."""
        temp = self.stack_list.size()
        return temp

    
    def is_empty(self) -> bool:
        """Returns True if the agenda has no items, and False otherwise."""
        if self.stack_list.size() == 0:   
            return True
        else:
            return False


class QueueAgenda(Agenda):
    """
    A child class that inherits from the Agenda class, which provides functionality for Queue type Agenda
    """
    def __init__(self):
        self.queue_list = Queue()

    def add(self, item: Any) -> None:
        """Adds an item to the agenda."""
        self.queue_list.enqueue(item)
        
    
    def remove(self) -> Any:
        """Removes and returns an next item on the agenda."""
        if self.is_empty():
            raise AgendaEmpty()
        return self.queue_list.dequeue()

    
    def next(self) -> Any:
        """Returns an next item on the agenda."""
        if self.is_empty():
            raise AgendaEmpty()

        return self.queue_list.first()


    
    def size(self) -> int:
        """Returns the number of items on the agenda."""
        temp = self.queue_list.size()
        return temp

    
    def is_empty(self) -> bool:
        """Returns True if the agenda has no items, and False otherwise."""
        return self.queue_list.is_empty()
