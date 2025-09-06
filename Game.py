import pygame, sys, random
pygame.mixer.init()

#nota importante "abs" funciona como valor absoluto cuando algo llega a negativo lo convierte a positivo, siempre es positivo.

highscore_variable = "highscore.txt" #nombre del file donde se guarda el highscore

def load_high_score():
    try:
        with open(highscore_variable, "r") as f:
            return int(f.read().strip()) #Lee_todo_el_contenido_del_archivo

    except:
        return 0

def save_high_score(value):
    try:
        with open(highscore_variable, "w") as f:
            f.write(str(int(value))) #escribe el highscore del archivo como un int
    except:
        pass


#sonidos descargados como mp3 y ajustes de volumen de esos sonidos (set_volume)
sound = pygame.mixer.Sound("sounds/ding-sfx-330333.mp3")
sound_celling_right_left_walls = pygame.mixer.Sound('sounds/box-sfx-323776.mp3')
lost_game_sound = pygame.mixer.Sound("sounds/big-explosion-sfx-369789.mp3")
level_up_sound = pygame.mixer.Sound('sounds/level-up-enhancement-8-bit-retro-sound-effect-153002.mp3')
sound_celling_right_left_walls.set_volume(1.0)
lost_game_sound.set_volume(1.0)
sound.set_volume(0.1)
pygame.mixer.music.load("sounds/drums-274805.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) #el -1 hace que reproduzca la musica en un loop infinito

#variables globales
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
game_state = STATE_PLAYING #te dice el estado actual de si esta jugando o si ya finalizo la partida.
high_score = load_high_score()
new_high_score = False  #dice si se superó el récord.



def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    global prev_ball_bottom

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 10
    if start:
        if start and ball_speed_x == 0 and ball_speed_y == 0: #
         ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
         ball_speed_y = -abs(speed)  # siempre empieza moviendose hacia arriba
         #borre start = false porque causaba un bug (el texto de press space bar permanecia escrito).

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if ball_speed_y > 0 and abs(ball.bottom - player.top) < 10:  #another fix
            # TODO Task 2: Fix score to increase by 1
            score += 1  # Increase player score
            ball.bottom = player.top - 1 #bug fix
            ball_speed_y *= -1  # Reverse ball's vertical direction
            #block for the same bug fix 23
            hit_offset = (ball.centerx - player.centerx) / (player.width / 2)
            ball_speed_x += hit_offset * 2
            #reduce X so it stays playable
            if abs(ball_speed_x) > max_ball_speed:
                ball_speed_x = max_ball_speed if ball_speed_x > 0 else -max_ball_speed

            # TODO Task 6: Add sound effects HERE
            sound.play()
            check_level()

    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction
        sound_celling_right_left_walls.play()


    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
        sound_celling_right_left_walls.play() #aplica el sonido del mp3 que escogimos

    #Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        #global llama a las variables fuera de la funcion "las globales' y permite modificarlas
        global game_state, high_score, new_high_score
        lost_game_sound.play()

        # verifica el high score y si es superior al pasado le da save en el archivo donde se guardan los highcores
        if score > high_score:
            high_score = score
            save_high_score(high_score)
            new_high_score = True
        else:
            new_high_score = False #si no es superado simplemente no se cumple la funcion de guardar el score

        game_state = STATE_GAME_OVER

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    #Resetea la bola y paddle al estado inicial y guarda el highscore.
    global ball_speed_x, ball_speed_y, score, level_up_score, level, start, new_high_score, game_state
    ball.center = (screen_width // 2, screen_height // 2)
    #la funcion global llama a todas las variables que queremos modificar incluso las que estan fuera del bloque local
    ball_speed_y, ball_speed_x = 0, 0
    #reinicia el score cuando el jugador decida si quiere jugar otra vez
    start = False
    new_high_score = False
    #para que la base vuelva al medio
    player.centerx = screen_width // 2

def play_again():
    global score, level, level_up_score, game_state, start
    score = 0
    level = 1
    level_up_score = 10
    game_state = STATE_PLAYING
    restart()   #vuelve todo_al_estado_inicial

    pygame.event.clear()
    pygame.mixer.music.unpause()

def increase_ball_speed(factor):
    #Multiplica la velocidad de la bola por factor
    global ball_speed_x, ball_speed_y, max_ball_speed
    if ball_speed_x == 0 and ball_speed_y == 0:
        return
    ball_speed_x *= factor
    ball_speed_y *= factor

    #Limittar velocidad para que sea jugable
    if abs(ball_speed_x) > max_ball_speed:
        ball_speed_x = max_ball_speed if ball_speed_x > 0 else -max_ball_speed
    if abs(ball_speed_y) > max_ball_speed:
        ball_speed_y = max_ball_speed if ball_speed_y > 0 else -max_ball_speed


def check_level():
    #Sube de nivel cuando score alcanza la meta
    global level, level_up_score, score
    while score >= level_up_score:
        level += 1
        level_up_score += 10
        increase_ball_speed(speed_increase_factor)
        level_up_sound.play()

def draw_game_over():
        #Pantalla de Game Over
        #Fondo oscuro con transparente
        fondo_oscuro = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        fondo_oscuro.fill((0, 0, 0, 170))  # Negro transparente
        screen.blit(fondo_oscuro, (0, 0))

        # Sizes para diferentes textos
        fuente_grande = pygame.font.Font('freesansbold.ttf', 50)  # Para el título
        fuente_media = pygame.font.Font('freesansbold.ttf', 35)  # Para el score
        fuente_peque = pygame.font.Font('freesansbold.ttf', 25)  # Para instrucciones

        # Textos principales
        texto_game_over = fuente_grande.render("Game Over", True, (255, 255, 255))
        texto_puntaje = fuente_media.render("Score: " + str(score), True, (255, 255, 255))
        texto_record = fuente_media.render("High Score: " + str(high_score), True, (255, 255, 255))
        #explicacion de colores
        #Es un color en formato RGB: (Rojo, Verde, Azul).
        #Cada número va de 0 a 255.
        #(255, 255, 255) significa blanco porque los tres colores están al máximo.
        #Ejemplos:
        #(255, 0, 0) → Rojo.
        #(0, 255, 0) → Verde.
        #(0, 0, 255) → Azul.
        #(0, 0, 0) → Negro.


        # Centro en X de la pantalla (para centrar_todo)
        centro_x = screen_width // 2

        # Dibujar los textos principales
        screen.blit(texto_game_over, (centro_x - texto_game_over.get_width() // 2, 160))
        screen.blit(texto_puntaje, (centro_x - texto_puntaje.get_width() // 2, 230))
        screen.blit(texto_record, (centro_x - texto_record.get_width() // 2, 270))

        # Mostrar mensaje de nuevo récord si aplica
        if new_high_score:
            texto_nuevo = fuente_peque.render("¡NEW HIGHSCORE!", True, (255, 215, 0))  # Dorado
            screen.blit(texto_nuevo, (centro_x - texto_nuevo.get_width() // 2, 310))

        # Instrucciones (estas SIEMPRE aparecen)
        texto_reiniciar = fuente_peque.render("Presiona [R] para jugar otra vez :D", True, (255, 255, 255))
        texto_salir = fuente_peque.render("Presiona [ESC] para salir :(", True, (255, 255, 255))

        screen.blit(texto_reiniciar, (centro_x - texto_reiniciar.get_width() // 2, 360))
        screen.blit(texto_salir, (centro_x - texto_salir.get_width() // 2, 390))

start = False #Arreglo de bug de space bar

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
bg_color = pygame.Color('black')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)# Ball (centered)
prev_ball_bottom = ball.bottom #bug fix 23
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(0, screen_height - 20, player_width, player_height) #fix to the player paddle
player.centerx = screen_width // 2

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
level = 1
level_up_score = 10

# Score Text setup
score = 0
speed_increase_factor = 1.15
max_ball_speed = 20
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score



# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Jemuel Rosario"
    name2 = "Jonathan Gonzalez"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = True


        elif game_state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #Play again
                    play_again()
                if event.key == pygame.K_ESCAPE: #Exit
                    pygame.quit()
                    sys.exit()

    if game_state == STATE_PLAYING:
        pressed = pygame.key.get_pressed()
        player_speed = 0
        if start:  # <only allow movement after the player has started the game
            if pressed[pygame.K_LEFT]:
                player_speed -= 6
            if pressed[pygame.K_RIGHT]:
                player_speed += 6
    else:
        # When not playing
        player_speed = 0

    if game_state == STATE_PLAYING:
        # Game Logic
        ball_movement()
        player_movement()

        # Visuals
        paddle_color = pygame.Color('green4')
        ball_color = pygame.Color('blue2')
        text_color = pygame.Color('brown1')
        level_color = pygame.Color('gold')

        screen.fill(bg_color)
        pygame.draw.rect(screen, paddle_color, player)  # paddle
        pygame.draw.ellipse(screen, ball_color, ball)  # ball

        # Show start prompt until the player presses SPACE
        if not start:
            prompt_font = pygame.font.Font('freesansbold.ttf', 30)  # fuente más pequeña (20 px)
            prompt = prompt_font.render("!Press SPACEBAR to start!", True, pygame.Color('white'))
            prompt_rect = prompt.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
            screen.blit(prompt, prompt_rect)

        # Score / Level
        player_text = basic_font.render(f'{score}', False, text_color)
        screen.blit(player_text, (screen_width / 2 - 15, 10))

        level_text = basic_font.render(f'Level: {level}', False, level_color)
        screen.blit(level_text, (screen_width - 150, 10))

    elif game_state == STATE_GAME_OVER:
        pygame.mixer.music.pause()
        draw_game_over()


    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second