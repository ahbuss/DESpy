from simkit.simkit import StateChangeListener

class SimpleStateChangeDumper(StateChangeListener):

    def stateChange(self, state_change_event):
        print(str(state_change_event))