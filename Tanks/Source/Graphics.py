
import pygame
import os.path
from pygame.locals import *
from Source import Tank, RespawnPoint,GameData, MenuScreen
from Source.MenuScreen import *
# Вспомогательные функции прорисовки
#проверяем не загружено ли что-то, кроместандартного BMP
if not pygame.image.get_extended():
    raise SystemExit( "Sorry, extended image module required")

def down(counter):
    if counter != 4:
        counter = counter + 1
    else:
        counter = 0
    return counter

def up(counter):
    if counter != 0:
        counter = counter - 1
    else:
        counter = 4
    return counter

def _up(counter):

    if (counter > -1 and counter < 7):
        counter = GameData._gamepad
    elif (counter > 6 and counter < 11):
        counter = GameData._maze
    elif (counter > 10 and counter < 16):
        counter = GameData._difficulty
    elif (counter > 15 and counter < 21):
        counter = GameData._gear_delay
    elif (counter > 20 and counter < 26):
        counter = GameData._ammo_load_time
    elif (counter > 25 and counter < 31):
        counter = GameData._max_temperature
    elif (counter > 30 and counter < 37):
        counter = GameData._bullet_speed
    elif (counter > 36 and counter < 38):
        counter = GameData._volume
    elif (counter > 37 and counter < 40):
        counter = GameData._credits

    return counter

def _down(counter):

    if (counter > -1 and counter < 7):
        counter = GameData._difficulty
    elif (counter > 6 and counter < 11):
        counter = GameData._gear_delay
    elif (counter > 10 and counter < 16):
        counter = GameData._ammo_load_time
    elif (counter > 15 and counter < 21):
        counter = GameData._max_temperature
    elif (counter > 20 and counter < 26):
        counter = GameData._bullet_speed
    elif (counter > 25 and counter < 31):
        counter = GameData._volume
    elif (counter > 30 and counter < 37):
        counter = GameData._credits
    elif (counter > 36 and counter < 38):
        counter = GameData._gamepad
    elif (counter > 37 and counter < 40):
        counter = GameData._maze

    return counter

def _left(counter):

    if (counter > 0 and counter < 7):
        counter = counter - 1
    elif counter == 0:
        counter = 0
    elif (counter > 7 and counter < 11):
        counter = counter - 1
    elif counter == 7:
        counter = 7
    elif (counter > 11 and counter < 16):
        counter = counter - 1
    elif counter == 11:
        counter = 11
    elif (counter > 16 and counter < 21):
        counter = counter - 1
    elif counter == 16:
        counter = 16
    elif (counter > 21 and counter < 26):
        counter = counter - 1
    elif counter == 21:
        counter = 21
    elif (counter > 26 and counter < 31):
        counter = counter - 1
    elif counter == 26:
        counter = 26
    elif (counter > 31 and counter < 37):
        counter = counter - 1
    elif counter == 31:
        counter = 31
    elif counter == 37:
        counter = 37
    elif (counter > 38 and counter < 40):
        counter = counter - 1
    elif counter == 38:
        counter = 38
    return counter

def _right(counter):

    if (counter > -1 and counter < 6):
        counter = counter + 1
    elif counter == 6:
        counter = 6
    elif (counter > 6 and counter < 10):
        counter = counter + 1
    elif counter == 10:
        counter = 10
    elif (counter > 10 and counter < 15):
        counter = counter + 1
    elif counter == 15:
        counter = 15
    elif (counter > 15 and counter < 20):
        counter = counter + 1
    elif counter == 20:
        counter = 20
    elif (counter > 20 and counter < 25):
        counter = counter + 1
    elif counter == 25:
        counter = 25
    elif (counter > 25 and counter < 30):
        counter = counter + 1
    elif counter == 30:
        counter = 30
    elif (counter > 30 and counter < 36):
        counter = counter + 1
    elif counter == 36:
        counter = 36
    elif counter == 37:
        counter = 37
    elif (counter > 37 and counter < 39):
        counter = counter + 1
    elif counter == 39:
        counter = 39

    return counter

# загрузка имиджа
def load_image(file, colorkey=-1):
    #загрузка из директории Sprites
    file = os.path.join('Sprites', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        #отлавливаем ошибки
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    surface = surface.convert()
    #проверка прозрачности картинки
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surface.get_at((0,0))
        surface.set_colorkey(colorkey, RLEACCEL)
    return surface
#Загрузка плеяды изображений
def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs
#загрузка бэкграунда(аналогично)
def load_background(file, colorkey=-1):
    file = os.path.join('Backgrounds', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit( 'Could not load image "%s" %s'%(file, pygame.get_error()))
    surface = surface.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surface.get_at((0,0))
        surface.set_colorkey(colorkey, RLEACCEL)
    return surface
#Загрузка плеяды бэкграундов
def load_backgrounds(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs
#Рисование бэкграунда
def draw_background(background, bgdtile, screen, blacksquare = False):
    for x in range(0, GameData.screenrect.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    if GameData.battleground[GameData.battlegroundnr].draw_water:
        for pool in GameData.battleground[GameData.battlegroundnr].water:
            pygame.draw.rect(background, (33,33,200), pool, 0)        
    if GameData.battleground[GameData.battlegroundnr].draw_walls:
        for wall in GameData.battleground[GameData.battlegroundnr].walls:
            pygame.draw.rect(background, (33,33,33), wall, 0)
    if blacksquare:
        pygame.draw.rect(background, (0,0,0), (1,1,1,1), 0)
    screen.blit(background, (0,0))
    pygame.display.flip()
#установка видимости
def determine_visibility(respawn_points, tanks, tanklist, active_screen, move_tanks_to_respawn_point = False):
    for respawn_point in respawn_points:
        respawn_point.kill()
    count = 0
    for respawn_point in GameData.battleground[GameData.battlegroundnr].respawnpoints:
        RespawnPoint(respawn_point[0],respawn_point[1],respawn_point[2])
        if move_tanks_to_respawn_point:
            tanklist[count].move_to_respawn_point(count)
        tanklist[count].visible = True
        count += 1
        for respawn_point in pygame.sprite.spritecollide(active_screen, respawn_points, 0):
            respawn_point.visible = False
        for tank in pygame.sprite.spritecollide(active_screen, tanks, 0):
            tank.visible = False 

