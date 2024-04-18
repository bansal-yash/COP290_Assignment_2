from numpy import character
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
height = 800
width = 1400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Screen")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

character_screen = False
selected_character = None

# Define fonts
font = pygame.font.Font(None, 36)

# Define button properties
button_width = 200
button_height = 50
button_spacing = 20
button_x = (width - button_width) // 2
button_y = height - 100  # Placing the button 100 pixels from the bottom of the screen
total_button_width = button_width * 4 + button_spacing * 3
button_start_x = (width - total_button_width) // 2  # Center buttons horizontally
button_start_y = height - 200

# Function to display "Choose Your Character" screen
def choose_character_screen():
    text = font.render("Choose Your Character", True, BLACK)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    
def draw_character_buttons():
    characters = ["lion", "giraffe", "poacher", "ranger"]
    for idx, character in enumerate(characters):
        button_rect = pygame.Rect(button_start_x + idx * (button_width + button_spacing), button_start_y, button_width, button_height)
        if selected_character == character:
            pygame.draw.rect(screen, BLACK, button_rect)
        else:
            pygame.draw.rect(screen, GRAY, button_rect)
        text = font.render(character.capitalize(), True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        
def play_screen():
    pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
    text = font.render("Play", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if(not(character_screen)):
                # print("here1")
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    character_screen = True
            else:
                print("here")
                characters = ["lion", "giraffe", "poacher", "ranger"]
                for idx, _ in enumerate(characters):
                    button_rect = pygame.Rect(button_start_x + idx * (button_width + button_spacing), button_start_y, button_width, button_height)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        
                        print("Selected character:", characters[idx])
                        character_screen = False
                    # Display "Choose Your Character" screen when the button is clicked
        screen.fill(WHITE)
    if(character_screen):
        choose_character_screen()
        draw_character_buttons()
    else:
        play_screen()
    # Clear the screen

    pygame.display.flip()
    

# Quit Pygame
pygame.quit()
sys.exit()
