import gym
from gym import error, spaces, utils
from gym.utils import seeding
from copter_env.envs.env import Environment
import os

class CopterEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print('init world')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(dir_path + '/data/world.jpg'):
            self.worldImagePath = os.path.exists(dir_path + '/data/world.jpg')
            print('World is loaded')
        else:
            raise IOError()


    def step(self, action):
        print('step')


    def reset(self):
        print('reset')


    def render(self, mode='human'):
        print('render')


    def close(self):
        print('close')