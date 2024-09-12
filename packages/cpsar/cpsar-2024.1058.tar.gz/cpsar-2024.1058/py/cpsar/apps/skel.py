""" WSGI MIXIN Application Skeleton
"""

import cpsar.runtime as R
import cpsar.ws as W

#W.MakoProgram or W.GProgram
class Program(W.GProgram):
    def main(self):
        pass

application = Program.app
