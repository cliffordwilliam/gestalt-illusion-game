from constants import *


class Test:
    def __init__(self, game):
        # self.sprite_sheet = pg.image.load(SPRITE_SHEET_1_PATH).convert_alpha()
        self.cam_rect = pg.Rect(0, 0, NATIVE_W, NATIVE_H)

    def event(self, event):
        if event.type == pg.KEYDOWN:
            print(event.key)

    def update(self, dt):
        pass

    def draw(self, NATIVE_SURF):
        # Fill native
        NATIVE_SURF.fill("red")
