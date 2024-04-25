#####################################################
##                                                 ##   
##          CODEBASE WRITTEN BY:                   ##
##           Cornell Baumann                       ##
##           (c)2023 Forward Productions           ##
##                                                 ##
#####################################################



import classes.splashscreen as splash
from classes.utils import *
import arcade


CONST = gameConstants()

def main():
    window = arcade.Window(CONST.screen_width, CONST.screen_height, CONST.screen_title)
    start_view = splash.splashScreen(CONST.screen_width, CONST.screen_height, 0.4, 2, 0)
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()