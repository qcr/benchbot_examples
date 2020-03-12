from __future__ import print_function

import os
import select
import signal
import sys
import json
import numpy as np

from benchbot_api import ActionResult, Agent
from benchbot_api.tools import ObservationVisualiser

try:
    input = raw_input
except NameError:
    pass


class EvaluateAgent(Agent):

    def __init__(self):
        self.vis = ObservationVisualiser()
        self.step_count = 0

        signal.signal(signal.SIGINT, self._die_gracefully)

    def _die_gracefully(self, sig, frame):
        print("")
        sys.exit(0)

    def is_done(self, action_result):
        # Finish immediately as we are only evaluating
        return True

    def pick_action(self, observations, action_list):
        # Should never get to this point?
        return ('move_next',
                {}) if 'move_next' in action_list else ('move_angle', {1.0})

    def save_result(self, filename, empty_results):
        # load the ground truth to base all detections from for eval
        with open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../../ground_truth/miniroom_1.json'), 'r') as f:
            h1_gt_dicts = json.load(f)['objects']

        # Perfect Semantic SLAM based upon ground-truth (for testing evaluation
        # process only)
        # Create list of detections. Each detection represented by a dictionary.
        det_dicts = [{
            "class": gt_dict["class"],
            "confidence": 1.0,
            "centroid": gt_dict["centroid"],
            "extent": gt_dict["extent"]
        } for gt_dict in h1_gt_dicts]

        # Add the detections to the empty_results dict provided, & save the
        # results in the requested location
        empty_results.update({'detections': det_dicts})
        with open(filename, "w") as f:
            json.dump(empty_results, f)
        return
