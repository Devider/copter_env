import numpy as np
import math
from copter_env.envs.utils import clip, concat_angles, createEnvironmentFromImage
import matplotlib.pyplot as plt

class Ship:
    SONAR_ANGELS = [-90, -30, 0, 30, 90]
    SONAR_DIST = 50

    def __init__(self):
        self.__x = 50
        self.__y = 50
        self.__azimuth = np.random.randint(0, 360)
        self.__speed = 0
        self.__yaw = 0
        self.__onLand = True


    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


    @property
    def sonarAngles(self):
        return self.SONAR_ANGELS

    @property
    def position(self):
        return self.__x, self.__y

    @property
    def direction(self):
        return self.__azimuth

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @property
    def yaw(self):
        return self.__yaw

    @yaw.setter
    def yaw(self, val):
        if not self.__onLand:
            self.__azimuth = concat_angles(self.__azimuth , int(val))

    def takeOff(self):
        self.__onLand = False

    def toLand(self):
        self.__onLand = True

    def isOnLand(self):
        return self.__onLand

    def fly(self):
        if not self.__onLand:
            self.__x = int(self.__x + self.speed * math.cos(self.__azimuth * math.pi / 180) + 0.5)
            self.__y = int(self.__y + self.speed * math.sin(self.__azimuth * math.pi / 180) + 0.5)

    def draw(self, world):
        for i in range(3):
            x_ = int(self.__x + i * math.cos(concat_angles(self.__azimuth, 180) * math.pi / 180) + 0.5)
            y_ = int(self.__y + i * math.sin(concat_angles(self.__azimuth, 180) * math.pi / 180) + 0.5)
            world[x_, y_] = [10, 230, 20]
            x_ = int(self.__x + i * math.cos(concat_angles(self.__azimuth, 180) * math.pi / 180) - 0.5)
            y_ = int(self.__y + i * math.sin(concat_angles(self.__azimuth, 180) * math.pi / 180) - 0.5)
            world[x_, y_] = [10, 230, 20]
        for i in range(3, 6):
            x_ = int(self.__x + i * math.cos(concat_angles(self.__azimuth, 180) * math.pi / 180) - 0.5)
            y_ = int(self.__y + i * math.sin(concat_angles(self.__azimuth, 180) * math.pi / 180) - 0.5)
            world[x_, y_] = [200, 30, 20]
            x_ = int(self.__x + i * math.cos(concat_angles(self.__azimuth, 180) * math.pi / 180) + 0.5)
            y_ = int(self.__y + i * math.sin(concat_angles(self.__azimuth, 180) * math.pi / 180) + 0.5)
            world[x_, y_] = [200, 30, 20]


class Environment:
    ROOM = 0
    WALL = 1
    START = 2
    FINISH = 3

    COL_MAP = {
        ROOM: [255, 255, 255],
        WALL: [0, 0, 0],
        START: [30, 200, 10],
        FINISH: [200, 10, 10],
    }

    def __init__(self, file):
        self.__env = createEnvironmentFromImage(file)
        (self.__x, self.__y) = self.__env.shape
        s = Ship()
        print(s)
        self.__ship = s
        self.__done = False

    def __mat2rgb(self, mat, col_map):
        viz = np.ones((*mat.shape, 3))
        for x_ in range(self.__x):
            for y_ in range(self.__y):
                viz[x_, y_] = col_map[mat[x_, y_]]
        return viz.astype('uint8')

    def to_rgb(self):
        r = self.__mat2rgb(self.__env, Environment.COL_MAP)
        self.__ship.draw(r)
        return r

    def checkShipIsDead(self):
        x, y = self.ship.position
        return self.__env[x, y] == Environment.WALL

    def chechIsComplete(self):
        return self.__env[self.ship.x, self.ship.y] == Environment.FINISH


    def step(self, action):
        '''
        action[0] - скорость
        action[1] - рысканье
        все [0..1]
        '''

        self.ship.speed = int(action[0])
        self.ship.yaw = int(action[1])

        if action[2] >= 0.5:
            self.ship.takeOff()
        else:
            self.ship.toLand()
        self.ship.fly()

    def getSonarData(self):
        sonar_data = np.zeros(len(Ship.SONAR_ANGELS))
        for idx, sonar_angle in enumerate(Ship.SONAR_ANGELS):
            angle = concat_angles(self.ship.direction, sonar_angle)
            for i in range(Ship.SONAR_DIST):
                x, y = self.__ship.position
                x_ = int(x + i * math.cos(angle * math.pi / 180))
                y_ = int(y + i * math.sin(angle * math.pi / 180))
                sonar_data[idx] = i
                if (self.__env[x_, y_] == Environment.WALL):
                    break
        return sonar_data


    @property
    def ship(self):
        return self.__ship
