# @title:    tile.py
# @author:   Jan Frederik Liebig
# @date:     19.06.2021

# Imports
import numpy as np
from numpy import uint8

# Code


class Tile:
    """
    Tile class for the gridworld
    """

    def __init__(self):
        self.object_id = 0
        self.object = None
        self.rendering_done = False
        self.rendering = None
        self.vision = False

    def render(self):
        """
        Renders the current tile and returns it
        object id:
            0 = empty
            1 = player dir up
            2 = player dir left
            3 = player dir right
            4 = player dir down
            5 = wall
            6 = teleport
            7 = lava
            8 = obstacle up
            9 = obstacle left
            10 = obstacle right
            11 = obstacle down
            12 = destination
            13 = helper
            14 = debugg
        """
        if self.rendering_done:
            return self.rendering
        else:
            #   0 = empty
            self.rendering = np.zeros(shape=(8, 8, 3), dtype=uint8)
            self.rendering[0, 0:] = (160, 160, 160)
            self.rendering[7, 0:] = (160, 160, 160)
            self.rendering[1:, 0] = (160, 160, 160)
            self.rendering[1:, 7] = (160, 160, 160)

            #   1 = player dir up
            if self.object_id == 1:
                self.rendering[2:6, 4] = (200, 0, 0)
                self.rendering[2:6, 3] = (200, 0, 0)
                self.rendering[3, 2] = (200, 0, 0)
                self.rendering[3, 5] = (200, 0, 0)
                self.rendering[4, 1] = (200, 0, 0)
                self.rendering[4, 6] = (200, 0, 0)

            #   2 = player dir left
            if self.object_id == 2:
                self.rendering[4, 2:6] = (200, 0, 0)
                self.rendering[3, 2:6] = (200, 0, 0)
                self.rendering[2, 3] = (200, 0, 0)
                self.rendering[5, 3] = (200, 0, 0)
                self.rendering[1, 4] = (200, 0, 0)
                self.rendering[6, 4] = (200, 0, 0)

            #   3 = player dir right
            if self.object_id == 3:
                self.rendering[4, 2:6] = (200, 0, 0)
                self.rendering[3, 2:6] = (200, 0, 0)
                self.rendering[2, 4] = (200, 0, 0)
                self.rendering[5, 4] = (200, 0, 0)
                self.rendering[1, 3] = (200, 0, 0)
                self.rendering[6, 3] = (200, 0, 0)

            #   4 = player dir down
            if self.object_id == 4:
                self.rendering[2:6, 4] = (200, 0, 0)
                self.rendering[2:6, 3] = (200, 0, 0)
                self.rendering[3, 1] = (200, 0, 0)
                self.rendering[3, 6] = (200, 0, 0)
                self.rendering[4, 2] = (200, 0, 0)
                self.rendering[4, 5] = (200, 0, 0)

            #   5 = wall
            if self.object_id == 5:
                self.rendering[0:8, 0:8] = (50, 50, 50)

            #   6 = teleport
            if self.object_id == 6:
                self.rendering[1:7, 1:7] = (0, 200, 0)

            #   7 = lava
            if self.object_id == 7:
                self.rendering[0:8, 0:8] = (230, 128, 0)

            #   8 = obstacle up
            if self.object_id == 8:
                self.rendering[2:6, 2:6] = (0, 0, 200)
                self.rendering[2, 2] = (0, 0, 0)
                self.rendering[2, 5] = (0, 0, 0)

            #   9 = obstacle left
            if self.object_id == 9:
                self.rendering[2:6, 2:6] = (0, 0, 200)
                self.rendering[2, 2] = (0, 0, 0)
                self.rendering[5, 2] = (0, 0, 0)

            #   10 = obstacle right
            if self.object_id == 10:
                self.rendering[2:6, 2:6] = (0, 0, 200)
                self.rendering[2, 5] = (0, 0, 0)
                self.rendering[5, 5] = (0, 0, 0)

            #   11 = obstacle down
            if self.object_id == 11:
                self.rendering[2:6, 2:6] = (0, 0, 200)
                self.rendering[5, 2] = (0, 0, 0)
                self.rendering[5, 5] = (0, 0, 0)

            #   12 = destination
            if self.object_id == 12:
                self.rendering[0:8, 0:8] = (170, 0.0, 170)

            #   13 = helper
            if self.object_id == 13:
                self.rendering[1:7, 1] = (0, 190, 0)
                self.rendering[1:7, 6] = (0, 190, 0)
                self.rendering[1, 1:7] = (0, 190, 0)
                self.rendering[6, 1:7] = (0, 190, 0)
                self.rendering[3:5, 3:5] = (190, 0, 0)

            if self.object_id == 14:
                self.rendering[0:8, 0:8] = (225, 50, 225)

        if self.vision:
            self.rendering[0:8] = self.rendering + (25, 25, 25)
        self.rendering_done = True
        return self.rendering

    def set_object(self, object_id: int, object=None):
        """
        Sets the object id of a tile
        @params:
            object_id => the if od the object to set
            object => the associated obstacle or teleporter-object, None else
        object id:
            0 = empty
            1 = player dir up
            2 = player dir left
            3 = player dir right
            4 = player dir down
            5 = wall
            6 = teleport
            7 = lava
            8 = obstacle up
            9 = obstacle left
            10 = obstacle right
            11 = obstacle down
            12 = destination
            13 = helper
            14 = debugg
        """
        self.rendering_done = False
        self.object_id = object_id
        self.object = object

    def set_vision(self):
        """
        Inverts the vision bool
        """
        self.vision = not self.vision
        self.rendering_done = False
