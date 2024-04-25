import arcade, math, os
from classes.utils import *

CONST = gameConstants()

#ALLOWS THE PLAYER TO SHOOT A LASER
class laser(arcade.Sprite):
    def __init__(self, x_pos, y_pos, orientation, shot_type):
        super().__init__()
        self.fuse = 0
        self.timer = 0
        self.type = 1 # = Laser Type
        self.center_x = x_pos
        self.center_y = y_pos
        self.theta = orientation
        self.texture_list = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/laser/greenlaser.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/laser/redlaser.png")
        ] #CHANGE COLOR DEFENDING IF THE PLAYER OR ENEMY SHOOTS IT
        self.texture = self.texture_list[shot_type]

        #ONLY USED FOR ENEMY SHOT
    def update(self):
        self.angle = self.theta * (180/math.pi)
        #MOVE ACCORDINTG TO SIN AND COS OF THE ANGLE
        self.center_x += CONST.bullet_travel_time * math.cos(self.theta)
        self.center_y += CONST.bullet_travel_time * math.sin(self.theta)
        if self.timer >= 15:
            self.kill()
#ALLOWS THE PLAYER TO SHOOT A MISSILE TAHT DOES 3x THE DAMAGE OF LASERS
class missile(arcade.Sprite):
    def __init__(self, x_pos, y_pos, orientation, targets):
        super().__init__()
        self.target_list = targets
        self.timer = 0
        self.fuse = 0
        self.type = 2 # = Missile Type
        self.explosion_timer = 0
        self.center_x = x_pos
        self.center_y = y_pos
        self.orientation = orientation
        self.angle = self.orientation * (180/math.pi)
        self.texture_list = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/missile/missile_frame_static.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/missile/missile_frame_1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/missile/missile_frame_2.png"),
        ]
        self.texture = self.texture_list[0]
        self.targets = arcade.get_closest_sprite(self, self.target_list)
        self.change_x = 2 * math.cos(self.orientation)
        self.change_y = 2 * math.sin(self.orientation)
        self.target_x = self.targets[0].center_x
        self.target_y = self.targets[0].center_y

    def calculate_angle(self):
        #RECALC ORIENTATION
        self.orientation = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)

    def update(self):
        self.targets = arcade.get_closest_sprite(self, self.target_list)
        #IF NO TARGETS ARE LEFT-> DESTROY ITSELF
        if not self.targets:
            self.kill()
        else:
            try:
                #GET THE FIRST (CLOSEST) TARGET
                self.target_x = self.targets[0].center_x
                self.target_y = self.targets[0].center_y 
            except:
                self.kill()
            #FIRST MOVE IN SAME DIRECTION AS PLAYER
        if self.timer < 1.5 and self.fuse < 15:
            self.center_x += self.change_x
            self.center_y += self.change_y
        elif self.timer >= 1.5 and self.fuse < 15:
            #ANIMATE THE "BOOSTER IGNITION"
            if self.timer >=1.5 and self.timer < 2:
                self.texture = self.texture_list[1]
            elif self.timer >= 2 and self.timer < 2.5:
                self.texture = self.texture_list[2]
            elif self.timer >= 2.5:
                self.timer = 1.5
            try:
                self.target_x = self.targets[0].center_x
                self.target_y = self.targets[0].center_y
            except:
                pass
            #RECALC ANGLE CONSTANTLY
            self.calculate_angle()
            self.angle = self.orientation * (180/math.pi)
            self.change_x = 6 * math.cos(self.orientation)
            self.change_y = 6 * math.sin(self.orientation)  
        
            self.center_x += self.change_x
            self.center_y += self.change_y
        if self.fuse  >= 14:
            #IF TO LONG WITHOUT A TARGET -> SELF DESTRUCT
            self.kill()
        if self.center_x == self.target_x and self.center_y == self.target_y:
            #IF OUT OF BOUNDS -> KLL
            self.kill()
#ALLOWS THE PLAYER TO DEPLOY A SHIELD THAT PREVENTS HIM FROM TAKING DAMAGE
class shield(arcade.Sprite):
    def __init__(self, player_x_pos, player_y_pos, time):
        super().__init__()
        self.player_x_pos = player_x_pos
        self.player_y_pos = player_y_pos
        self.center_x = self.player_x_pos
        self.center_y = self.player_y_pos
        self.animation_timer = 0
        self.max_time = time
        self.timer = 0
        self.frames = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/force_field/shield_frame_1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/force_field/shield_frame_2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/force_field/shield_frame_3.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/force_field/shield_frame_4.png")
        ]
        self.texture = self.frames[0]
        self.scale = .8

    def update(self):
        self.center_x = self.player_x_pos
        self.center_y = self.player_y_pos
        #ANIMTATE THE SHIELD ACCORDING TO ANIMATION TIMER
        if self.animation_timer >= 0 and self.animation_timer < .125:
            self.texture = self.frames[0]
        elif self.animation_timer >= .125 and self.animation_timer < .25:
            self.texture = self.frames[1]
        elif self.animation_timer >= .25 and self.animation_timer < .375:
            self.texture = self.frames[2]
        elif self.animation_timer >= .375 and self.animation_timer < .5:
            self.texture = self.frames[3]
        else:
            self.animation_timer = 0
        
        if self.timer >= self.max_time:
            self.kill()

class heal_bonus(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.type = "heal"
        self.center_x = x
        self.center_y = y
        self.y_offset = 0
        self.scale = 1.4
        self.frames = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/heal_bonus/heal_bonus_1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/heal_bonus/heal_bonus_2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/heal_bonus/heal_bonus_3.png")
        ]
        self.sin_wave = [
            math.sin(0),
            math.sin(math.pi/6),
            math.sin(math.pi/3),
            math.sin(math.pi/2),
            math.sin(2 *math.pi / 3),
            math.sin(5* math.pi/6),
            math.sin(math.pi),
            math.sin(7 * math.pi / 6),
            math.sin(4 * math.pi / 3),
            math.sin(3*math.pi/2),
            math.sin(3*math.pi/2),
            math.sin(5*math.pi/3),
            math.sin(11*math.pi/6),
        ] #SINE WAVE TO HAVE A HOVER ANIMATION TO THE SPRITE
        self.texture = self.frames[0]
        self.timer = 0
        self.lifetime = 12

    def update(self) -> None:
        if self.lifetime <= 0:
            self.kill()
        #ANIMTATE TEXTURE
        if self.timer < .25:
            self.texture = self.frames[0]
        elif self.timer >= .25 and self.timer <.5:
            self.texture = self.frames[1]
        elif self.timer >= .5 and self.timer < .75:
            self.texture = self.frames[2]
        elif self.timer >= .75 and self.timer < 1:
            self.texture = self.frames[1]
        elif self.timer >= 1 and self.timer < 1.25:
            self.texture = self.frames[0]
        else:
            self.timer = 0
        #ANIMTATE SINE WAVE
        if self.timer < .1:
            self.y_offset = self.sin_wave[0]
        elif self.timer >= .1 and self.timer < .2:
            self.y_offset = self.sin_wave[1]
        elif self.timer >= .2 and self.timer < .3:
            self.y_offset = self.sin_wave[2]
        elif self.timer >= .3 and self.timer < .4:
            self.y_offset = self.sin_wave[3]
        elif self.timer >= .4 and self.timer < .5:
            self.y_offset = self.sin_wave[4]
        elif self.timer >= .5 and self.timer < .6:
            self.y_offset = self.sin_wave[5]
        elif self.timer >= .6 and self.timer < .7:
            self.y_offset = self.sin_wave[6]
        elif self.timer >= .7 and self.timer < .8:
            self.y_offset = self.sin_wave[7]
        elif self.timer >= .8 and self.timer < .9:
            self.y_offset = self.sin_wave[8]
        elif self.timer >= .9 and self.timer < 1:
            self.y_offset = self.sin_wave[9]
        elif self.timer >= 1 and self.timer < 1.1:
            self.y_offset = self.sin_wave[10]
        elif self.timer >= 1.1 and self.timer < 1.2:
            self.y_offset = self.sin_wave[11]

        self.center_y = self.center_y + self.y_offset / 4
        
class ammo_bonus(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.type = "ammo"
        self.center_x = x
        self.center_y = y
        self.y_offset = 0
        self.scale = 1

        self.sin_wave = [
            math.sin(0),
            math.sin(math.pi/6),
            math.sin(math.pi/3),
            math.sin(math.pi/2),
            math.sin(2 *math.pi / 3),
            math.sin(5* math.pi/6),
            math.sin(math.pi),
            math.sin(7 * math.pi / 6),
            math.sin(4 * math.pi / 3),
            math.sin(3*math.pi/2),
            math.sin(3*math.pi/2),
            math.sin(5*math.pi/3),
            math.sin(11*math.pi/6),
        ]
        self.texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/ammo_bonus/ammo_bonus.png")
        self.timer = 0
        self.lifetime = 12

    def update(self) -> None:
        if self.lifetime <= 0:
            self.kill()
        
        #ANIMTATE SINE WAVE
        if self.timer < .1:
            self.y_offset = self.sin_wave[0]
        elif self.timer >= .1 and self.timer < .2:
            self.y_offset = self.sin_wave[1]
        elif self.timer >= .2 and self.timer < .3:
            self.y_offset = self.sin_wave[2]
        elif self.timer >= .3 and self.timer < .4:
            self.y_offset = self.sin_wave[3]
        elif self.timer >= .4 and self.timer < .5:
            self.y_offset = self.sin_wave[4]
        elif self.timer >= .5 and self.timer < .6:
            self.y_offset = self.sin_wave[5]
        elif self.timer >= .6 and self.timer < .7:
            self.y_offset = self.sin_wave[6]
        elif self.timer >= .7 and self.timer < .8:
            self.y_offset = self.sin_wave[7]
        elif self.timer >= .8 and self.timer < .9:
            self.y_offset = self.sin_wave[8]
        elif self.timer >= .9 and self.timer < 1:
            self.y_offset = self.sin_wave[9]
        elif self.timer >= 1 and self.timer < 1.1:
            self.y_offset = self.sin_wave[10]
        elif self.timer >= 1.1 and self.timer < 1.2:
            self.y_offset = self.sin_wave[11]
        else:
            self.timer = 0

        self.center_y = self.center_y + self.y_offset / 4
        
class base_shield(arcade.Sprite):
    def __init__(self, x, y, bullet_x, bullet_y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.angle = math.atan2(bullet_y - y, bullet_x - x) * 180/math.pi
        self.animation_timer = 0
        self.timer = 0
        self.frames = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_3.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_4.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_5.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_6.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_7.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_8.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_9.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_10.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_11.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/upgrades/base_shield/shield_12.png")
        ]
        self.texture = self.frames[0]

    def update(self):
        #ANIMATE TEXTURE, THEN SELF DESTRUCT (ONLY ESTHETIC PURPOSE)
        if self.animation_timer < 0.1:
            self.texture = self.frames[0]
        elif self.animation_timer >= 0.1 and self.animation_timer < .2:
            self.texture = self.frames[1]
        elif self.animation_timer >= 0.2 and self.animation_timer < .3:
            self.texture = self.frames[2]
        elif self.animation_timer >= 0.3 and self.animation_timer < .4:
            self.texture = self.frames[3]
        elif self.animation_timer >= 0.4 and self.animation_timer < .5:
            self.texture = self.frames[4]
        elif self.animation_timer >= 0.5 and self.animation_timer < .6:
            self.texture = self.frames[5]
        elif self.animation_timer >= 0.6 and self.animation_timer < .7:
            self.texture = self.frames[6]
        elif self.animation_timer >= 0.7 and self.animation_timer < .8:
            self.texture = self.frames[7]
        elif self.animation_timer >= 0.8 and self.animation_timer < .9:
            self.texture = self.frames[8]
        elif self.animation_timer >= 0.9 and self.animation_timer < 1:
            self.texture = self.frames[9]
        elif self.animation_timer >= 1 and self.animation_timer < 1.1:
            self.texture = self.frames[10]
        elif self.animation_timer >= 1.1 and self.animation_timer < 1.2:
            self.texture = self.frames[11]
        else:
            self.kill()

class lockdown(arcade.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.center_x = x_pos
        self.center_y = y_pos
        self.targets = None
        self.scale = 1
        self.frames = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/lockdown/lockdown_charge.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/weapons/lockdown/lockdown_on.png"),
        ] #TEXTURES
        self.charge = 0
        self.texture = self.frames[0]
        #NO LOGIC CODE (ONLY ESTHETIC POURPOSe)
    def update(self, delta_time: float = 1 / 60) -> None:
        #CHANGE TEXTURE ACCORDING TO TIMER 
        if self.charge >= 10:
            self.texture = self.frames[1]
        if  self.charge >= 25:
            self.kill()