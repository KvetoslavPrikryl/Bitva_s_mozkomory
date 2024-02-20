import pygame
import random

# Inicializace
pygame.init()

# Obrazovka
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bitva s mozkomory")

# Nastavení hry
fps = 60
clock = pygame.time.Clock()

# Classy
class Game:
    def __init__(self, one_playr, group_of_mozkomors):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.slow_down_cycle = 0

        self.one_playr = one_playr
        self.group_of_mozkomors = group_of_mozkomors

        # # Hudba v pozadí
        pygame.mixer.music.load("media/bg-music-hp.wav")
        pygame.mixer.music.play(-1, 0.0)

        # Fonty
        self.potter_font = pygame.font.Font("fonts\Harry.ttf", 24)
        self.potter_font_big = pygame.font.Font("fonts\Harry.ttf", 64)
        self.potter_font_header = pygame.font.Font("fonts\Harry.ttf", 90)

        # Obrázek v pozadí
        self.background_image = pygame.image.load("img/bg-dementors.png")
        self.background_image_rect = self.background_image.get_rect()
        self.background_image_rect.topleft = (0,0)

        # Obrázky
        blue_image = pygame.image.load("img\mozkomor-modry.png")
        green_image = pygame.image.load("img\mozkomor-zeleny.png")
        purple_image = pygame.image.load("img\mozkomor-ruzovy.png")
        yellow_image = pygame.image.load("img\mozkomor-zluty.png")
        self.mozkomors_images = [blue_image, green_image, purple_image, yellow_image]

        # Generujeme mozkomora, kterého chceme chytit
        self.mozkomor_catch_type = random.randint(0, 3)
        self.mozkomor_catch_image = self.mozkomors_images[self.mozkomor_catch_type]
        self.mozkomor_catch_image_rec = self.mozkomor_catch_image.get_rect()
        self.mozkomor_catch_image_rec.centerx = width // 2
        self.mozkomor_catch_image_rec.top = 25


    # Kód, který je volá stále dokola
    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:
            self.round_time += 1
            self.slow_down_cycle = 0

        # Kontrola kolize
        self.check_collistion()

    # Vykreslování ve hře
    def draw(self):
        dark_yellow = pygame.Color("#938f0c")
        blue = (21, 31, 217)
        green = (24, 194, 38)
        purple = (195, 23, 189)
        yollow = (195, 181, 23)
        colors = [blue, green, purple, yollow]

        # Nastavení textu
        catch_text = self.potter_font.render("Chyt tohoto mozkomora", True, dark_yellow)
        catch_text_reg = catch_text.get_rect()
        catch_text_reg.centerx = width // 2
        catch_text_reg.top = 5

        score_text = self.potter_font.render(f"Skore: {self.score}", True, dark_yellow)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 4)

        lives_text = self.potter_font.render(f"Zivoty: {self.one_playr.lives}", True, dark_yellow)
        lives_text_rec = lives_text.get_rect()
        lives_text_rec.topleft = (10, 30)

        round_text = self.potter_font.render(f"Kolo: {self.round_number}", True, dark_yellow)
        round_text_rec = round_text.get_rect()
        round_text_rec.topleft = (10, 60)

        time_text = self.potter_font.render(f"Cas kola: {self.round_time}",True, dark_yellow)
        time_text_rec = time_text.get_rect()
        time_text_rec.topright = (width - 10, 5)

        back_save_zone_text = self.potter_font.render(f"Bezpecna zona: {self.one_playr.save_zone}", True, dark_yellow)
        back_save_zone_text_rec = back_save_zone_text.get_rect()
        back_save_zone_text_rec.topright = (width - 10, 35)

        # Vykreslení do obrazovky
        screen.blit(catch_text, catch_text_reg)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rec)
        screen.blit(round_text, round_text_rec)
        screen.blit(time_text, time_text_rec)
        screen.blit(back_save_zone_text, back_save_zone_text_rec)
        # Obrázek mozkomora, kterého máme chytit
        screen.blit(self.mozkomor_catch_image, self.mozkomor_catch_image_rec)

        # Rámeček pro mozkomory
        pygame.draw.rect(screen, colors[self.mozkomor_catch_type], (0, 100, width, height - 200), 4)


    # Kontroluje kolizi mozkomora s Herrym
    def check_collistion(self):
        # S jakým mozkomorem jsme se srazili?
        collided_mozkomor = pygame.sprite.spritecollideany(self.one_playr, self.group_of_mozkomors)

        if collided_mozkomor:
            # srazili jsme se se správným mozkomorem
            if collided_mozkomor.type == self.mozkomor_catch_type:

                self.one_playr.catch_sound.play()
                self.score += 10 * self.round_number

                # Odstranění chyceného mozkomora
                collided_mozkomor.remove(self.group_of_mozkomors)

                #Jsou jěště nějací mozkomorové?
                if self.group_of_mozkomors:
                    self.chose_new_target()
                else: 
                    self.one_playr.reset()
                    self.start_new_round()
            else:
                self.one_playr.wrong_sound.play()
                self.one_playr.lives -= 1
                self.one_playr.reset()
                if self.one_playr.lives <= 0:
                    self.pause_game(f"Dosazene skore: {self.score}", "Stisknete enter, pokud chcete spustit hru.")
                    self.reset_game()


    # Začátek nového kola
    def start_new_round(self):
        self.score += int(100 * (self.round_number / (1 + self.round_time)))
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1
        self.one_playr.save_zone += 1

        for delted_mozkomor in self.group_of_mozkomors:
            self.group_of_mozkomors.remove(delted_mozkomor)

        for i in range(self.round_number):
            self.group_of_mozkomors.add(Mozkomor(random.randint(0, width - 64), random.randint(100, height -164), self.mozkomors_images[0], 0))
            self.group_of_mozkomors.add(Mozkomor(random.randint(0, width - 64), random.randint(100, height -164), self.mozkomors_images[1], 1))
            self.group_of_mozkomors.add(Mozkomor(random.randint(0, width - 64), random.randint(100, height -164), self.mozkomors_images[2], 2))
            self.group_of_mozkomors.add(Mozkomor(random.randint(0, width - 64), random.randint(100, height -164), self.mozkomors_images[3], 3))

        self.chose_new_target()

    # Vybírá nového mozkomora
    def chose_new_target(self):
        new_mozkomor_to_catch = random.choice(self.group_of_mozkomors.sprites())
        self.mozkomor_catch_type = new_mozkomor_to_catch.type
        self.mozkomor_catch_image = new_mozkomor_to_catch.image

    # Pauza před zahájením nové hry, nebo před spuštěním
    def pause_game(self, main_text, subheding_text):

        global lets_continue

        # Nastavení barvy
        dark_yellow = pygame.Color("#938f0c")
        black = (0,0,0)

        # Hlavní text pro pauznutí
        main_text_create = self.potter_font_header.render(main_text, True, dark_yellow)
        main_text_create_rec = main_text_create.get_rect()
        main_text_create_rec.center = (width // 2, height // 2)

        # Podnapis pro pauznutí
        subheding_text_create = self.potter_font_big.render(subheding_text, True, dark_yellow)
        subheding_text_create_rec = subheding_text_create.get_rect()
        subheding_text_create_rec.center = (width // 2 , height // 2 + 80)

        # Zobrazení textů
        screen.fill(black)
        screen.blit(main_text_create, main_text_create_rec)
        screen.blit(subheding_text_create, subheding_text_create_rec)
        pygame.display.update()

        # Zastavení hry
        paused = True
        while paused:
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                if one_event.type == pygame.QUIT:
                    paused = False
                    lets_continue = False

    # Resetuje hru 
    def reset_game(self):
        self.score = 0
        self.round_number = 0
        self.one_playr.lives = 5
        self.one_playr.save_zone = 3
        self.start_new_round()

        pygame.mixer.music.play(-1, 0.0)

class Playr(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/potter-icon.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.bottom = height - 10

        self.lives = 5
        self.save_zone = 3
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound("media\expecto-patronum.mp3")
        self.catch_sound.set_volume(0.1)
        self.wrong_sound = pygame.mixer.Sound("media\wrong.wav")
        self.wrong_sound.set_volume(0.1)

    # Kód, volaný stále dokola
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height - 100:
            self.rect.y += self.speed

    # Zpátky do bezpečné zóny
    def back_to_safe_zone(self):
        if self.save_zone > 0:
            self.save_zone -= 1
            self.rect.bottom = height - 10

    # Vrací hráče na výchozí pozici
    def reset(self):
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10

class Mozkomor(pygame.sprite.Sprite):
    def __init__(self, X, Y, img, mozkomor_type):
        super().__init__()
        # Nahrajeme obrázek mozkomora a umístíme ho
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (X, Y)

        # Typi mozkomorů: 0 = modrý, 1 = zelený, 2 = růžový, 3 = žlutý
        self.type = mozkomor_type

        # Nastavení náhodného směru
        self.x = random.choice([-1 , 1])
        self.y = random.choice([-1 , 1])
        self.speed = random.randint(1, 5)
        

    # Kód, volaný stále dokola
    def update(self):
        # Pohyb mozkomora
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

        # Odraz mozkomora
        if self.rect.left < 0 or self.rect.right > width:
            self.x = -1 * self.x
        if self.rect.top < 100 or self.rect.bottom > height - 100:
            self.y = -1 * self.y

# Skupina mozkomorů
mozkomor_group = pygame.sprite.Group()

# Skupina hráčů
player_group = pygame.sprite.Group()

# Umístění hráče
playr = Playr()
player_group.add(playr)

# Game
my_game = Game(playr, mozkomor_group)
my_game.pause_game("Harry Potter a bitva s mozkomory", "Stisknete enter pro zahajeni hry.")
my_game.start_new_round()

# Hlavní cyklus hry
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playr.back_to_safe_zone()


    # Vyplnění plochy
    screen.fill((0,0,0))
    screen.blit(my_game.background_image, my_game.background_image_rect)

    # Updatujeme grůpu mozkomorů
    mozkomor_group.draw(screen)
    mozkomor_group.update()

    # Updatujeme playera
    player_group.draw(screen)
    player_group.update()

    # Updatujeme objekt vytvořený podle classy Game
    my_game.update()
    my_game.draw()

    # Update obrazovky
    pygame.display.update()

    # Zpomalení cylku
    clock.tick(fps)

# Konec hry
pygame.quit()