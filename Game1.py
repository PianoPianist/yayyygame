import pygame
import random

# Initialize the game engine
pygame.init()
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (169, 50, 52)
BLUE = (0, 0, 255)
LIGHTRED = (191, 52, 52)
GREY = (129, 129, 129)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
CYAN = (81, 223, 210)
FONCOL = (36, 255, 0)

# Set the height and width of the screen
size = (1000, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("chekc")
 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
 

class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height, colour):
        image = pygame.Surface([width, height]).convert()
        image.set_colorkey(colour)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return image

class Skeleton(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
        super().__init__()
        sprite_sheet = SpriteSheet("bag.png")
        self.image = sprite_sheet.get_image(0, 0, 287, 287, BLACK)
        self.image = pygame.transform.scale(self.image, [33, 33])
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .47
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = 6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = -6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
        super().__init__()
        sprite_sheet = SpriteSheet("banana.png")
        self.image = sprite_sheet.get_image(0, 0, 340, 236, WHITE)
        self.image = pygame.transform.scale(self.image, [33, 33])
        self.rect = self.image.get_rect()
        
    
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .47
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
class Lives(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("Heart_icon.png")
        self.image = sprite_sheet.get_image(0, 0, 27, 27, GREY)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 60

class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("gdus.png")
        self.image = sprite_sheet.get_image(385, 257, 960, 1228, BLACK)
        self.image = pygame.transform.scale(self.image, [72, 72])
        self.rect = self.image.get_rect()
class Portal2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("bdus.png")
        self.image = sprite_sheet.get_image(385, 257, 960, 1228, BLACK)
        self.image = pygame.transform.scale(self.image, [72, 72])
        self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, skeleton, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.skeleton = skeleton
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, skeleton, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, skeleton, player)
 
        # Array with width, height, x, and y of platform        
        level = [[59, 500, 0, 0],
                 [1000-59, 56, 59, 0],
                 [59, 500, 1000-59, 0],
                 [1000, 59, 0, 500-55],
                 [185, 56, 0, 278],
                 [3, 26, 185, 284],
                 [62, 59, 188, 278+56],
                 [55, 59*4+42, 317, 0],
                 [68, 56, 188+61, 59*3-10],
                 [62*4, 120, 317+60, 334],
                 [62*2+3, 56, 814, 278],
                 [62, 56, 750, 334],
                 [55, 56*3, 567, 56],
                 [62*2+2, 56, 622, 167],
                 [55, 56, 629, 223],
                 ]
        
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.skeleton = self.skeleton
            block.player = self.player
            self.platform_list.add(block)
class Level_02(Level):
    """ Definition for level 1. """
 
    def __init__(self, skeleton, player):
        """ Create level 1. """
        # Call the parent constructor
        Level.__init__(self, skeleton, player)
        # Array with width, height, x, and y of platform        
        level = [[59, 500, 0, 0],
                 [1000-59, 56, 59, 0],
                 [59, 500, 1000-59, 0],
                 [1000, 59, 0, 500-55],
                 [310, 56, 0, 167],
                 [130, 53, 817, 171],
                 [183, 50, 503, 395],
                 [58*4+13, 54, 378, 224],
                 [55, 56, 379, 278],
                 [58, 55, 690, 169],
                 ]
        
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.skeleton = self.skeleton
            block.player = self.player
            self.platform_list.add(block)

class Level_03(Level):
    """ Definition for level 1. """
 
    def __init__(self, skeleton, player):
        """ Create level 1. """
        # Call the parent constructor
        Level.__init__(self, skeleton, player)
        # Array with width, height, x, and y of platform        
        level = [[59, 500, 0, 0],
                 [1000-59, 56, 59, 0],
                 [59, 500, 1000-59, 0],
                 [1000, 59, 0, 500-55],
                 [802-623, 55, 628, 280],
                 [809-753, 112, 753, 333],
                 [433-190, 273-226+6, 192, 226],
                 [247-192, 444-276, 192, 278],
                 [58, 53, 815, 337],
                 [58, 53, 127, 337],
                 [58, 53, 876, 227],
                 [58, 53, 65, 227],
                 [58, 53, 253, 113],
                 [747-692, 163-56, 692, 56],
                 ]
        
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.skeleton = self.skeleton
            block.player = self.player
            self.platform_list.add(block)


class Level_04(Level):
    """ Definition for level 1. """
 
    def __init__(self, skeleton, player):
        """ Create level 1. """
        # Call the parent constructor
        Level.__init__(self, skeleton, player)
        # Array with width, height, x, and y of platform        
        level = [[59, 500, 0, 0],
                 [1000-59, 56, 59, 0],
                 [59, 500, 1000-59, 0],
                 [1000, 59, 0, 500-55],
                 [183-59, 55, 59, 279],
                 [941-815, 443-282, 815, 333],
                 [872-813, 334-281, 815, 281],
                 [683-564, 332-278, 565, 280],
                 [941-750, 54, 750, 170],
                 [246-191, 163-52, 192, 56],
                 [66, 54, 127, 114],
                 [371-316, 223-55, 317, 55],
                 [559-504, 167-56, 504, 56],
                 [121, 49, 500, 336],
                 ]
        
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.skeleton = self.skeleton
            block.player = self.player
            self.platform_list.add(block)

class Level_05(Level): 
    def __init__(self, skeleton, player):
        Level.__init__(self, skeleton, player)
        level = [[47, 200, 0, 0],
                 [1000-59, 49, 59, 0],
                 [59, 500, 954, 0],
                 [1000, 59, 0, 458],
                 [247, 700, 0, 213],
                 [43, 413-41, 303, 41],
                 [953-704, 209-41, 704, 41],
                 [644-404, 413-376, 404, 378],
                 [396-346, 41, 346, 291],
                 [496-454, 375-211, 454, 211],
                 [300, 40, 346, 126],
                 [397-335, 207-166, 335, 166],
                 [647-603, 414-166, 603, 166],
                 [895-700, 42, 703, 251],
                 [42, 124, 855, 292],
                 [45, 71, 704, 345],
                 [110, 41, 748, 376],
                 [50, 41, 496, 250],
                 ]
        
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.skeleton = self.skeleton
            block.player = self.player
            self.platform_list.add(block)

var = True
var2 = True
#WARRIOR GAME

class Bomb(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("Untitled.png")
        self.image = sprite_sheet.get_image(0, 0, 41, 57, WHITE)
        self.rect = self.image.get_rect()

    def move(self):
        if score < 50:
            self.change_y = random.randint(2, 6)
        elif score > 50:
            self.change_y = random.randint(3, 8)
        else:
            self.change_y = random.randint(4, 10)
        self.rect.y += self.change_y
        if self.rect.y > 500:
            self.kill()


class Soldier(pygame.sprite.Sprite):

    def __init__(self):
        self.change_x = 0
        self.change_y = 0
        self.direction = "R"
        super().__init__()
        self.walking_frames_l = []
        self.walking_frames_r = []

        sprite_sheet = SpriteSheet("characters.png")
        self.image = sprite_sheet.get_image(0, 5, 111, 123, BLACK)
        self.walking_frames_l.append(self.image)

        self.image = sprite_sheet.get_image(120, 5, 111, 123, BLACK)
        self.walking_frames_l.append(self.image)
        self.image = sprite_sheet.get_image(230, 5, 111, 123, BLACK)
        self.walking_frames_l.append(self.image)

        self.image = sprite_sheet.get_image(0, 5, 111, 123, BLACK)
        self.image = pygame.transform.flip(self.image, True, False)
        self.walking_frames_r.append(self.image)
        self.image = sprite_sheet.get_image(120, 5, 111, 123, BLACK)
        self.image = pygame.transform.flip(self.image, True, False)
        self.walking_frames_r.append(self.image)
        self.image = sprite_sheet.get_image(230, 5, 111, 123, BLACK)
        self.image = pygame.transform.flip(self.image, True, False)
        self.walking_frames_r.append(self.image)

        self.image = self.walking_frames_r[0]

        self.rect = self.image.get_rect()
        self.rect.y = 497
        self.rect.x = 348
        self.frame = 0
        self.moved = 0

    def move(self):
        self.rect.x += self.change_x

    def walk(self):
        self.moved += abs(self.change_x)

        pixels_for_one_step = 45
        if self.moved > pixels_for_one_step:
            self.frame += 1
            self.moved = 0
            if self.frame >= len(self.walking_frames_r):
                self.frame = 0
        if self.direction == "R":
            self.image = self.walking_frames_r[self.frame]
        else:
            self.image = self.walking_frames_l[self.frame]

        if self.change_x == 0 and self.direction == "R":
            self.image = self.walking_frames_r[2]
        if self.change_x == 0 and self.direction == "L":
            self.image = self.walking_frames_l[2]

    def go_left(self):
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        self.direction = "R"
        self.change_x = 6

    def stop(self):
        self.change_x = 0
        self.image = self.walking_frames_r[2]


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.change_x = 0
        self.change_y = 0
        self.direction = ""
        sprite_sheet = SpriteSheet("Bullet_2.png")
        self.image = sprite_sheet.get_image(0, 0, 20, 66, BLACK)
        self.image = pygame.transform.rotate(self.image, 45)
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0

    def moveright(self):
        self.change_x = 2
        self.change_y = 2
        self.rect.y -= self.change_y
        self.rect.x -= self.change_x
        if self.rect.y < -30:
            self.kill()

    def moveleft(self):
        self.change_x = -2
        self.change_y = 2
        self.rect.y -= self.change_y
        self.rect.x -= self.change_x
        if self.rect.y < -30:
            self.kill()


class Liveswar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("Heart_icon.png")
        self.image = sprite_sheet.get_image(0, 0, 27, 27, GREY)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 45


def show_bomb():
    bomb = Bomb()
    bomb.rect.x = random.randint(0, 1000 - 48)
    bomb_list.add(bomb)
    all_sprites.add(bomb)

bomb = Bomb()
soldier = Soldier()
heart = Liveswar()
heart1 = Liveswar()
heart2 = Liveswar()

heart.rect.x = 60
heart1.rect.x = 90
heart2.rect.x = 120

all_sprites = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()
heart_list = pygame.sprite.Group()

all_sprites.add(soldier)
bomb_list.add(bomb)
all_sprites.add(bomb)

all_sprites.add(heart)
heart_list.add(heart)

all_sprites.add(heart1)
heart_list.add(heart1)

all_sprites.add(heart2)
heart_list.add(heart2)

screen_rect = screen.get_rect()
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
play = pygame.image.load("Play.png")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon(icon)
bg = pygame.image.load("3601933.jpg")
lives = 3
score = 0
fontwar = pygame.font.Font("MISTRAL.ttf", 30)
fontwar2 = pygame.font.Font("MISTRAL.ttf", 100)
heart = Liveswar()
lives2 = pygame.mixer.Sound("2 lives.mp3")
life1 = pygame.mixer.Sound("1 life.mp3")
lost = pygame.mixer.Sound('lost.mp3')
click = pygame.mixer.Sound("click.wav")
speak = ""
yesblit = ""
writeonce = "one"
prevhigh = 0
start = True
#playbg = pygame.image.load("Start.png")
#playbg = pygame.transform.scale(playbg, [1000, 500])
bulletsound = pygame.mixer.Sound("rumble.flac")
argh = pygame.mixer.Sound("1.mp3")
pygame.mixer.music.load("War Song.mp3")
pygame.mixer.music.play()

#screen.blit(playbg, [0, 0])
#screen.blit(play, [403, 225])
# Loop until the user clicks the close button.
done = False
#button1 = pygame.draw.rect(screen, GREEN, [200, 400, 100, 75])
#button2 = pygame.draw.rect(screen, GREEN, [500, 400, 100, 75])
#button3 = pygame.draw.rect(screen, GREEN, [800, 400, 100, 75])
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
game_num = -2
#pygame.init()
decided = False
mainscr = pygame.image.load("mainscreen.png")
mainscr = pygame.transform.scale(mainscr, [1000, 500])
one= pygame.draw.rect(screen, GREEN, [330, 350, 90, 90])
two = pygame.draw.rect(screen, GREEN, [480, 350, 90, 90])
three= pygame.draw.rect(screen, GREEN, [630, 350, 90, 90])

def main():
    global var
    global startyt
    global current_level_no
    global lvl_1
    global active_sprite_list
    global portal_list
    global player_list
    global enemy_list
    global current_level
    global heart_list
    global skeleton
    global player
    global font
    global font2
    global lives
    global jumpsound
    global icon 
    global lvl_2
    global lvl_3 
    global lvl_4 
    global lvl_5 
    #global lvl_6 
    global win 
    
    global yes
    global once 
    global yesblit
    global timeone
    global time_taken
    global level_list
    global lives
    global list1
    global portal
    global portal2
    
    global portalsound
    global death
    global heart
    global heart1
    global heart2
    global lastbest
    global prevhigh2
    global finaltime
    if var:
        
        #print("yes")
        font = pygame.font.Font("COOPBL.TTF", 30)
        font2 = pygame.font.Font("COOPBL.TTF", 50)
        icon = pygame.image.load("icon.png")
        lvl_2 = pygame.image.load("lvl_2.png")
        lvl_1 = pygame.image.load("lvl_1.png")
        lvl_3 = pygame.image.load("lvl_3.png")
        lvl_4 = pygame.image.load("lvl4.png")
        lvl_5 = pygame.image.load("lvl_5.png")
       # lvl_6 = pygame.image.load("lvl6.png")
        win = pygame.image.load("you_win.png")
        opendoc = "yes"
        yes = "yes"
        once = "one"
        yesblit = "no"
        timeone = 0
        time_taken = 0
        lives = 3
        level_list = []
        skeleton = Skeleton()
        player = Player()
        
        jumpsound = pygame.mixer.Sound("jump.ogg")
        portalsound = pygame.mixer.Sound("portal2.ogg")
        death = pygame.mixer.Sound("death.mp3")
        level_list.append(Level_01(skeleton, player) )
        level_list.append(Level_02(skeleton, player) )
        level_list.append(Level_03(skeleton, player) )
        level_list.append(Level_04(skeleton, player) )
        level_list.append(Level_05(skeleton, player) )
        #level_list.append(Level_06(skeleton, player) )
        current_level_no = 0
        current_level = level_list[current_level_no]
        
        lvl_2 = pygame.transform.scale(lvl_2, [1000, 500])
        lvl_1 = pygame.transform.scale(lvl_1, [1000, 500])
        lvl_3 = pygame.transform.scale(lvl_3, [1000, 500])
        lvl_4 = pygame.transform.scale(lvl_4, [1000, 500])
        lvl_5 = pygame.transform.scale(lvl_5, [1000, 500])
       # lvl_6 = pygame.transform.scale(lvl_6, [1000, 500])
        win = pygame.transform.scale(win, [1000, 500])
        icon = pygame.transform.scale(icon, [16, 16])
        pygame.display.set_caption("Mirror Roll")
        pygame.display.set_icon(icon)
        heart = Lives()
        heart1 = Lives()
        heart2 = Lives()
        portal = Portal()
        portal2 = Portal2()

        heart.rect.x = 60
        heart1.rect.x = 90
        heart2.rect.x = 120
        
        active_sprite_list = pygame.sprite.Group()
        player_list = pygame.sprite.Group()
        portal_list = pygame.sprite.Group()
        enemy_list = pygame.sprite.Group()
        heart_list = pygame.sprite.Group()

        
        heart_list.add(heart)
        heart_list.add(heart1)

        heart_list.add(heart2)
        
        skeleton.level = current_level
        player.level = current_level
        skeleton.rect.x = 870
        skeleton.rect.y = 231
        player.rect.x = 281
        player.rect.y = 118
        portal.rect.x = 475
        portal.rect.y = 260
        portal2.rect.x = 475
        portal2.rect.y = 260
        active_sprite_list.add(skeleton)
        active_sprite_list.add(player)
        active_sprite_list.add(portal)
        #active_sprite_list.add(portal2)
        portal_list.add(portal)
       # portal_list.add(portal2)
        player_list.add(player)
        
        enemy_list.add(skeleton)
        clock = pygame.time.Clock()
        var = False

     # Loop until the user clicks the close button.
    # Used to manage how fast the screen updates
    
 
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            skeleton.go_left()
            player.go_left()
        if event.key == pygame.K_RIGHT:
            skeleton.go_right()
            player.go_right()
        if event.key == pygame.K_UP:
            skeleton.jump()
            player.jump()
            if current_level_no !=7:
                jumpsound.play()
            
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and skeleton.change_x > 0:
            skeleton.stop()
        if event.key == pygame.K_RIGHT and skeleton.change_x < 0:
            skeleton.stop()
        if event.key == pygame.K_LEFT and player.change_x < 0:
            player.stop()
        if event.key == pygame.K_RIGHT and player.change_x > 0:
            player.stop()
    
    screen.fill(CYAN)
    if current_level_no == 0:
        screen.blit(lvl_1, [0, 0])
    if current_level_no == 1:
        
      #  portal = Portal()

        screen.blit(lvl_2, [0, 0])
        portal.rect.x = 575
        portal.rect.y = 320
        if yes == "yes":
            player.rect.y = 112
            player.rect.x = 79
            skeleton.rect.y = 112
            skeleton.rect.x = 895
            yes = "no"
    if current_level_no == 2:
      #  portal = Portal()
        
        screen.blit(lvl_3, [0, 0])
        portal.rect.x = 849
        portal.rect.y = 98
        if yes == "yes":
            player.rect.y = 409
            player.rect.x = 907
            skeleton.rect.y = 412
            skeleton.rect.x = 81
            yes = "no"
        active_sprite_list.remove(portal)
        portal_list.remove(portal)
        active_sprite_list.add(portal2)
        portal_list.add(portal2)
        portal2.rect.x = 856
        portal2.rect.y = 104
    if current_level_no == 3:
        #portal.sprite_sheet = SpriteSheet("bdus.png")
       
        
        screen.blit(lvl_4, [0, 0])
        
        if yes == "yes":
            player.rect.y = 214
            player.rect.x = 99
            skeleton.rect.y = 98
            skeleton.rect.x = 849
            yes = "no"
        active_sprite_list.remove(portal2)
        portal_list.remove(portal2)
        active_sprite_list.add(portal)
        portal_list.add(portal)
        portal.rect.x = 610
        portal.rect.y = 208
    if current_level_no == 4:
       # portal = Portal()
        screen.blit(lvl_5, [0, 0])
#        portal.rect.x = 519
 #       portal.rect.y = 300
        if yes == "yes":
            player.rect.y = 220
            player.rect.x = 516
            skeleton.rect.y = 171
            skeleton.rect.x = 158
            yes = "no"
        active_sprite_list.remove(portal)
        portal_list.remove(portal)
        active_sprite_list.add(portal2)
        portal_list.add(portal2)
        portal2.rect.x = 531
        portal2.rect.y = 305
  #  if current_level_no == 5:
   #   #  portal = Portal2()
    #    screen.blit(lvl_6, [0, 0])
     #   portal2.rect.x = 95
      #  portal2.rect.y = 210
       # if yes == "yes":
        #    player.rect.y = 133
         #   player.rect.x = 872
          #  skeleton.rect.y = 389
           # skeleton.rect.x = 226
            #yes = "no"

    active_sprite_list.update()
    if pygame.sprite.groupcollide(player_list, enemy_list, False, False):
        death.play()
        lives-=1
        yes = "yes"
        if current_level_no == 0:
            if yes == "yes":
                skeleton.rect.x = 870
                skeleton.rect.y = 231
                player.rect.x = 281
                player.rect.y = 118
                yes = "no"
        if current_level_no == 1:        
            if yes == "yes":
                player.rect.y = 112
                player.rect.x = 79
                skeleton.rect.y = 112
                skeleton.rect.x = 895
                yes = "no"
        if current_level_no == 2:
            if yes == "yes":
                player.rect.y = 409
                player.rect.x = 907
                skeleton.rect.y = 412
                skeleton.rect.x = 81
                yes = "no"
        if current_level_no == 3:
            if yes == "yes":
                player.rect.y = 214
                player.rect.x = 99
                skeleton.rect.y = 98
                skeleton.rect.x = 849
                yes = "no"
        if current_level_no == 4:
            if yes == "yes":
                player.rect.y = 220
                player.rect.x = 516
                skeleton.rect.y = 171
                skeleton.rect.x = 158
                yes = "no"
        if current_level_no ==5:
            if yes == "yes":
                player.rect.y = 133
                player.rect.x = 872
                skeleton.rect.y = 389
                skeleton.rect.x = 226
                yes = "no"
    if not( current_level_no == 2 or current_level_no == 4):
        #print("y", current_level_no)
        if pygame.sprite.groupcollide(portal_list, player_list, False, False):
            portalsound.play()
            if current_level_no < 4:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                skeleton.level = current_level
                yes = "yes"
            else:
                current_level_no = 7
                screen.blit(win, [0, 0])
                for i in active_sprite_list:
                    i.kill()
                    
        
        
        if pygame.sprite.groupcollide(portal_list, enemy_list, False, False):
            lives-=1
            yes = "yes"
            if current_level_no == 0:
                if yes == "yes":
                    skeleton.rect.x = 870
                    skeleton.rect.y = 231
                    player.rect.x = 281
                    player.rect.y = 118
                    yes = "no"
            if current_level_no == 1:        
                if yes == "yes":
                    player.rect.y = 112
                    player.rect.x = 79
                    skeleton.rect.y = 112
                    skeleton.rect.x = 895
                    yes = "no"
            if current_level_no == 2:
                if yes == "yes":
                    player.rect.y = 409
                    player.rect.x = 907
                    skeleton.rect.y = 412
                    skeleton.rect.x = 81
                    yes = "no"
            if current_level_no == 3:
                if yes == "yes":
                    player.rect.y = 214
                    player.rect.x = 99
                    skeleton.rect.y = 98
                    skeleton.rect.x = 849
                    yes = "no"
            if current_level_no == 4:
                if yes == "yes":
                    player.rect.y = 220
                    player.rect.x = 516
                    skeleton.rect.y = 171
                    skeleton.rect.x = 158
                    yes = "no"
            if current_level_no ==5:
                if yes == "yes":
                    player.rect.y = 133
                    player.rect.x = 872
                    skeleton.rect.y = 389
                    skeleton.rect.x = 226
                    yes = "no"
    else:
       # print("n", current_level_no)
        if pygame.sprite.groupcollide(portal_list, enemy_list, False, False):
            portalsound.play()
            if current_level_no < 4:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                skeleton.level = current_level
                yes = "yes"
            else:
                current_level_no = 7
                screen.blit(win, [0, 0])
                for i in active_sprite_list:
                    i.kill()
                    
        
        if pygame.sprite.groupcollide(portal_list, player_list, False, False):
            lives-=1
            yes = "yes"
            if current_level_no == 0:
                if yes == "yes":
                    skeleton.rect.x = 870
                    skeleton.rect.y = 231
                    player.rect.x = 281
                    player.rect.y = 118
                    yes = "no"
            if current_level_no == 1:        
                if yes == "yes":
                    player.rect.y = 112
                    player.rect.x = 79
                    skeleton.rect.y = 112
                    skeleton.rect.x = 895
                    yes = "no"
            if current_level_no == 2:
                if yes == "yes":
                    player.rect.y = 409
                    player.rect.x = 907
                    skeleton.rect.y = 412
                    skeleton.rect.x = 81
                    yes = "no"
            if current_level_no == 3:
                if yes == "yes":
                    player.rect.y = 214
                    player.rect.x = 99
                    skeleton.rect.y = 98
                    skeleton.rect.x = 849
                    yes = "no"
            if current_level_no == 4:
                if yes == "yes":
                    player.rect.y = 220
                    player.rect.x = 516
                    skeleton.rect.y = 171
                    skeleton.rect.x = 158
                    yes = "no"
            if current_level_no ==5:
                if yes == "yes":
                    player.rect.y = 133
                    player.rect.x = 872
                    skeleton.rect.y = 389
                    skeleton.rect.x = 226
                    yes = "no"
        #print(lives)
        #Update items in the level
    current_level.update()
    heart_list.draw(screen)
    # If the player gets near the right side, shift the world left (-x)
    if skeleton.rect.right > SCREEN_WIDTH:
        skeleton.rect.right = SCREEN_WIDTH
    time = font.render("Time: ", True, BLACK)
    level = font.render("Level " + str(current_level_no + 1), True, BLACK)
    screen.blit(time, [60, 95])
    screen.blit(level, [800, 60])
    time_taken = pygame.time.get_ticks() - startyt
    time_taken/=1000
    time_taken = round(time_taken, 2)
    high = font2.render("You got a new High Score!!", True, RED)
    # If the player gets near the left side, shift the world right (+x)
    if skeleton.rect.left < 0:
        skeleton.rect.left = 0
        
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH

    # If the player gets near the left side, shift the world right (+x)
    if player.rect.left < 0:
        player.rect.left = 0

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    active_sprite_list.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    if lives == 2:
        heart2.kill()
    if lives == 1:
        heart1.kill()
    if lives == 0:
        heart.kill()
        var = True
        main()
   # print(startyt)
    timetext = font.render(str(time_taken), True, BLACK)
    screen.blit(timetext, [150, 95])
    if current_level_no ==7:
        screen.blit(win, [0, 0])
        if once == "one":
            once = "zero"
            timeone = time_taken
            finaltime = font2.render(str(timeone), True, RED)
            with open("Time.txt", "a+") as doc:
                doc.seek(0)
                times = doc.readlines()
                for i in times:
                    i = float(i)
                    prevhigh2 = i
                    if time_taken < i:
                        yesblit = "yes"
                        doc.truncate(0)
                        doc.write(str(time_taken))
                        doc.close()
                        prevhigh2 = time_taken
        lastbest = font2.render(str(prevhigh2), True, RED)
        screen.blit (lastbest, [550, 296])
        screen.blit(finaltime, [550, 202])
        if yesblit == "yes":
            yesblit == "no"
            #screen.blit(high, [183, 415])
def main2():
    global var2
    global bg
    global soldier
    global screen_rect
    global all_sprites
    global bomb
    global bomb_list
    global bullet_list
    global fontwar
    global fontwar2
    global score
    global prevhigh
    global lives
    global yesblit 
    global bulletsound
    global heart2
    global argh
    global lives2
    global heart1
    global life1
    global heart
    global lost
    global writeonce 
    if var2:
        bomb = Bomb()
        soldier = Soldier()
        heart = Liveswar()
        heart1 = Liveswar()
        heart2 = Liveswar()

        heart.rect.x = 60
        heart1.rect.x = 90
        heart2.rect.x = 120

        all_sprites = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        bomb_list = pygame.sprite.Group()
        heart_list = pygame.sprite.Group()

        all_sprites.add(soldier)
        bomb_list.add(bomb)
        all_sprites.add(bomb)

        all_sprites.add(heart)
        heart_list.add(heart)

        all_sprites.add(heart1)
        heart_list.add(heart1)

        all_sprites.add(heart2)
        heart_list.add(heart2)

        screen_rect = screen.get_rect()
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        play = pygame.image.load("Play.png")
        icon = pygame.image.load("Icon.png")
        pygame.display.set_icon(icon)
        bg = pygame.image.load("abc.png")
        screen.blit(bg, [0, 0])
        lives = 3
        score = 0
        fontwar = pygame.font.Font("MISTRAL.ttf", 30)
        fontwar2 = pygame.font.Font("MISTRAL.ttf", 100)
        heart = Liveswar()
        lives2 = pygame.mixer.Sound("2 lives.mp3")
        life1 = pygame.mixer.Sound("1 life.mp3")
        lost = pygame.mixer.Sound('lost.mp3')
        click = pygame.mixer.Sound("click.wav")
        speak = ""
        yesblit = ""
        writeonce = "one"
        prevhigh = 0
        start = True
        #playbg = pygame.image.load("Start.png")
        #playbg = pygame.transform.scale(playbg, [1000, 500])
        bulletsound = pygame.mixer.Sound("rumble.flac")
        argh = pygame.mixer.Sound("1.mp3")
        pygame.mixer.music.load("War Song.mp3")
        pygame.mixer.music.play()
        var2 = False
    
    soldier.rect.clamp_ip(screen_rect)
    screen.blit(bg, [0, 0])
    all_sprites.draw(screen)
    soldier.move()
    soldier.walk()

    if bomb.rect.y > 100:
        show_bomb()
    for bullet in bullet_list:
        if bullet.direction == "R":
            bullet.moveright()
        else:
            bullet.moveleft()
    for bomb in bomb_list:
        bomb.move()
    if pygame.sprite.groupcollide(bomb_list, bullet_list, True, True):
        score += 1
        bulletsound.play()
    score_print = fontwar.render("Score: " + str(score), True, BLACK)
    lives_print = fontwar.render("Lives: ", True, BLACK)
    game_over = fontwar2.render("Game Over!", True, BLACK)
    final_score = fontwar2.render("Your score was " + str(score) + ".", True, BLACK)
    high_score = fontwar2.render("You got a high score!!", True, BLACK)
    last_high = fontwar2.render("Your last high score was " + str(prevhigh) + ".", True, BLACK)
    screen.blit(score_print, [10, 10])
    screen.blit(lives_print, [10, 40])
    soldier_hit_list = pygame.sprite.spritecollide(soldier, bomb_list, True)

    if len(bomb_list) == 0:
        show_bomb()

    for bomb in soldier_hit_list:
        bomb.kill()
        lives -= 1
        if lives == 2:
            heart2.kill()
            argh.play()
            lives2.play()
        if lives == 1:
            heart1.kill()
            argh.play()
            life1.play()
        if lives == 0:
            heart.kill()
            argh.play()
            lost.play()
            finalscore = str(score)
    if lives == 0:
        screen.blit(bg, [0, 0])
        screen.blit(game_over, [275, 100])
        screen.blit(final_score, [200, 200])
        if writeonce == "one":
            writeonce = "no"
            with open("Scores.txt", "a+") as doc:
                doc.seek(0)
                scores = doc.readlines()
                for i in scores:
                    i = int(i)
                    prevhigh = i
                    if score > i:
                        yesblit = "yes"
                        doc.truncate(0)
                        doc.write(finalscore)
                        doc.close()
                    else:
                        yesblit = "no"
        for bomb in soldier_hit_list:
            bomb.kill()
        soldier.kill()
        for bomb in bomb_list:
            bomb.kill()
        for bullet in bullet_list:
            bullet.kill()
    if yesblit == "yes":
        screen.blit(high_score, [150, 315])
    elif yesblit == "no":
        screen.blit(last_high, [30, 315])

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if one.collidepoint(event.pos):
                startyt = pygame.time.get_ticks()
                game_num = 0
                decided = True
            elif two.collidepoint(event.pos):
                game_num = 1
                decided = True
                #screen.blit(playbg, [0, 0])
                #screen.blit(play, [403, 225])
            elif three.collidepoint(event.pos):
                game_num = 2
                decided = True
        if event.type == pygame.KEYDOWN:
            if game_num == 1:
                if event.key == pygame.K_LEFT:
                    soldier.go_left()
                if event.key == pygame.K_RIGHT:
                    soldier.go_right()
                if event.key == pygame.K_SPACE:
                    bullet = Bullet()
                    if soldier.direction == "R":
                        bullet.direction = "R"
                        bullet.rect.x = soldier.rect.left - 23
                        bullet.rect.y = soldier.rect.top - 23
                    else:
                        bullet.image = pygame.transform.flip(bullet.image, True, False)
                        bullet.rect.x = soldier.rect.left + 110
                        bullet.rect.y = soldier.rect.top - 24
                        bullet.direction = "L"
                    all_sprites.add(bullet)
                    bullet_list.add(bullet)
        if event.type == pygame.KEYUP:
            if game_num == 1:
                if event.key == pygame.K_LEFT and soldier.change_x < 0:
                    soldier.stop()
                if event.key == pygame.K_RIGHT and soldier.change_x > 0:
                    soldier.stop()
    
    if not decided:
        screen.blit(mainscr, [0, 0, ])
        

       
    if game_num == 0:
        
        main()
    #elif game_num == 1:
    #    main2()
      #  hell = font2.render("hi main screen", True, BLACK)
       # screen.blit(hell, [400, 100])

     #   button1 = pygame.draw.rect(screen, GREEN, [200, 400, 100, 75])
      ##  button2 = pygame.draw.rect(screen, GREEN, [500, 400, 100, 75])
        #button3 = pygame.draw.rect(screen, GREEN, [800, 400, 100, 75])
   # if decided:screen.fill(CYAN)
    #if game_num == 0:
        
        #main()
    if game_num == 1:
        main2()
        
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()