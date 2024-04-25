import arcade, arcade.gui, random,json                          #DEFAULT PYTHON LIBRARIES
import classes.main_menu_interface as menu                      #GAME UI
import classes.player_abilities as ability                      #IMPORT PLAYER ABILITIES
from classes.game_over import *                                 #ALL WEAPONS FOR THE PLAYER AND SHOOTING THEM
from classes.utils import *                                     #ALL CONSTANTS TRHOUGHOUT THE GAME
from classes.player import *                                    #PLAYER CLASS | DRAW AND UPDATE
from classes.enemy import *                                     #ENEMY CLASS | DRAW AND UPDATE
from classes.baseSprite import *                                #DRAW AND UPDATE THE MAIN BASE
from classes.player_oob_marker import OOB_marker                #CHECKING FOR PLAYER OUT OF PLAY AREA
from classes.explosion import *                                 #IMPORT EXPLOSION CODE

CONST = gameConstants()                                         #GAME CONSTANTS RESUSED THOUGHOUT THE GAME

class GameView(arcade.View):
    def __init__(self, screen_width, screen_height, volume, difficulty, fullscreen):
        super().__init__()
        CONST.screen_width, CONST.screen_height, CONST.sound_setting,CONST.difficulty_setting, CONST.fullscreen = screen_width, screen_height, volume, difficulty, fullscreen               #TRANSFER THE DISPLAY SIZE INFORMATION FROM LAST VIEW
        self.player_sprite = None       #Player Sprite
        self.shot_list = None           #Shot list
        self.enemy_shot_list = None     #Enemy Shot list
        self.explosion_list = None      #Explosion list
        self.environment_list = None    #environment list
        self.shiled_list = None         #Shield list (don't mind the spelling mistake)
        self.items_list = None          #Items list
        self.base_shield_list = None    #Base shield list
        self.ability_list = None        #Ability list
        self.multicanon_on = False      #Is multicanon unlocked or no?
        self.physics_engine = arcade.PymunkPhysicsEngine #Pysics engine
        self.mouse = [0,0]              #Mouse coord
        self.stars = []                 #Star list
        self.wave_number = 9          #Current wave of enemies (n + 1)
        self.enemy_hp_progression = [3,3,4,4,5,6,6,7,8,9] #Progression of the enemy HP count according to index(n_wave)
        self.endless = False            #If n_wave > 9 ==> endless = true
        self.shield_times = [5,5,5,5,10,10,10,15,15,25]   #Shield use times and same cooldown times according to index(n_wave)
        self.wave_lenghts = [45, 60, 60, 75, 75, 90, 90, 120, 120, 180] #Lenght of wave according to index(n_wave)
        self.enemy_per_wave = [10, 20, 30, 40, 60, 75, 90, 125, 130, 200] #N enemies at n_wave
        self.damage_multiplacators = [1,1,1.3,1.3,1.5,1.5,1.5,1.5,1.5,2] #Damage Multiplier according to index(n_wave)
        self.damage_reduction = [1,0.9,0.8,0,8,0.8,0.8,0.8,0.7,0.7,0.7] #Damage reduction according to index(n_wave)
        self.difficulty_multiplicators = [1, 1, 0.60, 0.40]             #Difficulty multipliers for enemy spawn rate accordgin to index(n_difficulty)
        self.base_shield_hp_counts = [0,0,0,0,0,20,20,50,50,100]        #Base shield hp count according to index(n_wave)
        self.base_shield_hp = self.base_shield_hp_counts[self.wave_number]  #Define base shield
        self.difficulty_spawn_rate_factor = None    #Spawn rate mutliplier for enemies
        self.enemy_timer = 0                        #enemy timer for spawning
        self.ult_used = False                       #Ult used for ability
        self.ult_center_coord = [0,0]               #Default center for ult
        self.current_wave_timer = self.wave_lenghts[self.wave_number]   #Current wave timer    
        self.shield_on = False              #Shield on false per default
        self.base_shield_charge = 0         #0 per defautl
        self.base_defense = False           #not unlocked per default
        self.score_multiplier = 1           #1 per defgutl
        self.score_multiplier_timer = 0     #0 per default
        self.multiplier_on = False          #Off per default
        self.next_score_target = 10         #10 at x1 multiplier
        self.shield_timer = self.shield_times[self.wave_number]
        self.multiplier_cooldown = 5        #Constant 5 
        self.ricochet = False               #Ablity not on per default
        self.ricochet_targets = []          #empty per defautl
        self.ricochet_timer = 0             #o per default
        self.ricochet_max_targets = 8       #maximum tagets for icochet
        self.base_defense_timer = 0         #Timer for self defense
        self.lockdown_timer = 20            #Lockdown timer 20 per defautl
        self.ricochet_use_timer = 15        #15 per default
        self.main_theme_player = None       #audio palyer (uninitialized)
        self.window.set_mouse_visible(False)#Hide mouse -> show corsshair instead
            
    def setup(self):
        self.init_stars()                               #
        self.player_list = arcade.SpriteList()          #
        self.ui_sprite_list = arcade.SpriteList()       #
        self.base = arcade.SpriteList()                 #
        self.enemy_list = arcade.SpriteList()           #
        self.shot_list = arcade.SpriteList()            #
        self.explosion_list = arcade.SpriteList()       # INITIALIZE THE SPRITE LISTS
        self.enemy_shot_list = arcade.SpriteList()      #
        self.environment_list = arcade.SpriteList()     #
        self.base_shield_list = arcade.SpriteList()     #
        self.items_list = arcade.SpriteList()           #
        self.shiled_list = arcade.SpriteList()          #
        self.ability_list = arcade.SpriteList()         #
        self.base_sprite = base_sprite(CONST.screen_width, CONST.screen_height)         #
        self.environment_list.append(self.base_sprite)                                  #
        self.player_sprite = player()                                                   #Set and append default sprites
        self.oob_marker = OOB_marker(300,300,CONST.screen_width, CONST.screen_height)   #
        self.ui_sprite_list.append(self.oob_marker)                                     #
        self.player_list.append(self.player_sprite)                                     #
        self.amount_of_bullets = 200
        self.main_theme = arcade.load_sound(os.path.dirname(__file__) + "/assets/audio/music/game_main_theme.wav")#Start main audio theme 
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=CONST.DEFAULT_DAMPING, gravity=(0,0))             ###
        self.difficulty_spawn_rate_factor = self.difficulty_multiplicators[CONST.difficulty_setting]                ##Init physics engine and add coresspondant sprites

        self.physics_engine.add_sprite(self.player_sprite, friction=CONST.PLAYER_FRICTION, mass=CONST.PLAYER_MASS, moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,collision_type="player",max_horizontal_velocity=CONST.PLAYER_MAX_HORIZONTAL_SPEED, max_vertical_velocity=CONST.PLAYER_MAX_VERTICAL_SPEED, elasticity=0)
        self.physics_engine.add_sprite_list(self.enemy_list, friction=CONST.WALL_FRICTION, mass=CONST.PLAYER_MASS /2, collision_type="enemy",body_type=arcade.PymunkPhysicsEngine.DYNAMIC)

        #Append a shield instance for visual effect
        self.shiled_list.append(ability.base_shield(CONST.screen_width/2, CONST.screen_height/2, 500, 600))
        random.seed()
        self.main_theme_player = arcade.sound.play_sound(self.main_theme, looping=True, volume=CONST.sound_setting/20) #Start playing audio

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        #redefine the mouse positions for calculating atan2
        self.mouse[0] = x
        self.mouse[1] = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        #Shoot laser or missile according to the weapon selection
        if self.player_sprite.selected_weapon == 0:
            arcade.play_sound(CONST.laser_sound, looping=False)
            self.shoot_weapon('laser-x1')
        else:
            self.shoot_weapon('missile')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            #Get back to the main menu (also resets progress!!!!!)
            arcade.stop_sound(self.main_theme_player)
            menu_view = menu.homeScreen(CONST.screen_width, CONST.screen_height,CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen)
            self.window.show_view(menu_view)
        #Move player vars
        if symbol == arcade.key.W:
            self.player_sprite.w_pressed = True
        if symbol == arcade.key.S:
            self.player_sprite.s_pressed = True
        if symbol == arcade.key.A:
            self.player_sprite.a_pressed = True
        if symbol == arcade.key.D:
            self.player_sprite.d_pressed = True
        #Switch between laser and missile
        if symbol == arcade.key.KEY_1:
            self.player_sprite.selected_weapon = 0
        if symbol == arcade.key.KEY_2:
            if self.wave_number > 2:
                self.player_sprite.selected_weapon = 1
        #User lockdown ability
        if symbol == arcade.key.X:
            if self.wave_number > 5:
                self.use_ability("lockdown")
        #Use bounce laser
        if symbol == arcade.key.R:
            if self.wave_number > 8:
                self.use_ability("ricochet")
        #User shield
        if symbol == arcade.key.SPACE:
            if  not len(self.shiled_list) >= 1 and self.shield_timer >= self.shield_times[self.wave_number] and self.wave_number > 3:
                self.shiled_list.append(ability.shield(self.player_sprite.center_x, self.player_sprite.center_y, self.shield_times[self.wave_number]))
                self.shield_on = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol == arcade.key.W:
            self.player_sprite.w_pressed = False
        if symbol == arcade.key.S:
            self.player_sprite.s_pressed = False 
        if symbol == arcade.key.A:
            self.player_sprite.a_pressed = False
        if symbol == arcade.key.D:
            self.player_sprite.d_pressed = False

    def shoot_weapon(self, weapon_type):
        #Check if laser has been shot and if the multishot powerup has been unlocked
        if weapon_type == 'laser-x1' and self.player_sprite.shots_left > 0:
            self.player_sprite.shots_left-= 1
            if self.multicanon_on:
                #Place one central shot and 2 other left and right of the central one
                self.shot_list.append(ability.laser(self.player_sprite.center_x, self.player_sprite.center_y, self.player_sprite.player_orientation, 0))
                for i in range(1,2):
                    self.shot_list.append(ability.laser(self.player_sprite.center_x, self.player_sprite.center_y, self.player_sprite.player_orientation - (10*i)*(math.pi/180), 0))
                for i in range(1,2):
                    self.shot_list.append(ability.laser(self.player_sprite.center_x, self.player_sprite.center_y, self.player_sprite.player_orientation + (10*i)*(math.pi/180), 0))
            else:
                self.shot_list.append(ability.laser(self.player_sprite.center_x, self.player_sprite.center_y, self.player_sprite.player_orientation, 0))
        #If missile has been shot and the ammo is enough append a missile 
        elif weapon_type == 'missile' and self.player_sprite.missiles_left > 0:
            if len(self.enemy_list) != 0:
                self.player_sprite.missiles_left -= 1
                missile = ability.missile(self.player_sprite.center_x, self.player_sprite.center_y, self.player_sprite.player_orientation, self.enemy_list)
                self.shot_list.append(missile)

    def use_ability(self, ability_type):
        match ability_type:
            #Spawn a lockdown sprite and set the lockdown timer for ability
            case "lockdown":
                #ULLT RADIUS 346
                if len(self.ability_list) == 0 and self.lockdown_timer >= 20:
                    self.ult_center_coord = [self.player_sprite.center_x,self.player_sprite.center_y]
                    self.ability_list.append(ability.lockdown(self.ult_center_coord[0],self.ult_center_coord[1]))
                    self.lockdown_timer = 0
            case "ricochet":
                #If the cooldown has been reached use the ability
                if self.ricochet_use_timer >= 15:
                    #reset the bounce laser tagets and find new ones
                    self.ricochet_targets = None
                    possible_targets = []
                    for enemy in self.enemy_list:
                        possible_targets.append(enemy)
                    targets = []
                    #Find the first closest enemy  to the player
                    closest_enemy = arcade.get_closest_sprite(self.player_sprite, possible_targets)[0]
                    targets.append([closest_enemy, 0])
                    possible_targets.remove(closest_enemy)
                    #Then use a function style similat to Fold_List[] from mathematica to get every closest sprite relative to the last sprite
                    #in order to get a bounce laser effect
                    for i in range(self.ricochet_max_targets):
                        if i >= len(self.enemy_list) -1:
                            break
                        closest_enemy = arcade.get_closest_sprite(targets[i][0], possible_targets)[0]
                        targets.append( [closest_enemy, 0] )
                        possible_targets.remove(closest_enemy)
                    #Reset the timers and set the noew richochet targets
                    self.ricochet_targets = targets
                    self.ricochet_timer = len(self.ricochet_targets)
                    self.ricochet = True
                    self.ricochet_use_timer = 0

    def handle_enemy_spawning(self):
        #Calculate the amount of enemies/s
        enemy_per_second = ( self.wave_lenghts[self.wave_number] / self.enemy_per_wave[self.wave_number] ) * self.difficulty_spawn_rate_factor
        #Spawn an enemy every time the enemy/s value is overshot and if there ar not to many enemies otherwise the game gets unplayable at higher waves
        if self.enemy_timer >= enemy_per_second and len(self.enemy_list) < 39:
            self.enemy_timer = 0
            self.enemy_list.append(enemy(random.randint(0,CONST.screen_width), random.randint(0, CONST.screen_height), 10, self.enemy_hp_progression[self.wave_number], False))
            self.physics_engine.add_sprite_list(self.enemy_list, friction=CONST.WALL_FRICTION, collision_type="enemy",body_type=arcade.PymunkPhysicsEngine.DYNAMIC)

    def on_update(self, delta_time):
        #Check for player death or base death and load game overscreen if player or base hp drops to 0
        if self.player_sprite.hp <= 0:
            arcade.stop_sound(self.main_theme_player)
            player_score = {"score": CONST.player_score}
            with open(os.path.dirname(__file__) + '/assets/high_scores.json', 'w') as score_file:
                json.dump(player_score, score_file)
                
            self.enemy_list.clear()
            self.explosion_list.append(explosion(self.player_sprite.center_x, self.player_sprite.center_y))
            gameover = gameover_screen(CONST.screen_width, CONST.screen_height, CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen, CONST.player_score)
            self.window.show_view(gameover)
        if self.base_sprite.hp <= 0:
            arcade.stop_sound(self.main_theme_player)
            gameover = gameover_screen(CONST.screen_width, CONST.screen_height, CONST.sound_setting, CONST.difficulty_setting, CONST.fullscreen, CONST.player_score)
            self.window.show_view(gameover)
        ###################################
        #Sprite lists update
        #UPDATE PHYSICS ENGINE
        self.physics_engine.step()
        #UPDATE SPRITE LISTS
        self.player_list.update()
        self.shot_list.update()
        self.enemy_list.update()
        self.enemy_shot_list.update()
        self.ui_sprite_list.update()
        self.explosion_list.update()
        self.environment_list.update()
        self.shiled_list.update()
        self.items_list.update()
        self.base_shield_list.update()
        self.ability_list.update()
        #############################
        #Update all things related to delta_time see method update_timers() for more comments
        self.update_timers(delta_time)
        ###############################
        #Handle the enemy spawn rate according to wave lenght and selected difficulty
        self.handle_enemy_spawning()
        ####################################
        #Set the mouse x and y coordinates for the player sprite to calculate the correct atan2() angle
        self.player_sprite.mouse_x = self.mouse[0]
        self.player_sprite.mouse_y = self.mouse[1]

        #####################################
        #always set the player shield to follow it player by syncing its center to the player's
        for shieled in self.shiled_list:
            shieled.center_x = self.player_sprite.center_x
            shieled.center_y = self.player_sprite.center_y
        ###############################################
        #
        #Move Player according to its angle by calculating a force using sin() and cos() and a base speed 1250 (vertical) 700 (latteral)
        #
        #If the player should not be moveing we set it's firction to 1500 slowing it down 
        if self.player_sprite.w_pressed and not self.player_sprite.s_pressed:
            force = (1250 * math.cos(self.player_sprite.player_orientation) ,1250 * math.sin(self.player_sprite.player_orientation))
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.player_sprite.s_pressed and not self.player_sprite.w_pressed:
            force = (-1250 * math.cos(self.player_sprite.player_orientation) ,-1250 * math.sin(self.player_sprite.player_orientation))
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        if self.player_sprite.a_pressed and not self.player_sprite.d_pressed:
            force = (700 * math.cos(self.player_sprite.player_orientation + math.pi/2),700 * math.sin(self.player_sprite.player_orientation + math.pi/2))
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.player_sprite.d_pressed and not self.player_sprite.a_pressed:
            force = (700 * math.cos(self.player_sprite.player_orientation - math.pi/2),700 * math.sin(self.player_sprite.player_orientation - math.pi/2))
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite,  0)
        else:
            self.physics_engine.set_friction(self.player_sprite, 1500)
        #####################################################
        #
        #Check for enemy hit by player shot and handle enemy shooting
        for enemy in self.enemy_list:
            #Check if the cooldown for a shot is satisfied, then add a laser amiming at the player (same as enemy orientation)
            #Also reset the enemy's cooldown back to 0
            if enemy.delta_time_sum >= 2 and enemy.ulted == False:
                self.enemy_shot_list.append(ability.laser(enemy.center_x, enemy.center_y, enemy.orientation, 1))
                enemy.delta_time_sum = 0
            #Here we recalculate the orientation of the enemy using the update_target_x_y() method (see enemy sprite for more info)
            enemy.update_target_x_y(self.player_sprite.center_x, self.player_sprite.center_y)
            #Get all the player originated shots that collided with the enemy and check if the list is not Null -> This returns all the SHOTS
            collided = arcade.check_for_collision_with_list(enemy, self.shot_list) 
            if len(collided) != 0:
                #Destroy all the shots that hit
                for elem in collided:
                    elem.kill()
                #Check for shot type,
                #if shot is 1 -> laser, remove 1 hp multiplied by the damage bonus
                #Else -> missile, remove 3 hp multiplied by the damage bomus
                if elem.type == 1:
                    enemy.hp -= 1 * self.damage_multiplacators[self.wave_number]
                    arcade.play_sound(CONST.laser_hit, looping=False, volume=.25)
                else:
                    enemy.hp -= 3 * self.damage_multiplacators[self.wave_number]
                #Check if enemy has been destroyed, if yes kill the sprite, add 1 point multiplied by the score multiplier
                if enemy.hp <= 0:
                    CONST.player_score += 1 * self.score_multiplier
                    self.explosion_list.append(explosion(enemy.center_x, enemy.center_y))
                    #Once enemy is dead, 40% Chance ammo recharge 30% heal bonus.
                    #The bonuses are then added to the item list
                    choice = random.choice([2,2,2,2,1,1,1,0,0,0])
                    if choice == 1:
                        self.items_list.append(ability.heal_bonus(enemy.center_x, enemy.center_y))
                    elif choice == 2:
                        self.items_list.append(ability.ammo_bonus(enemy.center_x, enemy.center_y))
                    #Reset the score cooldown
                    self.score_multiplier_timer = self.multiplier_cooldown
                    #If it's the first hit, initialize the multiplier
                    if not self.multiplier_on:
                        self.multiplier_on = True
                    #If player has reached the score target skipt to the nect multiplier, and set next target
                    if CONST.player_score >= self.next_score_target:
                        self.score_multiplier = self.score_multiplier * 2
                        if self.score_multiplier >= 128:
                            self.score_multiplier = 128
                        self.next_score_target = CONST.player_score + 10 * self.score_multiplier
                    arcade.play_sound(CONST.laser_hit, volume=CONST.sound_setting, looping=False)
                    enemy.kill()

        #CHECK FOR SHIELD HIT
        #Using try: except: -> because if there is no shield the list index will fail the script
        #Kill every shot that hits the shield
        try:
            shield_collided = arcade.check_for_collision_with_list(self.shiled_list[0], self.enemy_shot_list)
            if len(shield_collided) != 0:
                for shot in shield_collided:
                    shot.kill()
        except:
            pass

        ##############################
        #Check for hit with base shield
        #Check if the distance from the shot the the base is smaller than the shield radius if yes kill the shot and append a new shield sprite/animation to it
        for shot in self.enemy_shot_list:
            if arcade.get_distance_between_sprites(shot, self.base_sprite) <= 182:
                if self.base_shield_hp > 0:
                    self.base_shield_hp -= 1
                    self.base_shield_list.append(ability.base_shield(CONST.screen_width/2, CONST.screen_height/2, shot.center_x, shot.center_y))
                    shot.kill()
        ################################
        #Check for impact with bnase
        #For every shot, substract 1,3 or 5 hp to the base according to the difficulty setting
        collided_with_base = arcade.check_for_collision_with_list(self.base_sprite, self.enemy_shot_list)
        for shot in collided_with_base:
            shot.kill()
            match CONST.difficulty_setting:
                case 0:
                    self.base_sprite.hp -= 1/1000
                case 1:
                    self.base_sprite.hp -= 1/1000
                case 2:
                    self.base_sprite.hp -= 3/1000
                case 3:
                    self.base_sprite.hp -= 5/1000
            shot.kill()
        
        #########################################
        #Check for player damage taken
        #Get all shots that collide and substract .2, .3, .3, .5 x damage multiplier to the player hp
        player_collided = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_shot_list)
        if len(player_collided) != 0:
            for shot in player_collided:
                shot.kill()
                if CONST.difficulty_setting != 0:
                    match CONST.difficulty_setting:
                        case 0:
                            self.player_sprite.hp -= .2 * self.damage_reduction[self.wave_number]
                        case 1:
                            self.player_sprite.hp -= .3 * self.damage_reduction[self.wave_number]
                        case 2:
                            self.player_sprite.hp -= .4 * self.damage_reduction[self.wave_number]
                        case 3:
                            self.player_sprite.hp -= .5 * self.damage_reduction[self.wave_number]

        ###########################
        #
        #Check for player item pickup
        #For each item taht collided, check it's type and either heal or recharge the player's ammo
        player_pickup_items = arcade.check_for_collision_with_list(self.player_sprite, self.items_list)
        if len(player_pickup_items) != 0:
            for item in player_pickup_items:
                item.kill()
                if item.type == "heal":
                    if self.player_sprite.hp + 5 >= 14: #Not more that 14 as to not overshoot the hp bar index
                        self.player_sprite.hp = 14
                    else:
                        self.player_sprite.hp += 5
                elif item.type == "ammo":
                    self.player_sprite.shots_left += 30
                    self.player_sprite.missiles_left += 2
        #########################
        #
        #Lockdown logic
        #After ult charge time (10s) change the state of each enemy to "ulted" so as the cannot shoot or move
        #After 25s release the enemies by resettinf their ulted status
        
        if len(self.ability_list) != 0 and self.ability_list[0].charge >= 10:
            for enemy in self.enemy_list:
                if arcade.get_distance(self.ult_center_coord[0], self.ult_center_coord[1], enemy.center_x, enemy.center_y) <= 346 and self.ult_used == False:
                    enemy.ulted = True
            self.ult_used = True
        if len(self.ability_list) != 0 and self.ability_list[0].charge >= 22:
            self.ult_used = False
        #Also clear all enemies ult status if they spawn in the ult radius after it's been used
        for enemy in self.enemy_list:
            if not self.ult_used:
                enemy.ulted = False

        #######################################
        #
        #Bounce Laser Ability
        #Try: Except: to avoid index(-1) error
        try:
            if self.ricochet and len(self.ricochet_targets) != 0:
                #user richochet timer as index to have a progression and not instant change
                self.ricochet_targets[math.floor(self.ricochet_timer)][0].alpha = 0
                if self.ricochet_targets[math.floor(self.ricochet_timer)][1] == 0:
                    #Same logic as normal enemy hit
                    CONST.player_score += 1 * self.score_multiplier
                    self.score_multiplier_timer = self.multiplier_cooldown
                    if not self.multiplier_on:
                        self.multiplier_on = True
                    if CONST.player_score >= self.next_score_target:
                        self.score_multiplier = self.score_multiplier * 2
                        if self.score_multiplier >= 128:
                            self.score_multiplier = 128
                        self.next_score_target += 10 * self.score_multiplier
                    self.explosion_list.append(explosion(self.ricochet_targets[math.floor(self.ricochet_timer)][0].center_x,self.ricochet_targets[math.floor(self.ricochet_timer)][0].center_y))
                    self.ricochet_targets[math.floor(self.ricochet_timer)][1] = 1
            elif not self.ricochet and len(self.ricochet_targets) != 0:
                #When all enemies have been hidden, kill the sprites
                for target in self.ricochet_targets:
                    target[0].kill()
        except:
            pass
        #Unlock the upgrades according to the wave number
        if self.wave_number > 3:
            self.base_defense = True
        if self.wave_number > 6:
            self.multicanon_on = True

        
        ######################
        #Base defender logic, shoots 45 lasers in a circular pattern every 5 seconds
        if self.base_defense and self.base_defense_timer >= 5:
            for i in range(45):
                self.shot_list.append(ability.laser(CONST.screen_width /2, CONST.screen_height/2, (self.base_sprite.angle + 8*i) * (math.pi/180), 0))
            self.base_defense_timer = 0
        
        ##############
        #Update reference position for OOB (out of bound) sprite
        self.oob_marker.player_position[0] = self.player_sprite.center_x
        self.oob_marker.player_position[1] = self.player_sprite.center_y

        #######################
        #Move the stars in a parralax way
        #We move them in the player_vector * -1
        #Each speed is multiplied by the star layer position to change it's relative speed
        star_x_vel , star_y_vel = self.physics_engine.get_physics_object(self.player_sprite).body.velocity[0] * -1 / 300, self.physics_engine.get_physics_object(self.player_sprite).body.velocity[1] * -1 / 300
        for star_list in self.stars:
            for star in star_list:
                star[0] += star_x_vel / CONST.LAYER_SPEED_DIVIDERS[star[2]]
                star[1] += star_y_vel / CONST.LAYER_SPEED_DIVIDERS[star[2]]

    def update_timers(self, dt):
        #
        #In order to animate sprites / count wave timers / handle cooldowns for abilities
        #
        #This method runs once un the update() method
        #we pass the delta_time parameter through to either add or substract it to counters or animation counters
        #See each sprite or timer for logic
        self.player_sprite.animation_timer += dt
        ####################
        #Determines if an enemy can shoot again or not yet
        self.enemy_timer += dt

        #######################
        #Animation timers, (see corresponding sprite for more info)
        for missile in self.shot_list:
            missile.timer += dt
            missile.fuse += dt
        for enemy in self.enemy_list:
            enemy.delta_time_sum += dt
        for explosion in self.explosion_list:
            explosion.animation_timer += dt
        for shield in self.shiled_list:
            shield.animation_timer += dt
            shield.timer += dt
        for item in self.items_list:
            item.timer += dt
            item.lifetime -= dt
        for shield in self.base_shield_list:
            shield.animation_timer += dt
        for ability in self.ability_list:
            ability.charge += dt
        self.base_sprite.timer += dt
        ###############################################################
        #Handles score multiplier
        #If the player get a point in the timeframe of the score_multiplier_timer
        #The multiplier stays on, should the player fail to get a point in time, the multiplier falls back to x1
        if self.multiplier_on:
            self.score_multiplier_timer -= dt
            if self.score_multiplier_timer <= 0:
                self.multiplier_on = False
                self.score_multiplier_timer = 0
                self.score_multiplier = 1
        #############################################
        #Handle the timer for player shield
        if self.shield_on:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_on = False
        else:
            self.shield_timer += dt
            if self.shield_timer >= self.shield_times[self.wave_number]:
                self.shield_timer = self.shield_times[self.wave_number]

        #####################################
        #Handle wave timer
        #Substract delta_time to the different wave lenghts
        #If wave timer < 0 ==> skip to next wave number and according wavelenght
        if not self.endless:
            self.current_wave_timer -= dt
            if self.current_wave_timer <= 0:
                self.enemy_list.clear()
                self.enemy_shot_list.clear()
                self.items_list.clear()
                self.current_wave_timer = 0
                self.wave_number += 1
                if self.wave_number > 9:
                    self.wave_number = 9
                    self.endless = True
                self.current_wave_timer = self.wave_lenghts[self.wave_number]

        #######################################
        #Handle bounce laser timer
        self.ricochet_timer -=  4 * dt
        if self.ricochet_timer <= 0:
            self.ricochet_timer = 0
            self.ricochet = False

        ####################
        #Handle base protection shield chargup time
        #
        #If the shield falls, recharge the shield for 15 seconds
        if self.base_shield_hp <= 0:
            self.base_shield_charge += dt
            if self.base_shield_charge >= 15:
                self.base_shield_charge = 0
                self.base_shield_hp = self.base_shield_hp_counts[self.wave_number]

        ######################################
        #
        #Base defense, lockdown, bouncelaser use cooldown handler
        #
        self.base_defense_timer += dt
        self.lockdown_timer += dt
        self.ricochet_use_timer += dt
        #############################
        #Passive base recharge speed
        #
        #If hp is greater than max hp set hp to max hp
        self.base_sprite.hp += dt/1000
        if self.base_sprite.hp >= 14:
            self.base_sprite.hp = 14

    def init_stars(self):
        #Draws a random pattern of stars according to the values in classes.utils
        #
        #COLORS and AMOUNT can be determined in classes.utils
        for loop in range(5):
                star_layer = []
                for i in range(CONST.STARS_PER_LAYER[loop]):
                    star = [random.randrange(0, CONST.screen_width - 1),
                           random.randrange(0, CONST.screen_height - 1), loop]
                    star_layer.append(star)
                self.stars.append(star_layer)

    def draw_game_interface(self):
        #BASIC INTERFACE IMPORTS
        #
        #The default textures (grayed out textures) for the interface are imported here
        #Should the ability be available, the variable will be overwritten later in the method
        #
        bullet_counter = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/bullet_counter.png")
        missile_counter = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/missile_counter.png")
        timer_tile = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/wave_counter.png")
        shield_tile = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/power_up_shield_bw.png")
        base_shield_timer = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/base_shield_1_bw.png")
        base_defense_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/base_shoot_bw.png")
        dmg_multi_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/dmg_1_bw.png")
        hp_boost_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/heal_boost_1_bw.png")
        lockdown_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/base_shoot_bw.png")
        multi_shot_texure = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/lockdown_bw.png")
        ricochet_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/ricochet_laser_tile_bw.png")      
        bullet_text = f"{self.player_sprite.shots_left}"
        missile_text = f"{self.player_sprite.missiles_left}"
        shield_text = ""
        base_shield_text = ""
        lockdown_timer = ""
        ricochet_timer = ""
        ##############################################################
        #DRAW WAVE TIMER
        #CHANGE FORMATTING AND COLOR ACCORDING TO TIMER VALUE
        if self.current_wave_timer >= 10:
            timer = f"{math.floor(self.current_wave_timer)}"
            timer_color = (255,255,255)
        else:
            timer = f"{round(self.current_wave_timer, 2)}"
            timer_color = (255,12,12)
        if self.endless:
            timer = "endless"
        #ACTUALLY DRAW THE TIMER
        wave_counter = f"Wave {self.wave_number + 1}"
        arcade.draw_scaled_texture_rectangle(CONST.screen_width/2, CONST.screen_height - 26.25, timer_tile, .25)
        arcade.draw_text(wave_counter, 0, CONST.screen_height - 13, (255,255,255), 10, font_name="Kenney Mini Square", align="center", width=CONST.screen_width)
        arcade.draw_text(timer, 0, CONST.screen_height - 42, timer_color, 24 , font_name="Kenney Mini Square", align="center", width=CONST.screen_width)
        ############################################################################
        #DRAW PLAYER LIVE SCORE AND SCORE COMBO
        arcade.draw_text("Score:", 20, 20, (255,255,255), 10, font_name="Kenney Mini Square")
        arcade.draw_text(f"{CONST.player_score}", 75, 20, (255,255,255), 20, font_name="Kenney Mini Square")
        if self.score_multiplier_timer != 0:
            arcade.draw_line(CONST.screen_width - 85, 20, CONST.screen_width - 85, 20 + 20 * (self.score_multiplier_timer / self.multiplier_cooldown), (255,255,255), 3)
            arcade.draw_text(f"{self.score_multiplier}x", 20, 20, (255,255,255), 20, font_name="Kenney Mini Square", width=CONST.screen_width - 40, align="right")
        #############################################################################
        #DRAW CHARGEUP TIME FOR LOCKDOWN ABILITY
        if len(self.ability_list) != 0 and self.ability_list[0].charge <= 10:
            ult_tile = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/lockdown_tile.png")
            arcade.draw_scaled_texture_rectangle(CONST.screen_width/2, CONST.screen_height - 200, ult_tile, .25)
            arcade.draw_text("lockdown", 0, CONST.screen_height - 190, (255,255,255), 10, font_name="Kenney Mini Square", align="center", width=CONST.screen_width)
            arcade.draw_text(f"{round(10 - self.ability_list[0].charge, 2)}", 0, CONST.screen_height - 220, (255,255,255), 20, font_name="Kenney Mini Square", align="center", width=CONST.screen_width)
        #PLAYER HEALTHBAR
        arcade.draw_scaled_texture_rectangle(258, CONST.screen_height - 45, CONST.player_healthbar[math.ceil(self.player_sprite.hp)], .5)
        #BASE_HEALTHBAR
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 258, CONST.screen_height - 45, CONST.base_healthbar[math.ceil(self.base_sprite.hp)], .5)
        
        ########################################################################
        #BASE WEAPONS
        #DRAW INGAME INDICATORS OF AMOUNT OF BULLETS
        #
        # IF AFTER WAVE 3 -> UNLOCK MISSILE
        #
        arcade.draw_scaled_texture_rectangle(40, CONST.screen_height - 75, bullet_counter, 1)
        if self.wave_number > 2:
            arcade.draw_scaled_texture_rectangle(40, CONST.screen_height - 140, missile_counter, 1)
            arcade.draw_text(missile_text, 80, CONST.screen_height - 150, arcade.color.WHITE, 20, font_name="Kenney Mini Square")
        arcade.draw_text(bullet_text, 80, CONST.screen_height - 85, arcade.color.WHITE, 20, font_name="Kenney Mini Square")
        if self.player_sprite.selected_weapon == 0:
            arcade.draw_line(10, CONST.screen_height - 100, 10, CONST.screen_height - 50, arcade.color.WHITE, 3)
        else:
            arcade.draw_line(10, CONST.screen_height - 165, 10, CONST.screen_height - 115, arcade.color.WHITE, 3)
        #
        #DEFINE ACTIVATED/DEACTIVATED ABILITIES
        #
        #Checks for each ability unlock if the current wave number allows
        #the player to use such ability and draw the correct tile in the menu accordingly
        #If the ability is not to be used, the tile will remain gray
        #
        if self.wave_number > 0:
            hp_boost_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/heal_boost_1.png")
        if self.wave_number > 1:
            hp_boost_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/heal_boost_2.png")
            dmg_multi_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/dmg_1.png")
        if self.wave_number > 2:
            shield_tile = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/power_up_shield.png")
            shield_text = f"{math.floor(self.shield_timer)}"
            if self.shield_timer >= self.shield_times[self.wave_number]:
                shield_text = "ready"
        if self.wave_number > 3:
            base_shield_timer = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/base_shield_1.png")
            if self.base_shield_charge >= 15 or self.base_shield_hp != 0:
                base_shield_text = "up"
            else:
                base_shield_text = f"{math.floor(self.base_shield_charge)}"
            dmg_multi_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/dmg_2.png")
        if self.wave_number > 4:
            base_defense_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/base_shoot.png")
            lockdown_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/lockdown.png")
            if self.lockdown_timer >= 20:
                lockdown_timer= "ready"
            else:
                lockdown_timer = f"{round(self.lockdown_timer)}"
        if self.wave_number > 5:
            base_shield_timer = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/base_shield_2.png")
        if self.wave_number > 6:
            hp_boost_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/heal_boost_3.png")
            multi_shot_texure = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/multishot.png")
        if self.wave_number > 7:
            base_shield_timer = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/base_shield_3.png")
            ricochet_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/ricochet_laser_tile.png")
            if self.ricochet_use_timer >= 15:
                ricochet_timer = "ready"
            else:
                ricochet_timer = f"{round(self.ricochet_use_timer)}"
        if self.wave_number > 8:
            dmg_multi_texture = arcade.load_texture(os.path.dirname(__file__) + "/assets/game_interface/dmg_3.png")  
        #DEFAULT ABILITY DRAW
        #
        #Here we draw all of the above defined ability tiles
        #They are drawn in a 2x4 arrangement on the top right of the screen
        #
        #RIGHT COLLUM
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 40, CONST.screen_height -75, multi_shot_texure, 1)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 40, CONST.screen_height -140, hp_boost_texture, 1)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 40, CONST.screen_height -205, dmg_multi_texture, 1)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 40, CONST.screen_height -270, base_defense_texture, 1)
        #LEFT COLLUM
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 105, CONST.screen_height -75, shield_tile, 1)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 105, CONST.screen_height -140, base_shield_timer, 1)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 105, CONST.screen_height -205, lockdown_texture, 1)
        arcade.draw_scaled_texture_rectangle(CONST.screen_width - 105, CONST.screen_height -270, ricochet_texture, 1)
        #LEFT COLLUMS TEXT   
        arcade.draw_text(shield_text, 0, CONST.screen_height - 85, (255,255,255), 20, font_name="Kenney Mini Square", align="right", width=CONST.screen_width - 145)
        arcade.draw_text(base_shield_text, 0, CONST.screen_height - 150, (255,255,255), 20, font_name="Kenney Mini Square", align="right", width=CONST.screen_width - 145)
        arcade.draw_text(lockdown_timer, 0, CONST.screen_height - 215, (255,255,255), 20, font_name="Kenney Mini Square", align="right", width=CONST.screen_width - 145)
        arcade.draw_text(ricochet_timer, 0, CONST.screen_height - 280, (255,255,255), 20, font_name="Kenney Mini Square", align="right", width=CONST.screen_width - 145)

    def on_draw(self):
        #RUDIMENTARY DRAW
        #SCREEN CLEAR AND DRAWING THE STARS
        #The color black comes from the classes.utils dataclass
        self.clear()
        #self.camera.use()
        arcade.set_background_color(CONST.BLACK)
        for star_layer in self.stars:
            for star in star_layer:
                arcade.draw_point(star[0], star[1], CONST.LAYER_COLORS[star[2]], 1)
        #Drawing all the different sprite lists.
        #Player shots, enemy shots, enemy list, environment list (base), items list, ui_sprite list ()
        self.shot_list.draw()           #all player and base shots
        self.enemy_list.draw()          #all enemies
        self.enemy_shot_list.draw()     #all enemy shots
        self.ui_sprite_list.draw()      #player out of bound marker (default position -200;-200)
        self.environment_list.draw()    #base sprite
        self.shiled_list.draw()         #player shield (max lenght 1)
        self.items_list.draw()          #Pickupable items (heal bonus, ammo recharge)
        self.base_shield_list.draw()    #base shield (max amount = shield hp)
        self.ability_list.draw()        #secondary abilites (lockdown, bounce laser)
        #################################
        #Draw the healthbar for each enemy
        for enemy in self.enemy_list:
            arcade.draw_scaled_texture_rectangle(enemy.center_x, enemy.center_y + 45, CONST.healthbar_textures[math.ceil(enemy.hp)],.30, 0, enemy.alpha)
            if len(self.ability_list) != 0 and self.ult_used and enemy.ulted == True:
                arcade.draw_line(self.ult_center_coord[0], self.ult_center_coord[1], enemy.center_x, enemy.center_y, (255,10,10),3)
        ##########################################
        #
        #Draw the laser beam for the bounce laser
        #Draws 4 lines with different colors from the player to ne first target enemy
        #The follows the list to draw the same lines from each enemy to the next
        #
        #First, hides the enemies and only destroys them once all of the have been "treated"
        if self.ricochet and self.ricochet_timer > 0:
            arcade.draw_line(self.player_sprite.center_x, self.player_sprite.center_y, self.ricochet_targets[0][0].center_x,self.ricochet_targets[0][0].center_y, (100,255,100), 10)
            arcade.draw_line(self.player_sprite.center_x, self.player_sprite.center_y, self.ricochet_targets[0][0].center_x,self.ricochet_targets[0][0].center_y, (149,255,140), 7)
            arcade.draw_line(self.player_sprite.center_x, self.player_sprite.center_y, self.ricochet_targets[0][0].center_x,self.ricochet_targets[0][0].center_y, (200,255,200), 4)
            arcade.draw_line(self.player_sprite.center_x, self.player_sprite.center_y, self.ricochet_targets[0][0].center_x,self.ricochet_targets[0][0].center_y, (255,255,255), 2)
            i = 0
            while i < (len(self.ricochet_targets) - 1):
                arcade.draw_line(self.ricochet_targets[i][0].center_x,self.ricochet_targets[i][0].center_y,self.ricochet_targets[i + 1][0].center_x,self.ricochet_targets[i + 1][0].center_y, (100,255,100), 10)
                arcade.draw_line(self.ricochet_targets[i][0].center_x,self.ricochet_targets[i][0].center_y,self.ricochet_targets[i + 1][0].center_x,self.ricochet_targets[i + 1][0].center_y, (149,255,140), 7)
                arcade.draw_line(self.ricochet_targets[i][0].center_x,self.ricochet_targets[i][0].center_y,self.ricochet_targets[i + 1][0].center_x,self.ricochet_targets[i + 1][0].center_y, (200,255,200), 4)
                arcade.draw_line(self.ricochet_targets[i][0].center_x,self.ricochet_targets[i][0].center_y,self.ricochet_targets[i + 1][0].center_x,self.ricochet_targets[i + 1][0].center_y, (255,255,255), 2)
                i += 1
        self.explosion_list.draw()
        ###########################################
        #
        #Draw the items
        #
        for heal in self.items_list:
            arcade.draw_text(f"{math.floor(heal.lifetime)}", heal.center_x + 30, heal.center_y - 7, arcade.color.WHITE, 14, font_name="Kenney Mini Square")
        ###################################
        #
        #Draw the crosshaire insteaf of the normal mouse, (gives some fps vibes)
        arcade.draw_scaled_texture_rectangle(self.mouse[0], self.mouse[1], arcade.load_texture(os.path.dirname(__file__) + "/assets/crosshair.png"), 1)
        #####################################
        #
        #Draw the player and interface on the last two, topmost layers, as to ensure they are never obstructed by other things
        self.player_list.draw()
        self.draw_game_interface()