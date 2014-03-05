from phidgetwrapper import PhidgetWrapper

def data(acc, agr, time):
    print('acc', acc, 'agr', agr, 'time', time)

if __name__ == "__main__":
    phidget = PhidgetWrapper(data)
