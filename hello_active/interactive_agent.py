import matplotlib.pyplot as plt
import numpy as np

try:
    input = raw_input
except NameError:
    pass


class InteractiveAgent(object):

    def __init__(self):
        self.fig = None
        self.axs = None

    def __visualise_observations(self, observations):
        if self.fig is None:
            plt.ion()
            self.fig, self.axs = plt.subplots(2, 2)
            self.fig.canvas.set_window_title("Agent Observations")
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

    def is_done(self):
        # Go FOREVER
        return False

    def pick_action(self, observations):
        self.__visualise_observations(observations)
        action = None
        action_args = None
        while (action is None):
            try:
                action_text = input(
                    "Enter next action (either 'd <distance_in_metres>'"
                    " or 'a <angle_in_degrees>'): ").split(" ")
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
            except Exception:
                print("ERROR: Invalid selection")
                action = None
        return action, action_args
