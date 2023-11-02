import random
import pygame
import pygame.freetype

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption('Гонка')
background_color = (0, 0, 0)
font = pygame.freetype.Font(None, 20)

PLAYER_SPEED = 6 
FPS = 60

class GameRoad(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.y += 3

class EnemyCars(pygame.sprite.Sprite):
    def __init__(self, image, position, speed):
        super().__init__()
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def remove(self):
        if self.rect.top > 800:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.remove()

class PlayerCar:
    def __init__(self, position, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.game_status = 'game'

    def wall(self):
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.left < 0:
            self.rect.left = 0

    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        elif key[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.wall()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def crashCar(self, traffic_cars):
        for car in traffic_cars:
            if car.rect.colliderect(self.rect):
                self.game_status = 'game_over'

def getCarSprite(filename, size, angle):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)
    return image

my_car_image = getCarSprite('sprites/player.png', (100, 70), -90)
road_image = pygame.image.load('sprites/road.png')
road_image = pygame.transform.scale(road_image, (500, 800))

car_sprites = []
car1 = getCarSprite('sprites/car1.png', (100, 70), 90)
car2 = getCarSprite('sprites/car2.png', (100, 70), -90)
car3 = getCarSprite('sprites/car3.png', (100, 70), -90)
car_sprites.extend((car1, car2, car3))

my_car = PlayerCar((300, 600), my_car_image)

road_group = pygame.sprite.Group()
spawn_road_time = pygame.USEREVENT
pygame.time.set_timer(spawn_road_time, 1000)

traffic_cars_group = pygame.sprite.Group()
spawn_traffic_time = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_traffic_time, 1000)

road = GameRoad(road_image, (250, 400))
road_group.add(road)
road = GameRoad(road_image, (250, 0))
road_group.add(road)

score = 0

def spawn_road():
    road_bg = GameRoad(road_image, (250, -600))
    road_group.add(road_bg)

def spawn_traffic():
    if my_car.game_status == 'game':
        position = (random.randint(40, 460), random.randint(-60, -40))
        speed = random.randint(7, 20)
        traffic_car = EnemyCars(random.choice(car_sprites), position, speed)
        traffic_cars_group.add(traffic_car)

        global score
        score += 1


def draw_all():
    road_group.update()
    road_group.draw(screen)
    traffic_cars_group.update()
    traffic_cars_group.draw(screen)
    my_car.draw(screen)

    score_text = f"Счет: {score}"
    text_surface, _ = font.render(score_text, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.topright = (screen.get_width() - 10, 10)
    font.render_to(screen, text_rect.topleft, score_text, (255, 255, 255))

def restart_game():
    my_car.rect.center = (300, 600)
    my_car.game_status = 'game'
    traffic_cars_group.empty()
    global score
    score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_road_time:
            spawn_road()
        if event.type == spawn_traffic_time:
            spawn_traffic()

    screen.fill(background_color)
    if my_car.game_status == 'game':
        my_car.movement()
        draw_all()
        my_car.crashCar(traffic_cars_group)
    elif my_car.game_status == 'game_over':
        game_over_text = f'Увы, вы проиграли! Ваш счет: {score}'
        restart_text = 'Нажмите R, чтобы сыграть еще раз.'
        text_surface, _ = font.render(game_over_text, (255, 255, 255))
        text_surface2, _ = font.render(restart_text, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect2 = text_surface2.get_rect()
        text_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - text_rect.height)
        text_rect2.center = (screen.get_width() // 2, screen.get_height() // 2 + text_rect2.height)
        font.render_to(screen, text_rect.topleft, game_over_text, (255, 255, 255))
        font.render_to(screen, text_rect2.topleft, restart_text, (255, 255, 255))


        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            restart_game()

    pygame.display.flip()
    clock.tick(FPS)
