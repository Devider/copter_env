class Ship:
    SONAR_ANGELS = [-90, -30, 0, 30, 90]
    SONAR_DIST = 50

    def __init__(self):
        self.x = 50
        self.y = 50
        self.azimuth = np.random.randint(0, 360)
        self.speed = 0
        self.yaw = 0
        self.onLand = True

    @property
    def sonarAngles(self):
        return self.SONAR_ANGELS

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def direction(self):
        return self.azimuth

    def setSpeed(self, speed):
        self.speed = clip(speed, 1, 0) * 3
        print(self.speed)

    def setYaw(self, val):
        if not self.onLand:
            self.azimuth = self.azimuth + clip(val, 10)

    def takeOff(self):
        self.onLand = False

    def toLand(self):
        self.onLand = True

    def fly(self):
        if not self.onLand:
            self.x = int(self.x + self.speed * math.cos(self.azimuth * math.pi / 180) + 0.5)
            self.y = int(self.y + self.speed * math.sin(self.azimuth * math.pi / 180) + 0.5)

    def draw(self, world):
        for i in range(3):
            x_ = int(self.x + i * math.cos(concat_angles(self.azimuth, 180) * math.pi / 180) + 0.5)
            y_ = int(self.y + i * math.sin(concat_angles(self.azimuth, 180) * math.pi / 180) + 0.5)
            world[x_, y_] = [10, 230, 20]
            x_ = int(self.x + i * math.cos(concat_angles(self.azimuth, 180) * math.pi / 180) - 0.5)
            y_ = int(self.y + i * math.sin(concat_angles(self.azimuth, 180) * math.pi / 180) - 0.5)
            world[x_, y_] = [10, 230, 20]
        for i in range(3, 6):
            x_ = int(self.x + i * math.cos(concat_angles(self.azimuth, 180) * math.pi / 180) - 0.5)
            y_ = int(self.y + i * math.sin(concat_angles(self.azimuth, 180) * math.pi / 180) - 0.5)
            world[x_, y_] = [200, 30, 20]
            x_ = int(self.x + i * math.cos(concat_angles(self.azimuth, 180) * math.pi / 180) + 0.5)
            y_ = int(self.y + i * math.sin(concat_angles(self.azimuth, 180) * math.pi / 180) + 0.5)
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
        self.env = createEnvironmentFromImage(file)
        (self.x, self.y) = self.env.shape
        self.ship = Ship()
        self.done = False

    def __mat2rgb(self, mat, col_map):
        viz = np.ones((*mat.shape, 3))
        for x_ in range(self.x):
            for y_ in range(self.y):
                viz[x_, y_] = col_map[mat[x_, y_]]
        return viz

    def draw(self):
        r = self.__mat2rgb(self.env, Environment.COL_MAP)
        self.ship.draw(r)
        plt.imshow(r / 255)

    def checkShip(self):
        if self.env[self.ship.x, self.ship.y] == Environment.WALL:
            self.done = True

    def step(self, action):
        '''
        action[0] - тангаж
        action[1] - крен
        action[2] - скорость
        все [0..1]
        '''
        self.ship.setSpeed(10)
        self.ship.setYaw(0)
        self.ship.fly()
        self.checkShip()

    def getSonarData(self):
        sonar_data = np.zeros(len(Ship.SONAR_ANGELS))
        for idx, sonar_angle in enumerate(Ship.SONAR_ANGELS):
            angle = concat_angles(self.ship.direction, sonar_angle)
            for i in range(Ship.SONAR_DIST):
                x, y = self.ship.position
                x_ = int(x + i * math.cos(angle * math.pi / 180))
                y_ = int(y + i * math.sin(angle * math.pi / 180))
                #                 print(self.ship.direction, sonar_angle, angle, x, y, x_, y_)
                if (self.env[x_, y_] == Environment.WALL):
                    continue
                sonar_data[idx] = i
        return sonar_data