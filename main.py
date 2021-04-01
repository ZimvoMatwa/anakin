import pygame
import os

pygame.font.init()
# pygame.mixer.init() #sounds of pygame
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init() #turn all of pygame on.


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #creates new window of specified dimensions
pygame.display.set_caption("TieFighter - PvP") #name of the game displayed at the top of the game window

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
# BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
# END_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'island.mp3'))

HEALTH_FONT = pygame.font.SysFont('Roboto', 40)
WINNER_FONT = pygame.font.SysFont('Roboto', 100)

FPS = 60 #defines the refresh rate we want the game to cap at
VEL = 5 #just a speed we decide the object should adjust by when pressed
BULLETS_VEL = 7
MAX_BULLETS = 9 #maximum no. of bullets each character can have on the screen/window at a time. this is not the max bullets they can have in their inventory
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 #py events with +n as their unique ID
RED_HIT = pygame.USEREVENT + 2 #we use event instead of random numbers because we want to interact with the event between classes as an event

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png')) #os.path.join is used instead of path/path/ because some devices us \
# YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)) #takes given object and scales it i.e. the passed object is now contained in this variable e.g. if a = 1 and b = a i.e. b = 1
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) #rotates object using given rotation in degrees
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE) #fills the window with specified RGB color index
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE) #rendering text to screen
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) #placing the rendered text in x,y. 10, 10 are paddings/pixels from the edges
    WIN.blit(yellow_health_text, (10, 10)) #these coordinates are simpler because the x is closer to the 0 x-axis

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))#use "blit" to draw/instert an object on the screen and enter object name+coorodinates. pygame 0.0 coordinates are at the top left corner and down y is +ve
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) #the x and y values are defined in main() function
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update() #updates the game window with changes made to the window

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #tracks when "a" is pressed, also checks if next movement will not be outside of screen
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 17:
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #tracks when "a" is pressed
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 17:
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red): #bullet movement, collion and removal from window
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet): #.colliderect() checks if the red Rect intersects/collides with yellow Rect 
            pygame.event.post(pygame.event.Event(RED_HIT)) #an event identifying if red was hit 
            yellow_bullets.remove(bullet) #removes the bullet(Rect) from window if it collides with object
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet) #remove the bullet once it reaches the edges

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL #this is -ve because the bullet is moving in the opposite direction i.e. we subtract positioning
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2)) #centers text
    pygame.display.update()

    pygame.time.delay(3500) #the time the rendered text will be on display for before game restarts

def main():
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #makes a rectangle of given size and position
    yellow = pygame.Rect(200, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS) #controls the speed of the while loop
        for event in pygame.event.get(): #loops through games to check what is happening and update
            if event.type == pygame.QUIT: #always check if user has quick game first
                run = False
                pygame.quit() #quits the game when you press the exit(x) button instead of restarting it

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: #ensures character does not have infinite bullets
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) #yellow.height/2 is half of the spaceship's height which is where rect will spawn & "-2" makes sure the bullet height is less than ?
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5) #width is not added because the ship is already where the bullet needs to originate. use // to make sure the numbers are not floating point
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()
    
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            # END_SOUND.play()
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() #tells us what keys are being pressed
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    # pygame.quit()
    main()

if __name__ == "__main__": #making sure the main function is only run when the code is run from this file and not as an import on another
    main()