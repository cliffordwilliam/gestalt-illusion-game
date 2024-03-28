from constants import *


class IntroCutscene:
    def __init__(self, game):
        # Game
        self.game = game

        # Text box
        self.text_box = pg.Rect(0, 0, NATIVE_W, (FONT_H * 5) + (2 * TILE_S))

        # Intro cutscene background init
        self.intro_cutscene_bg = pg.Surface((NATIVE_W, NATIVE_H))

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
        self.duration = 0

        # Sentences
        self.sentences = [
            "Lorem ipsum~dolor@sit amet",
            "Etiam euismod~tristique@pretium"
        ]
        self.sentences_index = 0
        self.sentences_i_len = len(self.sentences) - 1
        self.sentence = self.sentences[self.sentences_index]
        self.sentence_i_len = len(self.sentence) - 1
        self.displayed_text_index = -1

        # Displayed text / container
        self.displayed_text = ""
        self.displayed_rect = FONT.get_rect(self.displayed_text)
        self.displayed_text_2 = ""
        self.displayed_rect_2 = FONT.get_rect(self.displayed_text_2)
        self.displayed_text_3 = ""
        self.displayed_rect_3 = FONT.get_rect(self.displayed_text_3)
        self.container_index = 1

        # Typing timer
        self.typing_timer = 0
        self.typing_duration = 33

        # Delays
        self.end_sleep_time = 500
        self.start_sleep_time = 500

        # Menu input
        self.is_input_allowed = False

        # Prompt enter text
        enter = pg.key.name(self.game.key_bindings["enter"])
        self.tips_text = f'press {enter}'
        self.tips_rect = FONT.get_rect(self.tips_text)
        self.tips_rect.topright = NATIVE_RECT.topright
        self.tips_rect.x -= TILE_S
        self.tips_rect.y += TILE_S + (4 * FONT_H)

        # Blink flag
        self.blink_duration = 600
        self.blink_timer = 0
        self.blink_show = True

    def event(self, event):
        # Block input when fading
        if self.is_input_allowed == False:
            return

        # Input navigation / select
        if event.type == pg.KEYUP:
            # Enter press
            if event.key == self.game.key_bindings["enter"]:
                # Typing
                if self.displayed_text_index < self.sentence_i_len:
                    # Skip typing to show all index
                    self.displayed_text_index = self.sentence_i_len
                    for letter in self.sentence:
                        if letter == "~":
                            self.container_index = 2
                        elif letter == "@":
                            self.container_index = 3
                        else:
                            if self.container_index == 1:
                                self.displayed_text += letter
                                self.displayed_rect = FONT.get_rect(
                                    self.displayed_text)
                                self.displayed_rect.topleft = (TILE_S, TILE_S)
                            elif self.container_index == 2:
                                self.displayed_text_2 += letter
                                self.displayed_rect_2 = FONT.get_rect(
                                    self.displayed_text_2)
                                self.displayed_rect_2.topleft = (
                                    TILE_S, TILE_S + (FONT_H * 2))
                            elif self.container_index == 3:
                                self.displayed_text_3 += letter
                                self.displayed_rect_3 = FONT.get_rect(
                                    self.displayed_text_3)
                                self.displayed_rect_3.topleft = (
                                    TILE_S, TILE_S + (FONT_H * 4))

                # Not typing
                elif self.displayed_text_index == self.sentence_i_len:
                    # Still got more sentences, next sentence
                    if self.sentences_index < self.sentences_i_len:
                        # Next sentence index
                        self.sentences_index += 1

                        # Reset sentences
                        self.sentences_i_len = len(self.sentences) - 1
                        self.sentence = self.sentences[self.sentences_index]
                        self.sentence_i_len = len(self.sentence) - 1
                        self.displayed_text_index = -1

                        # Reset displayed text / container
                        self.displayed_text = ""
                        self.displayed_rect = FONT.get_rect(
                            self.displayed_text)
                        self.displayed_text_2 = ""
                        self.displayed_rect_2 = FONT.get_rect(
                            self.displayed_text_2)
                        self.displayed_text_3 = ""
                        self.displayed_rect_3 = FONT.get_rect(
                            self.displayed_text_3)
                        self.container_index = 1

                    # No more sentences, next scene
                    else:
                        # Block input
                        self.is_input_allowed = False

                        # Start fade
                        self.direction *= -1

    def update(self, dt):
        # Start delay
        if self.start_sleep_time > 0:
            self.start_sleep_time -= dt
            return

        # Update blink timer
        if self.displayed_text_index == self.sentence_i_len:
            self.blink_timer += dt
            if self.blink_timer > self.blink_duration:
                self.blink_timer = 0
                self.blink_show = not self.blink_show
        else:
            self.blink_timer = 0

        # Update displayed text
        if self.is_input_allowed == True:
            self.typing_timer += dt
            if self.typing_timer > self.typing_duration:
                self.typing_timer = 0

                if self.displayed_text_index < self.sentence_i_len:
                    self.displayed_text_index += 1
                    letter = self.sentence[self.displayed_text_index]
                    if letter == "~":
                        self.container_index = 2
                    elif letter == "@":
                        self.container_index = 3
                    else:
                        if self.container_index == 1:
                            self.displayed_text += letter
                            self.displayed_rect = FONT.get_rect(
                                self.displayed_text)
                            self.displayed_rect.topleft = (TILE_S, TILE_S)
                        elif self.container_index == 2:
                            self.displayed_text_2 += letter
                            self.displayed_rect_2 = FONT.get_rect(
                                self.displayed_text_2)
                            self.displayed_rect_2.topleft = (
                                TILE_S, TILE_S + (FONT_H * 2))
                        elif self.container_index == 3:
                            self.displayed_text_3 += letter
                            self.displayed_rect_3 = FONT.get_rect(
                                self.displayed_text_3)
                            self.displayed_rect_3.topleft = (
                                TILE_S, TILE_S + (FONT_H * 4))

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
                # Go to room 1
                self.game.set_scene("World")

    def draw(self, NATIVE_SURF):
        # Draw intro cutscene background
        NATIVE_SURF.blit(self.intro_cutscene_bg, (0, 0))

        # Draw container
        pg.draw.rect(NATIVE_SURF, "white", self.text_box, 1)

        # Draw displayed text
        FONT.render_to(NATIVE_SURF, self.displayed_rect,
                       self.displayed_text, "white")
        FONT.render_to(NATIVE_SURF, self.displayed_rect_2,
                       self.displayed_text_2, "white")
        FONT.render_to(NATIVE_SURF, self.displayed_rect_3,
                       self.displayed_text_3, "white")

        # Draw enter text blinking when not typing
        if self.displayed_text_index == self.sentence_i_len:
            if self.blink_show:
                FONT.render_to(NATIVE_SURF, self.tips_rect,
                               self.tips_text, "white", "black")

        # Draw curtain
        NATIVE_SURF.blit(self.curtain, (0, 0))
