
import pygame
from pygame.locals import *
import pickle

##########################
class BattleGround():
    #Поле битвы:ландшафт, стены...
    def __init__(self, name, background, walls_list, water_list, respawn_list, draw_walls = False, draw_water = False):
        self.name=name                      # name as displayed in the options screen
        self.background=background          # бэкграунд
        self.walls = walls_list             # лист объектов Rect()
        self.water=water_list               # лист объектов Rect()
        self.respawnpoints=respawn_list     # лист респаунов
        self.draw_walls = draw_walls        # устанавливается в значение"ложь", если преграды уже отрисованы на бэкграунде
        self.draw_water = draw_water        # устанавливается в значение"ложь", если вода уже отрисована на бэкграунде