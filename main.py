from constants import *
from scenes.options_screen import OptionsScreen
from scenes.created_by_splash_screen import CreatedBySplashScreen
from scenes.made_with_splash_screen import MadeWithSplashScreen
from scenes.title_screen import TitleScreen
from scenes.menu_screen import MenuScreen
from scenes.save_screen import SaveScreen
from scenes.intro_cutscene import IntroCutscene
from scenes.world import World
from scenes.test import Test
from sys import exit
from json import load


class Game:
    def __init__(self):
        # Debug
        self.is_development = True
        self.is_debug = False

        # Default values if there are no save settings data
        self.resolution = 4
        self.key_bindings = {
            "up": pg.K_UP,
            "down": pg.K_DOWN,
            "left": pg.K_LEFT,
            "right": pg.K_RIGHT,
            "enter": pg.K_RETURN,
            "pause": pg.K_ESCAPE,
            "jump": pg.K_SPACE,
        }

        # Read save settings data if exists and apply data
        self.saved_settings = {}
        try:
            with open(SETTING_PATH, "r") as settings_file:
                self.saved_settings = load(settings_file)
                self.resolution = self.saved_settings["resolution"]
                self.key_bindings = self.saved_settings["key_bindings"]
        except FileNotFoundError:
            pass

        self.window_w = NATIVE_W * self.resolution
        self.window_h = NATIVE_H * self.resolution
        self.window_surf = pg.display.set_mode((self.window_w, self.window_h))
        self.scenes = {
            "CreatedBySplashScreen": CreatedBySplashScreen,
            "MadeWithSplashScreen": MadeWithSplashScreen,
            "TitleScreen": TitleScreen,
            "MenuScreen": MenuScreen,
            "SaveScreen": SaveScreen,
            "IntroCutscene": IntroCutscene,
            "World": World,
            "Test": Test
        }
        self.current_scene = None
        self.is_option_screen = False

    def set_scene(self, value):
        self.current_scene = self.scenes[value](self)


game = Game()
game.set_scene("CreatedBySplashScreen")
# game.set_scene("MenuScreen")

# This thing is the user UI allowing them to change keybinding and resolution
option_screen = OptionsScreen(game)

# Main loop
while 1:
    # Dt
    dt = CLOCK.tick(FPS)

    # Get event
    for event in pg.event.get(EVENTS):
        # region Window quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # endregion Window quit

        # region debug toggle
        if game.is_development:
            if event.type == pg.KEYUP:
                if event.key == pg.K_0:
                    game.is_debug = not game.is_debug
        # endregion debug toggle

        # Option screen event
        if game.is_option_screen:
            option_screen.event(event)
        else:
            # Current scene event
            game.current_scene.event(event)

    # Clear native surface
    NATIVE_SURF.fill("black")

    # Current scene draw
    game.current_scene.draw(NATIVE_SURF)

    # Option screen update draw
    if game.is_option_screen:
        option_screen.draw(NATIVE_SURF)
        option_screen.update(dt)
    else:
        # Current scene update
        game.current_scene.update(dt)

    # Debug
    if game.is_debug:
        FONT.render_to(
            NATIVE_SURF, (0, 0), f'{int(CLOCK.get_fps())}', "white")

    # region Native to window and update window
    pg.transform.scale(NATIVE_SURF, (game.window_w,
                       game.window_h), game.window_surf)
    pg.display.update()
    # endregion Native to window and update window
