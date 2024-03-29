from constants import *

from actors.player import Player
from actors.fire import Fire


class World:
    def __init__(self, game):
        # Entities
        self.entities = {
            "Fire": Fire
        }

        # Game
        self.game = game

        # Transition curtain init
        self.transition_curtain = pg.Surface((NATIVE_W, NATIVE_H))
        self.transition_curtain.fill("black")

        # Start empty
        self.transition_curtain.set_alpha(0)
        self.transition_alpha = 0
        self.transition_fade_duration = 50
        self.transition_fade_timer = 0
        self.transition_direction = 1

        # Remainder and fade early flag
        self.transition_remainder = 0

        # Curtain init
        self.curtain = pg.Surface((NATIVE_W, NATIVE_H))
        self.curtain.fill("black")

        # Start full
        self.curtain.set_alpha(255)
        self.alpha = 255
        self.fade_duration = 1000
        self.fade_timer = 1000
        self.direction = -1

        # Remainder and fade early flag
        self.remainder = 0

        # TODO: Read the gmae data saved json to see which room to load
        # If no save file, then load bedroom and set player position to starting position
        # World scene should have a pause screen -> that can lead to the option screen toggler

        # Hard code pretend no save data, load this path, bedroom, first room
        # So save the name ("bedroom") to access the path values from the paths const dict
        # self.room_path = ROOM_PATHS["bedroom_balcony"]

        # region Room init
        self.room_path = ROOM_PATHS["bedroom"]
        self.room_dict = {}
        with open(self.room_path, 'r') as json_file:
            self.room_dict = load(json_file)

        # TODO: Once you read room: Iterate over the layers, there may be animated things in the bg_layers and entity in the collision layers
        # TODO: Each tiles / cells has unique names, so you can just check the ones that has animation that you know, instance it instead of drawing it and add it to entity array, have it be for loop and updated in update callback

        # Room bg layers, no 0, not a coordinate list
        self.bg_layers = self.room_dict["BG_LAYERS"]

        # Room collision layer, this one layer has 0, 0 = air, it is a coordinate list
        self.collision_layer = self.room_dict["COLLISION_LAYER"]

        # The collision draw layer removed all 0, it is used for drawing only
        self.collision_draw_layer = [x for x in self.collision_layer if x != 0]

        # Room fg layer, no 0, not a coordinate list
        self.fg_layers = self.room_dict["FG_LAYERS"]

        # This room tile size
        self.tile_s = self.room_dict["TILE_S"]

        # Room rect, room camera limit
        self.room_rect = self.room_dict["ROOM_RECT"]
        self.room_x_tu = self.room_rect[0] // self.tile_s
        self.room_y_tu = self.room_rect[1] // self.tile_s
        self.room_w_tu = self.room_rect[2] // self.tile_s
        self.room_h_tu = self.room_rect[3] // self.tile_s

        # Room background names that it needs to draw
        self.bg1 = self.room_dict["BG1"]
        self.bg2 = self.room_dict["BG2"]
        self.bg3 = self.room_dict["BG3"]
        self.bg4 = self.room_dict["BG4"]

        # Load this room sprite sheet
        self.sprite_sheet_png_name = self.room_dict["SPRITE_SHEET_PNG_NAME"]
        self.sprite_sheet_path = SPRITE_SHEET_PATHS[self.sprite_sheet_png_name]
        self.sprite_sheet_surf = pg.image.load(
            self.sprite_sheet_path).convert_alpha()
        # endregion

        # region Camera
        self.cam_rect = pg.FRect(0, 0, NATIVE_W, NATIVE_H)
        self.cam_lerp_weight = 0.2
        # endregion

        # Delays
        self.end_sleep_time = 500
        self.start_sleep_time = 500

        # Menu input
        self.is_input_allowed = False

        # Player
        self.player = Player(self.game, self.collision_layer, self.room_x_tu,
                             self.room_y_tu, self.room_w_tu, self.room_h_tu, self.cam_rect, self)
        # TODO: if there is no save data then set the player at the starting position
        self.player.rect.midbottom = (48, 144)

        # Set cam target to player
        self.cam_target = self.player.rect

        # Transition state
        self.is_transitioning = False

        # Hold player hit door
        self.door = None

        # Find animated sprites
        for i in range(len(self.bg_layers)):
            room = self.bg_layers[i]
            for j in range(len(room)):
                sprite = room[j]
                if sprite != 0:
                    name = sprite["name"]
                    x = sprite["xds"]
                    y = sprite["yds"]
                    if name in ["Fire"]:
                        entity = self.entities[name](
                            self.game, self.cam_rect, self.sprite_sheet_surf, x, y)
                        self.bg_layers[i][j] = {
                            "name": "entity", "obj": entity}

    def change_room(self):
        # region Replace this room with new room
        name = self.door["target"]
        # New room name -> load new json -> new room dict
        self.room_path = ROOM_PATHS[name]
        self.room_dict = {}
        with open(self.room_path, 'r') as json_file:
            self.room_dict = load(json_file)

        # Room bg layers, no 0, not a coordinate list
        self.bg_layers = self.room_dict["BG_LAYERS"]

        # Room collision layer, this one layer has 0, 0 = air, it is a coordinate list
        self.collision_layer = self.room_dict["COLLISION_LAYER"]

        # The collision draw layer removed all 0, it is used for drawing only
        self.collision_draw_layer = [x for x in self.collision_layer if x != 0]

        # Room fg layer, no 0, not a coordinate list
        self.fg_layers = self.room_dict["FG_LAYERS"]

        # This room tile size
        self.tile_s = self.room_dict["TILE_S"]

        # Room rect, room camera limit
        self.room_rect = self.room_dict["ROOM_RECT"]
        self.room_x_tu = self.room_rect[0] // self.tile_s
        self.room_y_tu = self.room_rect[1] // self.tile_s
        self.room_w_tu = self.room_rect[2] // self.tile_s
        self.room_h_tu = self.room_rect[3] // self.tile_s

        # Room background names that it needs to draw
        self.bg1 = self.room_dict["BG1"]
        self.bg2 = self.room_dict["BG2"]
        self.bg3 = self.room_dict["BG3"]
        self.bg4 = self.room_dict["BG4"]

        # Only load new sprite sheet if it is different from what I have now
        new_sprite_sheet_name = self.room_dict["SPRITE_SHEET_PNG_NAME"]
        if new_sprite_sheet_name != self.sprite_sheet_png_name:
            self.sprite_sheet_png_name = self.room_dict["SPRITE_SHEET_PNG_NAME"]
            self.sprite_sheet_path = SPRITE_SHEET_PATHS[self.sprite_sheet_png_name]
            self.sprite_sheet_surf = pg.image.load(
                self.sprite_sheet_path).convert_alpha()

        # Find animated sprites
        for i in range(len(self.bg_layers)):
            room = self.bg_layers[i]
            for j in range(len(room)):
                sprite = room[j]
                if sprite != 0:
                    name = sprite["name"]
                    x = sprite["xds"]
                    y = sprite["yds"]
                    if name in ["Fire"]:
                        entity = self.entities[name](
                            self.game, self.cam_rect, self.sprite_sheet_surf, x, y)
                        self.bg_layers[i][j] = {
                            "name": "entity", "obj": entity}

        # Player update collision
        self.player.collision_layer = self.collision_layer
        self.player.room_x_tu = self.room_x_tu
        self.player.room_y_tu = self.room_y_tu
        self.player.room_w_tu = self.room_w_tu
        self.player.room_h_tu = self.room_h_tu
        self.player.room_h_tu = self.room_h_tu
        # endregion Replace this room with new room

        # region Move player and camera by room direction
        direction = self.door["id"]
        if direction == "Left":
            self.player.rect.right = (
                self.room_rect[0] + self.room_rect[2]) - TILE_S
            self.cam_rect.x -= NATIVE_W

        elif direction == "Right":
            self.player.rect.left = self.room_rect[0] + TILE_S
            self.cam_rect.x += NATIVE_W
        # endregion Move player and camera by room direction

    def on_player_hit_door(self, door):
        # Block all updates with transition flag
        self.is_transitioning = True
        self.door = door

    def event(self, event):
        # Block input when fading
        if self.is_input_allowed == False:
            return

        # Block when transitioning
        if self.is_transitioning == True:
            return

        # Give input to player
        self.player.event(event)

    def update(self, dt):
        # region Update all bg sprites entity
        for room in self.bg_layers:
            for item in room:
                if item["name"] == "entity":
                    item["obj"].update(dt)
        # endregion Update all bg sprites entity

        # Start delay
        if self.start_sleep_time > 0:
            self.start_sleep_time -= dt
            return

        # Block when transitioning
        if self.is_transitioning == True:
            # Play the transition curtain
            # Update timer with direction and dt, go left or right
            self.transition_fade_timer += dt * self.transition_direction
            # Clamp timer
            self.transition_fade_timer = max(
                0, min(self.transition_fade_duration, self.transition_fade_timer))
            # Use timer as position
            fraction = self.transition_fade_timer / self.transition_fade_duration
            # Use position to update alpha value
            lerp_alpha = pg.math.lerp(0, 255, fraction)
            # Add prev round float loss
            lerp_alpha += self.transition_remainder
            # Round to int
            self.transition_alpha = max(0, min(255, round(lerp_alpha)))
            # Collect round loss
            self.transition_remainder = lerp_alpha - self.transition_alpha
            # Set alpha
            self.transition_curtain.set_alpha(self.transition_alpha)

            # End reached? Blink prompt
            if self.transition_fade_timer == 0:
                # Transition state is over
                self.is_transitioning = False
                self.transition_curtain.set_alpha(0)
                self.transition_alpha = 0
                self.transition_fade_duration = 50
                self.transition_fade_timer = 0
                self.transition_direction = 1
                # Remainder and fade early flag
                self.transition_remainder = 0

            # Other end reached?
            if self.transition_fade_timer == 50:
                # Change room
                self.change_room()
                # Reverse my direction
                self.transition_direction *= -1
                pass
            return

        # Update timer with direction and dt, go left or right
        self.fade_timer += dt * self.direction
        # Clamp timer
        self.fade_timer = max(0, min(self.fade_duration, self.fade_timer))
        # Use timer as position
        fraction = self.fade_timer / self.fade_duration
        # Use position to update alpha value
        lerp_alpha = pg.math.lerp(0, 255, fraction)
        # Add prev round float loss
        lerp_alpha += self.remainder
        # Round to int
        self.alpha = max(0, min(255, round(lerp_alpha)))
        # Collect round loss
        self.remainder = lerp_alpha - self.alpha
        # Set alpha
        self.curtain.set_alpha(self.alpha)

        # End reached? Blink prompt
        if self.fade_timer == 0:
            self.is_input_allowed = True

        # Other end reached?
        if self.fade_timer == 1000:
            self.end_sleep_time -= dt
            if self.end_sleep_time < 0:
                pass

        # region Update cam position
        # Update x position
        self.cam_rect.x = pg.math.smoothstep(
            self.cam_rect.x,
            self.cam_target.x - (NATIVE_W // 2),
            self.cam_lerp_weight
        )
        if abs(self.cam_rect.x) < 0.001:
            self.cam_rect.x = 0

        # Update y position
        self.cam_rect.y = pg.math.smoothstep(
            self.cam_rect.y,
            self.cam_target.y - (NATIVE_H // 2),
            self.cam_lerp_weight
        )
        if abs(self.cam_rect.y) < 0.001:
            self.cam_rect.y = 0

        # Limit cam to stay in room rect
        self.cam_rect.clamp_ip(self.room_rect)
        # endregion Update cam position

        # region Update player position
        self.player.update(dt)
        # endregion Update player position

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
                if item["name"] == "entity":
                    item["obj"].draw(NATIVE_SURF)
                    continue
                # Only update sprites that are in view
                if (self.cam_rect.x - item["region"][2] <= item["xds"] < self.cam_rect.right) and (self.cam_rect.y - item["region"][3] <= item["yds"] < self.cam_rect.bottom):
                    xd = item["xds"] - self.cam_rect.x
                    yd = item["yds"] - self.cam_rect.y
                    NATIVE_SURF.blit(self.sprite_sheet_surf,
                                     (xd, yd), item["region"])
        # endregion

        # region Draw player
        self.player.draw(NATIVE_SURF)
        # endregion Draw player

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

        # Draw curtain
        NATIVE_SURF.blit(self.curtain, (0, 0))

        # Draw transition curtain
        NATIVE_SURF.blit(self.transition_curtain, (0, 0))
