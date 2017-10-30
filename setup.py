from setuptools import setup

setup(name='gym_maze',
      version='0.0.1',
      install_requires=['gym', 'cython', 'numpy', 'scipy', 'pygame'],
      packages=['gym_maze', 'gym_maze.envs']
      )
