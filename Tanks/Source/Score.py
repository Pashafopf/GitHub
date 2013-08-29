import pygame
from Source import GameData
from pygame.locals import *

################
class Score(pygame.sprite.Sprite):
    #очки
    def __init__(self,text,color,x,y):
        """текстовое поле, отображающее количество смерте/убийств"""
        #это спрайт!
        pygame.sprite.Sprite.__init__(self, self.containers)
        #его шрифт и нач. параметры
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.font.set_italic(1)
        self.color = Color(color)
        self.score = 0
        self.lastscore = -1
        self.text = text
        #сразу апдэйтим
        self.update()
        #и помещаем в неизменные координаты
        self.rect = self.image.get_rect().move(x, y)
    #записываем очки
    def set_score(self,score):
        self.score = score
    
    #апдэйтим каждый килл
    def update(self):
        #если убил,то записывай новое значение
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = self.text % self.score
            self.image = self.font.render(msg, 0, self.color)
