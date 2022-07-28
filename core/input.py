# import standard library

# import third party library
from PySide6.QtCore import QEvent

# import local library

class KeyEvent:
    def __init__(self,key,type):
        self.key = key
        self.type = type

class Input(object):
    def __init__(self) -> None:
        # lists to store key states
        #   down, up: discrete event; lasts for one iteration
        #   pressed: continuous event, between down and up events
        self.keyDownList    = []
        self.keyUpList      = []
        self.keyPressedList = []

        self.keyEvents      = []

    def update(self):
        # Reset discrete key states
        self.keyDownList = []
        self.keyUpList = []

        # iterate over all user input events (such as keyboard or
        #  mouse) that occurred since the last time events were checked
        for event in self.keyEvents:
            # Check for keydown and keyup events;
            # get name of key from event 
            # and append to or remove from corresponding lists
            if event.type == QEvent.KeyPress:
                self.keyDownList.append(event.key)
                self.keyPressedList.append(event.key)
            elif event.type == QEvent.KeyRelease:
                self.keyUpList.append(event.key)
                self.keyPressedList.remove(event.key)
        self.keyEvents = []

    # functions to check key states
    def isKeyDown(self,key):
        return key in self.keyDownList
    
    def isKeyUp(self, key):
        return key in self.keyUpList
    
    def isKeyPressed(self, key):
        return key in self.keyPressedList

    def receiveKeyEvent(self, key, type):
        self.keyEvents.append(KeyEvent(key, type))