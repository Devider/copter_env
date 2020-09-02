import math
import matplotlib.pyplot as plt
import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)
import turtle


def clip(v, v_max, v_min=0):
    return max(min(v, v_max), v_min)


def concat_angles(angle1, angle2):
    return (angle1 + angle2) % 360;


def distance(x1, y1, x2, y2):
    deltaX = x1 - x2
    deltaY = y1 - y2
    return math.sqrt(math.pow(deltaX, 2) + Math.pow(deltaY, 2));


def getDistance(environement, x, y, directionAngle):
    MAX_LENGHT = 70;
    SENSOR_RAY_HALF_ANGLE = 15;

    direction = concat_angles(angle, directionAngle);
    for i in range(1, MAX_LENGHT):
        x_ = x + i * math.cos(direction * Math.PI / 180);
        y_ = y + i * math.sin(direction * Math.PI / 180);
        if (environement[x_, y_] == FieldType.WALL):
            return distance(x_, y_, x, y);
    return MAX_LENGHT


def createEnvironmentFromImage(file):
    im = plt.imread(file)
    x, y, _ = im.shape

    env = np.zeros((x, y))
    for x_ in range(x):
        for y_ in range(y):
            env[x_, y_] = 0 if im[x_, y_, :].mean() > 30 else 1

    env[20:80, 20:80] = 2
    env[(x - 80):(x - 20), (y - 80):(y - 20)] = 3
    return env