import arcade

from classes.main_menu_interface import *
from classes.utils import *

CONST = gameConstants()     #GET ESSENTIAL GAME CONSTANTS

#THIS THE THE SHORT SPLASHSCREEN WE SEE AT THE BEGINNING OF THE GAME
class splashScreen(arcade.View):
    def __init__(self, width, height, volume, difficulty, fullscreen):
        CONST.screen_width, CONST.screen_height, CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen = width, height, volume , difficulty, fullscreen
        super().__init__()
        self.timer = 4
        self.alpha_channel = 255

    #Update the alpha channel of the text according to the timer value, then  load game interface
    def on_update(self, delta_time: float):
        self.timer -= delta_time
        if self.timer <= 1:
            self.alpha_channel -= 5
            if self.alpha_channel <= 0:
                self.alpha_channel = 0
        if self.timer <= 0:
            home_view = homeScreen(CONST.screen_width, CONST.screen_height, CONST.sound_setting, 2, False)
            self.window.show_view(home_view)

    def on_key_press(self, symbol: int, modifiers: int):
        #Skip spalshcreen with space
        if symbol == arcade.key.SPACE:
            self.timer = 0
        
    def on_draw(self):
        #Draw text with greeting text and version info
        self.clear()
        arcade.set_background_color((0,0,0))
        splash_text = "Forward Production Presents:"
        version = "1.0 Release"
        arcade.draw_text(splash_text, 0, CONST.screen_height/2 - 15, (255,255,255, self.alpha_channel), 30, font_name="Kenney Mini Square", align="center", width=CONST.screen_width)
        arcade.draw_text(version, 0, 20 -5, (255,255,255, self.alpha_channel), 10,  align="center", width=CONST.screen_width)