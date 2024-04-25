import arcade, arcade.gui, os
from classes.utils import *

CONST = gameConstants()

class OOB_marker(arcade.Sprite):
    def __init__(self, x_pos, y_pos, screen_width, screen_height):
        super().__init__()
        CONST.screen_width, CONST.screen_height = screen_width, screen_height
        self.textures = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_up.png"),             #0
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_top_right.png"),      #1
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_right.png"),          #2
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_bottom_right.png"),   #3
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_down.png"),           #4
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_bottom_left.png"),    #5
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_left.png"),           #6
            arcade.load_texture(os.path.dirname(__file__) + "/assets/player_oob_marker/alert_top_left.png"),       #7
        ] #TEXTURE LIST
        self.texture = self.textures[1]
        self.center_x = x_pos
        self.center_y = y_pos

        self.player_position = [0,0]

    def update(self):
        #CHECK FOR OUT OF BOUNDS
        #CHECK FOR THE PLAYER POSITION AND DRAW THE ACCORD MARKER 
        #IF PLAYER OUT left OR OUT right
        #IF PLAYER OUT bottom OR OUT top
        if self.player_position[0] < 0:
            if self.player_position[1] < 0:
                #Bottom Left
                self.texture = self.textures[5]
                self.center_x = 60
                self.center_y = 60
                pass
            elif self.player_position[1] > CONST.screen_height:
                #Top left
                self.texture = self.textures[7]
                self.center_x =60
                self.center_y = CONST.screen_height - 60
                pass
            else:
                self.texture = self.textures[6]
                self.center_x = 60
                self.center_y = self.player_position[1]
                pass
        elif self.player_position[0] > CONST.screen_width:
            if self.player_position[1] < 0:
                #Bottom Right
                self.texture = self.textures[3]
                self.center_x = CONST.screen_width - 60
                self.center_y = 60
                pass
            elif self.player_position[1] > CONST.screen_height:
                #Top Right
                self.texture = self.textures[1]
                self.center_x = CONST.screen_width - 60
                self.center_y = CONST.screen_height - 60
                pass
            else:
                #Right
                self.texture = self.textures[2]
                self.center_x = CONST.screen_width - 60
                self.center_y = self.player_position[1]
                pass
        elif self.player_position[1] < 0:
            if self.player_position[0] < 0:
                #bottom left
                self.texture = self.textures[5]
                self.center_x = 60
                self.center_y = 60
                pass
            elif self.player_position[0] > CONST.screen_width:
                #bottom right
                self.texture = self.textures[3]
                self.texture = self.textures[3]
                self.center_x = CONST.screen_width - 60
                pass
            else:
                #bottom
                self.texture = self.textures[4]
                self.center_x = self.player_position[0]
                self.center_y = 60
                pass
        elif self.player_position[1] > CONST.screen_height:
            if self.player_position[0] < 0:
                #Top Left
                self.texture = self.textures[7]
                self.center_x = 60
                self.center_y = CONST.screen_height - 60
                pass
            elif self.player_position[0] > CONST.screen_width:
                #Top Right
                self.texture = self.textures[1]
                self.center_x = CONST.screen_width - 60
                self.center_y = CONST.screen_height - 60 
                pass
            else:
                #TOP
                self.texture = self.textures[0]
                self.center_x = self.player_position[0]
                self.center_y = CONST.screen_height - 60
                pass
        else:
            #PLAYER IS ON SCREEN -> Hide Icon out of sight
            self.center_x = - 400
            self.center_y = -400
            pass
