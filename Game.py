import pygame, sys, random
pygame.mixer.init()

#Sonidos extras
sound = pygame.mixer.Sound("sounds/ding-sfx-330333.mp3")
sound_celling_right_left_walls = pygame.mixer.Sound('sounds/box-sfx-323776.mp3')
lost_game_sound = pygame.mixer.Sound("sounds/big-explosion-sfx-369789.mp3")
sound_celling_right_left_walls.set_volume(1.0)
lost_game_sound.set_volume(1.0)
sound.set_volume(0.1)

pygame.mixer.music.load("sounds/drums-274805.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)





def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 7
    if start:
        if start and ball_speed_x == 0 and ball_speed_y == 0:
         ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
         ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
         start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # TODO Task 2: Fix score to increase by 1
            score += 1  # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction
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
        sound_celling_right_left_walls.play()

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        lost_game_sound.play()
        restart()  # Reset the game

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
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score, level_up_score, level
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    score = 0  # Reset player score
    level = 1 # Resets level
    level_up_score = 10 #Resets level up score



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
    leveled_up = False
    while score >= level_up_score:
        level += 1
        level_up_score += 10
        increase_ball_speed(speed_increase_factor)
        leveled_up = True

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
bg_color = pygame.Color('seashell4')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball (centered)
# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 200
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player paddle

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

start = False  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Jemuel Rosario"
    name2 = "Jonathan Gonzalez"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right

    # Game Logic
    ball_movement()
    player_movement()

    # Visuals
    paddle_color = pygame.Color('green4')
    ball_color = pygame.Color('blue2')
    text_color = pygame.Color('brown1')
    screen.fill(bg_color)  # Clear screen with background color
    pygame.draw.rect(screen, paddle_color, player)  # Draw player paddle
    # TODO Task 3: Change the Ball Color
    pygame.draw.ellipse(screen, ball_color, ball)  # Draw ball
    player_text = basic_font.render(f'{score}', False, text_color)  # Render player score
    screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen

    #Mostar nivel en pantalla
    level_text = basic_font.render(f'Level: {level}', False, text_color)
    screen.blit(level_text, (screen_width - 150, 10))
    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second