from constants import *
from json import dump


class OptionsScreen:
    def __init__(self, game):
        # Game
        self.game = game

        # Curtain init
        self.curtain = pg.Surface((NATIVE_W, NATIVE_H))
        self.curtain.fill("black")

        # Start full
        self.curtain.set_alpha(0)
        self.alpha = 0
        self.fade_duration = 125
        self.fade_timer = 0
        self.direction = 1
        self.remainder = 0

        # Button rects
        self.button_rects = []

        # Title text
        self.title_text = "options"
        self.title_rect = FONT.get_rect(self.title_text)
        self.title_rect.center = NATIVE_RECT.center
        self.title_rect.y = FONT_H * 2

        # Resolution button
        self.resolution_text = "resolution"
        self.resolution_rect = FONT.get_rect(self.resolution_text)
        self.resolution_rect.right = NATIVE_RECT.center[0] - 3
        self.resolution_rect.y += FONT_H * 4
        self.resolution_bg_rect = self.resolution_rect.inflate(6, 6)
        self.button_rects.append(self.resolution_bg_rect)

        # Resolution options
        self.resolutions = [
            "320 x 176",
            "640 x 352",
            "960 x 528",
            "1280 x 704"
        ]
        self.resolution_index = self.game.resolution - 1
        self.resolutions_len = len(self.resolutions)

        # Resolution value text
        self.resolution_value_text = self.resolutions[self.resolution_index]
        self.resolution_value_rect = FONT.get_rect(self.resolution_value_text)
        self.resolution_value_rect.left = NATIVE_RECT.center[0] + 3
        self.resolution_value_rect.y += FONT_H * 4
        self.resolution_value_bg_rect = self.resolution_value_rect.inflate(
            6, 6)

        # Up input button
        self.up_input_text = "up_input"
        self.up_input_rect = FONT.get_rect(self.up_input_text)
        self.up_input_rect.right = NATIVE_RECT.center[0] - 3
        self.up_input_rect.y += FONT_H * 6
        self.up_input_bg_rect = self.up_input_rect.inflate(6, 6)
        self.button_rects.append(self.up_input_bg_rect)

        # Up input value text
        self.up_input_value_text = pg.key.name(self.game.key_bindings["up"])
        self.up_input_value_rect = FONT.get_rect(self.up_input_value_text)
        self.up_input_value_rect.left = NATIVE_RECT.center[0] + 3
        self.up_input_value_rect.y += FONT_H * 6
        self.up_input_value_bg_rect = self.up_input_value_rect.inflate(
            6, 6)

        # Down input button
        self.down_input_text = "down_input"
        self.down_input_rect = FONT.get_rect(self.down_input_text)
        self.down_input_rect.right = NATIVE_RECT.center[0] - 3
        self.down_input_rect.y += FONT_H * 8
        self.down_input_bg_rect = self.down_input_rect.inflate(6, 6)
        self.button_rects.append(self.down_input_bg_rect)

        # Down input value text
        self.down_input_value_text = pg.key.name(
            self.game.key_bindings["down"])
        self.down_input_value_rect = FONT.get_rect(self.down_input_value_text)
        self.down_input_value_rect.left = NATIVE_RECT.center[0] + 3
        self.down_input_value_rect.y += FONT_H * 8
        self.down_input_value_bg_rect = self.down_input_value_rect.inflate(
            6, 6)

        # Right input button
        self.right_input_text = "right_input"
        self.right_input_rect = FONT.get_rect(self.right_input_text)
        self.right_input_rect.right = NATIVE_RECT.center[0] - 3
        self.right_input_rect.y += FONT_H * 10
        self.right_input_bg_rect = self.right_input_rect.inflate(6, 6)
        self.button_rects.append(self.right_input_bg_rect)

        # Right input value text
        self.right_input_value_text = pg.key.name(
            self.game.key_bindings["right"])
        self.right_input_value_rect = FONT.get_rect(
            self.right_input_value_text)
        self.right_input_value_rect.left = NATIVE_RECT.center[0] + 3
        self.right_input_value_rect.y += FONT_H * 10
        self.right_input_value_bg_rect = self.right_input_value_rect.inflate(
            6, 6)

        # Left input button
        self.left_input_text = "left_input"
        self.left_input_rect = FONT.get_rect(self.left_input_text)
        self.left_input_rect.right = NATIVE_RECT.center[0] - 3
        self.left_input_rect.y += FONT_H * 12
        self.left_input_bg_rect = self.left_input_rect.inflate(6, 6)
        self.button_rects.append(self.left_input_bg_rect)

        # Left input value text
        self.left_input_value_text = pg.key.name(
            self.game.key_bindings["left"])
        self.left_input_value_rect = FONT.get_rect(
            self.left_input_value_text)
        self.left_input_value_rect.left = NATIVE_RECT.center[0] + 3
        self.left_input_value_rect.y += FONT_H * 12
        self.left_input_value_bg_rect = self.left_input_value_rect.inflate(
            6, 6)

        # Enter input button
        self.enter_input_text = "enter_input"
        self.enter_input_rect = FONT.get_rect(self.enter_input_text)
        self.enter_input_rect.right = NATIVE_RECT.center[0] - 3
        self.enter_input_rect.y += FONT_H * 14
        self.enter_input_bg_rect = self.enter_input_rect.inflate(6, 6)
        self.button_rects.append(self.enter_input_bg_rect)

        # Enter input value text
        self.enter_input_value_text = pg.key.name(
            self.game.key_bindings["enter"])
        self.enter_input_value_rect = FONT.get_rect(
            self.enter_input_value_text)
        self.enter_input_value_rect.left = NATIVE_RECT.center[0] + 3
        self.enter_input_value_rect.y += FONT_H * 14
        self.enter_input_value_bg_rect = self.enter_input_value_rect.inflate(
            6, 6)

        # Pause input button
        self.pause_input_text = "pause_input"
        self.pause_input_rect = FONT.get_rect(self.pause_input_text)
        self.pause_input_rect.right = NATIVE_RECT.center[0] - 3
        self.pause_input_rect.y += FONT_H * 16
        self.pause_input_bg_rect = self.pause_input_rect.inflate(6, 6)
        self.button_rects.append(self.pause_input_bg_rect)

        # Pause input value text
        self.pause_input_value_text = pg.key.name(
            self.game.key_bindings["pause"])
        self.pause_input_value_rect = FONT.get_rect(
            self.pause_input_value_text)
        self.pause_input_value_rect.left = NATIVE_RECT.center[0] + 3
        self.pause_input_value_rect.y += FONT_H * 16
        self.pause_input_value_bg_rect = self.pause_input_value_rect.inflate(
            6, 6)

        # Jump input button
        self.jump_input_text = "jump_input"
        self.jump_input_rect = FONT.get_rect(self.jump_input_text)
        self.jump_input_rect.right = NATIVE_RECT.center[0] - 3
        self.jump_input_rect.y += FONT_H * 18
        self.jump_input_bg_rect = self.jump_input_rect.inflate(6, 6)
        self.button_rects.append(self.jump_input_bg_rect)

        # Jump input value text
        self.jump_input_value_text = pg.key.name(
            self.game.key_bindings["jump"])
        self.jump_input_value_rect = FONT.get_rect(
            self.jump_input_value_text)
        self.jump_input_value_rect.left = NATIVE_RECT.center[0] + 3
        self.jump_input_value_rect.y += FONT_H * 18
        self.jump_input_value_bg_rect = self.jump_input_value_rect.inflate(
            6, 6)

        # Apply button
        self.apply_text = "apply"
        self.apply_rect = FONT.get_rect(self.apply_text)
        self.apply_rect.right = NATIVE_RECT.center[0] - 3
        self.apply_rect.y += FONT_H * 30
        self.apply_bg_rect = self.apply_rect.inflate(6, 6)
        self.button_rects.append(self.apply_bg_rect)

        # Back button
        self.back_text = "back"
        self.back_rect = FONT.get_rect(self.back_text)
        self.back_rect.right = NATIVE_RECT.center[0] - 3
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

        if event.type == pg.KEYUP:
            if self.state == "Normal":
                # Press esc, block input fade
                if event.key == self.game.key_bindings["pause"]:
                    self.is_input_allowed = False
                    self.direction *= -1

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
                    # Resolution button pressed
                    if self.index == 0:
                        # Resolution state
                        self.state = "Resolution"
                        self.resolution_value_text = f'<{
                            self.resolutions[self.resolution_index]}>'
                        self.resolution_value_rect = FONT.get_rect(
                            self.resolution_value_text)
                        self.resolution_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.resolution_value_rect.y += FONT_H * 4
                        self.resolution_value_bg_rect = self.resolution_value_rect.inflate(
                            6, 6)

                    # Up input button pressed
                    if self.index == 1:
                        # UpInput state
                        self.state = "UpInput"
                        self.up_input_value_text = "Press any key to rebind"
                        self.up_input_value_rect = FONT.get_rect(
                            self.up_input_value_text)
                        self.up_input_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.up_input_value_rect.y += FONT_H * 6
                        self.up_input_value_bg_rect = self.up_input_value_rect.inflate(
                            6, 6)

                    # Down input button pressed
                    if self.index == 2:
                        # DownInput state
                        self.state = "DownInput"
                        self.down_input_value_text = "Press any key to rebind"
                        self.down_input_value_rect = FONT.get_rect(
                            self.down_input_value_text)
                        self.down_input_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.down_input_value_rect.y += FONT_H * 8
                        self.down_input_value_bg_rect = self.down_input_value_rect.inflate(
                            6, 6)

                    # Right input button pressed
                    if self.index == 3:
                        # RightInput state
                        self.state = "RightInput"
                        self.right_input_value_text = "Press any key to rebind"
                        self.right_input_value_rect = FONT.get_rect(
                            self.right_input_value_text)
                        self.right_input_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.right_input_value_rect.y += FONT_H * 10
                        self.right_input_value_bg_rect = self.right_input_value_rect.inflate(
                            6, 6)

                    # Left input button pressed
                    if self.index == 4:
                        # LeftInput state
                        self.state = "LeftInput"
                        self.left_input_value_text = "Press any key to rebind"
                        self.left_input_value_rect = FONT.get_rect(
                            self.left_input_value_text)
                        self.left_input_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.left_input_value_rect.y += FONT_H * 12
                        self.left_input_value_bg_rect = self.left_input_value_rect.inflate(
                            6, 6)

                    # Enter input button pressed
                    if self.index == 5:
                        # EnterInput state
                        self.state = "EnterInput"
                        self.enter_input_value_text = "Press any key to rebind"
                        self.enter_input_value_rect = FONT.get_rect(
                            self.enter_input_value_text)
                        self.enter_input_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.enter_input_value_rect.y += FONT_H * 14
                        self.enter_input_value_bg_rect = self.enter_input_value_rect.inflate(
                            6, 6)

                    # Pause input button pressed
                    if self.index == 6:
                        # PauseInput state
                        self.state = "PauseInput"
                        self.pause_input_value_text = "Press any key to rebind"
                        self.pause_input_value_rect = FONT.get_rect(
                            self.pause_input_value_text)
                        self.pause_input_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.pause_input_value_rect.y += FONT_H * 16
                        self.pause_input_value_bg_rect = self.pause_input_value_rect.inflate(
                            6, 6)

                    # Jump input button pressed
                    if self.index == 7:
                        # PauseInput state
                        self.state = "JumpInput"
                        self.jump_input_value_text = "Press any key to rebind"
                        self.jump_input_value_rect = FONT.get_rect(
                            self.jump_input_value_text)
                        self.jump_input_value_rect.left = NATIVE_RECT.center[0] + 3
                        self.jump_input_value_rect.y += FONT_H * 18
                        self.jump_input_value_bg_rect = self.jump_input_value_rect.inflate(
                            6, 6)

                    # Apply button pressed
                    elif self.index == self.button_rects_len - 2:
                        # Apply resolution game setting
                        self.game.resolution = self.resolution_index + 1
                        self.game.window_w = NATIVE_W * self.game.resolution
                        self.game.window_h = NATIVE_H * self.game.resolution
                        self.game.window_surf = pg.display.set_mode(
                            (self.game.window_w, self.game.window_h))

                        # Save resolution value to json settings
                        to_be_saved_settings = {
                            "resolution": self.game.resolution,
                            "key_bindings": self.game.key_bindings
                        }

                        # Write to json
                        with open(SETTING_PATH, "w") as settings_file:
                            dump(to_be_saved_settings, settings_file)

                    # Back button pressed
                    elif self.index == self.button_rects_len - 1:
                        self.is_input_allowed = False
                        self.direction *= -1

            elif self.state == "UpInput":
                # Check if the pressed key is already bound to another action
                existing_binding = None
                for action, key in self.game.key_bindings.items():
                    if event.key == key:
                        existing_binding = action
                        break

                # If the pressed key is not already bound, or if it's bound to the same action, update the key binding
                if not existing_binding or existing_binding == "up":
                    self.game.key_bindings["up"] = event.key
                    self.up_input_value_text = pg.key.name(event.key)
                    self.state = "Normal"
                else:
                    self.up_input_value_text = f"Key is already bound to '{
                        existing_binding}'."

            elif self.state == "DownInput":
                # Check if the pressed key is already bound to another action
                existing_binding = None
                for action, key in self.game.key_bindings.items():
                    if event.key == key:
                        existing_binding = action
                        break

                # If the pressed key is not already bound, or if it's bound to the same action, update the key binding
                if not existing_binding or existing_binding == "down":
                    self.game.key_bindings["down"] = event.key
                    self.down_input_value_text = pg.key.name(event.key)
                    self.state = "Normal"
                else:
                    self.down_input_value_text = f"Key is already bound to '{
                        existing_binding}'."

            elif self.state == "RightInput":
                # Check if the pressed key is already bound to another action
                existing_binding = None
                for action, key in self.game.key_bindings.items():
                    if event.key == key:
                        existing_binding = action
                        break

                # If the pressed key is not already bound, or if it's bound to the same action, update the key binding
                if not existing_binding or existing_binding == "right":
                    self.game.key_bindings["right"] = event.key
                    self.right_input_value_text = pg.key.name(event.key)
                    self.state = "Normal"
                else:
                    self.right_input_value_text = f"Key is already bound to '{
                        existing_binding}'."

            elif self.state == "LeftInput":
                # Check if the pressed key is already bound to another action
                existing_binding = None
                for action, key in self.game.key_bindings.items():
                    if event.key == key:
                        existing_binding = action
                        break

                # If the pressed key is not already bound, or if it's bound to the same action, update the key binding
                if not existing_binding or existing_binding == "left":
                    self.game.key_bindings["left"] = event.key
                    self.left_input_value_text = pg.key.name(event.key)
                    self.state = "Normal"
                else:
                    self.left_input_value_text = f"Key is already bound to '{
                        existing_binding}'."

            elif self.state == "EnterInput":
                # Check if the pressed key is already bound to another action
                existing_binding = None
                for action, key in self.game.key_bindings.items():
                    if event.key == key:
                        existing_binding = action
                        break

                # If the pressed key is not already bound, or if it's bound to the same action, update the key binding
                if not existing_binding or existing_binding == "enter":
                    self.game.key_bindings["enter"] = event.key
                    self.enter_input_value_text = pg.key.name(event.key)
                    self.state = "Normal"
                else:
                    self.enter_input_value_text = f"Key is already bound to '{
                        existing_binding}'."

            elif self.state == "PauseInput":
                # Check if the pressed key is already bound to another action
                existing_binding = None
                for action, key in self.game.key_bindings.items():
                    if event.key == key:
                        existing_binding = action
                        break

                # If the pressed key is not already bound, or if it's bound to the same action, update the key binding
                if not existing_binding or existing_binding == "pause":
                    self.game.key_bindings["pause"] = event.key
                    self.pause_input_value_text = pg.key.name(event.key)
                    self.state = "Normal"
                else:
                    self.pause_input_value_text = f"Key is already bound to '{
                        existing_binding}'."

            elif self.state == "JumpInput":
                # Check if the pressed key is already bound to another action
                existing_binding = None
                for action, key in self.game.key_bindings.items():
                    if event.key == key:
                        existing_binding = action
                        break

                # If the pressed key is not already bound, or if it's bound to the same action, update the key binding
                if not existing_binding or existing_binding == "jump":
                    self.game.key_bindings["jump"] = event.key
                    self.jump_input_value_text = pg.key.name(event.key)
                    self.state = "Normal"
                else:
                    self.jump_input_value_text = f"Key is already bound to '{
                        existing_binding}'."

            elif self.state == "Resolution":
                # Enter press
                if event.key == self.game.key_bindings["enter"]:
                    # Resolution state
                    self.resolution_value_text = self.resolutions[self.resolution_index]
                    self.state = "Normal"

                # Go left
                if event.key == self.game.key_bindings["left"]:
                    self.resolution_index -= 1
                    self.resolution_index = self.resolution_index % self.resolutions_len
                    self.resolution_value_text = f'<{
                        self.resolutions[self.resolution_index]}>'
                    self.resolution_value_rect = FONT.get_rect(
                        self.resolution_value_text)
                    self.resolution_value_rect.left = NATIVE_RECT.center[0] + 3
                    self.resolution_value_rect.y += FONT_H * 4
                    self.resolution_value_bg_rect = self.resolution_value_rect.inflate(
                        6, 6)

                # Go right
                if event.key == self.game.key_bindings["right"]:
                    self.resolution_index += 1
                    self.resolution_index = self.resolution_index % self.resolutions_len
                    self.resolution_value_text = f'<{
                        self.resolutions[self.resolution_index]}>'
                    self.resolution_value_rect = FONT.get_rect(
                        self.resolution_value_text)
                    self.resolution_value_rect.left = NATIVE_RECT.center[0] + 3
                    self.resolution_value_rect.y += FONT_H * 4
                    self.resolution_value_bg_rect = self.resolution_value_rect.inflate(
                        6, 6)

    def update(self, dt):
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
        if self.alpha == 255:
            self.is_input_allowed = True

        # Other end reached?
        elif self.alpha == 0:
            # Wait for end delay
            self.end_sleep_time -= dt
            if self.end_sleep_time < 0:
                # Deactivate my event and update
                self.game.is_option_screen = False

                # Reset my curtain
                self.curtain.set_alpha(0)
                self.alpha = 0
                self.fade_duration = 125
                self.fade_timer = 0
                self.direction = 1
                self.remainder = 0

    def draw(self, NATIVE_SURF):
        # Clear curtain
        self.curtain.fill("black")

        # Draw on curtain title
        FONT.render_to(self.curtain, self.title_rect, self.title_text, "white")

        # Draw on curtain resolution button
        pg.draw.rect(self.curtain, "black", self.resolution_bg_rect)
        FONT.render_to(self.curtain, self.resolution_rect,
                       self.resolution_text, "white")

        # Draw on curtain resolution value
        pg.draw.rect(self.curtain, "black", self.resolution_value_bg_rect)
        FONT.render_to(self.curtain, self.resolution_value_rect,
                       self.resolution_value_text, "white")

        # Draw on curtain up input button
        pg.draw.rect(self.curtain, "black", self.up_input_bg_rect)
        FONT.render_to(self.curtain, self.up_input_rect,
                       self.up_input_text, "white")

        # Draw on curtain up input value
        pg.draw.rect(self.curtain, "black", self.up_input_value_bg_rect)
        FONT.render_to(self.curtain, self.up_input_value_rect,
                       self.up_input_value_text, "white")

        # Draw on curtain down input button
        pg.draw.rect(self.curtain, "black", self.down_input_bg_rect)
        FONT.render_to(self.curtain, self.down_input_rect,
                       self.down_input_text, "white")

        # Draw on curtain down input value
        pg.draw.rect(self.curtain, "black", self.down_input_value_bg_rect)
        FONT.render_to(self.curtain, self.down_input_value_rect,
                       self.down_input_value_text, "white")

        # Draw on curtain right input button
        pg.draw.rect(self.curtain, "black", self.right_input_bg_rect)
        FONT.render_to(self.curtain, self.right_input_rect,
                       self.right_input_text, "white")

        # Draw on curtain right input value
        pg.draw.rect(self.curtain, "black", self.right_input_value_bg_rect)
        FONT.render_to(self.curtain, self.right_input_value_rect,
                       self.right_input_value_text, "white")

        # Draw on curtain left input button
        pg.draw.rect(self.curtain, "black", self.left_input_bg_rect)
        FONT.render_to(self.curtain, self.left_input_rect,
                       self.left_input_text, "white")

        # Draw on curtain left input value
        pg.draw.rect(self.curtain, "black", self.left_input_value_bg_rect)
        FONT.render_to(self.curtain, self.left_input_value_rect,
                       self.left_input_value_text, "white")

        # Draw on curtain enter input button
        pg.draw.rect(self.curtain, "black", self.enter_input_bg_rect)
        FONT.render_to(self.curtain, self.enter_input_rect,
                       self.enter_input_text, "white")

        # Draw on curtain enter input value
        pg.draw.rect(self.curtain, "black", self.enter_input_value_bg_rect)
        FONT.render_to(self.curtain, self.enter_input_value_rect,
                       self.enter_input_value_text, "white")

        # Draw on curtain pause input button
        pg.draw.rect(self.curtain, "black", self.pause_input_bg_rect)
        FONT.render_to(self.curtain, self.pause_input_rect,
                       self.pause_input_text, "white")

        # Draw on curtain pause input value
        pg.draw.rect(self.curtain, "black", self.pause_input_value_bg_rect)
        FONT.render_to(self.curtain, self.pause_input_value_rect,
                       self.pause_input_value_text, "white")

        # Draw on curtain jump input button
        pg.draw.rect(self.curtain, "black", self.jump_input_bg_rect)
        FONT.render_to(self.curtain, self.jump_input_rect,
                       self.jump_input_text, "white")

        # Draw on curtain jump input value
        pg.draw.rect(self.curtain, "black", self.jump_input_value_bg_rect)
        FONT.render_to(self.curtain, self.jump_input_value_rect,
                       self.jump_input_value_text, "white")

        # Draw on curtain apply button
        pg.draw.rect(self.curtain, "black", self.apply_bg_rect)
        FONT.render_to(self.curtain, self.apply_rect,
                       self.apply_text, "white")

        # Draw on curtain back button
        pg.draw.rect(self.curtain, "black", self.back_bg_rect)
        FONT.render_to(self.curtain, self.back_rect,
                       self.back_text, "white")

        # Draw on curtain middle line
        pg.draw.line(self.curtain, "white",
                     (self.resolution_bg_rect.right, self.resolution_bg_rect.y), (self.back_bg_rect.right, self.back_bg_rect.bottom))

        # Draw on curtain cursor
        if self.is_input_allowed == True:
            if self.state == "Normal":
                cursor_rect = self.button_rects[self.index]
                pg.draw.rect(self.curtain, "white", cursor_rect, 1)

            elif self.state == "Resolution":
                pg.draw.rect(self.curtain, "white",
                             self.resolution_value_bg_rect, 1)

        # Draw curtain on native
        NATIVE_SURF.blit(self.curtain, (0, 0))
