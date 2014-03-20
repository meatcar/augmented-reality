# Augmented Reality

An [ECE516H](http://wearcam.org/ece516/) Winter 2014 project at the University
of Toronto. The goal of this project is to enable a person to create drawings in the world around them.

This project uses the following hardware:

* [Epson Moverio BT-100](http://www.epson.co.uk/gb/en/viewcon/corporatesite/products/mainunits/overview/11373)
* [1042 - PhidgetSpacial 3/3/3 Basic](http://www.phidgets.com/products.php?product_id=1042)
* [SoftKinetic DepthSense 325](http://www.softkinetic.com/Store/tabid/579/ProductID/6/language/en-US/Default.aspx) (head-mounted)

Our codebase is written in Python3, Python2 and C++. The image processing and hand tracking is done with [SimpleCV](http://simplecv.org/). Graphics are generated in OpenGL using [PyOpenGL](http://pyopengl.sourceforge.net/). Accelerometer data is processed using numpy, scipy, and the [Phidget Python library](http://www.phidgets.com/docs/Language_-_Python).

## Installation

These instructions are for Linux (sorry).

#### DepthSense

Follow [Tu-Hoa Pham's instructions here](https://ph4m.wordpress.com/2014/02/11/getting-softkinetics-depthsense-sdk-to-work-on-arch-linux/) to set up the device on linux.
Look into the instructions under the depthsense folder for more details on installing our module

#### PhidgetSpacial
Follow [Phidget's install instructions](http://www.phidgets.com/docs/Language_-_Python) to install the python library on your machine. If you're using python3.3 or higher, you may have to modify the source code to change `"linux2"` to `"linux"`.

#### PyOpenGL
Follow [installation instrucions](http://pyopengl.sourceforge.net/documentation/installation.html) to install PyOpenGL. It is not available in pip.

#### SimpleCV
[Installation instructions for python2](https://github.com/sightmachine/simplecv#installation)

## Usage
Plug in all your hardware, attach the Phidget IMU to the glasses, and run `main.py`. You may have to execute it with root privileges to give access to the Phidget IMU, unless you set up the appropriate udev rules, as per [Phidgets wiki](http://www.phidgets.com/docs/OS_-_Linux#Setting_udev_Rules).
