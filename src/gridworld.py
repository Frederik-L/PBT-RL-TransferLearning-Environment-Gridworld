# @title:    gridworld.py
# @author:   Jan Frederik Liebig
# @date:     19.06.2021

# Imports
import random
import numpy as np
import matplotlib.pyplot as plt
import time
from numpy import uint8
from helper import Teleporter, Info, Obstacle
from tile import Tile


# Code


class Gridworld:
    """
    Gridworld RL-Environment
    directions:
        0 = up
        1 = left
        2 = right
        3 = down

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
        14 = debug

    actions:
        0 = forward
        1 = turn left
        2 = turn right
    """

    def __init__(
        self,
        grid_size: int = 10,
        observation_size: int = 5,
        random: bool = False,
        seed=None,
        obstacles: bool = False,
        max_steps: int = 0,
        num_obstacles: int = 6,
    ):
        """
        Initializes a gridworld
        @params:
            grid_size: int the size of the playable grid (square)
            observation_size: int = the size of the observation, only odd observation sizes allowed
            random: bool if True all objects are placed random
            seed: Any sets the seed for the gridworld, if None: int(time.time()) will be the seed
            obstacles: bool if True lava and obstacles will be placed random
            max_steps: int  number of allowed steps before run fails
            num_obstacles: int number of moving obstacles

        directions:
            0 = up
            1 = right
            2 = left
            3 = down
        """

        self.current_steps = 0
        self.current_reward_penalties = 0
        self.grid_size = grid_size
        assert observation_size % 2, "Error: Only odd observation sizes allowed"
        self.observation_size = observation_size
        self.obs_size = observation_size * 8
        self.n_actions = 3
        self.random = random
        if seed is None:
            self.seed = int(time.time())
        else:
            self.seed = seed
        self.obstacles = obstacles
        self.max_steps = max_steps
        self.num_obstacles = num_obstacles

        self.world, self.world_size = self.make_word()

        (
            self.player_x,
            self.player_y,
            self.player_direction,
            self.top_left_x,
            self.top_left_y,
        ) = self.init_player()

        self.goal_x, self.goal_y = self.init_goal()

        self.teleport = self.init_tp()

        self.helper_x, self.helper_y = self.init_helper()

        self.obstacle_list = self.init_obstacles()

        self.lava_x, self.helper_y = self.init_lava()

        self.set_vision()
        self.info = Info()
        self.done = False

    @staticmethod
    def make(environment_id: str, seed=None):
        """
        Makes a gridworld and returns a Gridworld object
        @params:
            environment_id => id of the environment to create
            seed => random seed, None default
        current environment ids:
            empty-10x10 => an empty 10x10 test world
            empty-10x10-random => an empty 10x10 test world with all objects random placed
            hardcore-10x10-random => a 10x10 world with all objects placed
        """

        if environment_id == "empty-10x10":
            return Gridworld(
                grid_size=10,
                observation_size=5,
                random=False,
                seed=seed,
                obstacles=False,
                max_steps=200,
                num_obstacles=0,
            )
        if environment_id == "empty-10x10-random":
            return Gridworld(
                grid_size=10,
                observation_size=5,
                random=True,
                seed=seed,
                obstacles=False,
                max_steps=200,
                num_obstacles=0,
            )

        if environment_id == "hardcore-10x10-random":
            return Gridworld(
                grid_size=10,
                observation_size=5,
                random=True,
                seed=seed,
                obstacles=True,
                max_steps=200,
                num_obstacles=3,
            )

    def make_word(self):
        world_size = self.grid_size + (2 * (self.observation_size - 1))
        world = [[Tile() for j in range(world_size)] for i in range(world_size)]
        for i in range(world_size):
            for j in range(self.observation_size - 1):
                world[i][j].set_object(5)
                world[j][i].set_object(5)
                world[world_size - 1 - j][i].set_object(5)
                world[i][world_size - 1 - j].set_object(5)
        return world, world_size

    def init_player(self):
        """
        Sets the player in the gridworld
        Returns player_x, player_y, player_direction,top_left_x, top_left_y
        """
        if not self.random:
            self.world[self.observation_size - 1][self.observation_size - 1].set_object(
                3
            )
            return (
                self.observation_size - 1,
                self.observation_size - 1,
                2,
                int(self.observation_size / 2),
                self.observation_size - 1,
            )
        else:
            x = random.randint(
                self.observation_size - 1, self.world_size - self.observation_size
            )
            y = random.randint(
                self.observation_size - 1, self.world_size - self.observation_size
            )
            direction = random.randint(0, 3)
            top_left_x = 0
            top_left_y = 0
            if direction == 0:
                top_left_x = x - self.observation_size + 1
                top_left_y = y - int(self.observation_size / 2)
            elif direction == 1:
                top_left_x = x - int(self.observation_size / 2)
                top_left_y = y - self.observation_size + 1
            elif direction == 2:
                top_left_x = x - int(self.observation_size / 2)
                top_left_y = y
            elif direction == 3:
                top_left_x = x
                top_left_y = y - int(self.observation_size / 2)

            self.world[x][y].set_object(direction + 1)
            return x, y, direction, top_left_x, top_left_y

    def init_goal(self):
        """
        Places the goal tile of the gridworld
        Returns x and y coordinates of the goal tile
        """
        if not self.random:
            self.world[self.world_size - self.observation_size][
                self.world_size - self.observation_size
            ].set_object(12)
            return (
                self.world_size - self.observation_size,
                self.world_size - self.observation_size,
            )
        else:
            set_goal = False
            while not set_goal:
                x = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                y = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                if self.world[x][y].object_id == 0:
                    set_goal = True

            self.world[x][y].set_object(12)
            return x, y

    def init_tp(self):
        """
        Creates a Teleporter-object and places it on the map.
        Returns the Teleporter-object
        """
        tp = Teleporter
        if not self.random:
            tp.x_1 = self.observation_size - 1
            tp.y_1 = self.observation_size + 1
            tp.x_2 = self.world_size - self.observation_size
            tp.y_2 = self.world_size - self.observation_size - 1

        else:
            set_tp = False

            while not set_tp:
                tp.x_1 = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                tp.y_1 = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                tp.x_2 = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                tp.y_2 = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )

                if (
                    self.world[tp.x_1][tp.y_1].object_id == 0
                    and self.world[tp.x_2][tp.y_2].object_id == 0
                ):
                    set_tp = True

        self.world[tp.x_1][tp.y_1].set_object(6, tp)
        self.world[tp.x_2][tp.y_2].set_object(6, tp)
        return tp

    def init_helper(self):
        """
        Places the helper-tile on the map
        Returns the x and y coordinates of the helper-tile
        """
        if not self.random:
            x = self.observation_size - 1
            y = self.observation_size

        else:
            set_helper = False

            while not set_helper:
                x = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                y = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                if self.world[x][y].object_id == 0:
                    set_helper = True

        self.world[x][y].set_object(13)

        return x, y

    def init_obstacles(self):
        """
        Creates a list of obstacles and places them on the map
        Returns the list of obstacles
        """
        obstacles = []
        if not self.obstacles:
            return obstacles
        for i in range(self.num_obstacles):
            set_obstacle = False
            while not set_obstacle:
                x = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                y = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                #   0 = obstacle up
                #   1 = obstacle left
                #   2 = obstacle down
                #   3 = obstacle right
                direction = random.randint(0, 3)
                if self.world[x][y].object_id == 0:
                    set_obstacle = True
            obstacle = Obstacle()
            obstacle.x = x
            obstacle.y = y
            obstacle.dead = False
            obstacle.direction = direction
            self.world[x][y].set_object(8 + direction, obstacle)
            obstacles.append(obstacle)
        return obstacles

    def init_lava(self):
        """
        Places a lava-tile on the map
        Returns the x and y coordinates of the lava-tile
        """
        if self.obstacles:
            set_helper = False
            while not set_helper:
                x = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                y = random.randint(
                    self.observation_size - 1, self.world_size - self.observation_size
                )
                if self.world[x][y].object_id == 0:
                    set_helper = True
            self.world[x][y].set_object(7)
        else:
            x, y = -1, -1
        return x, y

    def step(self, action):
        """
        Performs a step with the given action on the map
        @params:
            action => the action to perform
        Returns:
            next_state => Observation of the map after the step
            reward => Reward of this step
            done => True if the state is terminal
            info => Info object with all current game information

        actions:
            0 = forward
            1 = turn left
            2 = turn right
        """
        self.current_steps += 1
        self.info.num_steps += 1

        if self.current_steps > self.max_steps:
            self.done = True
            self.info.success = False
            reward = 0
            self.info.reward = 0
            next_state = self.get_observation()
            return next_state, reward, self.done, self.info

        self.set_vision()

        if action == 0:
            x, y = self.get_move()
            object_id = self.world[x][y].object_id

            #   0 = empty
            if object_id == 0:
                self.move_player(x, y)

            #   5 = wall
            if object_id == 5:
                self.info.wall_hit += 1
                self.current_reward_penalties += 0.05
                self.info.reward_penalty += 0.05

            #   6 = teleport
            if object_id == 6:
                teleport = self.world[x][y].object
                self.info.teleport = True
                if x == teleport.x_1 and y == teleport.y_1:
                    self.move_player(teleport.x_2, teleport.y_2)
                    self.world[x][y].set_object(0)
                else:
                    self.move_player(teleport.x_1, teleport.y_1)
                    self.world[x][y].set_object(0)
                self.world[teleport.x_1][teleport.y_1].object = None
                self.world[teleport.x_2][teleport.y_2].object = None

            #   7 = lava
            if object_id == 7:
                self.info.lava_hit = True
                self.info.success = False
                self.info.reward_penalty += 10
                self.current_reward_penalties += 10
                self.done = True

            #   8, 9 , 10, 11 = obstacle
            if object_id == 8 or object_id == 9 or object_id == 10 or object_id == 11:
                obstacle = self.world[x][y].object
                obstacle.dead = True
                self.world[x][y].object = None
                self.info.reward_penalty += 0.2
                self.info.obstacles_hit += 1
                self.move_player(x, y)
                self.current_reward_penalties += 0.2

                #   12 = destination
            if object_id == 12:
                self.move_player(x, y)
                self.done = True
                self.info.success = True

                #   13 = helper
            if object_id == 13:
                self.move_player(x, y)
                self.info.helper_found = True
                self.info.reward_penalty -= 0.1
                self.current_reward_penalties -= 0.1
        else:
            self.turn(action)

        for obstacle in self.obstacle_list:
            if not obstacle.dead:
                self.move_obstacle(obstacle)

        self.set_vision()
        next_state = self.get_observation()

        reward = self.get_reward()
        if self.done:
            self.info.reward += reward
        else:
            reward = 0

        return next_state, reward, self.done, self.info

    def get_move(self):
        """
        Calculates the next player coordinates in case of a step
        Returns the next x and y coordinates
        """
        if self.player_direction == 0:
            x = self.player_x - 1
            y = self.player_y

        elif self.player_direction == 1:
            x = self.player_x
            y = self.player_y - 1

        elif self.player_direction == 2:
            x = self.player_x
            y = self.player_y + 1

        elif self.player_direction == 3:
            x = self.player_x + 1
            y = self.player_y
        return x, y

    def move_player(self, x, y):
        """
        Moves the player to the given coordinates, if possible
        @params:
            x => the input x coordinate
            y => the input y coordinate
        """

        if self.player_direction == 0:
            self.top_left_x = x - self.observation_size + 1
            self.top_left_y = y - int(self.observation_size / 2)
        elif self.player_direction == 1:
            self.top_left_x = x - int(self.observation_size / 2)
            self.top_left_y = y - self.observation_size + 1
        elif self.player_direction == 2:
            self.top_left_x = x - int(self.observation_size / 2)
            self.top_left_y = y
        elif self.player_direction == 3:
            self.top_left_x = x
            self.top_left_y = y - int(self.observation_size / 2)

        self.world[self.player_x][self.player_y].set_object(0)
        self.world[x][y].set_object(self.player_direction + 1)
        self.player_x = x
        self.player_y = y

    #
    def turn(self, dir):
        """
        Turns the player in the given direction
        @params:
            dir => the direction to turn
        actions:
            1 = turn left
            2 = turn right
        """
        next_dir = 0

        if dir == 1:
            if self.player_direction == 0:
                next_dir = 1

            elif self.player_direction == 1:
                next_dir = 3

            elif self.player_direction == 2:
                next_dir = 0

            elif self.player_direction == 3:
                next_dir = 2

        if dir == 2:
            if self.player_direction == 0:
                next_dir = 2

            elif self.player_direction == 1:
                next_dir = 0

            elif self.player_direction == 2:
                next_dir = 3

            elif self.player_direction == 3:
                next_dir = 1

        if next_dir == 0:
            self.top_left_x = self.player_x - self.observation_size + 1
            self.top_left_y = self.player_y - int(self.observation_size / 2)
        elif next_dir == 1:
            self.top_left_x = self.player_x - int(self.observation_size / 2)
            self.top_left_y = self.player_y - self.observation_size + 1
        elif next_dir == 2:
            self.top_left_x = self.player_x - int(self.observation_size / 2)
            self.top_left_y = self.player_y
        elif next_dir == 3:
            self.top_left_x = self.player_x
            self.top_left_y = self.player_y - int(self.observation_size / 2)

        self.world[self.player_x][self.player_y].set_object(next_dir + 1)
        self.player_direction = next_dir

    #
    def move_obstacle(self, obstacle, move: int = -1):
        """
        Randomly generates the obstacles action and performs it
        @params:
            obstacle => to obstacle to perform an action
            move => optional: the action to perform
        Returns the Reward penalty of the obstacle move

        actions:
            0 = forward
            1 = turn left
            2 = turn right
        """
        move_done = False
        reward_penalty = 0
        if move == -1:
            move_done = True
        while not move_done:
            if not move_done:
                move = random.randint(0, 100)
                if move < 60:
                    move = 0
                elif move < 80:
                    move = 1
                else:
                    move = 2

            # turn left
            if move == 1:
                if obstacle.direction == 0:
                    obstacle.direction = 1

                elif obstacle.direction == 1:
                    obstacle.direction = 3

                elif obstacle.direction == 2:
                    obstacle.direction = 0

                elif obstacle.direction == 3:
                    obstacle.direction = 2

                move_done = True
                self.world[obstacle.x][obstacle.y].set_object(
                    obstacle.direction + 8, obstacle
                )

            # turn right
            if move == 2:
                if obstacle.direction == 0:
                    obstacle.direction = 2

                elif obstacle.direction == 1:
                    obstacle.direction = 0

                elif obstacle.direction == 2:
                    obstacle.direction = 3

                elif obstacle.direction == 3:
                    obstacle.direction = 1

                move_done = True
                self.world[obstacle.x][obstacle.y].set_object(
                    obstacle.direction + 8, obstacle
                )

            # make step
            if move == 0:
                n_x = 0
                n_y = 0
                if obstacle.direction == 0:
                    n_x = obstacle.x - 1
                    n_y = obstacle.y

                elif obstacle.direction == 1:
                    n_x = obstacle.x
                    n_y = obstacle.y - 1

                elif obstacle.direction == 2:
                    n_x = obstacle.x
                    n_y = obstacle.y + 1

                elif obstacle.direction == 3:
                    n_x = obstacle.x + 1
                    n_y = obstacle.y

                # next empty
                if self.world[n_x][n_y].object_id == 0:
                    move_done = True
                    self.world[obstacle.x][obstacle.y].set_object(0)
                    self.world[n_x][n_y].set_object(8 + obstacle.direction, obstacle)

                # next player
                if (
                    (self.world[n_x][n_y].object_id == 1)
                    or (self.world[n_x][n_y].object_id == 2)
                    or (self.world[n_x][n_y].object_id == 3)
                    or (self.world[n_x][n_y].object_id == 4)
                ):
                    move_done = True
                    self.world[obstacle.x][obstacle.y].set_object(0)
                    obstacle.dead = True
                    self.current_reward_penalties += 0.2
                    self.get_reward()
                    reward_penalty = 0.2

                # next lava
                if self.world[n_x][n_y].object_id == 7:
                    move_done = True
                    obstacle.dead = True
                    self.world[obstacle.x][obstacle.y].set_object(0)
                if move_done:
                    obstacle.x = n_x
                    obstacle.y = n_y
        return reward_penalty

    def get_reward(self):
        """
        Calculates the current reward
        Returns the current reward
        """
        reward = 1 - ((self.current_steps ** 1.5) / (self.max_steps ** 1.5))
        reward = reward - self.current_reward_penalties
        if reward < 0:
            self.done = True
            reward = 0
        return reward

    def get_observation(self):
        """
        Generates the current player observation
        Returns the current observation image
        """
        pixel_len = self.observation_size * 8
        image = np.zeros(shape=(pixel_len, pixel_len, 3), dtype=uint8)
        for i in range(self.observation_size):
            for j in range(self.observation_size):
                image[i * 8 : i * 8 + 8, j * 8 : j * 8 + 8] = (
                    self.world[self.top_left_x + i][self.top_left_y + j].render().copy()
                )
        # directions:
        #   0 = up
        #   1 = right
        #   2 = left
        #   3 = down
        if self.player_direction == 0:
            image = np.ndarray.copy(image)
            return image
        elif self.player_direction == 1:
            image = np.rot90(image)
            image = np.rot90(image)
            image = np.rot90(image)
            image = np.ndarray.copy(image)
            return image
        elif self.player_direction == 2:
            image = np.rot90(image)
            image = np.ndarray.copy(image)
            return image
        elif self.player_direction == 3:
            image = np.rot90(image)
            image = np.rot90(image)
            image = np.ndarray.copy(image)
            return image

        return image

    def render(self):
        """
        Renders the current map
        Returns an RGB image of the map
        """
        pixel_len = self.world_size * 8
        image = np.zeros(shape=(pixel_len, pixel_len, 3), dtype=uint8)
        for i in range(self.world_size):
            for j in range(self.world_size):
                image[i * 8 : i * 8 + 8, j * 8 : j * 8 + 8] = (
                    self.world[i][j].render().copy()
                )
        return image

    def set_vision(self):
        """
        Highlights the current observation
        """
        for i in range(self.observation_size):
            for j in range(self.observation_size):
                self.world[i + self.top_left_x][j + self.top_left_y].set_vision()

    def reset(self):
        """
        Creates a new map and resets all variables
        Returns an observation of the new map
        """
        self.world, self.world_size = self.make_word()
        (
            self.player_x,
            self.player_y,
            self.player_direction,
            self.top_left_x,
            self.top_left_y,
        ) = self.init_player()
        self.goal_x, self.goal_y = self.init_goal()
        self.teleport = self.init_tp()
        self.helper_x, self.helper_y = self.init_helper()
        self.obstacle_list = self.init_obstacles()
        self.init_lava()
        self.set_vision()
        self.current_steps = 0
        self.current_reward_penalties = 0
        self.info = Info()
        self.done = False
        return self.get_observation()


"""
Example World creation


gw = Gridworld.make("hardcore-10x10-random")
plt.imshow(gw.render())
plt.show()

gw = Gridworld.make("empty-10x10-random")
plt.imshow(gw.render())
plt.show()

gw = Gridworld.make("empty-10x10")
plt.imshow(gw.render())
plt.show()
"""
