import arcade, os
from classes.utils import *

CONST = gameConstants()

class base_sprite(arcade.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        CONST.screen_width = screen_width
        CONST.screen_height = screen_height
        self.timer = 0
        self.scale = 1
        self.hp = 14 #HP
        self.texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/homeship.png")
        self.center_x = CONST.screen_width/2
        self.center_y = CONST.screen_height/2
        self.angle = 0

    def update(self):
        #ANIMTATE A SLOW ROTATING BASE
        self.angle =  self.timer * 2
        if self.timer > 360:
            self.timer = 0