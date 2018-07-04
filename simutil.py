from simkit import StateChangeEvent
from simkit import StateChangeListener

class SimpleStateChangeDumper(StateChangeListener):

    def stateChange(self, stateChangeEvent):
        print(str(stateChangeEvent))