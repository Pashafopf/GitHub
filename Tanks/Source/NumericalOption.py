import pygame

#####################
class NumericalOption():
    #Цифровые значения,которые будут меняться в окне опций
    #инициализация
    def __init__(self,value,x,y):
        #как спрайт
        #само значение
        self.value = value
        self.lastvalue = -999  # невозможное значение для любой опции
    #смена значения
    def set(self,value):
        self.value = value
    
    #апдэйт
    def update(self):
        #если значение не совпадает с предыдущим
        if self.value != self.lastvalue:
            #заменяем последнее значение на новое
            self.lastvalue = self.value

