# Message system for the game:

# Special characters, in case I forget:
CLEAR_SCREEN = 'cls'

class Messenger:
    """ Prints messages to the screen for readability """
    def __init__(self, startLoc, maxLines, maxLength):
        """ Constructor """
        self.log = []
        self.currentIndex = 0 # top Line to print : Should be len(log) - maxLines
        self.startLoc = startLoc # The y location where the dialog starts
        self.maxLines = maxLines # Max lines that can be shown at any given time
        self.maxLength = maxLength # Max length of a line before wrapping to next line

    def AddText(self, message : str):
        if message == '':
            return #in case we try to add a blank string
        if message == CLEAR_SCREEN:
            self.log.clear()
            self.currentIndex = 0
            return # Clear the screen and leave
        s = ''
        for letter in message:
            if letter == '\n':
                self.log += [s]
                s = ''
            else:
                s += letter
                if len(s) >= self.maxLength:
                    self.log += [s]
                    s = ''
        if len(s) > 0:
            self.log += [s]

        self.currentIndex = len(self.log) - self.maxLines
        if self.currentIndex < 0:
            self.currentIndex = 0
    
    def PrintText(self, console):
        """ Displays the messages to the screen """
        drawPoint = 0
        while drawPoint < self.maxLines and drawPoint < len(self.log):
            console.print(x = 1, y = self.startLoc + drawPoint, string = self.log[drawPoint + self.currentIndex])
            drawPoint += 1