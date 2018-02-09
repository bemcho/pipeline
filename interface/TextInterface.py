import cmd
from pathlib import Path
import pickle
import sys
from pprint import pprint


class TextInterface(cmd.Cmd):
    """Text based interface for pipeline"""
    keep_going = None
    path = None
    prompt = 'Pipeline> '

    def __init__(self, keep_going, filename):
        super().__init__(completekey='tab')
        self.keep_going = keep_going
        self.path = Path(filename)

        try:
            with self.path.open('rb') as f:
                self.steps = pickle.load(f)

        except FileNotFoundError:
            self.steps = []

    def do_show(self,arg):
        """Shows all steps so far"""

        pprint(self.steps)

    def do_save(self, arg):
        """Save the pipeline"""

        with self.path.open('wb') as f:
            pickle.dump(self.steps, f)

    def do_quit(self, arg):
        """Exit Pipeline"""

        sys.exit(0)

    def do_exec(self, arg):
        """Append program invocation to the pipeline"""
        self.steps.append(arg)
        self.cmdqueue.append(arg)
