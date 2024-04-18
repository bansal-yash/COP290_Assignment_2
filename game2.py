import pygame
import pytmx
import sys
import random
import time

pygame.init()

# Constants for the screen size
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
LION_SIZE = (100, 32)
GIRAFFE_SIZE = (100, 100)

MAP_WIDTH = 4800
MAP_HEIGHT = 4800

Game_over = [False]
    

pygame.display.set_caption("Flashing Game Over")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font settings
font = pygame.font.Font(None, 48)
game_over_text = font.render("Game Over", True, WHITE)



# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load the game map using pytmx
tmx_data = pytmx.load_pygame("game/tmx/game_mao.tmx", pixelalpha=True)

def render_map(surface, tmx_data, camera):
    """Render the map with the camera offset."""
    tw = tmx_data.tilewidth
    th = tmx_data.tileheight

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, camera.apply(pygame.Rect(x * tw, y * th, tw, th)))

def process_object_layer(game_over,surface, tmx_data, camera):
    """Process and render objects from the object layer for visualization, including image objects."""
    if(not(game_over)):
        for obj in tmx_data.objects:
            if hasattr(obj, 'image') and obj.image:
                image = pygame.transform.scale(obj.image, (int(obj.width) * camera.zoom_level , int(obj.height) * camera.zoom_level ))
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                surface.blit(image, camera.apply(rect))

            elif hasattr(obj, 'points'):
                pygame.draw.polygon(surface, (255, 0, 0), [(camera.apply_point((p[0], p[1]))) for p in obj.points], 3)
            elif hasattr(obj, 'ellipse') and obj.ellipse:
                ellipse_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                pygame.draw.ellipse(surface, (255, 0, 0), camera.apply(ellipse_rect), 3)
            else:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                pygame.draw.rect(surface, (0, 255, 0), camera.apply(rect), 3)
    else:
        screen.fill(BLACK)
        screen.blit(game_over_text, (MAP_WIDTH // 2 - game_over_text.get_width() // 2, MAP_HEIGHT // 2 - game_over_text.get_height() // 2))
        


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

    def update(self, target):
        # Center the camera on the target
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2
        # Adjust the camera rectangle
        self.camera_rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))
        
    def zoom(self, increment):
        self.zoom_level = max(self.zoom_level + increment,1/3)
        
        center_x = self.camera_rect.x + (SCREEN_WIDTH / 2 / self.zoom_level)
        center_y = self.camera_rect.y + (SCREEN_HEIGHT / 2 / self.zoom_level)
        self.camera_rect.x = int(center_x - (SCREEN_WIDTH / 2 / self.zoom_level))
        self.camera_rect.y = int(center_y - (SCREEN_HEIGHT / 2 / self.zoom_level))
        self.camera_rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))
        
    def scroll(self, x, y):
        self.camera_rect.x = min(
            max(0, self.camera_rect.x + x),
            self.width - int(SCREEN_WIDTH / self.zoom_level),
        )
        self.camera_rect.y = min(
            max(0, self.camera_rect.y + y),
            self.height - int(SCREEN_HEIGHT / self.zoom_level),
        )
        
    def apply_point(self, point):
        """Adjust a point based on camera settings."""
        x, y = point
        x -= self.camera_rect.x
        y -= self.camera_rect.y
        return int(x * self.zoom_level), int(y * self.zoom_level)

def load_image(filename, size):
    image = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(image, size)

lion_images = {
    "sitting": load_image("animal_images/lion/sitting.png", LION_SIZE),
    "moving": [
        load_image("animal_images/lion/moving_1.png", LION_SIZE),
        load_image("animal_images/lion/moving_2.png", LION_SIZE),
        load_image("animal_images/lion/moving_3.png", LION_SIZE)
        # load_image("animal_images/lion/lion_moving4.png", LION_SIZE),
        # load_image("animal_images/lion/lion_moving5.png", LION_SIZE),
        # load_image("animal_images/lion/lion_moving6.png", LION_SIZE),
        
    ],
    "standing": load_image("animal_images/lion/standing.png", LION_SIZE),
    "sleeping": load_image("animal_images/lion/sleeping.png", LION_SIZE),
}

giraffe_images = {
    "moving": [
        load_image("animal_images/giraffe/moving_1.png", GIRAFFE_SIZE),
        load_image("animal_images/giraffe/moving_2.png", GIRAFFE_SIZE),
        load_image("animal_images/giraffe/moving_3.png", GIRAFFE_SIZE),
    ],
    "standing": load_image("animal_images/giraffe/standing.png", GIRAFFE_SIZE),
    "sitting": load_image("animal_images/giraffe/standing.png", GIRAFFE_SIZE),
    "dead": load_image("animal_images/giraffe/standing.png", LION_SIZE)
    
    
}

# Animal_images = {
#     "lion" : lion_images,
#     "giraffe": giraffe_images
# }

# vehical_image = {
#     "left": load_image("",21),
#     "right": load_image("",21),
#     "up": load_image("",21),
#     "down": load_image("",21),
# }


Giraffe_action = ["to_drink","to_rest"]
Giraffe_location_map = {
    "to_drink": (340,950),
    "to_rest" : (1500,900)
    # "to_rest" : (2000,2500)
    
}
# Lion_action = ["to_drink","to_kill","to_rest"]
Lion_action = ["to_kill"]

Lion_location_map = {
    "to_drink": (360,2752),
    "to_rest": (2200,2752)
}



Animal_action = {
    "lion": Lion_action,
    "giraffe" : Giraffe_action
}
Animal_location_map = {
    "lion": Lion_location_map,
    "giraffe" : Giraffe_location_map
}

def Animal_start(animal_type):
    x,y = Animal_location_map[animal_type]["to_rest"]
    if(animal_type == "lion"):
        return (random.randint(x-50,x+50),random.randint(y-20,y+20))
    elif(animal_type == "giraffe"):
        return (random.randint(x-200,x+200),random.randint(y-100,y+100))

def Animal_drink(animal_type):
    x,y = Animal_location_map[animal_type]["to_drink"]
    if(animal_type == "lion"):
        return (random.randint(x-40,x+40),random.randint(y-20,y+20))
    elif(animal_type == "giraffe"):
        return (random.randint(x-20,x+20),random.randint(y-200,y+200))


Animals = []
Preys = []
Predators = []

class Animal:
    
    def __init__(self, images, map_width, map_height,speed,animal_type):
        self.animal = animal_type
        self.images = images
        self.image = images["sitting"]
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = Animal_start(self.animal)
        
        self.frame_counter = 0
        self.frame_delay = 5
        self.moving_index = 0
        self.speed = speed
        self.map_width = map_width
        self.map_height = map_height
        self.dir = "stop"
        self.current_action = "none"
        self.loc_x = 0
        self.loc_y = 0
        self.alive = True
        self.time = 0
        self.predator = None
        self.pred_near = True
        
    def move_to_this_tile(self,x,y):
        # print(self.rect.x, self.rect.y)
        if self.rect.x < x:
            return "right"
        elif self.rect.x > x:
            return "left"
        
        if self.rect.y < y:
            return "up"
        elif self.rect.y > y:
            return "down"
        return "stop"

    def update(self,player,direction):
        if (self.alive):
            zoom_adjusted_speed = self.speed * camera.zoom_level
            zoom_adjusted_delay = self.frame_delay / camera.zoom_level
            if(player):
                move_dir = direction
            else:
                if(self.predator != None):
                    x,y = self.predator.get_location()
                    if abs(self.rect.x - x) < 160 and abs(self.rect.y - y) < 160 and self.pred_near:
                        
                        self.speed = 3 * self.speed
                        self.predator.set_speed(self.speed+3)
                        self.pred_near = False
                    dir = self.predator.get_dir()
                    if(dir == "up"):
                        self.dir = "up"
                    elif(dir == "down"):
                        self.dir = "down"
                    elif(dir == "right"):
                        self.dir = "right"
                    elif(dir == "left"):
                        self.dir = "left"
                    
                elif(self.current_action == "none"):
                    self.current_action = random.choice(Animal_action[self.animal])
                    print(self.current_action)
                    if(self.current_action == "to_kill"):
                        if(len(Preys) == 0):
                            screen.fill(BLACK)
                            Game_over[0] = True
                        else:
                            Preys[0].set_predator(self)
                            self.loc_x,self.loc_y = Preys[0].get_location()
                            if abs(self.rect.x - self.loc_x) < 40 and abs(self.rect.y - self.loc_y) < 40:
                                a = random.randint(0,1)
                                if(a == 1):
                                    Preys[0].killed()
                                    Preys.pop(0)
                                else:
                                    self.current_action = "none"
                                    Preys[0].set_predator(None)
                    elif(self.current_action == "to_drink"):
                        self.loc_x, self.loc_y = Animal_drink(self.animal)  
                    else:
                        self.loc_x ,self.loc_y = Animal_location_map[self.animal][self.current_action]
                
                        
                elif(self.current_action == "to_kill"):
                    if(len(Preys) != 0):
                        self.loc_x,self.loc_y = Preys[0].get_location()
                        if abs(self.rect.x - self.loc_x) < 20 and abs(self.rect.y - self.loc_y) < 20:
                            a = random.randint(0,1)
                            # print("Prey killed!")
                            if(a == 1):
                                Preys[0].killed()
                                Preys.pop(0)
                            else:
                                self.current_action = "none"
                                Preys[0].set_predator(None)
                    else:
                        # print("Game Over")
                        screen.fill(BLACK)
                        Game_over[0] = True
                        # process_object_layer(Game_over,screen, tmx_data, camera)
                # elif(self.current_action == "to_run"):
                #     self.dir ==    
                if(self.predator == None): 
                    self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)

                move_dir = self.dir
                
            if move_dir != "stop":
                if(not(player)):
                    if(abs(self.rect.x - self.loc_x) < zoom_adjusted_speed):
                            self.rect.x = self.loc_x
                            if(abs(self.rect.y - self.loc_y) < zoom_adjusted_speed):
                                self.rect.y = self.loc_y
                                move_dir = "stop"
                            else:
                                if(self.rect.y < self.loc_y):
                                    move_dir = "down"
                                    self.dir = "down"
                                else:
                                    move_dir = "up"
                                    self.dir = "up"
                if(self.animal == "lion"):
                    print(self.dir)

                if move_dir == "left":
                    self.rect.x -= zoom_adjusted_speed
                    self.image = pygame.transform.flip(
                        self.images["moving"][self.moving_index], True, False
                    )

                elif move_dir == "right":
                    
                    self.rect.x += zoom_adjusted_speed
                    self.image = self.images["moving"][self.moving_index]

                elif move_dir == "up":
                    self.rect.y -= zoom_adjusted_speed
                    self.image = pygame.transform.rotate(
                        self.images["moving"][self.moving_index], 90
                    )

                elif move_dir == "down":
                    self.rect.y += zoom_adjusted_speed
                    self.image = pygame.transform.rotate(
                        self.images["moving"][self.moving_index], -90
                    )
                

                self.frame_counter += 1
                if self.frame_counter >= zoom_adjusted_delay:
                    self.moving_index = (self.moving_index + 1) % len(self.images["moving"])
                    self.frame_counter = 0

            else:
                self.image = self.images["sitting"]
                self.moving_index = 0
                self.current_action = "none"

            self.rect.x = max(0, min(self.map_width - LION_SIZE[0], self.rect.x))
            self.rect.y = max(0, min(self.map_height - LION_SIZE[1], self.rect.y))
        else:
            self.image = pygame.transform.rotate(self.images["dead"], 90)
            
    
    def set_predator(self,pred):
        self.predator = pred
    
    def draw(self, surface, camera):
        scaled_rect = camera.apply(self.rect)
        scaled_image = pygame.transform.scale(
            self.image, (scaled_rect.width, scaled_rect.height)
        )
        surface.blit(scaled_image, scaled_rect.topleft)
    
    def get_location(self):
        return self.rect.x , self.rect.y
    
    def killed(self):
        self.alive = False
        self.image = pygame.transform.rotate(self.images["dead"], 90)
        
    def get_dir(self):
        return self.dir
    
    def set_speed(self,speed_new):
        self.speed = speed_new

    def set_action(self,action):
        self.current_action = "none"
    
num_lions = 1
num_giraffe = 1
for i in range(num_lions):
    ani = Animal(lion_images, MAP_WIDTH, MAP_HEIGHT,20,"lion")
    Animals.append(ani)
    Predators.append(ani)
    
for i in range(num_giraffe):
    ani = Animal(giraffe_images, MAP_WIDTH, MAP_HEIGHT,3,"giraffe")
    Animals.append(ani)
    Preys.append(ani)
    
camera = Camera(tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)

running = True

def check_predator():
    return

while running:
    
    player = False
    keys = pygame.key.get_pressed()
    if(player):
        if keys[pygame.K_w] :
            Animals[0].update(player,"up")
        if keys[pygame.K_s]:
            Animals[0].update(player,"down")
        if keys[pygame.K_a]:
            Animals[0].update(player,"left")
        if keys[pygame.K_d]:
            Animals[0].update(player,"right")
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
            # elif event.key == pygame.K_w:
            #     Animals[0].update(player,"up")
            #     print("this")

                

    keys = pygame.key.get_pressed()
    
    screen.fill((0, 100, 0)) 
    render_map(screen, tmx_data, camera)
    for i in range(len(Animals)):
        Animals[i].update(player,"stop")
        Animals[i].draw(screen, camera)
    process_object_layer(Game_over[0],screen, tmx_data, camera) 


    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS
