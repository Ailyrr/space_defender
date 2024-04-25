from dataclasses import dataclass
import arcade, os
#########################################################################################
#   THIS CLASS STORES ALL OF THE IMPORTANT CONSTANTS AND SOME TEXTURE AND AUDIO ON IT   #
#   THIS BEING A DATACLASSE, IT HAS NOT METHODS JUST VALUES                             #
#   MOST IMPORT ONES ARE SCREEN_WIDTH AND SCREEN_HEIGHT                                 #
#########################################################################################

@dataclass
class gameConstants:
    def __init__(self, width=1280, height=720, title="SpaceDefender V.0.9.5"):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title
        self.SPRITE_IMAGE_SIZE = 64
        self.SPRITE_SCALING_PLAYER = 0.5
        self.SPRITE_SCALING_TILES = 0.5
        self.SPRITE_SIZE = int(self.SPRITE_IMAGE_SIZE * self.SPRITE_SCALING_PLAYER)

        #Physics Engine CONSTS
        self.GRAVITY = 0
        self.DEFAULT_DAMPING = 0.5
        self.PLAYER_DAMPING = 0.7

        self.PLAYER_FRICTION = 1.0
        self.WALL_FRICTION = 0.9
        self.DYNAMIC_ITEM_FRICTION = 0.6

        self.PLAYER_MASS = 1.6

        self.PLAYER_MAX_HORIZONTAL_SPEED = 450
        self.PLAYER_MAX_VERTICAL_SPEED = 450

        #Global Textures
        self.healthbar_textures = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_0.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_10.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_20.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_30.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_40.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_50.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_60.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_70.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_80.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_90.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/enemy_healthbar/hb_100.png")
        ]
        self.player_healthbar = [                                                           #MAX INDEX = 14
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar_empty.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar13.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar12.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar11.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar10.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar9.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar8.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar7.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar6.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar5.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar4.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar3.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/player_healthbar/healthbar_full.png"),
        ]
        self.base_healthbar = [                                                           #MAX INDEX = 14
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar_empty.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar13.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar12.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar11.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar10.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar9.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar8.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar7.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar6.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar5.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar4.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar3.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/healthbar/base_healthbar/healthbar_full.png"),
        ]
        #SOUND EFFECTS
        self.title_theme = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/music/SpaceDefenderHomescreenTheme.wav")
        self.validate_sound = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/fx/game_start.wav")
        self.laser_sound = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/fx/laser.wav")
        self.select_sound = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/fx/button_select.wav")
        self.laser_hit = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/fx/laser_hit.wav")
        self.laser_hit = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/fx/laser_hit.wav")
        self.game_over = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/music/game_over.wav")
        #GAME STATS$
        self.sound_setting = 1
        self.difficulty_setting = 2
        self.enemy_wave_number = 1
        self.fullscreen = 0

        self.bullet_travel_time = 10
        self.enemy_count = 5
        self.player_score = 0   
        self.next_score_target = 10 
        self.boost_on = False

        #BACKGROUND STATS
        self.N_LAYERS = 5
        self.STARS_PER_LAYER = (20, 40, 50, 35, 25)
        self.NUM_STARS = sum(self.STARS_PER_LAYER)

        self.LAYER_SPEED_DIVIDERS = (1, 2, 4, 8, 16)
        self.WHITE = (255,255,255)
        self.BLACK = (20,20,40)
        self.LIGHTGRAY = (180, 180, 180)
        self.DARKGRAY = (120, 120, 120)
        self.BLUE_SHIFTED = (140, 140, 255)
        self.RED_SHIFTED = (200, 40, 40)
    
        self.LAYER_COLORS = [self.WHITE, self.LIGHTGRAY, self.DARKGRAY, self.BLUE_SHIFTED, self.RED_SHIFTED, self.DARKGRAY, self.BLUE_SHIFTED, self.RED_SHIFTED]