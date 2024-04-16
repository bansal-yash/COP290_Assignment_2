import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants for the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
LION_SIZE = (100, 32)

MAP_WIDTH = 4800
MAP_HEIGHT = 4800

# Reference screen size for speed calculation
REFERENCE_SCREEN_WIDTH = 800
BASE_LION_SPEED = 3.2  # Base speed, adjust this as needed for gameplay

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font initialization for displaying text
font = pygame.font.SysFont(None, 36)  # Choose an appropriate size

# Load the game map background
background_image = pygame.image.load("game_map.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (MAP_WIDTH, MAP_HEIGHT))

class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.width = width
        self.height = height
        self.zoom_level = 1.0

    def apply(self, rect):
        rect = rect.copy()
        rect.x -= self.camera_rect.x
        rect.y -= self.camera_rect.y
        rect.x = int(rect.x * self.zoom_level)
        rect.y = int(rect.y * self.zoom_level)
        rect.width = int(rect.width * self.zoom_level)
        rect.height = int(rect.height * self.zoom_level)
        return rect

    def scroll(self, x, y):
        self.camera_rect.x = min(
            max(0, self.camera_rect.x + x),
            self.width - int(SCREEN_WIDTH / self.zoom_level),
        )
        self.camera_rect.y = min(
            max(0, self.camera_rect.y + y),
            self.height - int(SCREEN_HEIGHT / self.zoom_level),
        )

    def zoom(self, increment):
        self.zoom_level = max(self.zoom_level + increment,1/6)
        
        center_x = self.camera_rect.x + (SCREEN_WIDTH / 2 / self.zoom_level)
        center_y = self.camera_rect.y + (SCREEN_HEIGHT / 2 / self.zoom_level)
        self.camera_rect.x = int(center_x - (SCREEN_WIDTH / 2 / self.zoom_level))
        self.camera_rect.y = int(center_y - (SCREEN_HEIGHT / 2 / self.zoom_level))
        self.camera_rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))

def load_image(filename, size):
    image = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(image, size)

# Load lion images
lion_images = {
    "sitting": load_image("animal_images/lion/sitting.png", LION_SIZE),
    "moving": [
        load_image("animal_images/lion/moving_1.png", LION_SIZE),
        load_image("animal_images/lion/moving_2.png", LION_SIZE),
        load_image("animal_images/lion/moving_3.png", LION_SIZE),
    ],
    "standing": load_image("animal_images/lion/standing.png", LION_SIZE),
    "sleeping": load_image("animal_images/lion/sleeping.png", LION_SIZE),
}

class Lion:
    def __init__(self, images, map_width, map_height, base_speed):
        self.images = images
        self.image = images["sitting"]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, map_width - LION_SIZE[0])
        self.rect.y = random.randint(0, map_height - LION_SIZE[1])
        self.moving_index = 0
        self.base_speed = base_speed
        self.map_width = map_width
        self.map_height = map_height
        self.dir = "stop"

    def update(self, camera):
        self.speed = self.base_speed * camera.zoom_level  # Adjust speed based on zoom

        to_change = random.choices([0, 1], weights=[40, 1])[0]
        if to_change:
            self.dir = "left"

        move_dir = self.dir

        if move_dir != "stop":
            if move_dir == "left":
                self.rect.x -= self.speed
                self.image = pygame.transform.flip(self.images["moving"][self.moving_index], True, False)
            elif move_dir == "right":
                self.rect.x += self.speed
                self.image = self.images["moving"][self.moving_index]
            elif move_dir == "up":
                self.rect.y -= self.speed
                self.image = pygame.transform.rotate(self.images["moving"][self.moving_index], 90)
            elif move_dir == "down":
                self.rect.y += self.speed
                self.image = pygame.transform.rotate(self.images["moving"][self.moving_index], -90)
            self.moving_index = (self.moving_index + 1) % len(self.images["moving"])

        self.rect.x = max(0, min(self.map_width - LION_SIZE[0], self.rect.x))
        self.rect.y = max(0, min(self.map_height - LION_SIZE[1], self.rect.y))

    def draw(self, surface, camera):
        scaled_rect = camera.apply(self.rect)
        scaled_image = pygame.transform.scale(
            self.image, (scaled_rect.width, scaled_rect.height)
        )
        surface.blit(scaled_image, scaled_rect.topleft)

lion = Lion(lion_images, MAP_WIDTH, MAP_HEIGHT, BASE_LION_SPEED)
camera = Camera(MAP_WIDTH, MAP_HEIGHT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            camera.zoom(event.y * 0.1)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                camera.scroll(-event.rel[0], -event.rel[1])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS and pygame.key.get_mods() & pygame.KMOD_META and not pygame.key.get_mods() & pygame.KMOD_ALT:
                camera.zoom(-0.1)
            elif event.key == pygame.K_EQUALS and pygame.key.get_mods() & pygame.KMOD_META and pygame.key.get_mods() & pygame.KMOD_SHIFT and not pygame.key.get_mods() & pygame.KMOD_ALT:
                camera.zoom(0.1)

    lion.update(camera)

    screen.fill((0, 100, 0))  # Dark green, like a forest
    background_rect = camera.apply(background_image.get_rect())
    screen.blit(
        pygame.transform.scale(
            background_image, (background_rect.width, background_rect.height)
        ),
        background_rect,
    )

    lion.draw(screen, camera)

    # Display the zoom level
    zoom_text = font.render(f"Zoom: {camera.zoom_level:.2f}", True, (255, 255, 255))
    screen.blit(zoom_text, (50, 50))  # Position the zoom level text on the screen

    pygame.display.flip()
