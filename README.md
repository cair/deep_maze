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
    

    # Reset environment
    env = gym.make("maze-arr-11x11-full-deterministic-v0")
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

## Available Environments
There are several configurations available for gym-maze.

### Naming Convention
[name]-[representation]-[size_w]x[size_h]-[type]-v0

**name** - Name of the environment

**representation** - How the state is represented to the user. 'Img' delivers a **84x84x3** state while 'Arr' delivers size of the game board (9x9 game delivers  9x9 state)

**size_w** - Indicates width of game board

**size_h** - Indicates height of game board

**type** - Indicates weither RNG is deterministic (non-random) or stochastic (random). There is also a full-random mode that also remove randomness from spawn location


### Environment List
```
maze-arr-11x11-deterministic-v0
maze-arr-13x13-deterministic-v0
maze-arr-15x15-deterministic-v0
maze-arr-17x17-deterministic-v0
maze-arr-19x19-deterministic-v0
maze-arr-25x25-deterministic-v0
maze-arr-35x35-deterministic-v0
maze-arr-55x55-deterministic-v0
maze-arr-9x9-deterministic-v0
maze-arr-11x11-full-deterministic-v0
maze-arr-13x13-full-deterministic-v0
maze-arr-15x15-full-deterministic-v0
maze-arr-17x17-full-deterministic-v0
maze-arr-19x19-full-deterministic-v0
maze-arr-25x25-full-deterministic-v0
maze-arr-35x35-full-deterministic-v0
maze-arr-55x55-full-deterministic-v0
maze-arr-9x9-full-deterministic-v0
maze-arr-11x11-stochastic-v0
maze-arr-13x13-stochastic-v0
maze-arr-15x15-stochastic-v0
maze-arr-17x17-stochastic-v0
maze-arr-19x19-stochastic-v0
maze-arr-25x25-stochastic-v0
maze-arr-35x35-stochastic-v0
maze-arr-55x55-stochastic-v0
maze-arr-9x9-stochastic-v0
maze-v0
maze-img-11x11-deterministic-v0
maze-img-13x13-deterministic-v0
maze-img-15x15-deterministic-v0
maze-img-17x17-deterministic-v0
maze-img-19x19-deterministic-v0
maze-img-25x25-deterministic-v0
maze-img-35x35-deterministic-v0
maze-img-55x55-deterministic-v0
maze-img-9x9-deterministic-v0
maze-img-11x11-full-deterministic-v0
maze-img-13x13-full-deterministic-v0
maze-img-15x15-full-deterministic-v0
maze-img-17x17-full-deterministic-v0
maze-img-19x19-full-deterministic-v0
maze-img-25x25-full-deterministic-v0
maze-img-35x35-full-deterministic-v0
maze-img-55x55-full-deterministic-v0
maze-img-9x9-full-deterministic-v0
maze-img-11x11-stochastic-v0
maze-img-13x13-stochastic-v0
maze-img-15x15-stochastic-v0
maze-img-17x17-stochastic-v0
maze-img-19x19-stochastic-v0
maze-img-25x25-stochastic-v0
maze-img-35x35-stochastic-v0
maze-img-55x55-stochastic-v0
maze-img-9x9-stochastic-v0
```

## Licence
Copyright 2017 Per-Arne Andersen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.