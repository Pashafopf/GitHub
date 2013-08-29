import pygame

#####################
class CreditScreen(pygame.sprite.Sprite):
    #Заставка с которой игрок может начать новую игру
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        newpos = self.rect.move((60, 100))
        self.rect = newpos

