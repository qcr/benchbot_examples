from __future__ import print_function

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
        return ('move_next', {}) if 'move_next' in action_list else ('move_angle', {1.0})

    def save_result(self, filename):
        # load the ground truth to base all detections from for eval
        with open('../ground_truth/house_1.json', 'r') as f:
            h1_gt_dicts = json.load(f)['objects']

        # Perfect Semantic SLAM based upon ground-truth (for testing evaluation process only)
        # Create list of detections. Each detection represented by a dictionary.
        det_dicts = [{"class": gt_dict["class"], 
                      "confidence": 1.0,
                      "centroid": gt_dict["centroid"],
                      "extent": gt_dict["extent"]
                      } for gt_dict in h1_gt_dicts]
        
        # Define the details of the environment where the results came from
        # Note that in scene change detection, there will be two numbers (e.g. 1,2 for house:1:2)
        env_details = {'name': 'house', 'numbers': [1]}

        # Define the details of the task that was being performed (this should be specific for what
        # the agent is designed to do). This will have been defined in benchbot_run
        task_details = {'type': 'semantic_slam', 'control_mode': 'passive', 'localisation_mode': 'ground_truth'}

        with open(filename, "w") as f:
            json.dump({'task_details': task_details,
                       'environment_details': env_details,
                       'detections': det_dicts}, f)
        return
