class Shape:
    ''' The shape that the player is interacting with.
    '''

    def __init__(self, height, width, x, y, z):
        self.height = height
        self.width = width

        self.xangle = 0
        self.yangle = 0
        self.zangle = 180

        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "shape: x:%g y:%g z:%g height:%g width:%g" % (
                self.x,
                self.y,
                self.z,
                self.height,
                self.width)

