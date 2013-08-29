import pygame
from Source import GameData

#####################
class MenuScreen(pygame.sprite.Sprite):

    images = []
    count = 0
    #Заставка с которой игрок может начать новую игру
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        newpos = self.rect.move((110, 93))
        self.rect = newpos

    def update(self):
        self.image = MenuScreen.images[self.count]
