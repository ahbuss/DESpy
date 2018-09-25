from simkit.base import StateChangeListener

class SimpleStateChangeDumper(StateChangeListener):

    def state_change(self, state_change_event):
        print(str(state_change_event))