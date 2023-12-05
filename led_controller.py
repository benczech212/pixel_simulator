import pygame
import time
import random
import app

class Pixel:
    def __init__(self, pixel_id, color=(0, 0, 0), speed=0.1):
        self.pixel_id = pixel_id
        self.color = color
        self.color_target = color
        self.speed = speed

    def draw(self, surface, box_width, box_height, screen_width, pixel_count):
        rect = pygame.Rect(self.pixel_id * (screen_width // pixel_count), 0, box_width, box_height)

        # Fill background with black to erase old text
        pygame.draw.rect(surface, (0, 0, 0), rect)

        # Draw new pixel information
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (50, 50, 50), rect, 2)  # Outline in gray
        font = pygame.font.Font(None, int(20 * screen_width / 1920))  # Adjust the font size based on screen width

        # Display pixel ID
        text = font.render(str(self.pixel_id), True, (255, 255, 255))
        text_rect = text.get_rect(center=(rect.centerx, box_height + int(20 * screen_width / 1920)))  # Adjust the position based on screen width

        # Display pixel color, target color, and speed
        text_color = font.render(f"Color: {self.color}", True, (255, 255, 255))
        text_target_color = font.render(f"Target: {self.color_target}", True, (255, 255, 255))

        # Round speed to 2 decimal places
        rounded_speed = round(self.speed, 2)
        text_speed = font.render(f"Speed: {rounded_speed}", True, (255, 255, 255))

        text_color_rect = text_color.get_rect(center=(rect.centerx, box_height + int(40 * screen_width / 1920)))
        text_target_color_rect = text_target_color.get_rect(center=(rect.centerx, box_height + int(60 * screen_width / 1920)))
        text_speed_rect = text_speed.get_rect(center=(rect.centerx, box_height + int(80 * screen_width / 1920)))

        # Draw black box to cover the old text
        pygame.draw.rect(surface, (0, 0, 0), (rect.left, box_height + int(10 * screen_width / 1920), rect.width, int(90 * screen_width / 1920)))

        surface.blit(text, text_rect)  # Display pixel ID
        surface.blit(text_color, text_color_rect)
        surface.blit(text_target_color, text_target_color_rect)
        surface.blit(text_speed, text_speed_rect)

    def get_color(self):
        return self.color

    def set_target(self, target):
        self.color_target = target

    def step_towards_target(self):
        self.color = tuple(
            int(current + (target - current) * self.speed) for current, target in zip(self.color, self.color_target)
        )


class Pixels:
    def __init__(self, pixel_count, surface, screen_width):
        speed_min, speed_max = app.settings.get('default_color_speed_min', 0.05), app.settings.get('default_color_speed_max', 0.05)
        self.pixels = [Pixel(pixel_id=i, speed=random.uniform(speed_min, speed_max)) for i in range(pixel_count)]
        self.box_width = 0
        self.box_height = 0
        self.surface = surface
        self.screen_width = screen_width
        self.pixel_count = pixel_count

    def set_box_dimensions(self, box_width, box_height):
        self.box_width = box_width
        self.box_height = box_height

    def clear(self):
        for pixel in self.pixels:
            pixel.color_target = (0, 0, 0)

    def fill(self, color):
        for pixel in self.pixels:
            pixel.color_target = color

    def show(self):
        for pixel in self.pixels:
            pixel.step_towards_target()
            pixel.draw(self.surface, self.box_width, self.box_height, self.screen_width, self.pixel_count)

    def get_colors(self):
        return [pixel.get_color() for pixel in self.pixels]

    def random_speeds(self, min=app.settings.get('default_color_speed_min', 0.05), max=app.settings.get('default_color_speed_max', 0.2)):
        for pixel in self.pixels:
            pixel.speed = random.uniform(min, max)

    def print_info(self):
        print("Pixel Colors:")
        for i, color in enumerate(self.get_colors()):
            print(f"Pixel {i}: {color}")

    def fade_to_colors(self, new_colors, fade_duration):
        start_time = time.monotonic()
        current_colors = self.get_colors()
        while time.monotonic() - start_time < fade_duration:
            elapsed_time = time.monotonic() - start_time
            ratio = elapsed_time / fade_duration
            interpolated_colors = [
                tuple(int(current + (new - current) * ratio) for current, new in zip(current_colors[i], new_colors[i]))
                for i in range(len(current_colors))
            ]
            for pixel, color in zip(self.pixels, interpolated_colors):
                pixel.set_target(color)

            pygame.display.flip()
            # pygame.time.delay(10)