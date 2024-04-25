import arcade, math, os
from classes.utils import *

#GAME CONSTANTS
CONST = gameConstants()

class player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        #Setup Initial Position && load texture
        self._hit_box_algorithm = "Simple"
        self.player_textures = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player/player_frame_static.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player/player_frame_1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player/player_frame_2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player/player_frame_1_back.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player/player_frame_2_back.png"),
        ] #TEXURE LIST TO ANIMATE IT
        self.hp = 14
        self.selected_weapon = 0 #DEFINES IF IT SHOOTS LASER OR MISSILES
        self.texture = self.player_textures[0]
        self.center_x = CONST.screen_width/2 - 250   #ORIGINAL POSITION
        self.center_y = CONST.screen_height/2
        #Define Player Orientation angle [Radians] && Mouse X for calculating aTan()
        self.player_orientation = 90 * (math.pi / 180)
        self.mouse_x = 0
        self.mouse_y = 0

        self.scale = .9

        #AMOUNTS
        self.shots_left = 100 #AMMO LEFT
        self.missiles_left = 10

        self.animation_timer = 0 #ANIMATION TIMER

        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False

    def calculate_player_angle(self):
        #RECALC ANGLE TOWARDS MOUSE POSITION
        self.player_orientation = math.atan2(self.mouse_y - self.center_y, self.mouse_x - self.center_x)


    def update(self):
        #PREVENT THE HP TO GET OUT OF INDEX DEFINED INTERVAL
        if self.hp <= 0:
            self.hp = 0
        elif self.hp > 14:
            self.hp = 14

        self.calculate_player_angle()
        self.angle = self.player_orientation * (180/ math.pi)
        #CHANGE ANIMATION TIMER ACCORDING TO FORWARD OR BACKWARD MOTION
        if self.w_pressed == True:
            if self.animation_timer > 0 and self.animation_timer <= 0.25:
                self.texture = self.player_textures[1]
            elif self.animation_timer > 0.25 and self.animation_timer <= 0.5:
                self.texture = self.player_textures[2]
            elif self.animation_timer > 0.5:
                self.animation_timer = 0
        elif self.s_pressed == True:
            if self.animation_timer > 0 and self.animation_timer <= 0.25:
                self.texture = self.player_textures[3]
            elif self.animation_timer > 0.25 and self.animation_timer <= 0.5:
                self.texture = self.player_textures[4]
            elif self.animation_timer > 0.5:
                self.animation_timer = 0
        else:
            self.texture = self.player_textures[0]