# @title:    helper.py
# @author:   Jan Frederik Liebig
# @date:     19.06.2021

# Imports
from dataclasses import dataclass

# Code


@dataclass
class Teleporter:
    """
    Dataclass for the gridworld teleporter containing the x and y coordinates of both tiles
    """

    x_1: int = -1
    y_1: int = -1
    x_2: int = -1
    y_2: int = -1


@dataclass
class Info:
    """
    Dataclass for the informations of the current episode
    """

    num_steps: int = 0
    reward_penalty: float = 0
    reward: float = 0
    success: bool = False
    helper_found: int = 0
    obstacles_hit: int = 0
    lava_hit: bool = False
    wall_hit: int = 0
    teleport: bool = False

    def __str__(self):
        return (
            f"Info[number of steps: {self.num_steps}; reward penalty: {self.reward_penalty}; reward: {self.reward}; "
            f"success: {self.success}; helper found: {self.helper_found}; obstacles hit: {self.obstacles_hit}; "
            f"lava hit: {self.lava_hit}; wall hit: {self.wall_hit}; teleport use: {self.teleport}"
        )


@dataclass
class Obstacle:
    """
    Dataclass of the gridworld obstacle containing coordinates and direction
    """

    x: int = -1
    y: int = -1
    direction: int = 0
    dead: bool = False
