# A class built to handle key input and
# actions taken by them

class Action:
    pass # Abstract class

class EscapeAction(Action):
    pass # To-Do

class MovementAction(Action):
    """ Dictates what happens when a movement key is pressed """
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

class ExamineAction(Action):
    """ Dictates what happens when the examine key is pressed """
    pass # Nothing needed as of yet, just the reference that the action is being taken

class UseAction(Action):
    """ Dictates what happens when the Use key is pressed """
    pass