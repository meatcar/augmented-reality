from head import Head
from shape import Shape
from view import View
from dots import Dots
from handtracker import HandTracker
from controller import Controller
# from key_controller import KeyController
from constants import Mode

if __name__ == "__main__":
    head = Head()
    shape = Shape(height=0.4, width=0.4, x=0, y=0, z=-9)
    dots = Dots()

    # Cube
    view = View(head=head, shape=shape, dots=dots, mode=Mode.MPU_MODE)

    handtracker = HandTracker(dots)
    controller = Controller(head, use_phidget=False, use_MPU=True)
    
    # keycontroller = KeyController(head, shape)
    
    try:
        view.run()
    finally:
        # cleans up the mess we make after a kill
        handtracker.proc.kill()

