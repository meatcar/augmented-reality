class Dots:
    ''' The head of the player, from where the view is rendered.
    '''

    def __init__(self, arr=None):
        self.dots = []
        if arr is not None:
            self.dots += arr

    def add(self, x, y, z):
        self.dots += [(x, y, z)]

    def __str__(self):
        return self.dots.__str__()

    def __repr__(self):
        return self.dots.__repr__()

