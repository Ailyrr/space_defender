import arcade, arcade.gui, os
from classes.game import GameView
from classes.utils import *
from classes.settings_menu_interface import *

#Init Consts
CONST = gameConstants()

class homeScreen(arcade.View):
    def __init__(self, width, height, volume, difficulty, fullscreen):
        CONST.screen_width, CONST.screen_height, CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen = width, height, volume, difficulty, fullscreen
        super().__init__()
        self.BG = arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/background.png")
        self.selected_btn = 0
        self.scaling = 1
        if CONST.fullscreen == 0:
            self.scaling = 0.7
        self.button_index = [1,0,0]
        self.btns = [
            [arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/main_menu/play_btn.png"), arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/main_menu/play_btn_selected.png")],
            [arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/main_menu/set_btn.png"), arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/main_menu/set_btn_selected.png")],
            [arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/main_menu/quit_btn.png"), arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/main_menu/quit_btn_selected.png")]
        ] #BUTTONS
        self.title_screen_title = arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/main_menu/home_screen_title.png")
        self.music = CONST.title_theme
        self.validate_sound = CONST.validate_sound
        self.now_playing = arcade.play_sound(self.music, looping=True, volume=CONST.sound_setting)
        self.muted = False

    def update_selected_btn(self, direction):
        #IF KEY PRESS UP CHANGE SELECTED BUTTON, SME FOR DOWJN
        if direction == 'up':
            self.button_index = [0,0,0]
            self.selected_btn += 1
            if self.selected_btn > 2:
                self.selected_btn = 0
            self.button_index[self.selected_btn] = 1
        elif direction == 'down':
            self.button_index = [0,0,0]
            self.selected_btn -= 1
            if self.selected_btn < 0:
                self.selected_btn = 2
            self.button_index[self.selected_btn] = 1
    

    def draw_buttons(self):
        #DRAW THE THREE BUTTONS WITH THE y OFFSET
        offset = [40, -100, -240]
        for i in range(3):
            if self.button_index[i] == 1:
                arcade.draw_scaled_texture_rectangle(CONST.screen_width/2, CONST.screen_height/2 + offset[i] * self.scaling, self.btns[i][1],1 * self.scaling) #310/140
            else:
                arcade.draw_scaled_texture_rectangle(CONST.screen_width/2, CONST.screen_height/2 + offset[i] * self.scaling, self.btns[i][0],1 * self.scaling) #310/140

    def draw_title_screen(self):
        #DRAW THE GAME TITLE
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2, CONST.screen_height/2 + 200, self.title_screen_title, 1.4)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            arcade.play_sound(CONST.select_sound, looping=False, volume=CONST.sound_setting)
            self.update_selected_btn('down')
        elif symbol == arcade.key.DOWN:
            arcade.play_sound(CONST.select_sound, looping=False, volume=CONST.sound_setting)
            self.update_selected_btn('up')
        #USER ENTER KEY FOR EITHER QUITTING THE GAME
        #OR GO TO THE SETTINGS MENU
        #OR LAUNCHING A GAME SETTING
        if symbol == arcade.key.ENTER:
            if self.selected_btn == 0:
                arcade.play_sound(self.validate_sound, looping=False, volume=CONST.sound_setting)
                arcade.stop_sound(self.now_playing)
                game_view = GameView(CONST.screen_width, CONST.screen_height, CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen) #NEW VIEW CLASS
                game_view.setup()
                self.window.show_view(game_view)
            elif self.selected_btn == 1:
                arcade.stop_sound(self.now_playing)
                settings_view = settingsScreen(CONST.screen_width, CONST.screen_height, CONST.sound_setting , CONST.difficulty_setting, CONST.fullscreen)
                self.window.show_view(settings_view)
            elif self.selected_btn == 2:
                arcade.close_window()
        
    def on_draw(self):
        self.clear()
        arcade.set_background_color((0,0,0))
        arcade.draw_lrwh_rectangle_textured(0, 0, CONST.screen_width, CONST.screen_height, self.BG, 0, 120)
        self.draw_title_screen()
        self.draw_buttons()
        #DRAW THE TIPS UNDER 
        text = "Use                    to select and                    to validate"
        arcade.draw_text(text, CONST.screen_width/2 - 300 * self.scaling, CONST.screen_height/2 - 370 * self.scaling, arcade.color.WHITE, 20 * self.scaling, font_name="Kenney Mini Square")
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2 - 190 * self.scaling, CONST.screen_height/2 - 360 * self.scaling, arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/key_icons/arrows.png"),.25 * self.scaling)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2 + 125 * self.scaling, CONST.screen_height/2 - 360 * self.scaling, arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/key_icons/enter.png"),.25 * self.scaling)
