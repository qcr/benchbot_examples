from __future__ import print_function

import select
import signal
import sys

from benchbot_api import ActionResult, Agent
from benchbot_api.tools import ObservationVisualiser

try:
    input = raw_input
except NameError:
    pass


class GuidedAgent(Agent):

    def __init__(self):
        self.vis = ObservationVisualiser()
        self.step_count = 0

        signal.signal(signal.SIGINT, self._die_gracefully)

    def _die_gracefully(self, sig, frame):
        print("")
        sys.exit(0)

    def is_done(self, action_result):
        # Go forever as long as we have a action_result of SUCCESS
        return action_result != ActionResult.SUCCESS

    def pick_action(self, observations, action_list):
        # Perform a sanity check to confirm we have valid actions available
        if 'move_next' not in action_list:
            raise ValueError(
                "We don't have any usable actions. Is BenchBot running in the "
                "right mode (passive), or should it have exited (collided / "
                "finished)?")

        # Update the visualisation
        self.vis.visualise(observations, self.step_count)

        if self.step_count == 0:
            print("Press ENTER to begin (Ctrl^C to exit): ", end='')
            sys.stdout.flush()
            i = None
            while not i:
                i, _, _ = select.select([sys.stdin], [], [], 0)
                self.vis.update()
            sys.stdin.readline()

        self.step_count += 1
        return ('move_next', {})

    def save_result(self, filename, empty_results, empty_object_fn):
        # We have no results, we'll skip saving
        return
