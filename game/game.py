import pygame
import pytmx
import sys

def load_pygame(filename):
    """ Load map data from TMX file """
    tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
    return tmx_data

def draw_map(surface, tmx_data, offset_x, offset_y):
    """ Draw the map on a pygame surface with given offsets """
    tw = tmx_data.tilewidth
    th = tmx_data.tileheight
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * tw - offset_x, y * th - offset_y))

def run():
    pygame.init()
    screen = pygame.display.set_mode((1500, 1500))
    tmx_data = load_pygame("tmx/game_mao.tmx")  # Make sure path is correct
    clock = pygame.time.Clock()

    offset_x, offset_y = 0, 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    offset_x -= 30  # Scroll left
                elif event.key == pygame.K_RIGHT:
                    offset_x += 30  # Scroll right
                elif event.key == pygame.K_UP:
                    offset_y -= 30  # Scroll up
                elif event.key == pygame.K_DOWN:
                    offset_y += 30  # Scroll down

        # Limit the scrolling to the map size
        offset_x = max(0, min(tmx_data.width * tmx_data.tilewidth - 1500, offset_x))
        offset_y = max(0, min(tmx_data.height * tmx_data.tileheight - 1500, offset_y))

        screen.fill((0, 0, 0))  # Clear the screen with black
        draw_map(screen, tmx_data, offset_x, offset_y)  # Draw the TMX map with scrolling
        pygame.display.flip()  # Update the full display Surface to the screen
        clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
