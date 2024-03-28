from constants import *


class MenuScreen:
    def __init__(self, game):
        # Game
        self.game = game

        # Main menu background init
        self.main_menu_bg = pg.image.load(MAIN_MENU_PATH).convert_alpha()

        # Curtain init
        self.curtain = pg.Surface((NATIVE_W, NATIVE_H))
        self.curtain.fill("black")

        # Start full
        self.curtain.set_alpha(255)
        self.alpha = 255
        self.fade_duration = 500
        self.fade_timer = 500
        self.direction = -1
        self.remainder = 0

        # Button rects
        self.button_rects = []

        # Start button
        self.start_text = "start"
        self.start_rect = FONT.get_rect(self.start_text)
        self.start_rect.bottomleft = NATIVE_RECT.bottomleft
        self.start_rect.x += FONT_W * 12
        self.start_rect.y -= FONT_H * 10
        self.start_bg_rect = self.start_rect.inflate(6, 6)
        self.button_rects.append(self.start_bg_rect)

        # Options button
        self.options_text = "options"
        self.options_rect = FONT.get_rect(self.options_text)
        self.options_rect.bottomleft = NATIVE_RECT.bottomleft
        self.options_rect.x += FONT_W * 12
        self.options_rect.y -= FONT_H * 8
        self.options_bg_rect = self.options_rect.inflate(6, 6)
        self.button_rects.append(self.options_bg_rect)

        # Exit button
        self.exit_text = "exit"
        self.exit_rect = FONT.get_rect(self.exit_text)
        self.exit_rect.bottomleft = NATIVE_RECT.bottomleft
        self.exit_rect.x += FONT_W * 12
        self.exit_rect.y -= FONT_H * 6
        self.exit_bg_rect = self.exit_rect.inflate(6, 6)
        self.button_rects.append(self.exit_bg_rect)

        # Button rects len
        self.button_rects_len = len(self.button_rects)

        # Delays
        self.end_sleep_time = 500
        self.start_sleep_time = 500

        # Menu input
        self.is_input_allowed = False
        self.index = 0

        # Tips text
        enter = pg.key.name(self.game.key_bindings["enter"])
        up = pg.key.name(self.game.key_bindings["up"])
        down = pg.key.name(self.game.key_bindings["down"])
        left = pg.key.name(self.game.key_bindings["left"])
        right = pg.key.name(self.game.key_bindings["right"])
        self.tips_text = f'select: {enter}, navigate: {
            up}, {down}, {left}, {right}'
        self.tips_rect = FONT.get_rect(self.tips_text)
        self.tips_rect.bottomright = NATIVE_RECT.bottomright
        self.tips_rect.x -= TILE_S
        self.tips_rect.y -= TILE_S

    def event(self, event):
        # Block when fading
        if self.is_input_allowed == False:
            return

        # Input navigation / select
        if event.type == pg.KEYUP:
            # Go up
            if event.key == self.game.key_bindings["up"]:
                self.index -= 1
                self.index = self.index % self.button_rects_len

            # Go down
            if event.key == self.game.key_bindings["down"]:
                self.index += 1
                self.index = self.index % self.button_rects_len

            # Enter press
            elif event.key == self.game.key_bindings["enter"]:
                # Options button pressed
                if self.index == 1:
                    # Activate option event and update
                    self.game.is_option_screen = True
                    return

                # Block input
                self.is_input_allowed = False

                # Start fade
                self.direction *= -1

    def update(self, dt):
        # Start delay
        if self.start_sleep_time > 0:
            self.start_sleep_time -= dt
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
            self.is_input_allowed = True

        # Other end reached?
        if self.alpha == 255:
            # Wait for end delay
            self.end_sleep_time -= dt
            if self.end_sleep_time < 0:
                # Start button pressed
                if self.index == 0:
                    self.game.set_scene("SaveScreen")

                # Exit button pressed
                elif self.index == 2:
                    pg.quit()
                    exit()

    def draw(self, NATIVE_SURF):
        # Draw main menu background
        NATIVE_SURF.blit(self.main_menu_bg, (0, 0))

        # Draw start button
        pg.draw.rect(NATIVE_SURF, "black", self.start_bg_rect)
        FONT.render_to(NATIVE_SURF, self.start_rect, self.start_text, "white")

        # Draw options button
        pg.draw.rect(NATIVE_SURF, "black", self.options_bg_rect)
        FONT.render_to(NATIVE_SURF, self.options_rect,
                       self.options_text, "white")

        # Draw exit button
        pg.draw.rect(NATIVE_SURF, "black", self.exit_bg_rect)
        FONT.render_to(NATIVE_SURF, self.exit_rect,
                       self.exit_text, "white")

        # Draw tips text
        enter = pg.key.name(self.game.key_bindings["enter"])
        up = pg.key.name(self.game.key_bindings["up"])
        down = pg.key.name(self.game.key_bindings["down"])
        left = pg.key.name(self.game.key_bindings["left"])
        right = pg.key.name(self.game.key_bindings["right"])
        self.tips_text = f'select: {enter}, navigate: {
            up}, {down}, {left}, {right}'
        self.tips_rect = FONT.get_rect(self.tips_text)
        self.tips_rect.bottomright = NATIVE_RECT.bottomright
        self.tips_rect.x -= TILE_S
        self.tips_rect.y -= TILE_S
        FONT.render_to(NATIVE_SURF, self.tips_rect,
                       self.tips_text, "white", "black")

        # Draw cursor
        if self.is_input_allowed == True:
            cursor_rect = self.button_rects[self.index]
            pg.draw.rect(NATIVE_SURF, "white", cursor_rect, 1)

        # Draw curtain
        NATIVE_SURF.blit(self.curtain, (0, 0))
