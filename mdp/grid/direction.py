"""
Utilities for representing stepping directions for the "Grid-MDP" problem.
"""

# a direction is represented a 2D vector and its name
Up = ((-1, 0), 'Up')
Right = ((0, 1), 'Right')
Down = ((1, 0), 'Down')
Left = ((0, -1), 'Left')
NoOp = ((0, 0), 'NoOp')

directions = [Up, Right, Down, Left]


def getPerpDirections(direction):
    """
    Returns the 2 perpendicular directions to a given direction
    """
    if direction == Up or direction == Down:
        return [Left, Right]
    elif direction == Right or direction == Left:
        return [Up, Down]
    else:
        return NoOp


def directionToString(direction):
    """
    returns a string representation of a direction
    """
    if direction == Up:
        return '^'
    elif direction == Right:
        return '>'
    elif direction == Down:
        return 'v'
    elif direction == Left:
        return '<'
    else:
        return '+'
