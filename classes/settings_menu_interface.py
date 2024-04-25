import arcade, os, math
from classes.utils import *
import classes.main_menu_interface as main_menu_interface

CONST = gameConstants()

class settingsScreen(arcade.View):
    def __init__(self, screen_width, screen_height, sound, difficulty, fullscreen):
        CONST.screen_width, CONST.screen_height,CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen = screen_width, screen_height, sound, difficulty, fullscreen
        super().__init__()
        self.BG = arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/background.png")
        self.selected_btn = 2 #Selected btn per default
        self.scaling = .75 #Scaling of the interface size
        #THE TEXTURE LISTS REPRESENT THE PROGRESSION OF EACH BUTTON AS IT'S VALUE CHANGES, THE VALUE IS THEN THE index(VALUE) for the texture
        self.sound_slider = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_0.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_3.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_4.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_5.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_6.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_7.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_8.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/slider_9.png"),
        ]
        self.muted_icon = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/unmuted_icon.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/sound_levels/muted_icon.png"),
        ]
        self.difficulty_buttons = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/difficulty_selector/peaceful.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/difficulty_selector/easy.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/difficulty_selector/medium.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/difficulty_selector/hard.png")
        ]
        self.fullscreen_buttons = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/fullscreen_settings/off.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/fullscreen_settings/on.png"),
        ]
        self.fullscreen_button_selector = arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/fullscreen_settings/btn.png")
        self.difficulty_button_selector = arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/difficulty_selector/difficulty_btn.png")
        self.pointer = arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/menu_selector.png")
        if CONST.sound_setting == 0:
            self.muted = True
        else:
            self.muted = False
        if CONST.fullscreen == 0:
            self.fullscreen = 0
        else:
            self.fullscreen = 1
        self.layer_offsets = [-150 *self.scaling ,0,150 *self.scaling]
        self.selected_sound_level = CONST.sound_setting
        self.selected_difficulty = CONST.difficulty_setting

    def on_key_press(self, symbol: int, modifiers: int):
        #LEFT OR RIGHT CHANGES THE VALUE OF THE SELECTED BUTTON
        if symbol == arcade.key.LEFT:
            if self.selected_btn == 2:
                self.selected_sound_level -= 0.1
                if self.selected_sound_level < 0:
                    self.selected_sound_level = 0
            elif self.selected_btn == 1:
                self.selected_difficulty -=1
                if self.selected_difficulty < 0:
                    self.selected_difficulty = 3
            elif self.selected_btn == 0:
                if self.fullscreen == 0:
                    self.fullscreen += 1
                    if self.fullscreen > 1:
                        self.fullscreen = 1
                elif self.fullscreen == 1:
                    self.fullscreen -= 1

        if symbol == arcade.key.RIGHT:
            if self.selected_btn == 2:
                self.selected_sound_level += 0.1
                if self.selected_sound_level > 0.9:
                    self.selected_sound_level = 0.9
            elif self.selected_btn == 1:
                self.selected_difficulty += 1
                if self.selected_difficulty > 3:
                    self.selected_difficulty = 0
            elif self.selected_btn == 0:
                if self.fullscreen == 0:
                    self.fullscreen += 1
                    if self.fullscreen > 1:
                        self.fullscreen = 1
                elif self.fullscreen == 1:
                    self.fullscreen -= 1
        #UP AND DOWN CHANGES THE SELECTED BUTTON
        if symbol == arcade.key.DOWN:
            arcade.play_sound(CONST.select_sound, looping=False, volume=CONST.sound_setting)
            self.selected_btn -= 1
            if self.selected_btn < 0:
                self.selected_btn = 0
        
        if symbol == arcade.key.UP:
            arcade.play_sound(CONST.select_sound, looping=False, volume=CONST.sound_setting)
            self.selected_btn += 1
            if self.selected_btn > 2:
                self.selected_btn = 2

        if symbol == arcade.key.ENTER:
            if self.muted:
                sound_set = 0
            else:
                sound_set = self.selected_sound_level + (1/10)

            if self.fullscreen != CONST.fullscreen:
                self.window.set_fullscreen(not self.window.fullscreen)
                CONST.screen_width, CONST.screen_height = self.window.get_size()
                self.window.set_viewport(0, CONST.screen_width, 0, CONST.screen_height)
            
            menu_view = main_menu_interface.homeScreen(CONST.screen_width, CONST.screen_height,sound_set, self.selected_difficulty, self.fullscreen)
            self.window.show_view(menu_view)

        if symbol == arcade.key.M:
            if self.muted == False and self.selected_btn == 2:
                self.muted = True
            else:
                self.muted = False

    def on_draw(self):
        self.clear()
        #DRAW EACH BUTTON ACCRODDING TO IT'S POSITION AND SCALING
        arcade.set_background_color((0,0,0))
        arcade.draw_lrwh_rectangle_textured(0,0,CONST.screen_width,CONST.screen_height, self.BG, 0, 120)

        arcade.draw_rectangle_filled(CONST.screen_width/2, CONST.screen_height/2, 1400 * self.scaling, 600 *self.scaling, (0,0,0,140))
        arcade.draw_text("Settings Menu", 0, CONST.screen_height - 200, (255,255,255), 40, font_name="Kenney Mini Square", align="center", width=CONST.screen_width)
        #SOUND SETTINGS
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2, CONST.screen_height/2 + 150*self.scaling , self.sound_slider[int(self.selected_sound_level*10)],1*self.scaling)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2 - 500*self.scaling, CONST.screen_height/2 + 150*self.scaling, self.muted_icon[self.muted],.5*self.scaling)
        if self.muted:
            sound_level = f"{0}"
        else:
            sound_level = f"{math.ceil((self.selected_sound_level) * 10 + 1)}"
        arcade.draw_text(sound_level, CONST.screen_width / 2 + 500*self.scaling, CONST.screen_height / 2 + 135*self.scaling, (255,255,255), 30 *self.scaling,font_name="Kenney Mini Square")
        #DIFFICULTY SETTINGS
        arcade.draw_scaled_texture_rectangle(CONST.screen_width /2 - 375*self.scaling, CONST.screen_height/2, self.difficulty_button_selector, .5*self.scaling)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width /2 , CONST.screen_height/2, self.difficulty_buttons[self.selected_difficulty], .5*self.scaling)
        #FULLSCREEN SETTINGS
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2 - 375*self.scaling, CONST.screen_height/2 - 150*self.scaling, self.fullscreen_button_selector, .5*self.scaling)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2, CONST.screen_height/2 - 150*self.scaling, self.fullscreen_buttons[self.fullscreen], .5*self.scaling)
        #POINTER
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2 - 650*self.scaling, CONST.screen_height/2 + self.layer_offsets[self.selected_btn], self.pointer, 0.30*self.scaling)
        
        
        #CONTROL TIPS
        text = "Use                    to select and                    to validate"
        arcade.draw_text(text, CONST.screen_width/2 - 300*self.scaling, CONST.screen_height/2 - 370*self.scaling, arcade.color.WHITE, 20*self.scaling, font_name="Kenney Mini Square")
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2 - 190*self.scaling, CONST.screen_height/2 - 360*self.scaling, arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/key_icons/arrows.png"),.25*self.scaling)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2 + 125*self.scaling, CONST.screen_height/2 - 360*self.scaling, arcade.load_texture(os.path.dirname(__file__) + "/assets/menu_textures/key_icons/enter.png"),.25*self.scaling)
