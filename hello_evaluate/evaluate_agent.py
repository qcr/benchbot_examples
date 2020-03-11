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

_SEM_SLAM_TESTS = ['sem_slam_perfect', 'sem_slam_50_iou', 'sem_slam_25_iou', 'sem_slam_no_chair', 
                   'sem_slam_only_chair', 'sem_slam_double_det']
_SCD_TESTS = ['scd_perfect', 'scd_no_rem', 'scd_no_add']

class EvaluateAgent(Agent):

    def __init__(self, test_type, task_details):
        self.vis = ObservationVisualiser()
        self.step_count = 0
        
        # Quickly check the test corresponds with the type of experiment being run
        if task_details['type'] == 'scd' and test_type not in _SCD_TESTS:
            raise ValueError("Error! you cannot run {} test when running Scene Change Detection task!".format(test_type))
        if task_details['type'] == 'semantic_slam' and test_type not in _SEM_SLAM_TESTS:
            raise ValueError("Error! you cannot run {} test when running Semantic SLAM task!".format(test_type))
        
        self.test_type = test_type
        self.task_details = task_details

        signal.signal(signal.SIGINT, self._die_gracefully)

    def _die_gracefully(self, sig, frame):
        print("")
        sys.exit(0)

    def is_done(self, action_result):
        # Finish immediately as we are only evaluating
        return True

    def pick_action(self, observations, action_list):

        if self.step_count == 0:
            print("Press ENTER to run {} experiment".format(self.test_type), end='')
            sys.stdout.flush()
            i = None
            while not i:
                i, _, _ = select.select([sys.stdin], [], [], 0)
                self.vis.update()
            sys.stdin.readline()

        self.step_count += 1
        return ('move_next', {}) if 'move_next' in action_list else ('move_angle', {1.0})

    def save_result(self, filename):
        # load the ground truth to base all detections from for eval
        with open('../ground_truth/house_1.json', 'r') as f:
            h1_gt_dicts = json.load(f)['objects']
        with open('../ground_truth/house_2.json', 'r') as f:
            h2_gt_dicts = json.load(f)['objects']
        
        ############################################################
        #                           TESTS                          #
        ############################################################

        # Perfect Semantic SLAM
        if self.test_type == 'sem_slam_perfect':
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"]
                          } for gt_dict in h1_gt_dicts]
            env_details = {'name': 'house', 'numbers': [1]}
        
        # Semantic SLAM with approx 50% IoU all objects
        elif self.test_type == 'sem_slam_50_iou':
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict['centroid'],
                          # note the small addition should just deal with floating point errors
                          "extent": list(np.array(gt_dict["extent"]) * [0.5, 1, 1] + [1e-12, 0, 0])
                          } for gt_dict in h1_gt_dicts]
            env_details = {'name': 'house', 'numbers': [1]}
        
        # Semantic SLAM with approx 25% IoU all objects
        elif self.test_type == 'sem_slam_25_iou':
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict['centroid'],
                          # note the small addition should just deal with floating point errors
                          "extent": list(np.array(gt_dict["extent"]) * [0.25, 1, 1] + [1e-12, 0, 0])
                          } for gt_dict in h1_gt_dicts]
            env_details = {'name': 'house', 'numbers': [1]}
        
        # Semantic SLAM where one class is missed
        elif self.test_type == 'sem_slam_no_chair':
            print("Missing 1 class of {}".format(len(np.unique([gt_dict["class"] for gt_dict in h1_gt_dicts]))))
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"]
                          } for gt_dict in h1_gt_dicts if gt_dict["class"] != "chair"]
            env_details = {'name': 'house', 'numbers': [1]}

        # Semantic SLAM where using only one class
        elif self.test_type == 'sem_slam_only_chair':
            print("Using 1 class of {}".format(len(np.unique([gt_dict["class"] for gt_dict in h1_gt_dicts]))))
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"]
                          } for gt_dict in h1_gt_dicts if gt_dict["class"] == "chair"]
            env_details = {'name': 'house', 'numbers': [1]}
        
        # Semantic SLAM mAP halved by double detections
        elif self.test_type == 'sem_slam_double_det':
            class_confs = {}
            det_dicts = []
            for gt_dict in h1_gt_dicts:
                if gt_dict["class"] not in class_confs.keys():
                    class_confs[gt_dict["class"]] = 1.0
                # Create the false positive with slightly higher confidence than the true positive
                det_dicts.append({
                    "class": gt_dict["class"],
                    "confidence": class_confs[gt_dict["class"]],
                    "centroid": [0.0, 0.0, 0.0],
                    "extent": [0.01, 0.01, 0.01]
                })
                class_confs[gt_dict["class"]] -= 0.01

                # Create the true positive with perfect overlap
                det_dicts.append({
                    "class": gt_dict["class"],
                    "confidence": class_confs[gt_dict["class"]],
                    "centroid": gt_dict["centroid"],
                    "extent": gt_dict["extent"]
                })
                class_confs[gt_dict["class"]] -= 0.01
            env_details = {'name': 'house', 'numbers': [1]}
        

        # Scene Change Detection Perfect
        elif self.test_type == 'scd_perfect':
            
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"],
                          "changed_state": "removed"
                          } for gt_dict in h1_gt_dicts if gt_dict not in h2_gt_dicts]
            
            det_dicts += [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"],
                          "changed_state": "added"
                          } for gt_dict in h2_gt_dicts if gt_dict not in h1_gt_dicts]

            print(self.task_details)
            env_details = {'name': 'house', 'numbers': [1,2]}
        
        # Scene Change Detection missed removed
        elif self.test_type == 'scd_no_rem':
            
            rem_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"],
                          "changed_state": "removed"
                          } for gt_dict in h1_gt_dicts if gt_dict not in h2_gt_dicts]
            print("{} removed objects ignored".format(len(rem_dicts)))
            print(rem_dicts)
            
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"],
                          "changed_state": "added"
                          } for gt_dict in h2_gt_dicts if gt_dict not in h1_gt_dicts]

            print(self.task_details)
            env_details = {'name': 'house', 'numbers': [1,2]}
        
        # Scene Change Detection missed added
        elif self.test_type == 'scd_no_add':
            
            det_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"],
                          "changed_state": "removed"
                          } for gt_dict in h1_gt_dicts if gt_dict not in h2_gt_dicts]
            
            
            add_dicts = [{"class": gt_dict["class"], 
                          "confidence": 1.0,
                          "centroid": gt_dict["centroid"],
                          "extent": gt_dict["extent"],
                          "changed_state": "added"
                          } for gt_dict in h2_gt_dicts if gt_dict not in h1_gt_dicts]
            print("{} added objects ignored".format(len(add_dicts)))
            print(add_dicts)

            print(self.task_details)
            env_details = {'name': 'house', 'numbers': [1,2]}

        else:
            raise ValueError("invalid test type!")

        with open(filename, "w") as f:
            json.dump({'task_details': self.task_details,
                       'environment_details': env_details,
                       'detections': det_dicts}, f)
        return
