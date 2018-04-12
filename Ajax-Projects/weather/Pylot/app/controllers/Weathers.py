from system.core.controller import *

class Weathers(Controller):
    def __init__(self, action):
        super(Weathers, self).__init__(action)

    def index(self):
        return self.load_view('index.html')

