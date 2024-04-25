import arcade, random, os

#EXPLOSTION HAS 10 TEXTURES REPRESENTING TO PROGRESSION OF THE EXPLOSION
#THE TEXTURE CHANGES ACCORDING TO THE ANIMATION_TIMER
#WHEN THE TIMER IS TO BIG THE SPRITE IS KILLED
class explosion(arcade.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.center_x = x_pos
        self.center_y = y_pos
        self.scale = 2.1
        self.angle = random.randint(0,360)
        self.animation_timer = 0
        self.explosion_frames = [
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_1.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_2.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_3.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_4.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_5.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_6.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_7.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_8.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_9.png"),
            arcade.load_texture(os.path.dirname(__file__) + "/assets/explosion/explosion_frame_10.png")
        ]
        self.texture = self.explosion_frames[3]

    def update(self):
        if self.animation_timer >= 0 and self.animation_timer < 0.1:
            self.texture = self.explosion_frames[0]
        elif self.animation_timer >= 0.1 and self.animation_timer < 0.2:
            self.texture = self.explosion_frames[1]
        elif self.animation_timer >= 0.2 and self.animation_timer < 0.3:
            self.texture = self.explosion_frames[2]
        elif self.animation_timer >= 0.3 and self.animation_timer < 0.4:
            self.texture = self.explosion_frames[3]
        elif self.animation_timer >= 0.4 and self.animation_timer < 0.5:
            self.texture = self.explosion_frames[4]
        elif self.animation_timer >= 0.5 and self.animation_timer < 0.6:
            self.texture = self.explosion_frames[5]
        elif self.animation_timer >= 0.6 and self.animation_timer < 0.7:
            self.texture = self.explosion_frames[6]
        elif self.animation_timer >= 0.7 and self.animation_timer < 0.8:
            self.texture = self.explosion_frames[7]
        elif self.animation_timer >= 0.8 and self.animation_timer < 0.9:
            self.texture = self.explosion_frames[8]
        elif self.animation_timer >= 0.9 and self.animation_timer < 1:
            self.texture = self.explosion_frames[9]
        elif self.animation_timer >= 1 and self.animation_timer < 1.1:
            self.texture = self.explosion_frames[9]
        else:
            self.kill()

