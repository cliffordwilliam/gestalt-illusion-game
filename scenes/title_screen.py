from constants import *


class TitleScreen:
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
        self.can_skip_fade_out = False

        # Logo
        self.logo_text = "gestalt illusion"
        self.logo_rect = FONT.get_rect(self.logo_text)
        self.logo_rect.center = NATIVE_RECT.center

        # Prompt
        self.prompt_text = "press any key"
        self.prompt_rect = FONT.get_rect(self.prompt_text)
        self.prompt_rect.center = NATIVE_RECT.center
        self.prompt_rect.y += FONT_H * 2

        # Prompt blink
        self.prompt_alpha = 0
        self.prompt_fade_duration = 1000
        self.prompt_fade_timer = 0
        self.prompt_direction = 1
        self.prompt_remainder = 0

        # Delays
        self.end_sleep_time = 500
        self.start_sleep_time = 500

    def event(self, event):
        # Press any key to fade early
        if event.type == pg.KEYUP:
            if self.can_skip_fade_out == True:
                self.can_skip_fade_out = False
                self.fade_timer = 0

            # End reached? Go the other way
            elif self.fade_timer == 0:
                self.direction *= -1
                self.prompt_alpha = 255

    def update(self, dt):
        # Start delay
        if self.start_sleep_time > 0:
            self.start_sleep_time -= dt
            if self.start_sleep_time < 0:
                self.can_skip_fade_out = True
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
            # Update timer with direction and dt, go left or right
            self.prompt_fade_timer += dt * self.prompt_direction
            # Clamp timer
            self.prompt_fade_timer = max(
                0, min(self.prompt_fade_duration, self.prompt_fade_timer))
            # Use timer as position
            fraction = self.prompt_fade_timer / self.prompt_fade_duration
            # Use position to update alpha value
            lerp_alpha = pg.math.lerp(0, 122, fraction)
            # Add prev round float loss
            lerp_alpha += self.prompt_remainder
            # Round to int
            self.prompt_alpha = max(0, min(122, round(lerp_alpha)))
            # Collect round loss
            self.prompt_remainder = lerp_alpha - self.prompt_alpha
            # Bounce on either end
            if self.prompt_alpha == 0 or self.prompt_alpha == 122:
                self.prompt_direction *= -1

        # Other end reached?
        if self.fade_timer == 1000:
            self.end_sleep_time -= dt
            if self.end_sleep_time < 0:
                self.game.set_scene("MenuScreen")

    def draw(self, NATIVE_SURF):
        # Draw logo
        FONT.render_to(NATIVE_SURF, self.logo_rect, self.logo_text, "white")

        # Draw prompt
        FONT.render_to(NATIVE_SURF, self.prompt_rect,
                       self.prompt_text, (255, 255, 255, self.prompt_alpha))

        # Draw curtain
        NATIVE_SURF.blit(self.curtain, (0, 0))
