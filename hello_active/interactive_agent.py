from __future__ import print_function

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import select
import signal
import sys
from scipy.spatial.transform import Rotation as Rot

try:
    input = raw_input
except NameError:
    pass


def _set_axes_radius(ax, origin, radius):
    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])


def _set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])

    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)


class InteractiveAgent(object):

    def __init__(self):
        self.fig = None
        self.axs = None

        signal.signal(signal.SIGINT, self._die_gracefully)

    def __plot_frame(self, frame_name, frame_data):
        # NOTE currently assume that everything has parent frame 'map'
        L = 0.2
        print(frame_name)
        print(frame_data)
        origin = frame_data['translation_xyz']
        # BUG map has no rotation aspect, handling it here but it should have a rotation.
        if 'rotation_rpy' in frame_data.keys():
            orientation = frame_data['rotation_rpy']
        else:
            orientation = [0, 0, 0]
        rot_obj = Rot.from_euler('XYZ', orientation)
        x_vector = rot_obj.apply([1, 0, 0])
        y_vector = rot_obj.apply([0, 1, 0])
        z_vector = rot_obj.apply([0, 0, 1])
        self.axs[1, 1].quiver(origin[0],
                              origin[1],
                              origin[2],
                              x_vector[0],
                              x_vector[1],
                              x_vector[2],
                              length=L,
                              normalize=True,
                              color='r')
        self.axs[1, 1].quiver(origin[0],
                              origin[1],
                              origin[2],
                              y_vector[0],
                              y_vector[1],
                              y_vector[2],
                              length=L,
                              normalize=True,
                              color='g')
        self.axs[1, 1].quiver(origin[0],
                              origin[1],
                              origin[2],
                              z_vector[0],
                              z_vector[1],
                              z_vector[2],
                              length=L,
                              normalize=True,
                              color='b')
        self.axs[1, 1].text(origin[0], origin[1], origin[2], frame_name)

    def __visualise_observations(self, observations):
        if self.fig is None:
            plt.ion()
            self.fig, self.axs = plt.subplots(2, 2)
            self.axs[1, 1].remove()
            self.axs[1, 1] = self.fig.add_subplot(2, 2, 4, projection='3d')
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
        self.axs[0, 1].axis('equal')
        self.axs[0, 1].set_title("laser (robot frame)")
        self.axs[1, 1].clear()
        self.__plot_frame('map', {'translation_xyz': [0, 0, 0]})
        for k, v in observations['poses'].items():
            self.__plot_frame(k, v)
        # self.axs[1, 1].axis('equal') Unimplemented for 3d plots... wow...
        _set_axes_equal(self.axs[1, 1])
        self.axs[1, 1].set_title("poses (world frame)")

    def _die_gracefully(self, sig, frame):
        print("")
        sys.exit(0)

    def is_done(self):
        # Go FOREVER
        return False

    def pick_action(self, observations):
        self.__visualise_observations(observations)
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
                    plt.draw()
                    self.fig.canvas.start_event_loop(0.0001)
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
        return action, action_args
