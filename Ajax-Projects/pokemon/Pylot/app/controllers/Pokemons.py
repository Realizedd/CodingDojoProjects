from system.core.controller import *

class Pokemons(Controller):
    def __init__(self, action):
        super(Pokemons, self).__init__(action)
   
    def index(self):
        return self.load_view('index.html')

