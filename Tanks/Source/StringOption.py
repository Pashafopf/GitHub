import pygame

#####################################################################
class StringOption():
    """Текстовые значение,которые меняют в окне опций"""
    def __init__(self,value,x,y):
        #это спрайт!

        self.value = value
        #и последнее значение
        self.lastvalue = ""
        #сразу его и заапдэйтим,для порядку,
        self.update()

    #кстанавливаем значение
    def set(self,value):
        self.value = value
    
    #апдэйтим это значение
    def update(self):
        #если не равно последнему введённому
        if self.value != self.lastvalue:
            #устанавливаем его,в переменную lastvalue записываем его
            self.lastvalue = self.value

