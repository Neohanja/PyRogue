# A class built to handle key input and
# actions taken by them

class Action:
    pass # Abstract class, not intended to be used as a stand-alone.

class EscapeAction(Action):
    pass # To-Do

class ToolTipUI(Action):
    """ Shows/Hides hotkey tooltip UI """
    pass

class MovementAction(Action):
    """ Dictates what happens when a movement key is pressed """
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

class ExamineAction(Action):
    """ Dictates what happens when the examine key (I) is pressed """
    pass # Nothing needed as of yet, just the reference that the action is being taken

class UseAction(Action):
    """ Dictates what happens when the Use key (E) is pressed """
    pass

class EnterAction(Action):
    """ When the player presses enter """
    pass

class TextKeyPress(Action):
    """ Needed to parse through key pressing """
    def __init__(self, letter : str):
        self.letter = letter