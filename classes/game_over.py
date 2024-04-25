import arcade, json
from classes.utils import *
import classes.main_menu_interface as menu

CONST = gameConstants()

#JUST DRAWS A BLACK SCREEN AND DISPLAYS THE FINAL SCORE
#LISTEN TO SPACEBAR INPUT TO GO BACK TO THE MENU
class gameover_screen(arcade.View):
    def __init__(self, screen_width, screen_height, sound, difficulty, fullscreen, player_score):
        CONST.screen_width, CONST.screen_height, CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen, CONST.player_score = screen_width, screen_height, sound, difficulty, fullscreen, player_score
        super().__init__()
        self.banner_animation_timer = 0
        self.skull_animation_timer = 0
        self.banner_texture = None
        self.skull_texture = None
        with open(os.path.dirname(__file__) + "/assets/high_scores.json", "r") as f:
            self.high_score = json.load(f)
        arcade.play_sound(CONST.game_over, volume=CONST.sound_setting, looping=False)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            menu_view = menu.homeScreen(CONST.screen_width, CONST.screen_height,CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen)
            self.window.show_view(menu_view)

    def on_draw(self):
        self.clear()
        arcade.set_background_color((0,0,0))
        text = "GAME OVER!"
        arcade.draw_text(text, 0, CONST.screen_height/2, (255,255,255), 60, align="center", width=CONST.screen_width, font_name="Kenney Mini Square")
        text = f"Your Score was: {CONST.player_score}"
        arcade.draw_text(text, 0, CONST.screen_height/2 - 40, (255,255,255), 20, align="center", width=CONST.screen_width, font_name="Kenney Mini Square")


        text = f"Your Highscore: {self.high_score['score']}"
        arcade.draw_text(text, 0, CONST.screen_height/2 - 80, (255,255,255), 20, align="center", width=CONST.screen_width, font_name="Kenney Mini Square")
        text = f"Press [SPACEBAR] to go back to the home screen"
        arcade.draw_text(text, 0, 0 + 40, (255,255,255), 10, align="center", width=CONST.screen_width, font_name="Kenney Mini Square")