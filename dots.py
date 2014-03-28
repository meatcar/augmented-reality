class Dots:
    ''' The head of the player, from where the view is rendered.
    '''

    def __init__(self, arr=None):
        self.dots = []
        self.count = 0
        self.cleanslate = False
        if arr is not None:
            self.dots += arr

    def add(self, x, y, z):
        self.dots += [(x, y, z)]
        self.count += 1

    def get_last_two(self):
        if self.count > 1:
            self.count = 0
            return self.dots[-1], self.dots[-2]
        return None, None

    def reset(self):
        self.cleanslate = True
        self.dots = []
        self.count = 0
    
    def is_clean_slate(self):
        #TODO: sync on clean slate var
        slate = self.cleanslate
        self.cleanslate = False
        return slate

    def __str__(self):
        return self.dots.__str__()

    def __repr__(self):
        return self.dots.__repr__()

