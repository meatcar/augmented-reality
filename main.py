from head import Head
from shape import Shape
from view import View
from dots import Dots
#from controller import Controller
from key_controller import KeyController

if __name__ == "__main__":
    head = Head()
    shape = Shape(height=0.4, width=0.4, x=0, y=0, z=-9)
    dots = Dots()

    # Cube
    dots.add(-140, -36, 413)
    dots.add(-170, -39, 501)
    dots.add(-146, -37, 443)
    dots.add(-141, -14, 414)
    dots.add(-192,  16, 535)
    dots.add(-141,  38, 399)
    dots.add(-111,  83, 431)
    dots.add( -76, 105, 421)
    dots.add( -45, 109, 460)
    dots.add( -23,  90, 590)
    dots.add( -22,  38, 638)
    dots.add( -20,  45, 651)
    dots.add(  29,  46, 662)
    dots.add(  87,  37, 610)
    dots.add( 162,  48, 654)
    dots.add( 165,   6, 708)
    dots.add(  82, -31, 657)
    dots.add(  22, -16, 623)
    dots.add(  22, -63, 562)
    dots.add(  22,-108, 620)
    dots.add(  -9,-132, 690)
    dots.add(-116,-105, 617)
    dots.add(-171, -84, 665)
    dots.add(-201,  -5, 627)
    dots.add(-186,  14, 546)
    dots.add(-185, 246, 477)

    view = View(head=head, shape=shape, dots=dots)

    #controller = Controller(head)
    keycontroller = KeyController(head, shape)

    view.run()

