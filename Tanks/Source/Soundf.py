import pygame
import os.path
from pygame.mixer import *
from Source import GameData


class dummysound:#(болванка)
    # помощь для отловки ошибок при загрузке музыки из файла
    #заваодим тупую функцию бесконечного плэйинга
    def play(self): pass
#загрузка мьюзикс
def load_sound(file):

    #проверка:можем ли использовать миксер?
    if not pygame.mixer: return dummysound()
    #добавляем в путь название папки,где хранится музыка
    file = os.path.join('Sound', file)
    #отлавливаем ошибку загрузки элемента
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    #если не получилоь, то выводим ошибку пайгейма
    except pygame.error:
        print ('Warning, unable to load,', file)
    return dummysound()
