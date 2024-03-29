from constants import *


class Player:
    def __init__(self, game, collision_layer, room_x_tu, room_y_tu, room_w_tu, room_h_tu, cam_rect, world):
        # World
        self.world = world

        # Game
        self.game = game

        # Collision layer and room
        self.collision_layer = collision_layer
        self.room_x_tu = room_x_tu
        self.room_y_tu = room_y_tu
        self.room_w_tu = room_w_tu
        self.room_h_tu = room_h_tu

        # Cam rect
        self.cam_rect = cam_rect

        # Name
        self.name = "Player"

        # Inputs
        self.is_left_pressed = 0
        self.is_right_pressed = 0
        self.is_down_pressed = False

        # Sprite sheet surface
        self.sprite_sheet_surface = pg.image.load(
            SPRITE_SHEET_PATHS["player_sprite_sheet.png"]
        ).convert_alpha()

        # Sprite sheet flipped surface
        self.sprite_sheet_flipped_surface = pg.image.load(
            SPRITE_SHEET_PATHS["player_sprite_sheet_flipped.png"]
        ).convert_alpha()

        # Surface
        self.surface = self.sprite_sheet_surface
        self.surface_offset_x = 21
        self.surface_offset_y = 14

        # Rect
        self.rect = pg.FRect(0, 0, 6, 31)

        # Movement
        self.max_run = 0.09
        self.run_lerp_weight = 0.2
        self.max_fall = 0.270
        self.normal_gravity = 0.000533
        self.heavy_gravity = 0.001066
        self.gravity = self.normal_gravity
        self.jump_vel = -0.230
        self.velocity = pg.math.Vector2()
        self.remainder_x = 0
        self.remainder_y = 0

        # Object sprite sheet regions
        self.frames_dict = {}
        with open(ACTORS_JSON_DATA_PATHS["player_sprite_sheet.json"], 'r') as file:
            self.frames_dict = load(file)

        # Object frames list name
        self.frames_list_name = "idle"
        self.frames_list = self.frames_dict[self.frames_list_name]
        self.frames_list_len = len(self.frames_list)
        self.frames_list_index_len = self.frames_list_len - 1

        # Object frame index
        self.frame_index = 0
        self.frame_data = self.frames_list[self.frame_index]

        # Object frame frame data
        self.frame_data_frame = self.frame_data['frame']
        self.frame_tuple_region = (
            self.frame_data_frame['x'],
            self.frame_data_frame['y'],
            self.frame_data_frame['w'],
            self.frame_data_frame['h']
        )

        # Object frame duration data
        self.frame_duration = self.frame_data['duration']

        # Object frame index updater counter
        self.total_dt = 0

        # Object state
        self.state = "idle"

        # Object direction
        self.facing_direction = 1
        self.old_facing_direction = self.facing_direction

        # Object direction input
        self.direction = 0

        # Collision check
        self.is_on_floor = False

    def event(self, event):
        if event.type == pg.KEYDOWN:
            # Just pressed left
            if event.key == self.game.key_bindings["left"]:
                # Set is pressed left 1
                self.is_left_pressed = 1

            # Just pressed right
            if event.key == self.game.key_bindings["right"]:
                # Set is pressed right 1
                self.is_right_pressed = 1

            # Just pressed down
            if event.key == self.game.key_bindings["down"]:
                # Set is pressed down true
                self.is_down_pressed = True

            # Just pressed jump
            elif event.key == self.game.key_bindings["jump"]:
                # Idle, run crouch can jump
                if self.state in [
                    "idle",
                    "run",
                    "crouch"
                ]:
                    # Exit up
                    self.set_state("up")

        elif event.type == pg.KEYUP:
            # Just released left
            if event.key == self.game.key_bindings["left"]:
                # Set is released left 0
                self.is_left_pressed = 0

            # Just released right
            if event.key == self.game.key_bindings["right"]:
                # Set is released right 0
                self.is_right_pressed = 0

            # Just released down
            if event.key == self.game.key_bindings["down"]:
                # Set is released down false
                self.is_down_pressed = False

            # Just released jump
            elif event.key == self.game.key_bindings["jump"]:
                # Idle, run crouch can jump
                if self.state == "up":
                    self.gravity = self.heavy_gravity

    # Object update
    def update(self, dt):
        # region Update velocity with gravity
        self.velocity.y += self.gravity * dt
        self.velocity.y = min(self.velocity.y, self.max_fall)
        # endregion Update velocity with gravity

        # region Update x velocity with direction
        self.velocity.x = pg.math.smoothstep(
            self.velocity.x,
            self.direction * self.max_run,
            self.run_lerp_weight
        )
        if abs(self.velocity.x) < 0.001:
            self.velocity.x = 0
        # endregion Update x velocity with direction

        # region Update direction sign for movement
        direction_x = 0
        if self.velocity.x > 0:
            direction_x = 1
        if self.velocity.x < 0:
            direction_x = -1

        direction_y = 0
        if self.velocity.y > 0:
            direction_y = 1
        if self.velocity.y < 0:
            direction_y = -1
        # endregion Update direction sign for movement

        # region Update horizontal position
        # Distance to cover horizontally
        amount = self.velocity.x * dt
        self.remainder_x += amount
        displacement_x = round(self.remainder_x)

        if direction_x != 0:
            self.remainder_x -= displacement_x
            displacement_x = abs(displacement_x)
            # Check 1px at a time
            while displacement_x > 0:
                # Player currrent pos to tu
                possible_x_tu = (self.rect.centerx // TILE_S) - self.room_x_tu
                possible_y_tu = (self.rect.centery // TILE_S) - self.room_y_tu

                # Debug draw player real rect
                if self.game.is_debug:
                    xd = self.rect.x - self.cam_rect.x
                    yd = self.rect.y - self.cam_rect.y
                    pg.draw.rect(NATIVE_SURF, "green",
                                 (xd, yd, self.rect.width, self.rect.height), 1)

                # Possible positions
                player_tl_tu = (possible_x_tu - 1, possible_y_tu - 1)
                player_tt_tu = (possible_x_tu, possible_y_tu - 1)
                player_tr_tu = (possible_x_tu + 1, possible_y_tu - 1)
                player_ml_tu = (possible_x_tu - 1, possible_y_tu - 0)
                player_mr_tu = (possible_x_tu + 1, possible_y_tu - 0)
                player_bl_tu = (possible_x_tu - 1, possible_y_tu + 1)
                player_bm_tu = (possible_x_tu, possible_y_tu + 1)
                player_br_tu = (possible_x_tu + 1, possible_y_tu + 1)

                # Select the ones needed with direction
                possible_pos_tus = []
                if direction_x == 0 and direction_y == 0:
                    possible_pos_tus = []
                elif direction_x == 0 and direction_y == -1:
                    possible_pos_tus = [player_tl_tu,
                                        player_tt_tu, player_tr_tu]
                elif direction_x == 1 and direction_y == -1:
                    possible_pos_tus = [
                        player_tl_tu, player_tt_tu, player_tr_tu, player_mr_tu, player_br_tu]
                elif direction_x == 1 and direction_y == 0:
                    possible_pos_tus = [player_tr_tu,
                                        player_mr_tu, player_br_tu]
                elif direction_x == 1 and direction_y == 1:
                    possible_pos_tus = [
                        player_bl_tu, player_bm_tu, player_br_tu, player_mr_tu, player_tr_tu]
                elif direction_x == 0 and direction_y == 1:
                    possible_pos_tus = [
                        player_bl_tu, player_bm_tu, player_br_tu]
                elif direction_x == -1 and direction_y == 1:
                    possible_pos_tus = [
                        player_tl_tu, player_ml_tu, player_bl_tu, player_bm_tu, player_br_tu]
                elif direction_x == -1 and direction_y == 0:
                    possible_pos_tus = [
                        player_tl_tu, player_ml_tu, player_bl_tu]
                elif direction_x == -1 and direction_y == -1:
                    possible_pos_tus = [
                        player_bl_tu, player_ml_tu, player_tl_tu, player_tt_tu, player_tr_tu]

                # Check filtered_possible_locations_tu
                possible_cells = []
                for possible_pos_tu in possible_pos_tus:
                    possible_x_tu = possible_pos_tu[0]
                    possible_y_tu = possible_pos_tu[1]

                    # Clamp withing room
                    possible_x_tu = max(
                        min(possible_x_tu, self.room_w_tu - 1), self.room_x_tu)
                    possible_y_tu = max(
                        min(possible_y_tu, self.room_h_tu - 1), self.room_y_tu)
                    possible_x_tu = int(possible_x_tu)
                    possible_y_tu = int(possible_y_tu)

                    # Tu -> cell
                    cell = self.collision_layer[possible_y_tu *
                                                self.room_w_tu + possible_x_tu]

                    # Debug draw possible cell
                    if self.game.is_debug:
                        possible_xd = ((possible_x_tu + self.room_x_tu) * TILE_S) - \
                            self.cam_rect.x
                        possible_yd = ((possible_y_tu + self.room_y_tu) * TILE_S) - \
                            self.cam_rect.y
                        pg.draw.lines(
                            NATIVE_SURF,
                            "green",
                            True,
                            [
                                (possible_xd, possible_yd),
                                (possible_xd + TILE_S, possible_yd),
                                (possible_xd + TILE_S, possible_yd + TILE_S),
                                (possible_xd, possible_yd + TILE_S),
                            ]
                        )

                    # Air? look somewhere else
                    if cell == 0:
                        continue

                    # Found rect?
                    possible_cells.append(cell)

                    # Debug draw possible found cells
                    if self.game.is_debug:
                        pg.draw.rect(
                            NATIVE_SURF,
                            "yellow",
                            [
                                possible_xd,
                                possible_yd,
                                TILE_S,
                                TILE_S
                            ]
                        )

                # My future position
                xds = self.rect.x
                yds = self.rect.y
                xds += direction_x
                w = xds + self.rect.width
                h = yds + self.rect.height

                # Debug draw my future rect
                if self.game.is_debug:
                    pg.draw.rect(
                        NATIVE_SURF,
                        "blue",
                        [xds - self.cam_rect.x, yds - self.cam_rect.y,
                            self.rect.width, self.rect.height],
                        1
                    )

                # AABB with all possible neighbours
                is_collide = False
                for cell in possible_cells:
                    # Cell rect
                    c_xds = cell["xds"]
                    c_yds = cell["yds"]
                    c_w = c_xds + TILE_S
                    c_h = c_yds + TILE_S
                    # Future hit something? Break set flag to true
                    if (c_xds < w and xds < c_w and c_yds < h and yds < c_h):
                        is_collide = True
                        break

                # Future hit? Break
                if is_collide:
                    # Found door?
                    if cell["name"] == "Door":
                        self.world.on_player_hit_door(cell)
                        self.velocity.y = 0
                        self.remainder_y = 0
                    break

                # Future no hit? Move to next pixel
                displacement_x -= 1
                self.rect.x += direction_x
                self.rect.clamp_ip(self.cam_rect)
        # endregion Update horizontal position

        # region Update vertical position
        # Distance to cover vertically
        amount = self.velocity.y * dt
        self.remainder_y += amount
        displacement_y = round(self.remainder_y)

        if direction_y != 0:
            self.remainder_y -= displacement_y
            displacement_y = abs(displacement_y)

            # Check 1px at a time
            while displacement_y > 0:
                # Player currrent pos to tu
                possible_x_tu = (self.rect.centerx // TILE_S) - self.room_x_tu
                possible_y_tu = (self.rect.centery // TILE_S) - self.room_y_tu

                # Debug draw player real rect
                if self.game.is_debug:
                    xd = self.rect.x - self.cam_rect.x
                    yd = self.rect.y - self.cam_rect.y
                    pg.draw.rect(NATIVE_SURF, "green",
                                 (xd, yd, self.rect.width, self.rect.height), 1)

                # Possible positions
                player_tl_tu = (possible_x_tu - 1, possible_y_tu - 1)
                player_tt_tu = (possible_x_tu, possible_y_tu - 1)
                player_tr_tu = (possible_x_tu + 1, possible_y_tu - 1)
                player_ml_tu = (possible_x_tu - 1, possible_y_tu - 0)
                player_mr_tu = (possible_x_tu + 1, possible_y_tu - 0)
                player_bl_tu = (possible_x_tu - 1, possible_y_tu + 1)
                player_bm_tu = (possible_x_tu, possible_y_tu + 1)
                player_br_tu = (possible_x_tu + 1, possible_y_tu + 1)

                # Select the ones needed with direction
                possible_pos_tus = []
                if direction_x == 0 and direction_y == 0:
                    possible_pos_tus = []
                elif direction_x == 0 and direction_y == -1:
                    possible_pos_tus = [player_tl_tu,
                                        player_tt_tu, player_tr_tu]
                elif direction_x == 1 and direction_y == -1:
                    possible_pos_tus = [
                        player_tl_tu, player_tt_tu, player_tr_tu, player_mr_tu, player_br_tu]
                elif direction_x == 1 and direction_y == 0:
                    possible_pos_tus = [player_tr_tu,
                                        player_mr_tu, player_br_tu]
                elif direction_x == 1 and direction_y == 1:
                    possible_pos_tus = [
                        player_bl_tu, player_bm_tu, player_br_tu, player_mr_tu, player_tr_tu]
                elif direction_x == 0 and direction_y == 1:
                    possible_pos_tus = [
                        player_bl_tu, player_bm_tu, player_br_tu]
                elif direction_x == -1 and direction_y == 1:
                    possible_pos_tus = [
                        player_tl_tu, player_ml_tu, player_bl_tu, player_bm_tu, player_br_tu]
                elif direction_x == -1 and direction_y == 0:
                    possible_pos_tus = [
                        player_tl_tu, player_ml_tu, player_bl_tu]
                elif direction_x == -1 and direction_y == -1:
                    possible_pos_tus = [
                        player_bl_tu, player_ml_tu, player_tl_tu, player_tt_tu, player_tr_tu]

                # Check filtered_possible_locations_tu
                possible_cells = []
                for possible_pos_tu in possible_pos_tus:
                    possible_x_tu = possible_pos_tu[0]
                    possible_y_tu = possible_pos_tu[1]

                    # Clamp withing room
                    possible_x_tu = max(
                        min(possible_x_tu, self.room_w_tu - 1), self.room_x_tu)
                    possible_y_tu = max(
                        min(possible_y_tu, self.room_h_tu - 1), self.room_y_tu)
                    possible_x_tu = int(possible_x_tu)
                    possible_y_tu = int(possible_y_tu)

                    # Tu -> cell
                    cell = self.collision_layer[possible_y_tu *
                                                self.room_w_tu + possible_x_tu]

                    # Debug draw possible cell
                    if self.game.is_debug:
                        possible_xd = ((possible_x_tu + self.room_x_tu) * TILE_S) - \
                            self.cam_rect.x
                        possible_yd = ((possible_y_tu + self.room_y_tu) * TILE_S) - \
                            self.cam_rect.y
                        pg.draw.lines(
                            NATIVE_SURF,
                            "green",
                            True,
                            [
                                (possible_xd, possible_yd),
                                (possible_xd + TILE_S, possible_yd),
                                (possible_xd + TILE_S, possible_yd + TILE_S),
                                (possible_xd, possible_yd + TILE_S),
                            ]
                        )

                    # Air? look somewhere else
                    if cell == 0:
                        continue

                    # Found rect?
                    possible_cells.append(cell)

                    # Debug draw possible found cells
                    if self.game.is_debug:
                        pg.draw.rect(
                            NATIVE_SURF,
                            "yellow",
                            [
                                possible_xd,
                                possible_yd,
                                TILE_S,
                                TILE_S
                            ]
                        )

                # My future position
                xds = self.rect.x
                yds = self.rect.y
                yds += direction_y
                w = xds + self.rect.width
                h = yds + self.rect.height

                # Debug draw my future rect
                if self.game.is_debug:
                    pg.draw.rect(
                        NATIVE_SURF,
                        "blue",
                        [xds - self.cam_rect.x, yds - self.cam_rect.y,
                            self.rect.width, self.rect.height],
                        1
                    )

                # AABB with all possible neighbours
                is_collide = False
                for cell in possible_cells:
                    # Cell rect
                    c_xds = cell["xds"]
                    c_yds = cell["yds"]
                    c_w = c_xds + TILE_S
                    c_h = c_yds + TILE_S
                    # Future hit something? Break set flag to true
                    if (c_xds < w and xds < c_w and c_yds < h and yds < c_h):
                        is_collide = True
                        break

                # Future hit? Break
                if is_collide:
                    if direction_y == 1:
                        self.is_on_floor = True
                        self.velocity.y = 0
                    break

                # Future no hit? Move to next pixel
                self.is_on_floor = False
                displacement_y -= 1
                self.rect.y += direction_y
                self.rect.clamp_ip(self.cam_rect)
        # endregion Update vertical position

        # region Update facing direction and old facing direction
        if self.direction != 0:
            self.old_facing_direction = self.facing_direction
            self.facing_direction = self.direction
        # endregion Update facing direction and old facing direction

        # region Get horizontal input direction
        self.direction = self.is_right_pressed - self.is_left_pressed
        # endregion Get horizontal input direction

        # Idle
        if self.state == "idle":
            # region Exit to run
            if self.direction != 0:
                self.set_state("run")
            # endregion Exit to run

            # region Exit to crouch
            elif self.is_down_pressed:
                self.set_state("crouch")
            # endregion Exit to crouch

            # Exit jump in just pressed event input

        # Run
        elif self.state == "run":
            # region Exit to idle
            if self.direction == 0:
                self.set_state("idle")
            # endregion Exit to idle

            # region Exit to crouch
            elif self.is_down_pressed:
                self.set_state("crouch")
            # endregion Exit to crouch

            # region Exit to down
            elif not self.is_on_floor:
                self.set_state("down")
            # endregion Exit to down

            # Exit jump in just pressed event input

            # region Handle turning - frame perfect
            if self.facing_direction == 1:
                self.surface = self.sprite_sheet_surface
            elif self.facing_direction == -1:
                self.surface = self.sprite_sheet_flipped_surface
            if self.old_facing_direction != self.facing_direction:
                self.set_frames_list_name("turn")
            # endregion Handle turning - frame perfect

        # Crouch
        elif self.state == "crouch":
            # region Exit to run
            if not self.is_down_pressed and self.direction != 0:
                self.set_state("run")
            # endregion Exit to run

            # region Exit to idle
            elif not self.is_down_pressed and self.direction == 0:
                self.set_state("idle")
            # endregion Exit to idle

            # Exit jump in just pressed event input

            # region Cannot move direction 0
            self.direction = 0
            # endregion Cannot move direction 0

        # Up
        elif self.state == "up":
            # region Exit to down
            if self.velocity.y > 0:
                self.set_state("down")
            # endregion Exit to down

        # Down
        elif self.state == "down":
            # region Exit to run
            if self.is_on_floor and self.direction != 0:
                self.set_state("run")
            # endregion Exit to run

            # region Exit to idle
            if self.is_on_floor and self.direction == 0:
                self.set_state("idle")
            # endregion Exit to idle

            # region Exit to crouch
            if self.is_on_floor and self.is_down_pressed:
                self.set_state("crouch")
            # endregion Exit to crouch

        # region update total dt, set frame index
        self.total_dt += dt
        if self.total_dt >= self.frame_duration:
            self.total_dt = 0
            self.set_frame_index(self.frame_index + 1)
        # endregion update total dt, set frame index

    # Set state
    def draw(self, NATIVE_SURF):
        # region Render a region of the player sprite sheet
        NATIVE_SURF.blit(
            self.surface,
            (
                (self.rect.x - self.surface_offset_x) - self.cam_rect.x,
                (self.rect.y - self.surface_offset_y) - self.cam_rect.y
            ),
            self.frame_tuple_region
        )
        # endregion Render a region of the player sprite sheet

    # Set frame_index
    def set_frame_index(self, value):
        # Update frame index
        self.frame_index = value

        # On last frame?
        if self.frame_index > self.frames_list_index_len:
            # region Reset frame index or stay at last index
            if self.frames_list_name in [
                "idle",
                "run",
                "up",
                "down"
            ]:
                self.frame_index = 0

            # Stay on last frame
            else:
                self.frame_index -= 1
            # endregion Reset frame index or stay at last index

            # Animation transitions to idle
            if self.frames_list_name in [
                "stop",
                "land"
            ]:
                self.set_frames_list_name("idle")

            # Animation transitions to run
            elif self.frames_list_name in [
                "idle_run",
                "turn"
            ]:
                self.set_frames_list_name("run")

            # Animation transitions to down
            elif self.frames_list_name == "up_down":
                self.set_frames_list_name("down")

        # Update frame data
        self.frame_data = self.frames_list[self.frame_index]

        # Update frame data frame
        self.frame_data_frame = self.frame_data['frame']
        self.frame_tuple_region = (
            self.frame_data_frame['x'],
            self.frame_data_frame['y'],
            self.frame_data_frame['w'],
            self.frame_data_frame['h']
        )

        # Update frame data duration
        self.frame_duration = self.frame_data['duration']

    # Set frames_list_name
    def set_frames_list_name(self, value):
        # Update frame list name
        self.frames_list_name = value

        # Update frame list, len and index len
        self.frames_list = self.frames_dict[self.frames_list_name]
        self.frames_list_len = len(self.frames_list)
        self.frames_list_index_len = self.frames_list_len - 1

        # Reset frame index and dt
        self.total_dt = 0
        self.set_frame_index(0)

    # Set state
    def set_state(self, value):
        old_state = self.state
        self.state = value

        # From idle
        if old_state == "idle":
            # To run
            if self.state == "run":
                # region Handle turning
                if self.facing_direction == 1:
                    self.surface = self.sprite_sheet_surface
                elif self.facing_direction == -1:
                    self.surface = self.sprite_sheet_flipped_surface
                if self.old_facing_direction == self.facing_direction:
                    # Play run transition animation
                    self.set_frames_list_name("idle_run")
                elif self.old_facing_direction != self.facing_direction:
                    # Play turn to run transition animation
                    self.set_frames_list_name("turn")
                # endregion Handle turning

            # To crouch
            elif self.state == "crouch":
                # region Play crouch animation
                self.set_frames_list_name("crouch")
                # endregion Play crouch animation

            # To up
            elif self.state == "up":
                # region Set jump vel
                self.velocity.y = self.jump_vel
                # endregion Set jump vel

                # region Play up animation
                self.set_frames_list_name("up")
                # endregion Play up animation

        # From run
        elif old_state == "run":
            # To idle
            if self.state == "idle":
                # region Play stop animation
                self.set_frames_list_name("stop")
                # endregion Play stop animation

            # To crouch
            elif self.state == "crouch":
                # region Play crouch animation
                self.set_frames_list_name("crouch")
                # endregion Play crouch animation

            # To up
            elif self.state == "up":
                # region Set jump vel
                self.velocity.y = self.jump_vel
                # endregion Set jump vel

                # region Play up animation
                self.set_frames_list_name("up")
                # endregion Play up animation

            # To down
            elif self.state == "down":
                # region set Heavy gravity
                self.gravity = self.heavy_gravity
                # endregion set Heavy gravity

                # region Play up down transition animation
                self.set_frames_list_name("up_down")
                # endregion Play up down transition animation

        # From crouch
        elif old_state == "crouch":
            # To idle
            if self.state == "idle":
                # region Play idle animation
                self.set_frames_list_name("idle")
                # endregion Play idle animation

            # To run
            elif self.state == "run":
                # region Handle turning
                if self.facing_direction == 1:
                    self.surface = self.sprite_sheet_surface
                elif self.facing_direction == -1:
                    self.surface = self.sprite_sheet_flipped_surface
                if self.old_facing_direction == self.facing_direction:
                    # Play run transition animation
                    self.set_frames_list_name("idle_run")
                elif self.old_facing_direction != self.facing_direction:
                    # Play turn to run transition animation
                    self.set_frames_list_name("turn")
                # endregion Handle turning

            # To up
            elif self.state == "up":
                # region Set jump vel
                self.velocity.y = self.jump_vel
                # endregion Set jump vel

                # region Play up animation
                self.set_frames_list_name("up")
                # endregion Play up animation

        # From up
        elif old_state == "up":
            # To down
            if self.state == "down":
                # region set Heavy gravity
                self.gravity = self.heavy_gravity
                # endregion set Heavy gravity

                # region Play up down transition animation
                self.set_frames_list_name("up_down")
                # endregion Play up down transition animation

        # From down
        elif old_state == "down":
            # region Reset gravity
            self.gravity = self.normal_gravity
            # endregion Reset gravity

            # To idle
            if self.state == "idle":
                # region Play land animation
                self.set_frames_list_name("land")
                # endregion Play land animation

            # To run
            if self.state == "run":
                # region Handle turning
                if self.facing_direction == 1:
                    self.surface = self.sprite_sheet_surface
                elif self.facing_direction == -1:
                    self.surface = self.sprite_sheet_flipped_surface
                if self.old_facing_direction == self.facing_direction:
                    # Play run transition animation
                    self.set_frames_list_name("idle_run")
                elif self.old_facing_direction != self.facing_direction:
                    # Play turn to run transition animation
                    self.set_frames_list_name("turn")
                # endregion Handle turning

            # To crouch
            elif self.state == "crouch":
                # region Play crouch animation
                self.set_frames_list_name("crouch")
                # endregion Play crouch animation
