''' Globals for View bs '''

def enum(**modes):
    ''' Fake enum class, returns new type Mode '''
    return type('Mode', (), modes)

Mode = enum(KEY_MODE = 0, IMU_MODE = 1, MPU_MODE = 2)

