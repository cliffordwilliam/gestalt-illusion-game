from constants import *


class SaveScreen:
    def __init__(self, game):
        # Game
        self.game = game

        # Save background init
        self.save_bg = pg.Surface((NATIVE_W, NATIVE_H))

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

        # Title text
        self.title_text = "game data"
        self.title_rect = FONT.get_rect(self.title_text)
        self.title_rect.x += FONT_W * 12
        self.title_rect.y = FONT_H * 2

        # Data 1 options
        self.data_options = [
            "Load",
            "Delete",
            "Cancel",
        ]
        self.data_options_len = len(self.data_options)

        # Data 1 button
        self.data_1_text = "data 1"
        self.data_1_rect = FONT.get_rect(self.data_1_text)
        self.data_1_rect.x += FONT_W * 12
        self.data_1_rect.y += FONT_H * 4
        self.data_1_bg_rect = self.data_1_rect.inflate(6, 6)
        self.button_rects.append(self.data_1_bg_rect)
        self.data_1_index = 0

        # Data 1 value text
        self.data_1_value_text = self.data_options[self.data_1_index]
        self.data_1_value_rect = FONT.get_rect(self.data_1_value_text)
        self.data_1_value_rect.right = NATIVE_RECT.right
        self.data_1_value_rect.x -= FONT_W * 12
        self.data_1_value_rect.y += FONT_H * 4
        self.data_1_value_bg_rect = self.data_1_value_rect.inflate(
            6, 6)

        # Data 2 button
        self.data_2_text = "data 2"
        self.data_2_rect = FONT.get_rect(self.data_2_text)
        self.data_2_rect.x += FONT_W * 12
        self.data_2_rect.y += FONT_H * 6
        self.data_2_bg_rect = self.data_2_rect.inflate(6, 6)
        self.button_rects.append(self.data_2_bg_rect)
        self.data_2_index = 0

        # Data 2 value text
        self.data_2_value_text = self.data_options[self.data_2_index]
        self.data_2_value_rect = FONT.get_rect(self.data_2_value_text)
        self.data_2_value_rect.right = NATIVE_RECT.right
        self.data_2_value_rect.x -= FONT_W * 12
        self.data_2_value_rect.y += FONT_H * 6
        self.data_2_value_bg_rect = self.data_2_value_rect.inflate(
            6, 6)

        # Data 3 button
        self.data_3_text = "data 3"
        self.data_3_rect = FONT.get_rect(self.data_3_text)
        self.data_3_rect.x += FONT_W * 12
        self.data_3_rect.y += FONT_H * 8
        self.data_3_bg_rect = self.data_3_rect.inflate(6, 6)
        self.button_rects.append(self.data_3_bg_rect)
        self.data_3_index = 0

        # Data 3 value text
        self.data_3_value_text = self.data_options[self.data_3_index]
        self.data_3_value_rect = FONT.get_rect(self.data_3_value_text)
        self.data_3_value_rect.right = NATIVE_RECT.right
        self.data_3_value_rect.x -= FONT_W * 12
        self.data_3_value_rect.y += FONT_H * 8
        self.data_3_value_bg_rect = self.data_3_value_rect.inflate(
            6, 6)

        # Back button
        self.back_text = "back"
        self.back_rect = FONT.get_rect(self.back_text)
        self.back_rect.x += FONT_W * 12
        self.back_rect.y += FONT_H * 32
        self.back_bg_rect = self.back_rect.inflate(6, 6)
        self.button_rects.append(self.back_bg_rect)

        # Button rects len
        self.button_rects_len = len(self.button_rects)

        # Delays
        self.end_sleep_time = 500
        self.start_sleep_time = 500

        # Menu input
        self.is_input_allowed = False
        self.index = 0

        # State
        self.state = "Normal"

    def event(self, event):
        # Block input when fading
        if self.is_input_allowed == False:
            return

        # Input navigation / select
        if event.type == pg.KEYUP:
            if self.state == "Normal":
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
                    # Data 1 button pressed
                    if self.index == 0:
                        # Data 1 state
                        self.state = "Data1"
                        self.data_1_value_text = f'<{
                            self.data_options[self.data_1_index]}>'
                        self.data_1_value_rect = FONT.get_rect(
                            self.data_1_value_text)
                        self.data_1_value_rect.right = NATIVE_RECT.right
                        self.data_1_value_rect.x -= FONT_W * 12
                        self.data_1_value_rect.y += FONT_H * 4
                        self.data_1_value_bg_rect = self.data_1_value_rect.inflate(
                            6, 6)

                    # Data 2 button pressed
                    elif self.index == 1:
                        # Data 1 state
                        self.state = "Data2"
                        self.data_2_value_text = f'<{
                            self.data_options[self.data_2_index]}>'
                        self.data_2_value_rect = FONT.get_rect(
                            self.data_2_value_text)
                        self.data_2_value_rect.right = NATIVE_RECT.right
                        self.data_2_value_rect.x -= FONT_W * 12
                        self.data_2_value_rect.y += FONT_H * 6
                        self.data_2_value_bg_rect = self.data_2_value_rect.inflate(
                            6, 6)

                    # Data 3 button pressed
                    elif self.index == 2:
                        # Data 1 state
                        self.state = "Data3"
                        self.data_3_value_text = f'<{
                            self.data_options[self.data_3_index]}>'
                        self.data_3_value_rect = FONT.get_rect(
                            self.data_3_value_text)
                        self.data_3_value_rect.right = NATIVE_RECT.right
                        self.data_3_value_rect.x -= FONT_W * 12
                        self.data_3_value_rect.y += FONT_H * 8
                        self.data_3_value_bg_rect = self.data_3_value_rect.inflate(
                            6, 6)

                    # Back button pressed
                    elif self.index == self.button_rects_len - 1:
                        self.is_input_allowed = False
                        self.direction *= -1

            elif self.state == "Data1":
                # Enter press
                if event.key == self.game.key_bindings["enter"]:
                    # Load Data 1
                    if self.data_1_index == 0:
                        print("LOAD DATA 1 JSON")

                        # Block input
                        self.is_input_allowed = False

                        # Start fade
                        self.direction *= -1

                    # Delete Data 1
                    elif self.data_1_index == 1:
                        print("DELETE DATA 1 JSON")

                        # Block input
                        self.is_input_allowed = False

                        # Start fade
                        self.direction *= -1

                    # Cancel Data 1
                    elif self.data_1_index == 2:
                        print("CANCEL")
                        self.data_1_value_text = self.data_options[0]
                        self.data_1_value_rect = FONT.get_rect(
                            self.data_1_value_text)
                        self.data_1_value_rect.right = NATIVE_RECT.right
                        self.data_1_value_rect.x -= FONT_W * 12
                        self.data_1_value_rect.y += FONT_H * 4
                        self.data_1_value_bg_rect = self.data_1_value_rect.inflate(
                            6, 6)
                        self.state = "Normal"

                # Go left data 1
                if event.key == self.game.key_bindings["left"]:
                    self.data_1_index -= 1
                    self.data_1_index = self.data_1_index % self.data_options_len
                    self.data_1_value_text = f'<{
                        self.data_options[self.data_1_index]}>'
                    self.data_1_value_rect = FONT.get_rect(
                        self.data_1_value_text)
                    self.data_1_value_rect.right = NATIVE_RECT.right
                    self.data_1_value_rect.x -= FONT_W * 12
                    self.data_1_value_rect.y += FONT_H * 4
                    self.data_1_value_bg_rect = self.data_1_value_rect.inflate(
                        6, 6)

                # Go right data 1
                if event.key == self.game.key_bindings["right"]:
                    self.data_1_index += 1
                    self.data_1_index = self.data_1_index % self.data_options_len
                    self.data_1_value_text = f'<{
                        self.data_options[self.data_1_index]}>'
                    self.data_1_value_rect = FONT.get_rect(
                        self.data_1_value_text)
                    self.data_1_value_rect.right = NATIVE_RECT.right
                    self.data_1_value_rect.x -= FONT_W * 12
                    self.data_1_value_rect.y += FONT_H * 4
                    self.data_1_value_bg_rect = self.data_1_value_rect.inflate(
                        6, 6)

            elif self.state == "Data2":
                # Enter press
                if event.key == self.game.key_bindings["enter"]:
                    # Load Data 2
                    if self.data_2_index == 0:
                        print("LOAD DATA 2 JSON")

                        # Block input
                        self.is_input_allowed = False

                        # Start fade
                        self.direction *= -1

                    # Delete Data 2
                    elif self.data_2_index == 1:
                        print("DELETE DATA 2 JSON")

                        # Block input
                        self.is_input_allowed = False

                        # Start fade
                        self.direction *= -1

                    # Cancel Data 2
                    elif self.data_2_index == 2:
                        print("CANCEL")
                        self.data_2_value_text = self.data_options[0]
                        self.data_2_value_rect = FONT.get_rect(
                            self.data_2_value_text)
                        self.data_2_value_rect.right = NATIVE_RECT.right
                        self.data_2_value_rect.x -= FONT_W * 12
                        self.data_2_value_rect.y += FONT_H * 6
                        self.data_2_value_bg_rect = self.data_2_value_rect.inflate(
                            6, 6)
                        self.state = "Normal"

                # Go left data 2
                if event.key == self.game.key_bindings["left"]:
                    self.data_2_index -= 1
                    self.data_2_index = self.data_2_index % self.data_options_len
                    self.data_2_value_text = f'<{
                        self.data_options[self.data_2_index]}>'
                    self.data_2_value_rect = FONT.get_rect(
                        self.data_2_value_text)
                    self.data_2_value_rect.right = NATIVE_RECT.right
                    self.data_2_value_rect.x -= FONT_W * 12
                    self.data_2_value_rect.y += FONT_H * 6
                    self.data_2_value_bg_rect = self.data_2_value_rect.inflate(
                        6, 6)

                # Go right data 2
                if event.key == self.game.key_bindings["right"]:
                    self.data_2_index += 1
                    self.data_2_index = self.data_2_index % self.data_options_len
                    self.data_2_value_text = f'<{
                        self.data_options[self.data_2_index]}>'
                    self.data_2_value_rect = FONT.get_rect(
                        self.data_2_value_text)
                    self.data_2_value_rect.right = NATIVE_RECT.right
                    self.data_2_value_rect.x -= FONT_W * 12
                    self.data_2_value_rect.y += FONT_H * 6
                    self.data_2_value_bg_rect = self.data_2_value_rect.inflate(
                        6, 6)

            elif self.state == "Data3":
                # Enter press
                if event.key == self.game.key_bindings["enter"]:
                    # Load Data 3
                    if self.data_3_index == 0:
                        print("LOAD DATA 3 JSON")

                        # Block input
                        self.is_input_allowed = False

                        # Start fade
                        self.direction *= -1

                    # Delete Data 3
                    elif self.data_3_index == 1:
                        print("DELETE DATA 3 JSON")

                        # Block input
                        self.is_input_allowed = False

                        # Start fade
                        self.direction *= -1

                    # Cancel Data 3
                    elif self.data_3_index == 2:
                        print("CANCEL")
                        self.data_3_value_text = self.data_options[0]
                        self.data_3_value_rect = FONT.get_rect(
                            self.data_3_value_text)
                        self.data_3_value_rect.right = NATIVE_RECT.right
                        self.data_3_value_rect.x -= FONT_W * 12
                        self.data_3_value_rect.y += FONT_H * 8
                        self.data_3_value_bg_rect = self.data_3_value_rect.inflate(
                            6, 6)
                        self.state = "Normal"

                # Go left data 3
                if event.key == self.game.key_bindings["left"]:
                    self.data_3_index -= 1
                    self.data_3_index = self.data_3_index % self.data_options_len
                    self.data_3_value_text = f'<{
                        self.data_options[self.data_3_index]}>'
                    self.data_3_value_rect = FONT.get_rect(
                        self.data_3_value_text)
                    self.data_3_value_rect.right = NATIVE_RECT.right
                    self.data_3_value_rect.x -= FONT_W * 12
                    self.data_3_value_rect.y += FONT_H * 8
                    self.data_3_value_bg_rect = self.data_3_value_rect.inflate(
                        6, 6)

                # Go right data 3
                if event.key == self.game.key_bindings["right"]:
                    self.data_3_index += 1
                    self.data_3_index = self.data_3_index % self.data_options_len
                    self.data_3_value_text = f'<{
                        self.data_options[self.data_3_index]}>'
                    self.data_3_value_rect = FONT.get_rect(
                        self.data_3_value_text)
                    self.data_3_value_rect.right = NATIVE_RECT.right
                    self.data_3_value_rect.x -= FONT_W * 12
                    self.data_3_value_rect.y += FONT_H * 8
                    self.data_3_value_bg_rect = self.data_3_value_rect.inflate(
                        6, 6)

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
                # Data 1 button pressed
                if self.index == 0:
                    self.game.set_scene("IntroCutscene")

                # Data 2 button pressed
                elif self.index == 1:
                    self.game.set_scene("IntroCutscene")

                # Data 3 button pressed
                elif self.index == 2:
                    self.game.set_scene("IntroCutscene")

                # Back button pressed
                elif self.index == self.button_rects_len - 1:
                    self.game.set_scene("MenuScreen")

    def draw(self, NATIVE_SURF):
        # Draw save background
        NATIVE_SURF.blit(self.save_bg, (0, 0))

        # Draw title
        FONT.render_to(NATIVE_SURF, self.title_rect, self.title_text, "white")

        # Draw data 1 button
        pg.draw.rect(NATIVE_SURF, "black", self.data_1_bg_rect)
        FONT.render_to(NATIVE_SURF, self.data_1_rect,
                       self.data_1_text, "white")

        # Draw data 1 value
        pg.draw.rect(NATIVE_SURF, "black", self.data_1_value_bg_rect)
        FONT.render_to(NATIVE_SURF, self.data_1_value_rect,
                       self.data_1_value_text, "white")

        # Draw data 2 button
        pg.draw.rect(NATIVE_SURF, "black", self.data_2_bg_rect)
        FONT.render_to(NATIVE_SURF, self.data_2_rect,
                       self.data_2_text, "white")

        # Draw data 2 value
        pg.draw.rect(NATIVE_SURF, "black", self.data_2_value_bg_rect)
        FONT.render_to(NATIVE_SURF, self.data_2_value_rect,
                       self.data_2_value_text, "white")

        # Draw data 3 button
        pg.draw.rect(NATIVE_SURF, "black", self.data_3_bg_rect)
        FONT.render_to(NATIVE_SURF, self.data_3_rect,
                       self.data_3_text, "white")

        # Draw data 3 value
        pg.draw.rect(NATIVE_SURF, "black", self.data_3_value_bg_rect)
        FONT.render_to(NATIVE_SURF, self.data_3_value_rect,
                       self.data_3_value_text, "white")

        # Draw back button
        pg.draw.rect(NATIVE_SURF, "black", self.back_bg_rect)
        FONT.render_to(NATIVE_SURF, self.back_rect,
                       self.back_text, "white")

        # Draw cursor
        if self.is_input_allowed == True:
            if self.state == "Normal":
                cursor_rect = self.button_rects[self.index]
                pg.draw.rect(NATIVE_SURF, "white", cursor_rect, 1)

            elif self.state == "Data1":
                pg.draw.rect(NATIVE_SURF, "white",
                             self.data_1_value_bg_rect, 1)

        # Draw curtain
        NATIVE_SURF.blit(self.curtain, (0, 0))
