from head import Head
from shape import Shape
from view import View
from dots import Dots
from handtracker import HandTracker
#from controller import Controller
from key_controller import KeyController

if __name__ == "__main__":
    head = Head()
    shape = Shape(height=0.4, width=0.4, x=0, y=0, z=-9)
    dots = Dots()
    #dots.add(0,0,0)

    # Cube
    view = View(head=head, shape=shape, dots=dots)

    handtracker = HandTracker(dots)
    #controller = Controller(head)
    keycontroller = KeyController(head, shape)

    view.run()

