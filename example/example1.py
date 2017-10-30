import gym
import gym_maze
import os

if __name__ == '__main__':

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

    env = gym.make("maze-v0")
    env.render()

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
