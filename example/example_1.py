
import gym
import gym_maze
import pygame
if __name__ == "__main__":

    env = gym.make("Maze-Arr-11x11-NormalMaze-v0")

    while True:
        a = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:
                    a = 0

                if event.key == pygame.K_UP:
                    a = 1

                if event.key == pygame.K_LEFT:
                    a = 2

                if event.key == pygame.K_RIGHT:
                    a = 3
        if a is None:
            continue

        s, r, t, info = env.step(a)
        env.render()

        if t:
            env.reset()

    # Direct initialization
    m = MazeGame((11, 11), mechanic=MazeGame.POMDPMaze, mechanic_args=dict(vision=3))
    m.set_preprocess(dict(
        image=dict(),
        #resize=dict(size=(84, 84)),
        #grayscale=dict()
    ))

    fps = 0
    now = time.time()
    while True:
        a = random.randint(0, 3)
        m.render()
        data = m.step(a)



        if m.terminal:
            m.reset()

        if time.time() >= now + 1:
            print(fps)
            fps = 0
            now = time.time()

        fps += 1

