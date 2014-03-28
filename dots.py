class Dots:
    ''' The head of the player, from where the view is rendered.
    '''

    def __init__(self, arr=None):
        self.dots = []
        self.count = 0
        if arr is not None:
            self.dots += arr

    def add(self, x, y, z):
        self.dots += [(x, y, z)]
        self.count += 1

    def getLastTwo(self):
        if self.count > 1:
            self.count = 0
            return self.dots[-1], self.dots[-2]
        return None, None

    def __str__(self):
        return self.dots.__str__()

    def __repr__(self):
        return self.dots.__repr__()

