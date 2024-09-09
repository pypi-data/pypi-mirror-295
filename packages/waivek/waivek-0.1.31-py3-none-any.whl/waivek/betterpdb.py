import pdb
import sys

class BetterPdb(pdb.Pdb):
    def post_mortem(self, t=None, frame=None):
        # If no traceback is provided, use the current exception
        if t is None:
            t = sys.exc_info()[2]
        # Call the original post_mortem
        self.reset()
        if t is not None:
            print("Entering post mortem debugging\n")
            self.interaction(frame, t)

    def _cmdloop(self, *args, **kwds):
        # Override the _cmdloop method to print "HELLO" before calling the original method
        print("HELLO")
        return super()._cmdloop(*args, **kwds)
