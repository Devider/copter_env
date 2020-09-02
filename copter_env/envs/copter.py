import gym
from gym import error, spaces, utils
from gym.utils import seeding
from copter_env.envs.env import Environment
import os

class CopterEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print('init world')
        path = os.path.dirname(os.path.realpath(__file__)) + '/data/world.jpg'
        if os.path.exists(path):
            self.worldImagePath = path
            print('World is loaded')
        else:
            raise IOError()

        self.viewer = None


    def step(self, action):
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


