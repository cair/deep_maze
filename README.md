# Maze environment for GYM

## Installation
```bash
pip install git+https://github.com/CAIR-UIA/DeepMaze.git
```

## Basic Usage
```python
import gym
import gym_maze # This is required in order to load gym-maze
import os

if __name__ == '__main__':
    
    # Configure the environment
    os.environ["gym_maze_width"] = str(5)
    os.environ["gym_maze_height"] = str(5)
    os.environ["gym_maze_screen_width"] = str(640)
    os.environ["gym_maze_screen_height"] = str(480)
    os.environ["gym_maze_no_random"] = str(0)
    os.environ["gym_maze_change_map_after"] = str(10000000000000)
    os.environ["gym_maze_state_representation"] = "image"
    os.environ["gym_maze_funny"] = str(0)
    os.environ["image_state_width"] = str(80)
    os.environ["image_state_height"] = str(80)

    # Create GYM environment
    env = gym.make("maze-v0")

    # Reset environment
    s = env.reset()

    # Set terminal state to false
    terminal = False

    while not terminal:
        # Draw environment on screen
        env.render()  # For image you MUST call this

        # Draw action from distribution
        a = env.action_space.sample()

        # Perform action in environment
        s1, r, t, _ = env.step(a)
        terminal = t

        s = s1
```

## Licence
Copyright 2017 Per-Arne Andersen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.