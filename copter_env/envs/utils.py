import math
import matplotlib.pyplot as plt
import numpy as np


def clip(v, v_max, v_min=0):
    return max(min(v, v_max), v_min)


def concat_angles(angle1, angle2):
    return (angle1 + angle2) % 360;


def distance(x1, y1, x2, y2):
    deltaX = x1 - x2
    deltaY = y1 - y2
    return math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2));

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