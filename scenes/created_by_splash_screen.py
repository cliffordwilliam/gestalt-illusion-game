import pygame as pg
from constants import *


class CreatedBySplashScreen:
    def __init__(self, game):
        # Game
        self.game = game

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
        self.can_fade_out = False
        self.screen_time = 2000

        # Logo
        self.logo_text = "made by clifford william"
        self.logo_rect = FONT.get_rect(self.logo_text)
        self.logo_rect.center = NATIVE_RECT.center

        # Tips text
        self.tips_text = "press any key to skip"
        self.tips_rect = FONT.get_rect(self.tips_text)
        self.tips_rect.bottomright = NATIVE_RECT.bottomright
        self.tips_rect.x -= TILE_S
        self.tips_rect.y -= TILE_S

        # Delays
        self.end_sleep_time = 500
        self.start_sleep_time = 500

    def event(self, event):
        # Press any key to fade early
        if event.type == pg.KEYUP:
            if self.can_fade_out == True:
                self.direction *= -1
                self.can_fade_out = False

    def update(self, dt):
        # Start delay
        if self.start_sleep_time > 0:
            self.start_sleep_time -= dt
            if self.start_sleep_time < 0:
                self.can_fade_out = True
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

        # End reached?
        if self.alpha == 0:
            # Player cannot fade out early
            self.can_fade_out = False
            # Wait for logo screen time before reversing
            self.screen_time -= dt
            if self.screen_time < 0:
                self.direction *= -1

        # Other end reached?
        elif self.alpha == 255:
            self.end_sleep_time -= dt
            if self.end_sleep_time < 0:
                self.game.set_scene("MadeWithSplashScreen")

    def draw(self, NATIVE_SURF):
        # Draw logo
        FONT.render_to(NATIVE_SURF, self.logo_rect, self.logo_text, "white")

        # Draw tips text
        FONT.render_to(NATIVE_SURF, self.tips_rect, self.tips_text, "white")

        # Draw curtain
        NATIVE_SURF.blit(self.curtain, (0, 0))
