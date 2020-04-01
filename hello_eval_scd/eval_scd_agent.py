from __future__ import print_function

import os
import select
import signal
import sys
import json
import numpy as np
from benchbot_api import Agent
from class_list import CLASS_LIST, get_class_id

_GROUND_TRUTH1 = os.path.join(os.path.dirname(__file__),
                             'ground_truth_miniroom_1.json')

_GROUND_TRUTH2 = os.path.join(os.path.dirname(__file__),                                                                                                                                                                                                                  'ground_truth_miniroom_2.json')


class EvalSCDAgent(Agent):

    def is_done(self, action_result):
        # Finish immediately as we are only evaluating
        return True

    def pick_action(self, observations, action_list):
        # Should never get to this point?
        return None, {}

    def save_result(self, filename, empty_results, empty_object_fn):
        # NOTE we assume always that we are moving from miniroom1 to miniroom2
        # load the ground truth to base all detections from for eval
        with open(_GROUND_TRUTH1, 'r') as f:
            m1_gt_dicts = json.load(f)['objects']
        with open(_GROUND_TRUTH2, 'r') as f:
            m2_gt_dicts = json.load(f)['objects']

        # Determine which objects are added and which are removed
        gt_rem_dicts = [gt_dict for gt_dict in m1_gt_dicts if gt_dict not in m2_gt_dicts]
        gt_add_dicts = [gt_dict for gt_dict in m2_gt_dicts if gt_dict not in m1_gt_dicts]

        # Create list of detections. Each detection represented by a dictionary.
#        # Scenario 1: Perfect
#
#        # Add detections for added objects (note state_probs)
#        det_dicts = [{
#            "prob_dist": [0.0 if idx != get_class_id(gt_dict['class']) else 1.0 for idx in range(len(CLASS_LIST))],
#            "centroid": gt_dict["centroid"],
#            "extent": gt_dict["extent"],
#            "state_probs": [1.0, 0.0, 0.0]
#        } for gt_dict in gt_add_dicts]
#
#        # Add detections for removed objects (note state_probs)
#        det_dicts += [{
#            "prob_dist": [0.0 if idx != get_class_id(gt_dict['class']) else 1.0 for idx in range(len(CLASS_LIST))],
#            "centroid": gt_dict["centroid"],
#            "extent": gt_dict["extent"],
#            "state_probs": [0.0, 1.0, 0.0]
#        } for gt_dict in gt_rem_dicts]
#

#        # Scenario 2: Only added (No FP)
#
#        # Add detections for added objects (note state_probs)
#        det_dicts = [{
#            "prob_dist": [0.0 if idx != get_class_id(gt_dict['class']) else 1.0 for idx in range(len(CLASS_LIST))],
#            "centroid": gt_dict["centroid"],
#            "extent": gt_dict["extent"],
#            "state_probs": [1.0, 0.0, 0.0]
#        } for gt_dict in gt_add_dicts]
#
        # Scenario 3: Only added (FPs)

        # Add detections for added objects (note state_probs)
        det_dicts = [{
            "prob_dist": [0.0 if idx != get_class_id(gt_dict['class']) else 1.0 for idx in range(len(CLASS_LIST))],
            "centroid": gt_dict["centroid"],
            "extent": gt_dict["extent"],
            "state_probs": [1.0, 0.0, 0.0]
        } for gt_dict in gt_add_dicts]

        # Add detections for removed objects (note state_probs currently say added with 50% confidence)
        det_dicts += [{
            "prob_dist": [0.0 if idx != get_class_id(gt_dict['class']) else 1.0 for idx in range(len(CLASS_LIST))],
            "centroid": gt_dict["centroid"],
            "extent": gt_dict["extent"],
            "state_probs": [0.5, 0.0, 0.5]
        } for gt_dict in gt_rem_dicts]


        # Add the detections to the empty_results dict provided, & save the
        # results in the requested location
        empty_results.update({'proposals': det_dicts})
        with open(filename, "w") as f:
            json.dump(empty_results, f)
        return











