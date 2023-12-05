import json
import pygame
import sys
import os

# Load settings from settings.json
with open("settings.json") as settings_file:
    settings = json.load(settings_file)

# Set the display to the second monitor
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{settings['screen_width']} , 0"

# Pygame setup
pygame.init()

# Create the screen on the second monitor
screen_width, screen_height = settings.get("screen_width", 1920), settings.get("screen_height", 1920)
screen = pygame.display.set_mode((screen_width, screen_height))


# Function to display information below the pixels
def display_info_below(effect_name, total_duration, elapsed_time, screen):
    font_info_below = pygame.font.Font(None, 36)
    info_text = f"Effect: {effect_name} | Total Duration: {total_duration:.2f}s | Elapsed Time: {elapsed_time:.2f}s"
    text_surface = font_info_below.render(info_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() + 50))
    screen.blit(text_surface, text_rect)

def handle_quit_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)
def hsv_to_rgb(h, s, v):
    h /= 360
    s /= 100
    v /= 100
    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    if i % 6 == 0:
        r, g, b = v, t, p
    elif i % 6 == 1:
        r, g, b = q, v, p
    elif i % 6 == 2:
        r, g, b = p, v, t
    elif i % 6 == 3:
        r, g, b = p, q, v
    elif i % 6 == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    v = mx * 100
    return int(h), int(s), int(v)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_rgb(color1, color2, t):
    r = int(lerp(color1[0], color2[0], t))
    g = int(lerp(color1[1], color2[1], t))
    b = int(lerp(color1[2], color2[2], t))
    return r, g, b


def lerp_hsv_from_rgb(rgb1, rgb2, t):
    hsv1 = rgb_to_hsv(*rgb1)
    hsv2 = rgb_to_hsv(*rgb2)
    lerped_hsv = (lerp(hsv1[0], hsv2[0], t), lerp(hsv1[1], hsv2[1], t), lerp(hsv1[2], hsv2[2], t))
    lerped_rgb = hsv_to_rgb(*lerped_hsv)
    return lerped_rgb