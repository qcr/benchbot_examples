from __future__ import print_function

import numpy as np
import select
import signal
import sys

from benchbot_api.tools import ObservationVisualiser

try:
    input = raw_input
except NameError:
    pass


class InteractiveAgent(object):

    def __init__(self):
        self.vis = ObservationVisualiser()
        self.step_count = 0

        signal.signal(signal.SIGINT, self._die_gracefully)

    def _die_gracefully(self, sig, frame):
        print("")
        sys.exit(0)

    def is_done(self):
        # Go FOREVER
        return False

    def pick_action(self, observations):
        self.vis.visualise(observations, self.step_count)
        action = None
        action_args = None
        while (action is None):
            try:
                print(
                    "Enter next action (either 'd <distance_in_metres>'"
                    " or 'a <angle_in_degrees>'): ",
                    end='')
                sys.stdout.flush()
                i = None
                while not i:
                    i, _, _ = select.select([sys.stdin], [], [], 0)
                    self.vis.update()
                action_text = sys.stdin.readline().split(" ")
                if action_text[0] == 'a':
                    action = 'move_angle'
                    action_args = {
                        'angle':
                            np.radians(0 if len(action_text) ==
                                       1 else float(action_text[1]))
                    }
                elif action_text[0] == 'd':
                    action = 'move_distance'
                    action_args = {
                        'distance':
                            0
                            if len(action_text) == 1 else float(action_text[1])
                    }
                else:
                    raise ValueError()
            except Exception as e:
                print(e)
                print("ERROR: Invalid selection")
                action = None
        self.step_count += 1
        return action, action_args
