import matplotlib.pyplot as plt
import numpy as np

from benchbot_api import ActionResult, Agent
from benchbot_api.tools import ObservationVisualiser

try:
    input = raw_input
except NameError:
    pass


class LineAgent(Agent):
    _ACTIONS = [('move_distance', {
        'distance': 1.0
    }), ('move_angle', {
        'angle': 90
    })]

    _ACTION_SEQUENCE = [0, 1, 1]

    _ITERATION_LIMIT = 10

    def __init__(self):
        self.vis = ObservationVisualiser()

        self.next_action_index = 0
        self.iteration_count = 0

    def is_done(self, action_result):
        # Continue as long as we have a action_result of SUCCESS & have not
        # reached iteration_count
        return (self.iteration_count >= LineAgent._ITERATION_LIMIT or
                action_result != ActionResult.SUCCESS)

    def pick_action(self, observations, action_list):
        # Perform a sanity check to confirm we have valid actions available
        if ('move_distance' not in action_list or
                'move_angle' not in action_list):
            raise ValueError(
                "We don't have any usable actions. Is BenchBot running in the "
                "right mode (active), or should it have exited (collided / "
                "finished)?")

        # Update the visualisation
        self.vis.visualise(
            observations,
            self.iteration_count * len(LineAgent._ACTION_SEQUENCE) +
            self.next_action_index)

        # Wait until the user presses Enter to perform the next action
        input("Press Enter to execute next action")

        # Figure out which action, & return the selection
        action = LineAgent._ACTIONS[LineAgent._ACTION_SEQUENCE[
            self.next_action_index]]
        if self.next_action_index == len(self._ACTION_SEQUENCE) - 1:
            self.next_action_index = 0
            self.iteration_count += 1
        else:
            self.next_action_index += 1
        return action

    def save_result(self, filename, empty_results, empty_object_fn):
        # We have no results, we'll skip saving
        return
