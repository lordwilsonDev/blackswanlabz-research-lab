from pass_controller import *

class BadController(Controller):
    def dispatch(self, event):
        return

def create_controller():
    return BadController()
