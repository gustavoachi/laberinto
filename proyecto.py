from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed

        self.rect = self.image.get_rect()

        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    side = "left"
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
 
        #imagen de pared - un rectángulo del tamaño y color requerido
        self.image = Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))
 
        #cada objeto debe almacenar el rect - la propiedad rectangular
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
 
    def draw_wall(self):
        draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Laberinto")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

#agregamos sonido para ganar o perder
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

player = Player('hero.png', 5, win_height - 80, 4)
cyborg = Enemy('cyborg.png', win_width - 80, 280, 2)
treasure = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

w1 = Wall(154, 205, 50, 100, 20 , 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20 , 10, 380)

w4 = Wall(154, 205, 50, 220, 110 , 10, 370)
w5 = Wall(154, 205, 50, 325, 30 , 10, 370)
w6 = Wall(154, 205, 50, 430, 110 , 10, 370)

font.init()
main_font = font.Font(None, 70)
button_font = font.Font(None, 35)
win_text = main_font.render('¡GANASTE!', True, (255, 215, 0))
lose_text = main_font.render('¡PERDISTE!', True, (180, 0, 0))

game = True
finish = False
clock = time.Clock()
FPS = 60

# Función para mostrar botones
def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse_pos = mouse.get_pos()
    click = mouse.get_pressed()

    if x + w > mouse_pos[0] > x and y + h > mouse_pos[1] > y:
        draw.rect(window, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        draw.rect(window, inactive_color, (x, y, w, h))

    text_surf = button_font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    window.blit(text_surf, text_rect)

# Funciones para cambiar el estado del juego
def game_intro():
    global in_menu, game, finish
    in_menu = True
    finish = False
    while in_menu:
        for e in event.get():
            if e.type == QUIT:
                in_menu = False
                game = False

        window.fill((0, 102, 204))
        large_text = main_font.render("Laberinto", True, (255, 255, 255))
        window.blit(large_text, (win_width / 2 - large_text.get_width() / 2, win_height / 4))

        draw_button("Jugar", 250, 300, 200, 50, (0, 255, 0), (0, 200, 0), start_game)
        draw_button("Salir", 250, 400, 200, 50, (255, 0, 0), (200, 0, 0), quit_game)

        display.update()
        clock.tick(15)

def start_game():
    global in_menu, finish, player, cyborg, treasure
    in_menu = False
    finish = False
    player.rect.x = 5
    player.rect.y = win_height - 80
    cyborg.rect.x = win_width - 80
    cyborg.rect.y = 280
    treasure.rect.x = win_width - 120
    treasure.rect.y = win_height - 80

def quit_game():
    global in_menu,game,finish
    game = False
    in_menu = False
    finish = False

def game_over_screen(message):
    global finish, game
    finish = True
    while finish:
        for e in event.get():
            if e.type == QUIT:
                finish = False
                game = False

        window.fill((0, 102, 204))
        large_text = main_font.render(message, True, (255, 255, 255))
        window.blit(large_text, (win_width / 2 - large_text.get_width() / 2, win_height / 4))

        draw_button("Reiniciar", 250, 300, 200, 50, (0, 255, 0), (0, 200, 0), start_game)
        draw_button("Salir", 250, 400, 200, 50, (255, 0, 0), (200, 0, 0), quit_game)

        display.update()
        clock.tick(15)

# Mostrar el menú de inicio
game_intro()

while game:
    for e in event.get():
       if e.type == QUIT:
           game = False

    if not finish:
        window.blit(background,(0, 0))

        player.update()
        cyborg.update()

        player.reset()
        cyborg.reset()
        treasure.reset()
    
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
    
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
    
        #Juego ganado
        if sprite.collide_rect(player, treasure):
            game_over_screen('¡GANASTE!')
            money.play()

        #Juego perdido
        
        if sprite.collide_rect(player, cyborg) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6):
            game_over_screen('¡PERDISTE!')
            kick.play()


    display.update()
    clock.tick(FPS)