"""Encapsulates a single step of the pipeline

Each step is represented by a subclass of Step, which is instantiated
by the interface

"""

from subprocess import PIPE, Popen
from pathlib import Path
from datetime import datetime


class Step:
    """An abstract representation of single class step
    """

    def run(self, data, args):
        """Execute the step

        The parameters are string datato feed intothe pipeline
        additional arguments to pass to the program.

        The return value is 2-tuple containing string data to the next program, and a list
        of command lines to be passed to the next program

        """

        return '', []


class ExecStep(Step):
    """Represents the execution of the program as a pipeline"""
    args = None

    def __init__(self, args):
        self.args = args

    def run(self, data, args=None):
        """Run the program with the given input and arguments"""

        p = Popen(self.args,
                  stdin=PIPE,
                  stdout=PIPE,
                  bufsize=0,
                  universal_newlines=True)
        out, err = p.communicate(data)
        return out, []


class ArgsStep(Step):
    """Split the output of the prior step into arguments"""

    def __init__(self, seperator=None):
        """Collect the separator pattern to use for split"""
        self.seperator = seperator

    def run(self, data, args=None):
        """Perform the spilt and return result as 2-tuple"""
        return '', data.split(self.seperator)


class StoreStep(Step):
    """Redirects the output of the prior step into a file"""

    def __init__(self, filename):
        self.path = Path(filename)

    def run(self, data, args=None):
        with self.path.open('w') as f:
            f.write(data)
            f.close()
