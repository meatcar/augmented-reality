class Head:
    ''' The head of the player, from where the view is rendered.
    '''

    def __init__(self, eye_distance=0.065, fov=60, x=0, y=0, z=0):
        self.eye_distance = eye_distance
        self.fov = fov

        self.xangle = 90
        self.yangle = 90
        self.zangle = 0

        self.rot_matrix = None

        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "(x:%.2f y:%.2f z:%.2f) \n (xa:%.2f ya:%.2f za:%.2f)" %(
                self.x,
                self.y,
                self.z,
                self.xangle,
                self.yangle,
                self.zangle) #+ str(self.rot_matrix)

