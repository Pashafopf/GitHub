# DefaultBot: driving around randomly and shooting without aiming.
# When a wall is hit, DefaultBot turn to a random direction while trying to spray bullets.
# DefaultBot tries to turn towards the middle of the arena when hitting the outer borders.

import random
from Source import GameData

def DefaultBot(tank):
    #Очень простой AI
    #рандомим первое действие
    action=random.random()*100
    #если меньше 20, то делай так
    if action < 20:
        #вверх-вверх
        tank.command_queue.append("up")
        tank.command_queue.append("up")
    #больше 20, но меньше 30
    if action > 20 and action < 30:
        #двигай влево
        tank.command_queue.append("left")
    #больше 30, но меньше 40
    if action > 30 and action < 40:
        #двигай вправо
        tank.command_queue.append("right")
    #равно 40
    if action == 40:
        #5 раз делай так
        for t in range(0,6):
            #влево-выстрел
            tank.command_queue.append("left")
            tank.command_queue.append("shoot")
    #равно 50
    if action == 50:
        #5 раз делай тАк
        for t in range(0,6):
            #вправо-выстрел
            tank.command_queue.append("right")
            tank.command_queue.append("shoot")
    #равно 45
    if action == 45:
        #делай так:влево-выстрел-вправо-вправо-выстрел-влево-выстрел
        tank.command_queue.append("left")
        tank.command_queue.append("shoot")
        tank.command_queue.append("right")
        tank.command_queue.append("right")
        tank.command_queue.append("shoot")
        tank.command_queue.append("left")
        tank.command_queue.append("shoot")
    # возрастание triggerhappiness делает игру более сложной
    if action > 100 - GameData.triggerhappiness:
        tank.command_queue.append("shoot")
    # Avoid walls in a random direction
    for wall in GameData.battleground[GameData.battlegroundnr].walls:
        if wall.colliderect(tank.rect):
            if random.random() < 0.5:
                for i in range(0,int(random.random() * 450 / GameData.angle)):
                    tank.command_queue.append("left")
                    tank.command_queue.append("shoot")
                tank.command_queue.append("flush")
            else:
                for i in range(0,int(random.random() * 450 / GameData.angle)):
                    tank.command_queue.append("right")
                    tank.command_queue.append("shoot")
                tank.command_queue.append("flush")
    # Avoid water in a random direction
    for pool in GameData.battleground[GameData.battlegroundnr].water:
        if pool.colliderect(tank.rect):
            if random.random() < 0.5:
                for i in range(0,int(random.random() * 450 / GameData.angle)):
                    tank.command_queue.append("shoot")
                    tank.command_queue.append("left")                    
                tank.command_queue.append("flush")
            else:
                for i in range(0,int(random.random() * 450 / GameData.angle)):
                    tank.command_queue.append("shoot")
                    tank.command_queue.append("right")
                tank.command_queue.append("flush")
    # Avoid borders and turn towards the centre of the arena
    if (tank.y < 60) and (tank.angle < 180):
        if tank.x < 400:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("right")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
        else:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("left")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
    elif tank.y > 668 and (tank.angle > 180):
        if tank.x < 400:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("left")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
        else:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("right")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
    elif tank.x > 705 and ((tank.angle < 90) or (tank.angle > 270)):
        if tank.y < 400:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("right")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
        else:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("left")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
    elif tank.x < 60 and (90 < tank.angle < 270):
        if tank.y < 400:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("left")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
        else:
            for i in range(0,int(120/GameData.angle)):
                tank.command_queue.append("right")
            tank.command_queue.append("shoot")
            for i in range(0,int(10)):
                tank.command_queue.append("pass")
            tank.command_queue.append("flush")
