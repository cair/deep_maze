import math
import inspect
from abc import abstractmethod, ABC


class BaseMazeMechanic(ABC):

    def __init__(self, maze_game, **kwargs):
        """
        The BaseMazeMechanic. Cannot be initialized
        :param maze_game: MazeGame instance
        :param kwargs: dict of custom arguments
        """
        # Retrieve the stack to backtrack the caller class
        called_by_maze_game = False
        for stack_item in inspect.stack():
            if "self" in stack_item[0].f_locals.keys():
                caller_class = stack_item[0].f_locals["self"].__class__
                if "MazeGame" in str(caller_class):
                    called_by_maze_game = True

        # Ensure that Mechanic is constructed from MazeGame
        if not called_by_maze_game:
            raise ImportError("BaseMazeMechanic was not called from MazeGame. This is illegal behaviour!")
        self.game = maze_game

    @abstractmethod
    def on_start(self):
        raise NotImplementedError("on_start() must be properly overridden!")

    @abstractmethod
    def on_update(self):
        raise NotImplementedError("on_update() must be properly overridden!")

    @abstractmethod
    def on_terminal(self):
        raise NotImplementedError("on_terminal() must be properly overridden!")


class NormalMaze(BaseMazeMechanic):
    def __init__(self, maze_game, **kwargs):
        """
        NormalMaze. Has no additional mechanics
        :param maze_game: MazeGame instance
        :param kwargs: dict of custom arguments
        """
        super().__init__(maze_game, **kwargs)

    def on_start(self):
        pass

    def on_terminal(self):
        pass

    def on_update(self):
        pass


class POMDPMaze(BaseMazeMechanic):
    def __init__(self, maze_game, **kwargs):
        """
        The POMDPMaze. Adds FOW
        :param maze_game: MazeGame instance
        :param kwargs: dict of custom arguments
        """
        super().__init__(maze_game, **kwargs)

        self.vision = kwargs.get("vision")
        self.fog_color = kwargs.get("fog_color") if kwargs.get("fog_color") else (105, 105, 105)
        self.fog_sprites_idx = []
        self.show_target = kwargs.get("show_target") if kwargs.get("show_target") else False

    def on_start(self):
        # 1. Start out with no vision at all
        for sprite in self.game.sprite_maze:
            sprite.set_color(self.fog_color)

        if not self.show_target:
            self.game.sprite_target.set_color(self.fog_color)

        self.on_update()

    def on_terminal(self):
        pass

    def on_update(self):

        self._reset_fow()
        self._update_fow()
        self._update_target_fow()

    def _reset_fow(self):
        # Reset previous fow sprites
        for index in self.fog_sprites_idx:
            sprite = self.game.sprites.get_sprite(index)
            sprite.set_color(self.fog_color)
        self.fog_sprites_idx.clear()

    def _update_fow(self):
        p_x, p_y = self.game.player
        # Reveal vision area
        for x in range(max(0, p_x - self.vision), min(self.game.width, p_x + self.vision)):
            for y in range(max(0, p_y - self.vision), min(self.game.height, p_y + self.vision)):
                index = x + (y * self.game.height)
                sprite = self.game.sprites.get_sprite(index)
                sprite.set_color(sprite.original_color)
                self.fog_sprites_idx.append(index)

    def _update_target_fow(self):
        # If the target is hidden
        if not self.show_target:
            # Measure distance between player and target
            dist = math.hypot(self.game.target[0] - self.game.player[0], self.game.target[1] - self.game.player[1])
            if dist < self.vision:
                self.game.sprite_target.set_color(self.game.sprite_target.original_color)
            else:
                self.game.sprite_target.set_color(self.fog_color)


class POMDPLimitedMaze(POMDPMaze):
    """
    The POMDPLimitedMaze. Further adds FOW to walls
    :param maze_game: MazeGame instance
    :param kwargs: dict of custom arguments
    """
    def __init__(self, maze_game, **kwargs):
        super().__init__(maze_game, **kwargs)
        self.target_index = None

    def on_start(self):
        super().on_start()

        # Determine index of the goal
        self.target_index = self.game.target[0] + (self.game.target[1] * self.game.height)

    def on_terminal(self):
        super().on_terminal()

    def on_update(self):
        self._reset_fow()
        self._update_fow()
        self._update_target_fow()

    def _update_fow(self):
        p_x, p_y = self.game.player

        for direction in [
            [(x, p_y, True) for x in range(p_x, min(self.game.width, p_x + self.vision))],
            [(x, p_y, True) for x in reversed(range(max(0, p_x - self.vision), p_x))],
            [(p_x, y, False) for y in range(p_y, min(self.game.height, p_y + self.vision))],
            [(p_x, y, False) for y in reversed(range(max(0, p_y - self.vision), p_y))]]:

            for x, y, is_horizontal in direction:
                index = x + (y * self.game.height)
                self.fog_sprites_idx.append(index)

                if self.game.maze.grid[x, y] == 1:
                    break

                # Check neighbours, the player should see the walls
                index_0 = None
                index_1 = None
                if is_horizontal:
                    # We are looking for horizontal neighbours
                    x_0, y_0 = x, max(0, y - 1)
                    x_1, y_1 = x, min(self.game.height - 1, y + 1)

                    if self.game.maze.grid[x_0, y_0] == 1:
                        index_0 = x_0 + (y_0 * self.game.height)
                    if self.game.maze.grid[x_1, y_1] == 1:
                        index_1 = x_1 + (y_1 * self.game.height)
                else:
                    # We are looking for vertical neighbours
                    x_0, y_0 = max(0, x - 1), y
                    x_1, y_1 = min(self.game.width - 1, x + 1), y

                    if self.game.maze.grid[x_0, y_0] == 1:
                        index_0 = x_0 + (y_0 * self.game.height)
                    if self.game.maze.grid[x_1, y_1] == 1:
                        index_1 = x_1 + (y_1 * self.game.height)

                if index_0:
                    self.fog_sprites_idx.append(index_0)
                if index_1:
                    self.fog_sprites_idx.append(index_1)

        for fog_sprite_idx in self.fog_sprites_idx:
            fog_sprite = self.game.sprites.get_sprite(fog_sprite_idx)
            fog_sprite.set_color(fog_sprite.original_color)

    def _update_target_fow(self):
        if not self.show_target:
            if self.target_index in self.fog_sprites_idx:
                self.game.sprite_target.set_color(self.game.sprite_target.original_color)
            else:
                self.game.sprite_target.set_color(self.fog_color)


class TimedPOMDPLimitedMaze(POMDPLimitedMaze):
    def __init__(self, maze_game, **kwargs):
        super().__init__(maze_game, **kwargs)
        self.delay = kwargs.get("delay") if kwargs.get("delay") else 5
        self.ticks = 0

    def on_start(self):

        self.ticks = 0

    def on_terminal(self):
        super().on_terminal()

    def on_update(self):
        self.ticks += 1
        if self.ticks == self.delay:
            super().on_start()

        if self.ticks >= self.delay:
            super().on_update()


class TimedPOMDPMaze(POMDPMaze):
    """
    The TimedPOMDPMaze. Adds FOW after a delay (ticks)
    :param maze_game: MazeGame instance
    :param kwargs: dict of custom arguments
    """
    def __init__(self, maze_game, **kwargs):
        super().__init__(maze_game, **kwargs)
        self.delay = kwargs.get("delay") if kwargs.get("delay") else 5
        self.ticks = 0

    def on_start(self):

        self.ticks = 0

    def on_terminal(self):
        super().on_terminal()

    def on_update(self):
        self.ticks += 1
        if self.ticks == self.delay:
            super().on_start()

        if self.ticks >= self.delay:
            super().on_update()
