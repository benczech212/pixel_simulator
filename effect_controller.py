import pygame
import time
import random
import led_controller
import app
import effect_library



default_color_speed = app.settings.get("default_color_speed", 0.1)
tick_count = 0


# Pygame setup
pygame.init()
screen_width, screen_height = app.settings.get("screen_width", 1920), app.settings.get("screen_height", 1920)
pixel_count = app.settings.get("pixel_count", 1)
box_width = screen_width // pixel_count
box_height = app.settings.get("box_height",50)

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Information display variables
font_info = pygame.font.Font(None, 36)
info_y = screen_height + 100  # Adjusted position
tick_count = 0

# Create Pixels object
pixel_manager = led_controller.Pixels(pixel_count,screen,screen_width)
pixel_manager.set_box_dimensions(box_width, box_height)

while True:
    effect_choice = random.choice([
        "rainbow",
        #  "test_effect",
        # "rest_effect"
        ])

    if effect_choice == "rainbow_cycle":
        effect_library.rainbow_cycle(pixel_manager, speed=10)
    elif effect_choice == "test_effect":
        effect_library.test_effect(pixel_manager)
    elif effect_choice == "rest_effect":
        effect_library.rest_effect(pixel_manager, fade_out=False)
    elif effect_choice == "rainbow":
        effect_library.rainbow(pixel_manager, speed=1)
    pixel_manager.show()

    # app.display_info_below(effect_choice, screen)

    pygame.display.flip()
    clock.tick(60)
    pygame.time.delay(1000)