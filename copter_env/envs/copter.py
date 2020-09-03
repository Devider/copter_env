import gym
from gym import error, spaces, utils
from gym.utils import seeding
from copter_env.envs.env import Environment
import os
import numpy as np

class CopterEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/data/world.jpg'
        if os.path.exists(path):
            self.worldImagePath = path
            print('World is loaded')
        else:
            raise IOError()

        self.action_space = spaces.Box(
            low=np.array([-1.0, 0, 0]),
            high=np.array([1, 1, 1]),
            # shape=(3,),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=0,
            high=50,
            shape=(5,),
            dtype=np.int32,
        )

        self.viewer = None


    def step(self, action):
        print('Action received', action)
        o = self.env.getSonarData()
        r = 0
        if self.env.ship.isOnLand():
            r -= 10
        if not self.env.checkShipIsDead():
            r += 1
        else:
            r -= 1000
        r += self.env.ship.speed * 3

        d = self.env.checkShipIsDead() or self.env.chechIsComplete()

        self.env.step(action)

        return (o, r, d, {})


    def reset(self):

        self.env = Environment(self.worldImagePath)
        return self.env.getSonarData()


    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        if mode == 'rgb_array':
            return self.env.to_rgb()

        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(self.env.to_rgb()[:, :, ::-1])
            return self.viewer.isopen

        else:
            assert 0, "Render mode '%s' is not supported" % mode


    def close(self):
        self.viewer.close()


