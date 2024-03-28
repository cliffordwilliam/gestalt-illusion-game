import pygame as pg
from os.path import join
import pygame.freetype as font
from json import load

pg.init()

SETTING_PATH = join("saves", "settings.json")
FONT_PATH = join("assets", "cg_pixel_3x5_mono.ttf")
MAIN_MENU_PATH = join("assets", "main_menu.png")
ROOM_PATHS = {
    "bedroom": join("room_json_data", "stage_1", "bedroom.json"),
    "bedroom_balcony": join("room_json_data", "stage_1", "bedroom_balcony.json")
}
SPRITE_SHEET_PATHS = {
    "stage_1_sprite_sheet.png": join("assets", "stage_1_sprite_sheet.png")
}
TILE_S = 16
FONT_H = 5
FONT_W = 3
FPS = 60
NATIVE_W = 320
NATIVE_H = 176
FONT = font.Font(FONT_PATH, FONT_H)
NATIVE_SURF = pg.Surface((NATIVE_W, NATIVE_H))
NATIVE_RECT = NATIVE_SURF.get_rect()
CLOCK = pg.time.Clock()
EVENTS = [pg.KEYDOWN, pg.KEYUP, pg.QUIT]
