
class FiniteStateMachine:
    def __init__(self):
        self.state = None

    def transition(self, new_state):
        self.state = new_state