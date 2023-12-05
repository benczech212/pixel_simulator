import pygame
import time
import random
import led_controller
import app

DEFAULT_EFFECT_DURATION_MIN = app.settings.get('default_effect_duration_min',5)
DEFAULT_EFFECT_DURATION_MAX = app.settings.get('default_effect_duration_max',5)

screen = pygame.display.set_mode((app.settings["screen_width"], app.settings["screen_height"]))

tick_count = 0



# Function to smoothly fade to a new color
def fade_to_color(pixels, new_color, effect_duration=random.randint(DEFAULT_EFFECT_DURATION_MIN, DEFAULT_EFFECT_DURATION_MAX)):
    start_time = time.monotonic()
    while time.monotonic() - start_time < effect_duration:
        app.handle_quit_event()

        elapsed_time = time.monotonic() - start_time
        ratio = elapsed_time / effect_duration
        pixels.fade_to_colors([new_color] * len(pixels.pixels), effect_duration)  # Fade to new color

        pixels.show(screen)

        # Display information
        app.display_info_below("Fade to Color", effect_duration, elapsed_time, screen)

        pygame.display.flip()
        pygame.time.delay(10)  # Added a slight delay to improve performance


# Function for test effect
def test_effect(pixels,colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)], effect_duration=random.randint(DEFAULT_EFFECT_DURATION_MIN, DEFAULT_EFFECT_DURATION_MAX)):
    start_time = time.monotonic()

    while time.monotonic() - start_time < effect_duration:
        app.handle_quit_event()

        elapsed_time = time.monotonic() - start_time
        current_color_index = int(elapsed_time) % len(colors)
        pixels.fill(colors[current_color_index])

        pixels.show(screen)

        # Display information below the pixels
        app.display_info_below("Test Effect", effect_duration, elapsed_time, screen)

        pygame.display.flip()
        pygame.time.delay(10)  # Added a slight delay to improve performance

# Function for rest effect
def rest_effect(pixels, fade_out=False, effect_duration=random.randint(DEFAULT_EFFECT_DURATION_MIN, DEFAULT_EFFECT_DURATION_MAX)):
    start_time = time.monotonic()

    while time.monotonic() - start_time < effect_duration:
        app.handle_quit_event()

        elapsed_time = time.monotonic() - start_time

        if fade_out:
            fade_ratio = min(1, elapsed_time / effect_duration)  # Ensure fade_ratio doesn't exceed 1
            pixels.fade_to


def rainbow_cycle(pixels, speed=1, effect_duration=random.randint(DEFAULT_EFFECT_DURATION_MIN, DEFAULT_EFFECT_DURATION_MAX)):
    global tick_count
    start_time = time.monotonic()
    while time.monotonic() - start_time < effect_duration:
        app.handle_quit_event()  # Check for quit event

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        elapsed_time = time.monotonic() - start_time

        colors = [app.wheel(int((i / pixels.pixel_count * 255 + tick_count * speed) % 255)) for i in range(pixels.pixel_count)]
        tick_count += 1
        if tick_count % 5 == 0:
            pixels.fade_to_colors(colors, 0.5)  # Slower transition for smoother effect

            pixels.show(screen)

        # Display information below the pixels
        app.display_info_below("Rainbow Cycle", effect_duration, elapsed_time,screen)

        pygame.display.flip()
        pygame.time.delay(10)  # Added a slight delay to improve performance
        
def rainbow(pixels, speed=1, effect_duration=5):
    speed *= 8 # multiply by some amount to scale this value up
    start_time = time.monotonic()
    while time.monotonic() - start_time < effect_duration:
        app.handle_quit_event()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        elapsed_time = time.monotonic() - start_time
        time.monotonic()
        # Calculate color based on time and speed
        time_inc = time.monotonic() * speed * 8
        hues = []
        for pixel_id in range(pixels.pixel_count):
            pix_inc = pixel_id * 8
            hues.append(int(time_inc + pix_inc) % 360)

        colors = [app.hsv_to_rgb(hue, 100, 100) for hue in hues]
        pixels.fade_to_colors(colors,0.01)
        # pixels.fill(color)
        pixels.show()

        # Display information below the pixels
        app.display_info_below("Rainbow", effect_duration, elapsed_time,screen)

        pygame.display.flip()
        pygame.time.delay(10)  # Added a slight delay to improve performance
