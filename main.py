from cair_maze.maze_game import MazeGame
import random
import time
if __name__ == "__main__":

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



