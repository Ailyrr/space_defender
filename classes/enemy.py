import arcade, math, os
from classes.utils import *

CONST = gameConstants()

class enemy(arcade.Sprite):
    def __init__(self, x_0, y_0, max_speed, hp, ulted):
        super().__init__()
        self.texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/enemy.png")
        self.orientation = 0 #Radians
        self.center_x = x_0
        self.center_y = y_0
        self.hp = hp
        self.target_x = CONST.screen_width / 2 #ORIGINAL TARGET IT BASE
        self.target_y = CONST.screen_height / 2
        self.max_speed = max_speed
        self.delta_time_sum = 0
        if ulted:
            self.ulted = True
        else:
            self.ulted = False

    def calculate_enemy_angle(self):
        #RECALCULATE ANGLE TO PLAYER
        self.orientation = math.atan2((self.target_y-self.center_y),(self.target_x-self.center_x))

    def update_target_x_y(self, x, y):
        #UPDATES THE TARGET X AND Y POSITION
        self.target_x = x
        self.target_y = y

    def update(self):
        if not self.ulted:
            self.calculate_enemy_angle()
            self.angle = self.orientation * (180/math.pi)
        #IF THE ENEMY GOES OUT OF BOUND IT DIES 
        if self.center_x == 0 or self.center_x == CONST.screen_width or self.center_y == 0 or self.center_y == CONST.screen_height:
            self.kill()