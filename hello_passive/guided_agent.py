from __future__ import print_function

import select
import signal
import sys

from benchbot_api.tools import ObservationVisualiser

try:
    input = raw_input
except NameError:
    pass


class GuidedAgent(object):

    def __init__(self):
        self.vis = ObservationVisualiser()
        self.step_count = 0

        signal.signal(signal.SIGINT, self._die_gracefully)

    def _die_gracefully(self, sig, frame):
        print("")
        sys.exit(0)

    def is_done(self):
        # TODO exit when through list of poses
        return False

    def pick_action(self, observations):
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
        return 'move_next', {}
