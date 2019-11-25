import matplotlib.pyplot as plt
import numpy as np
from pynput.keyboard import Key, Listener
import sys
from termios import tcflush, TCIFLUSH
import time

try:
    input = raw_input
except NameError:
    pass

class DriveAgent(object):

    def __init__(self):
        self.fig = None
        self.axs = None
        self.distance_step = 0.1
        self.angle_step = 1.0
        self.print_msg = ""

    def __visualise_observations(self, observations):
        if self.fig is None:
            plt.ion()
            self.fig, self.axs = plt.subplots(2, 2)
            self.fig.canvas.set_window_title("Agent Observations")
            plt.show()
        self.axs[0, 0].clear()
        self.axs[0, 0].imshow(observations['image_rgb'])
        self.axs[0, 0].get_xaxis().set_visible(False)
        self.axs[0, 0].get_yaxis().set_visible(False)
        self.axs[0, 0].set_title("image_rgb")
        self.axs[1, 0].clear()
        self.axs[1, 0].imshow(observations['image_depth'],
                              cmap="hot",
                              clim=(np.amin(observations['image_depth']),
                                    np.amax(observations['image_depth'])))
        self.axs[1, 0].get_xaxis().set_visible(False)
        self.axs[1, 0].get_yaxis().set_visible(False)
        self.axs[1, 0].set_title("image_depth")
        self.axs[0, 1].clear()
        self.axs[0, 1].plot(0, 0, c='r', marker=">")
        self.axs[0, 1].scatter(
            [x[0] * np.cos(x[1]) for x in observations['laser']['scans']],
            [x[0] * np.sin(x[1]) for x in observations['laser']['scans']],
            c='k',
            s=4,
            marker='s')
        self.axs[0, 1].set_title("laser (robot frame)")
        self.axs[1, 1].clear()
        # TODO
        self.axs[1, 1].plot()
        self.axs[1, 1].set_title("poses (world frame)")
        plt.draw()
        plt.pause(0.0001)

    def is_done(self):
        # Go FOREVER
        return False

    def pick_action(self, observations):
        self.__visualise_observations(observations)

        # using this to get around changing non-local variables in 2.7
        # In 3 would use nonlocal but for some reason my machine is not installing benchbot in python3
        # action_data_dict = {'action': None, 'action_args': None}

        action = None
        action_args = None
        print_msg = ""

        # Nested function for handling key event from keyboard listener
        # that can output an action based on key strokes
        def on_press(key):

            # FOR PYTHON3 IMPLEMENTATION
            # Define we are using the nonlocal variables action and action_args
            # This allows us to change the variables from within the nested function
            nonlocal action
            nonlocal action_args

            # choose action based on input and print chosen action to screen
            # NOTE use \r to remove key stroke on command line from screen
            # NOTE the commands here will work even if you aren't on the main screen. Probably not desirable

            # # TEMP
            # action_data_dict['action'] = 'move_distance'
            # action_data_dict['action_args'] = {'distance': 0.0}
            # return False

            # Forwards command
            if key == Key.up:
                action = 'move_distance'
                action_args = {'distance': self.distance_step}
                print("\rforwards {0:.2f} metres".format(self.distance_step))
                self.print_msg = "forwards {0:.2f} metres".format(self.distance_step)

            # Backwards command
            elif key == Key.down:
                action = 'move_distance'
                action_args = {'distance': -self.distance_step}
                print("\rbackwards {0:.2f} metres".format(self.distance_step))
                self.print_msg = "backwards {0:.2f} metres".format(self.distance_step)

            # Turn right command
            elif key == Key.right:
                action = 'move_angle'
                action_args = {'angle': np.radians(-self.angle_step)}
                print("\rright {0:.2f} degrees".format(self.angle_step))
                self.print_msg = "right {0:.2f} degrees".format(self.angle_step)

            # Turn left command
            elif key == Key.left:
                action = 'move_angle'
                action_args = {'angle': np.radians(self.angle_step)}
                print("\rleft {0:.2f} degrees".format(self.angle_step))
                self.print_msg = "left {0:.2f} degrees".format(self.angle_step)

            else:
                # Need to use a try except here because only way to check if the key was a letter?
                try:
                    if key.char == 'o':
                        print("")
                        tcflush(sys.stdin, TCIFLUSH)
                        # Check how to safely take these inputs and handle exceptions
                        self.distance_step = float(input("give new distance step size in metres: "))
                        self.angle_step = float(input("give new angle step size in degrees: "))
                        action = 'move_distance'
                        action_args = {'distance': 0}
                        self.print_msg = ""

                except AttributeError:
                    # Do nothing if it is a special key we don't care about
                    pass

            # return False to stop listening for input
            # NOTE There must be a better way of doing all this
            return False
        count = 0
        while (action is None):
            # if count == 1000000:
            #     action = 'move_distance'
            #     action_args = {'distance': self.distance_step}
            # count += 1
            # time.sleep(1)
            # create a listener that listens for key presses and updated action
            # based on the key presses
            with Listener(on_press=on_press) as listener:
                listener.join()
        
        # TEMP OLD CODE
        # action = None
        # action_args = None
        # while (action is None):
        #     try:
        #         action_text = input(
        #             "Enter next action (either 'd <distance_in_metres>'"
        #             " or 'a <angle_in_degrees>'): ").split(" ")
        #         if action_text[0] == 'a':
        #             action = 'move_angle'
        #             action_args = {
        #                 'angle':
        #                     np.radians(0 if len(action_text) ==
        #                                1 else float(action_text[1]))
        #             }
        #         elif action_text[0] == 'd':
        #             action = 'move_distance'
        #             action_args = {
        #                 'distance':
        #                     0
        #                     if len(action_text) == 1 else float(action_text[1])
        #             }
        #         else:
        #             raise ValueError()
        #     except Exception:
        #         print("ERROR: Invalid selection")
        #         action = None
        # return action, action_args

        # print("\rChosen Action: {}".format(action))
        # print("Action Args: {}".format(action_args))
        return action, action_args
