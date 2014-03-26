#!/bin/python

import sys
from threading import Thread
import subprocess
import numpy

class HandTracker(object):

    dots = None
    proc = None

    def __init__(self, dots):
        self.dots = dots

        self.proc = subprocess.Popen(
                ["python2", "handtracking/dsHandTracker.py"],
                stdout=subprocess.PIPE
        )

        self.out = self.proc.stdout

        # exec handtracking/dsHandTracker.py
        # save pipe on self
        self.t = Thread(target=self.track)
        self.t.daemon = True
        self.t.start()

    def track(self):
        while True:
            for line in self.proc.stdout:
                points = numpy.fromstring(line, dtype="int32", sep=",")
                self.dots.add(points[0], points[1], points[2])

if __name__ == "__main__":
    ht = HandTracker(None);
    while True:
        pass
