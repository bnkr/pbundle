"""Nose wrapper which will select unittests.TestCase instances because I'm
oldskool."""
import nose
import unittest
import os
import nose.plugins.logcapture

class UnittestCapturePlugin(object):
    enabled = True

    def wantClass(self, cls):
        """Only TestCase instances."""
        return issubclass(cls, unittest.TestCase)

    def wantFile(self, path):
        """Only python modules and no private modules."""
        if os.path.basename(path)[0] == "_":
            return False

        if os.path.splitext(path)[-1] != ".py":
            return False

        if not os.path.exists(os.path.join(os.path.dirname(path), "__init__.py")):
            return False

        return True

    def wantModule(self, module):
        """Only root module 'tests'."""
        return module.__name__.split(".")[0] == "tests"

if __name__ == "__main__":
    nose.run(plugins=[UnittestCapturePlugin(), nose.plugins.logcapture.LogCapture()])
