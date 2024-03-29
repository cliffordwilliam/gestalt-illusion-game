from constants import *


class Fire:
    def __init__(self, game, cam_rect, sprite_sheet_surface, x, y):
        # Position
        self.x = x
        self.y = y

        # Game
        self.game = game

        # Cam rect
        self.cam_rect = cam_rect

        # Name
        self.name = "Fire"

        # Sprite sheet surface
        self.sprite_sheet_surface = sprite_sheet_surface

        # Object sprite sheet regions
        self.frames_dict = {}
        with open(ACTORS_JSON_DATA_PATHS["fire_sprite_sheet.json"], 'r') as file:
            self.frames_dict = load(file)

        # Object frames list name
        self.frames_list_name = "burn"
        self.frames_list = self.frames_dict[self.frames_list_name]
        self.frames_list_len = len(self.frames_list)
        self.frames_list_index_len = self.frames_list_len - 1

        # Object frame index
        self.frame_index = 0
        self.frame_index = random.randint(
            self.frame_index, self.frames_list_index_len)
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

    # Object update
    def update(self, dt):
        # region update total dt, set frame index
        self.total_dt += dt
        if self.total_dt >= self.frame_duration:
            self.total_dt = 0
            self.set_frame_index(self.frame_index + 1)

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
        # endregion update total dt, set frame index

    # Set frame_index
    def set_frame_index(self, value):
        # Update frame index
        self.frame_index = value

        # On last frame?
        if self.frame_index > self.frames_list_index_len:
            self.frame_index = 0

    # Set state
    def draw(self, NATIVE_SURF):
        # Only update sprites that are in view
        if (self.cam_rect.x - 16 <= self.x < self.cam_rect.right) and (self.cam_rect.y - 16 <= self.y < self.cam_rect.bottom):
            # region Render a region of the player sprite sheet
            NATIVE_SURF.blit(
                self.sprite_sheet_surface,
                (
                    (self.x) - self.cam_rect.x,
                    (self.y) - self.cam_rect.y
                ),
                self.frame_tuple_region
            )
            # endregion Render a region of the player sprite sheet
