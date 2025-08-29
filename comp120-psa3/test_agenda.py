"""
Module: test_agenda

pytest module for the StackAgenda and QueueAgenda classes.
"""
import pytest
from agenda import StackAgenda, QueueAgenda, AgendaEmpty


def test_stack_is_empty():
    """ Tests that the StackAgenda's is_empty method works for both empty and
    non-empty agendas. """
    agenda = StackAgenda()

    assert agenda.is_empty()  # checks that it starts out as empty

    # TODONE: add an item to the agenda and check that is_empty returns false
    agenda.add("*")
    assert agenda.is_empty() == False

# TODONE: Write the rest of your pytest test case functions for your StackAgenda and
# QueueAgenda classes below this line. You should have a total of 11 different
# test cases/functions (in addition to the one already defined above).

def test_queue_is_empty():
    """ Tests that the QueueAgenda's is_empty method works for both empty and
    non-empty agendas. """
    agenda = QueueAgenda()

    assert agenda.is_empty()

    agenda.add("*")
    assert agenda.is_empty() == False

def test_stack_size():
    """ Tests that the StackAgenda's size method works for empty, one item, and
    greater than one agendas."""
    agenda = StackAgenda()

    assert agenda.size() == 0

    agenda.add("*")
    assert agenda.size() == 1

    agenda.add("*")
    agenda.add("#")
    assert agenda.size() > 1

def test_queue_size():
    """ Tests that the QueueAgenda's size method works for empty, one item, and
    greater than one agendas."""
    agenda = QueueAgenda()

    assert agenda.size() == 0

    agenda.add("*")
    assert agenda.size() == 1

    agenda.add("*")
    agenda.add("#")
    assert agenda.size() > 1

def test_stack_remove():
    """ Tests that the StackAgenda's remove method works for agendas with multiple items."""
    agenda = StackAgenda()
    agenda.add("*")
    agenda.add("#")
    agenda.add("o")
    assert agenda.remove() == "o"


def test_queue_remove():
    """ Tests that the QueueAgenda's remove method works for agendas with multiple items."""
    agenda = QueueAgenda()
    agenda.add("*")
    agenda.add("#")
    agenda.add("o")
    assert agenda.remove() == "*"

def test_stack_consec_remove():
    """ Tests that the StackAgenda's remove method works, when called consecutively times for agendas with multiple items."""
    agenda = StackAgenda()
    agenda.add("*")
    agenda.add("#")
    agenda.add("o")
    assert agenda.remove() == "o"
    assert agenda.remove() == "#"
    assert agenda.remove() == "*"

def test_stack_consec_next():
    """ Tests that the StackAgenda's next method works, when called consecutively times for agendas with multiple items."""
    agenda = StackAgenda()
    agenda.add("*")
    agenda.add("#")
    agenda.add("o")
    assert agenda.next() == "o"
    assert agenda.next() == "o"
    assert agenda.next() == "o"


def test_queue_consec_remove():
    """ Tests that the QueueAgenda's remove method works, when called consecutively times for agendas with multiple items."""
    agenda = QueueAgenda()
    agenda.add("*")
    agenda.add("#")
    agenda.add("o")
    assert agenda.remove() == "*"
    assert agenda.remove() == "#"
    assert agenda.remove() == "o"

def test_queue_consec_next():
    """ Tests that the QueueAgenda's next method works, when called consecutively times for agendas with multiple items."""
    agenda = QueueAgenda()
    agenda.add("*")
    agenda.add("#")
    agenda.add("o")
    assert agenda.next() == "*"
    assert agenda.next() == "*"
    assert agenda.next() == "*"

def test_stack_AgendaEmpty():
    """ Tests that the StackAgenda's next and remove method raises an AgendaEmpty Error, when called for agendas with no items."""
    agenda = StackAgenda()
    with pytest.raises(AgendaEmpty):
        agenda.next()
    with pytest.raises(AgendaEmpty):
        agenda.remove()
    # FINISH

def test_queue_AgendaEmpty():
    """ Tests that the QueueAgenda's next and remove method raises an AgendaEmpty Error, when called for agendas with no items."""
    agenda = QueueAgenda()
    with pytest.raises(AgendaEmpty):
        agenda.next()
    with pytest.raises(AgendaEmpty):
        agenda.remove()


# DO NOT change anything below this line
if __name__ == "__main__":
    pytest.main(['test_agenda.py'])
