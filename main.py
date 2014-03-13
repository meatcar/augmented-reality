from head import Head
from shape import Shape
from view import View
from dots import Dots
from controller import Controller
from key_controller import KeyController

if __name__ == "__main__":
    head = Head()
    shape = Shape(height=0.4, width=0.4, x=0, y=0, z=-9)
    dots = Dots()

    # Cube
    dots.add(1,0,-2)
    dots.add(1,1,-2)
    dots.add(0,1,-2)
    dots.add(0,0,-2)
    dots.add(1,0,-2)
    dots.add(1,0,-3)
    dots.add(1,1,-3)
    dots.add(0,1,-3)
    dots.add(0,0,-3)
    dots.add(1,0,-3)
    dots.add(1,1,-3)
    dots.add(1,1,-2)
    dots.add(0,1,-2)
    dots.add(0,1,-3)
    dots.add(0,0,-3)
    dots.add(0,0,-2)
    dots.add(0,0,-2)

    view = View(head=head, shape=shape, dots=dots)

    #controller = Controller(head)
    keycontroller = KeyController(head, shape)

    view.run()

