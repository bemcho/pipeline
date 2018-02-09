import cmd
import pickle
import sys
from pathlib import Path
from pprint import pprint
from subprocess import check_output
from .Step import *


class TextInterface(cmd.Cmd):
    """Text based interface for pipeline"""
    keep_going = None
    path = None
    prompt = 'Pipeline> '
    last_output = ''

    def __init__(self, keep_going, filename):
        super().__init__(completekey='tab')
        self.keep_going = keep_going
        self.path = Path(filename)

        try:
            with self.path.open('rb') as f:
                self.steps = pickle.load(f)

        except FileNotFoundError:
            self.steps = []

    def do_show(self, arg):
        """Shows all steps so far"""
        pprint(self.steps)

    def do_reset(self, arg):
        """Resets all steps so far"""
        self.steps = []
        pprint(self.steps)

    def do_save(self, arg):
        """Save the pipeline"""
        with self.path.open('wb') as f:
            pickle.dump(self.steps, f)

    def do_store(self, arg):
        """Store the step output"""
        StoreStep(arg).run(self.last_output)

    def do_quit(self, arg):
        """Exit Pipeline"""
        sys.exit(0)

    def do_run(self, arg):
        """Runs all saved commands as pipeline"""
        for step in self.steps[:]:
            self.run_step(step)
            pprint(self.last_output)

    def run_step(self, arg):
        """Helper method for running steps"""
        self.last_output = ExecStep(arg).run(self.last_output)[0]

    def do_exec(self, arg):
        """Append program invocation to the pipeline"""
        step_arg = ArgsStep().run(arg)[1]
        self.run_step(step_arg)
        self.steps.append(step_arg)
        pprint(self.last_output)
