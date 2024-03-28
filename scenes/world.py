from constants import *


class World:
    def __init__(self, game):
        # Game
        self.game = game

        # TODO: Read the gmae data saved json to see which room to load
        # If no save file, then load bedroom and set player position to starting position
        # World scene should have a pause screen -> that can lead to the option screen toggler

        # Hard code pretend no save data, load this path, bedroom, first room
        # So save the name ("bedroom") to access the path values from the paths const dict
        # self.room_path = ROOM_PATHS["bedroom_balcony"]
        self.room_path = ROOM_PATHS["bedroom"]
        self.room_dict = {}
        with open(self.room_path, 'r') as json_file:
            self.room_dict = load(json_file)

        # Room init
        self.bg_layers = self.room_dict["BG_LAYERS"]
        self.collision_layer = self.room_dict["COLLISION_LAYER"]
        self.collision_draw_layer = [x for x in self.collision_layer if x != 0]
        self.fg_layers = self.room_dict["FG_LAYERS"]
        self.tile_s = self.room_dict["TILE_S"]
        self.room_rect = self.room_dict["ROOM_RECT"]
        self.room_x_tu = self.room_rect[0] // self.tile_s
        self.room_y_tu = self.room_rect[1] // self.tile_s
        self.room_w_tu = self.room_rect[2] // self.tile_s
        self.room_h_tu = self.room_rect[3] // self.tile_s
        self.sprite_sheet_png_name = self.room_dict["SPRITE_SHEET_PNG_NAME"]
        self.sprite_sheet_path = SPRITE_SHEET_PATHS[self.sprite_sheet_png_name]
        self.bg1 = self.room_dict["BG1"]
        self.bg2 = self.room_dict["BG2"]
        self.bg3 = self.room_dict["BG3"]
        self.bg4 = self.room_dict["BG4"]
        self.sprite_sheet_surf = pg.image.load(
            self.sprite_sheet_path).convert_alpha()

        # Camera
        self.cam_rect = pg.Rect(0, 0, NATIVE_W, NATIVE_H)

        # region Input flags
        self.is_w_pressed = 0
        self.is_a_pressed = 0
        self.is_s_pressed = 0
        self.is_d_pressed = 0
        # endregion

    def change_room_to(self, name):
        self.room_path = ROOM_PATHS[name]
        self.room_dict = {}
        with open(self.room_path, 'r') as json_file:
            self.room_dict = load(json_file)

        # Room init
        self.bg_layers = self.room_dict["BG_LAYERS"]
        self.collision_layer = self.room_dict["COLLISION_LAYER"]
        self.collision_draw_layer = [x for x in self.collision_layer if x != 0]
        self.fg_layers = self.room_dict["FG_LAYERS"]
        self.tile_s = self.room_dict["TILE_S"]
        self.room_rect = self.room_dict["ROOM_RECT"]
        self.room_x_tu = self.room_rect[0] // self.tile_s
        self.room_y_tu = self.room_rect[1] // self.tile_s
        self.room_w_tu = self.room_rect[2] // self.tile_s
        self.room_h_tu = self.room_rect[3] // self.tile_s
        self.sprite_sheet_png_name = self.room_dict["SPRITE_SHEET_PNG_NAME"]
        self.sprite_sheet_path = SPRITE_SHEET_PATHS[self.sprite_sheet_png_name]
        self.bg1 = self.room_dict["BG1"]
        self.bg2 = self.room_dict["BG2"]
        self.bg3 = self.room_dict["BG3"]
        self.bg4 = self.room_dict["BG4"]
        self.sprite_sheet_surf = pg.image.load(
            self.sprite_sheet_path).convert_alpha()

    def event(self, event):
        # Key down
        if event.type == pg.KEYDOWN:
            # region Cam input flag
            if event.key == self.game.key_bindings["up"]:
                self.is_w_pressed = 1
            if event.key == self.game.key_bindings["left"]:
                self.is_a_pressed = 1
            if event.key == self.game.key_bindings["down"]:
                self.is_s_pressed = 1
            if event.key == self.game.key_bindings["right"]:
                self.is_d_pressed = 1
            # endregion

        # Key up
        elif event.type == pg.KEYUP:
            # region Cam input flag
            if event.key == self.game.key_bindings["up"]:
                self.is_w_pressed = 0
            if event.key == self.game.key_bindings["left"]:
                self.is_a_pressed = 0
            if event.key == self.game.key_bindings["down"]:
                self.is_s_pressed = 0
            if event.key == self.game.key_bindings["right"]:
                self.is_d_pressed = 0
            # endregion

            # Testing only to switch room, this needs to be on doors
            # TODO: Move rooms into their own individual class, because 1 room can have things in it, enemies, doors, cutscene trigger and so on
            # if event.key == pg.K_1:
            #     self.change_room_to("bedroom_balcony")
            # if event.key == pg.K_2:
            #     self.change_room_to("bedroom")

    def update(self, dt):
        self.cam_rect.x += (self.is_d_pressed - self.is_a_pressed) * 2
        self.cam_rect.y += (self.is_s_pressed - self.is_w_pressed) * 2

    def draw(self, NATIVE_SURF):
        # region Backgrounds
        # Each names are unique ids
        if self.bg1 == "sky":
            x = (-self.cam_rect.x * 0.05) % NATIVE_W
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x, 0), (0, 0, 320, 179))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x - NATIVE_W, 0), (0, 0, 320, 179))
        if self.bg2 == "clouds":
            x = (-self.cam_rect.x * 0.1) % NATIVE_W
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x, 0), (0, 176, 320, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x - NATIVE_W, 0), (0, 176, 320, 160))
        if self.bg3 == "trees":
            x = (-self.cam_rect.x * 0.5) % NATIVE_W
            # 1
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x, 32), (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x - NATIVE_W, 32), (320, 448, 80, 160))
            # 2
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x + 96, 64),
                             (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x + 96 - NATIVE_W, 64), (320, 448, 80, 160))
            # 3
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x + 160, 32),
                             (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x + 160 - NATIVE_W, 32), (320, 448, 80, 160))
            # 4
            NATIVE_SURF.blit(self.sprite_sheet_surf, (x + 224, 16),
                             (320, 448, 80, 160))
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (x + 224 - NATIVE_W, 16), (320, 448, 80, 160))

        if self.bg4 == "blue_glow":
            NATIVE_SURF.blit(self.sprite_sheet_surf,
                             (0, 48), (0, 512, 320, 128))
        # endregion

        # region Draw all bg sprites
        for room in self.bg_layers:
            for item in room:
                # Only update sprites that are in view
                if (self.cam_rect.x - item["region"][2] <= item["xds"] < self.cam_rect.right) and (self.cam_rect.y - item["region"][3] <= item["yds"] < self.cam_rect.bottom):
                    xd = item["xds"] - self.cam_rect.x
                    yd = item["yds"] - self.cam_rect.y
                    NATIVE_SURF.blit(self.sprite_sheet_surf,
                                     (xd, yd), item["region"])
        # endregion

        # region Draw all collision sprites
        for item in self.collision_draw_layer:
            # Only update sprites that are in view
            if (self.cam_rect.x - item["region"][2] <= item["xds"] < self.cam_rect.right) and (self.cam_rect.y - item["region"][3] <= item["yds"] < self.cam_rect.bottom):
                xd = item["xds"] - self.cam_rect.x
                yd = item["yds"] - self.cam_rect.y
                NATIVE_SURF.blit(self.sprite_sheet_surf,
                                 (xd, yd), item["region"])
        # endregion

        # region Draw all fg sprites
        for room in self.fg_layers:
            for item in room:
                # Only update sprites that are in view
                if (self.cam_rect.x - item["region"][2] <= item["xds"] < self.cam_rect.right) and (self.cam_rect.y - item["region"][3] <= item["yds"] < self.cam_rect.bottom):
                    xd = item["xds"] - self.cam_rect.x
                    yd = item["yds"] - self.cam_rect.y
                    NATIVE_SURF.blit(self.sprite_sheet_surf,
                                     (xd, yd), item["region"])
        # endregion
