from head import Head
from shape import Shape
from view import View
from controller import Controller
from key_controller import KeyController

if __name__ == "__main__":
    head = Head()
    shape = Shape(height=0.4, width=0.4, x=0, y=0, z=-1)

    view = View(head, shape)

    controller = Controller(head)
    #keycontroller = KeyController(head, shape)

    view.run()

