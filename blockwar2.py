"""
 Show how to fire bullets at the mouse.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""
import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pygame.font.init()

scoreboard = pygame.font.SysFont('Calibri',30)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
# --- Classes


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super(Block,self).__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()
    def update(self):
        if self.rect.x < 10:
            self.rect.x = 10
        if self.rect.x > (SCREEN_WIDTH-10):
            self.rect.x = SCREEN_WIDTH-10
        if self.rect.y < 10:
            self.rect.y = 10
        if self.rect.y > (SCREEN_HEIGHT-10):
            self.rect.y = SCREEN_HEIGHT-10
        
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super(Player,self).__init__()
        self.frags = 0
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.level = 1
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = 0
    def die (self):
        self.rect.x = SCREEN_WIDTH/2
        self.rect.y = SCREEN_HEIGHT/2
        
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """

        # Call the parent class (Sprite) constructor
        super(Bullet,self).__init__()

        # Set up the image for the bullet
        self.image = pygame.Surface([4, 4])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y

        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 5
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity

    def update(self):
        """ Move the bullet. """

        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()



# --- Create the window

# Initialize Pygame
pygame.init()

# Set the height and width of the screen

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("poop raiders")
pygame.mouse.set_visible(False)
# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites

for i in range(50):
    # This represents a block
    block = Block(BLUE)

    # Set a random location for the block
    block.rect.x = random.randrange(SCREEN_WIDTH)
    block.rect.y = random.randrange(SCREEN_HEIGHT - 50)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a red player block
player = Player()
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

player.rect.x = SCREEN_WIDTH / 2
player.rect.y = SCREEN_HEIGHT / 2

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button

            # Get the mouse position
            pos = pygame.mouse.get_pos()

            mouse_x = pos[0]
            mouse_y = pos[1]
            
            # Create the bullet based on where we are, and where we want to go.
            bullet = Bullet(player.rect.x, player.rect.y, mouse_x, mouse_y)

            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_DOWN:
                player.vel_y = player.vel_y + 1
            if event.key == pygame.K_UP:
                player.vel_y = player.vel_y - 1
            if event.key == pygame.K_LEFT:
                player.vel_x = player.vel_x - 1
            if event.key == pygame.K_RIGHT:
                player.vel_x = player.vel_x + 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player.vel_y = 0
            if event.key == pygame.K_UP:
                player.vel_y = 0
            if event.key == pygame.K_RIGHT:
                player.vel_x = 0
            if event.key == pygame.K_LEFT:
                player.vel_x = 0
                
    # --- Game logic

    #move the player by velocity
    player.rect.x = player.rect.x + player.vel_x
    player.rect.y = player.rect.y + player.vel_y
    if player.rect.x > (SCREEN_WIDTH - 20):
        #player.rect.x = (SCREEN_WIDTH - 10)
        player.vel_x = 0
    if player.rect.x < 0:
        #player.rect.x = 0
        player.vel_x = 0
    if player.rect.y > (SCREEN_HEIGHT -20):
        #player.rect.y = (SCREEN_HEIGHT-10)
        player.vel_y = 0
    if player.rect.y < 0:
        #player.rect.y = 10
        player.vel_y = 0
    #count the bad guys
    blockcount = 0
    for block in block_list:
        blockcount += 1
    if blockcount < 10:
        player.level += 1
        while blockcount < 50:
            block = Block(BLUE)
    # Set a random location for the block
            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(SCREEN_HEIGHT - 50)
    # Add the block to the list of objects
            block_list.add(block)
            all_sprites_list.add(block)
            blockcount += 1

    #move the bad guys
    for block in block_list:
        block.rect.x = block.rect.x + (random.randrange(-1,2))
        block.rect.y = block.rect.y + (random.randrange(-1,2))
        block_hit_list = pygame.sprite.spritecollide(player, block_list, True)
        for block in block_hit_list:
            player.frags = player.frags -1
            player.die()

    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            player.frags += 1
            score += 1
            print(player.frags)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    # --- Draw a frame

    # Clear the screen
    screen.fill(WHITE)

    #draw the score
    scores = "frags: " + str(player.frags) + " level: " + str(player.level)
    scoretext = scoreboard.render(scores,False,(0,0,0))
    screen.blit(scoretext,(SCREEN_WIDTH/2,0))
    #draw the reticule
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]
    pygame.draw.circle(screen,RED,[mouse_x,mouse_y],3,2)
    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)


pygame.quit()
