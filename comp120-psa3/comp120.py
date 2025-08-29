"""
module: comp120

Implementations of Stack and Queue classes.

WARNING: DO NOT MODIFY THIS FILE IN ANY WAY
"""

from typing import Any

class EmptyStructureError(Exception):
    """Error to indicate that an item has been requested when a structure
    (e.g. stack or queue) is empty."""
    pass

class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in last-in, first-out order. When removing an item from the stack,
    the most recently-added item is the one that is removed.
    """
    _items: list[Any]

    def __init__(self) -> None:
        """Initializes a new, empty stack"""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return len(self._items) == 0

    def push(self, item: Any) -> None:
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """

        if self.is_empty():
            raise EmptyStructureError()

        return self._items.pop()

    def peek(self) -> Any:
        """Return the element at the top of this stack.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.peek()
        'goodbye'
        >>> s.peek()
        'goodbye'
        """

        if self.is_empty():
            raise EmptyStructureError()

        return self._items[-1]

    def size(self) -> int:
        """Get the number of items in the stack"""
        return len(self._items)


class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in first-in, first-out order. When removing an item from the
    queue, the oldest item is the one that is removed.
    """

    _items: list[Any]

    def __init__(self) -> None:
        """Create new, empty queue."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        return len(self._items) == 0

    def enqueue(self, item: Any) -> None:
        """Add an item to the back of the queue."""
        self._items.insert(0, item)

    def dequeue(self) -> Any:
        """Remove and return the element at the front of this queue.

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """

        if self.is_empty():
            raise EmptyStructureError()

        return self._items.pop()

    def first(self) -> Any:
        """Return the element at the front of this queue.

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.first()
        'hello'
        >>> q.first()
        'hello'
        """

        if self.is_empty():
            raise EmptyStructureError()

        return self._items[-1]

    def size(self) -> int:
        """Get the number of items in the queue"""
        return len(self._items)
