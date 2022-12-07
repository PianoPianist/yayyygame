import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (234, 13, 17)
GREY = (129, 129, 129)


class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height, colour):
        image = pygame.Surface([width, height]).convert()
        image.set_colorkey(colour)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return image


class Bomb(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("Untitled.png")
        self.image = sprite_sheet.get_image(2, 2, 48, 48, WHITE)
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

        sprite_sheet = SpriteSheet("touse.png")
        self.image = sprite_sheet.get_image(0, 0, 150, 205, BLACK)
        self.walking_frames_l.append(self.image)

        self.image = sprite_sheet.get_image(233, 0, 140, 210, BLACK)
        self.walking_frames_l.append(self.image)
        self.image = sprite_sheet.get_image(425, 5, 123, 210, BLACK)
        self.walking_frames_l.append(self.image)

        self.image = sprite_sheet.get_image(0, 0, 150, 205, BLACK)
        self.image = pygame.transform.flip(self.image, True, False)
        self.walking_frames_r.append(self.image)
        self.image = sprite_sheet.get_image(233, 0, 140, 210, BLACK)
        self.image = pygame.transform.flip(self.image, True, False)
        self.walking_frames_r.append(self.image)
        self.image = sprite_sheet.get_image(425, 5, 123, 210, BLACK)
        self.image = pygame.transform.flip(self.image, True, False)
        self.walking_frames_r.append(self.image)

        self.image = self.walking_frames_r[0]

        self.rect = self.image.get_rect()
        self.rect.y = 297
        self.rect.x = 100
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
        self.image = sprite_sheet.get_image(0, 0, 27, 27, BLACK)
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


class Lives(pygame.sprite.Sprite):
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


'''def main():
    global bomb
    global score
    global prevhigh
    global lives
    global yesblit
    global writeonce

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
    score_print = font.render("Score: " + str(score), True, BLACK)
    lives_print = font.render("Lives: ", True, BLACK)
    game_over = font2.render("Game Over!", True, BLACK)
    final_score = font2.render("Your score was " + str(score) + ".", True, BLACK)
    high_score = font2.render("You got a high score!!", True, BLACK)
    last_high = font2.render("Your last high score was " + str(prevhigh) + ".", True, BLACK)
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
        screen.blit(last_high, [25, 315])'''


pygame.init()
pygame.mixer.init()
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Warrior")
clock = pygame.time.Clock()
done = False

bomb = Bomb()
soldier = Soldier()
heart = Lives()
heart1 = Lives()
heart2 = Lives()

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
font = pygame.font.Font("MISTRAL.ttf", 30)
font2 = pygame.font.Font("MISTRAL.ttf", 100)
heart = Lives()
lives2 = pygame.mixer.Sound("2 lives.mp3")
life1 = pygame.mixer.Sound("1 life.mp3")
lost = pygame.mixer.Sound('lost.mp3')
click = pygame.mixer.Sound("click.wav")
speak = ""
yesblit = ""
writeonce = "one"
prevhigh = 0
start = False
playbg = pygame.image.load("Start.png")
playbg = pygame.transform.scale(playbg, [1000, 500])
bulletsound = pygame.mixer.Sound("rumble.flac")
argh = pygame.mixer.Sound("1.mp3")
pygame.mixer.music.load("War Song.mp3")
pygame.mixer.music.play()
screen.blit(playbg, [0, 0])
screen.blit(play, [403, 225])
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click.play()
            pos = event.pos
            if pos[0] >= 403 and pos[0] <= 596:
                if pos[1] >= 250 and pos[1] <= 340:
                    start = True
        if event.type == pygame.KEYDOWN:
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
            if event.key == pygame.K_LEFT and soldier.change_x < 0:
                soldier.stop()
            if event.key == pygame.K_RIGHT and soldier.change_x > 0:
                soldier.stop()
    
    if start == True:
        screen.blit(bg, [0, 0])
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
        score_print = font.render("Score: " + str(score), True, BLACK)
        lives_print = font.render("Lives: ", True, BLACK)
        game_over = font2.render("Game Over!", True, BLACK)
        final_score = font2.render("Your score was " + str(score) + ".", True, BLACK)
        high_score = font2.render("You got a high score!!", True, BLACK)
        last_high = font2.render("Your last high score was " + str(prevhigh) + ".", True, BLACK)
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

    clock.tick(60)
    pygame.display.flip()
pygame.quit()
