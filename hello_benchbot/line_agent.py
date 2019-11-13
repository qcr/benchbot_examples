import matplotlib.pyplot as plt
import numpy as np

try:
    input = raw_input
except NameError:
    pass


class LineAgent(object):
    _ACTIONS = [('move_distance', {
        'distance': 1.0
    }), ('move_angle', {
        'angle': 0.5 * np.pi
    })]

    _ACTION_SEQUENCE = [0, 1, 1]

    def __init__(self):
        self.fig = None
        self.axs = None
        self.next_action_index = 0

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
        input("Press Enter to execute next action")
        action = LineAgent._ACTIONS[LineAgent._ACTION_SEQUENCE[
            self.next_action_index]]
        self.next_action_index = (
            0 if self.next_action_index == len(self._ACTION_SEQUENCE) -
            1 else self.next_action_index + 1)
        return action
