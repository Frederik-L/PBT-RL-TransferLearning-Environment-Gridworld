# @title:    test_gw.py
# @author:   Jan Frederik Liebig
# @date:     29.06.2021

# Imports
from src.gridworld import Gridworld
from src.tile import Tile
from src.helper import Obstacle
import matplotlib.pyplot as plt

# Code


class GridworldTest:
    """
    Vision tests for the gridworld
    """

    def __init__(self, render_test: bool = True):
        """
        Performs all tests
        @param:
            render_test => true, if all tests including rendering should be performed
        """
        self.success = [0, 0]
        self.test_render()
        self.test_render_tile()
        if render_test:
            self.test_render_observation()
            self.test_render_step()
            self.test_render_turn_left()
            self.test_render_turn_right()
            self.test_render_obstacle_turn_left()
            self.test_render_obstacle_turn_right()
            self.test_render_obstacle_step()
        self.test_helper()

    def test_render(self):
        """
        Renders all different gridworld modes
        """

        gw = Gridworld.make("empty-10x10")
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()

        gw = Gridworld.make("empty-10x10-random")
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()

        gw = Gridworld.make("hardcore-10x10-random")
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()

    def test_render_tile(self):
        """
        Renders all tiles
        """
        tile = Tile()
        print(
            """0 = empty
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
            14 = debug"""
        )
        for i in range(15):
            tile.set_object(i)
            img = tile.render()
            plt.imshow(img)
            plt.show()
            tile.set_vision()
            img = tile.render()
            plt.imshow(img)
            plt.show()
            tile.set_vision()

    def test_render_observation(self):
        """
        Renders an observation for all modes
        """
        gw = Gridworld.make("empty-10x10")
        plt.imshow(gw.render())
        plt.show()
        plt.imshow(gw.get_observation())
        plt.show()

        gw = Gridworld.make("empty-10x10-random")
        plt.imshow(gw.render())
        plt.show()
        plt.imshow(gw.get_observation())
        plt.show()

        gw = Gridworld.make("hardcore-10x10-random")
        plt.imshow(gw.render())
        plt.show()
        plt.imshow(gw.get_observation())
        plt.show()

    def test_render_step(self):
        """
        Performs a step in every gridworld and renders before and after
        """
        gw = Gridworld.make("empty-10x10")
        plt.imshow(gw.render())
        plt.show()
        gw.step(0)
        plt.imshow(gw.render())
        plt.show()

        gw = Gridworld.make("empty-10x10-random")
        plt.imshow(gw.render())
        plt.show()
        gw.step(0)
        plt.imshow(gw.render())
        plt.show()

        gw = Gridworld.make("hardcore-10x10-random")
        plt.imshow(gw.render())
        plt.show()
        gw.step(0)
        plt.imshow(gw.render())
        plt.show()

    def test_render_turn_left(self):
        """
        Performs a turn left for every direction
        """
        gw = Gridworld.make("empty-10x10")
        plt.imshow(gw.render())
        plt.show()
        gw.step(1)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()
        gw.step(1)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()
        gw.step(1)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()
        gw.step(1)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()

    def test_render_turn_right(self):
        """
        Performs a turn right for every direction
        """
        gw = Gridworld.make("empty-10x10")
        plt.imshow(gw.render())
        plt.show()
        gw.step(2)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()
        gw.step(2)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()
        gw.step(2)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()
        gw.step(2)
        gw.world[gw.top_left_x][gw.top_left_y].set_object(14)
        plt.imshow(gw.render())
        plt.show()

    def test_render_obstacle_turn_left(self):
        """
        Turns an obstacle right and renders the before and after
        """
        gw = Gridworld.make("hardcore-10x10-random")
        plt.imshow(gw.render())
        plt.show()
        for i in range(5):
            gw.world[0][i].set_object(14)
            gw.move_obstacle(gw.obstacle_list[0], 1)
            plt.imshow(gw.render())
            plt.show()

    def test_render_obstacle_turn_right(self):
        """
        Turns an obstacle right and renders the before and after
        """
        gw = Gridworld.make("hardcore-10x10-random")
        plt.imshow(gw.render())
        plt.show()
        for i in range(5):
            gw.world[0][i].set_object(14)
            gw.move_obstacle(gw.obstacle_list[0], 2)
            plt.imshow(gw.render())
            plt.show()

    def test_render_obstacle_step(self):
        """
        Performs an obstacle step and renders the bevore and after
        """
        gw = Gridworld.make("empty-10x10")
        obstacle = Obstacle()
        obstacle.x = 10
        obstacle.y = 10
        obstacle.direction = 0
        gw.obstacle_list.append(obstacle)
        gw.world[10][10].set_object(8, obstacle)
        plt.imshow(gw.render())
        plt.show()

        for i in range(5):
            gw.world[0][i].set_object(14)
            gw.move_obstacle(gw.obstacle_list[0], 0)
            plt.imshow(gw.render())
            plt.show()
            gw.move_obstacle(gw.obstacle_list[0], 1)
            plt.imshow(gw.render())
            plt.show()

    def test_helper(self):
        """
        Tests if the helper tile works as intended

        @returns:
            0 if Helper correct
            1 if Error: Reward penalty not 0
        """
        gw = Gridworld.make("empty-10x10")
        if gw.current_reward_penalties > 0:
            return 1
        gw.step(0)
        if gw.current_reward_penalties == -0.1:
            return 0


gw_test = GridworldTest(True)
