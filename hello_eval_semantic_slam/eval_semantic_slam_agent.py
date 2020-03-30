from __future__ import print_function

import os
import select
import signal
import sys
import json
import numpy as np
from benchbot_api import Agent
from class_list import CLASS_LIST, get_class_id

_GROUND_TRUTH = os.path.join(os.path.dirname(__file__),
                             'ground_truth_miniroom_1.json')


class EvalSemanticSLAMAgent(Agent):

    def is_done(self, action_result):
        # Finish immediately as we are only evaluating
        return True

    def pick_action(self, observations, action_list):
        # Should never get to this point?
        return None, {}

    def save_result(self, filename, empty_results):
        # load the ground truth to base all detections from for eval
        with open(_GROUND_TRUTH, 'r') as f:
            h1_gt_dicts = json.load(f)['objects']

        # Perfect Semantic SLAM based upon ground-truth (for testing evaluation
        # process only)
        # Create list of detections. Each detection represented by a dictionary.
        det_dicts = [{
            "prob_dist": [0.0 if idx != get_class_id(gt_dict['class']) else 1.0 for idx in range(len(CLASS_LIST))],
            "centroid": gt_dict["centroid"],
            "extent": gt_dict["extent"]
        } for gt_dict in h1_gt_dicts]

        # Add the detections to the empty_results dict provided, & save the
        # results in the requested location
        empty_results.update({'proposals': det_dicts})
        with open(filename, "w") as f:
            json.dump(empty_results, f)
        return
