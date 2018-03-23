from setuptools import setup

setup(name='gym_maze',
      version='2.0.0',
      install_requires=['gym', 'numpy', 'pygame', 'scikit-image'],
      packages=['gym_maze', 'gym_maze.envs', 'cair_maze']
      )
