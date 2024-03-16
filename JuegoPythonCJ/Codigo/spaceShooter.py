import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Multimedia/Audio/Fondo.mp3")
pygame.mixer.music.play(loops=-1)

# Definición de constantes
WIDTH, HEIGHT = 900, 700
WINDOW_SIZE = (WIDTH, HEIGHT)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Clase principal del juego
class SpaceShooter:
    def __init__(self):
        # Crear ventana del juego
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.background_image = pygame.image.load("Multimedia/Background/Background_4.png").convert()
        self.player = Player(self)
        self.meteor = Meteor(self)
        self.meteors = pygame.sprite.Group()  # Grupo de meteoritos
        self.bullets = pygame.sprite.Group()  # Grupo de balas
        self.all_sprites.add(self.player)
        self.score = 0



        # Agregar meteoritos
        for _ in range(8):
            self.add_meteor()

    def draw_background(self):  
        """Dibuja el fondo del juego en la ventana."""
        self.window.blit(self.background_image, (0, 0))

    def handle_events(self):
        """Maneja los eventos del juego."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

    def add_meteor(self):
        """Agrega un meteorito al juego."""
        meteor = Meteor(self)
        self.all_sprites.add(meteor)  
        self.meteors.add(meteor)

    def quit_game(self):
        """Cierra el juego correctamente."""   
        pygame.quit()
        sys.exit()

    def run(self):
        """Bucle principal del juego."""
        running = True
        while running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
            

    def update(self):
        """Actualiza los elementos del juego."""
        self.all_sprites.update()
        
        # Colisiones bala - meteorito 
        hits = pygame.sprite.groupcollide(self.bullets, self.meteors, True, True)
        for hit in hits:
            self.score += 1
            self.meteor.explocion_sound.play()
            # Crear nuevo meteorito
            self.add_meteor()

        # Colisiones jugador - meteorito
        hits = pygame.sprite.spritecollide(self.player, self.meteors, True)
        if hits:
            self.player.shield -=25 
            self.add_meteor()
            if self.player.shield <= 0:
                self.quit_game()  # Si hay colisión, el juego termina 

    def draw(self):
        """Dibuja los elementos del juego en la ventana."""
        self.window.fill(BLACK)
        self.draw_background()
        self.all_sprites.draw(self.window) 
        self.draw_text() 
        self.draw_shield(self.player.shield)
        pygame.display.flip()
        
    def draw_text(self): 
        """Dibuja el puntaje en la ventana."""
        font = pygame.font.SysFont("serif", 25)
        text_surface = font.render(str(self.score), True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH // 2, 10)
        self.window.blit(text_surface, text_rect)
        
    def draw_shield(self, porcentaje):
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = (porcentaje / 100) * BAR_LENGHT
        border = pygame.Rect(5, 5, BAR_LENGHT, BAR_HEIGHT)
        fill = pygame.Rect(5, 5, fill, BAR_HEIGHT)
        pygame.draw.rect(self.window, GREEN, fill)
        pygame.draw.rect(self.window, WHITE, border, 2)

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, space_shooter):
        super().__init__()
        self.space_shooter = space_shooter
        # Cargar las imágenes del jugador
        self.spriteP = ["Multimedia/Player/idle.png", "Multimedia/Player/Move1.png"]
        self.images = [pygame.image.load(image).convert() for image in self.spriteP]
        self.image = self.images[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2  # Centrar la nave horizontalmente
        self.rect.bottom = HEIGHT - 10  # Alinear la nave en la parte inferior de la ventana
        self.speed = 5
        self.laser_sound = pygame.mixer.Sound("Multimedia/Audio/Laser_02.mp3")
        self.shield = 100

    def update(self):
        """Controla el movimiento del jugador."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(self.images[1], True, False)  # Invertir la imagen horizontalmente
            self.image.set_colorkey(BLACK)
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.images[1]
            self.image.set_colorkey(BLACK)
        else:
            self.image = self.images[0]
            self.image.set_colorkey(BLACK)
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))  # Limitar el movimiento dentro de la ventana

    def shoot(self):
        """Dispara una bala."""
        bullet = Bullet(self.rect.centerx, self.rect.top) 
        self.space_shooter.all_sprites.add(bullet) 
        self.space_shooter.bullets.add(bullet)
        self.laser_sound.play()


# Clase para el meteorito
class Meteor(pygame.sprite.Sprite):
    def __init__(self, space_shooter):
        super().__init__()
        self.spriteM = ["Multimedia/Enemy/Meteor_01.png", "Multimedia/Enemy/Meteor_02.png",
                        "Multimedia/Enemy/Meteor_03.png", "Multimedia/Enemy/Meteor_04.png",
                        "Multimedia/Enemy/Meteor_05.png", "Multimedia/Enemy/Meteor_06.png",
                        "Multimedia/Enemy/Meteor_07.png", "Multimedia/Enemy/Meteor_08.png",]
        self.images = [pygame.image.load(image).convert() for image in self.spriteM]
        self.image = random.choice(self.images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(5, 10)
        self.speedx = random.randrange(-5, 5)
        self.explocion_sound = pygame.mixer.Sound("Multimedia/Audio/Explocion_01.mp3")

    def update(self):
        """Actualiza la posición del meteorito."""
        self.rect.x += self.speedx 
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)    
    

# Clase para la bala
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Multimedia/Bullet/Charge.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10 

    def update(self):
        """Actualiza la posición de la bala."""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            
class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.title_text = self.font.render("Space Shooter", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.start_text = self.font.render("Press SPACE to start", True, WHITE)
        self.start_rect = self.start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.quit_text = self.font.render("Press Q to quit", True, WHITE)
        self.quit_rect = self.quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        break
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            self.game.window.fill(BLACK)
            self.game.window.blit(self.title_text, self.title_rect)
            self.game.window.blit(self.start_text, self.start_rect)
            self.game.window.blit(self.quit_text, self.quit_rect)
            pygame.display.flip()

        self.game.run()  # Una vez que salimos del bucle, comenzamos el juego principal


if __name__ == "__main__":
    game = SpaceShooter()
    inicio = MainMenu(game)
    inicio.run()
