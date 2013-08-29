#! /usr/bin/env python

################

import math                         # импорт библиотеки матем функций
import os.path                      # импорт библиотеки для работы с файловой системой
import pygame                       # импорт библиотеки для разработки 2D игр
from pygame.locals import *
from pygame.mixer import *

from Source import BattleGround     # импорт класса,где прописаны картинки воды, ландшафтов, респауны
from Source import GameData         # содержит все глобальные переменные
from Source.Tank  import *            # класс танчика
from Source import TankCopy         # иконка танка на панели очке
from Source import Score            # класс панели очков
from Source import Bullet           # класс пули
from Source import Explosion        # класс взрыва танчика
from Source.Thermometer  import *     # класс, описывающий количество пуль на экране от одного танчика в секунду
from Source.RespawnPoint import *      # класс точки восстановления
from Source import Graphics         # вспомогательные графические функции
from Source import Soundf           # вспомогательные звуковые функции
from Source import GameOver         # класс экрана гейм овер
from Source.Logo import *             # класс логотипа игры
from Source.SplashScreen  import *    # класс экрана заставки
from Source.MenuScreen import *       # класс экрана меню
from Source.CreditScreen import *       # класс экрана благодарностей
from Source.Gear import *            # класс скорости танчиков
from Source import StringOption     # класс строки опции
from Source import NumericalOption  # класс номера опций
from Source import Options          # класс экрана опций
from Source.Options import *
from Source import DefaultBot       # класс ИИ
###################

def main(): # главная функция
    # Инициализируем библиотеку pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():#условие запустится ли звук
        print ('Внимание, игра будет без звука')
        pygame.mixer = None
    clock = pygame.time.Clock()


    print ("------------------------------------------------")
    print ("---                  Tanks                   ---")
    print ("------------------------------------------------")
    print("---       Programming by Pavel Shvydkin       ---")
    print ("---         Graphics by Pavel Shvydkin       ---")
    print ("---   Explosion graphics by Grigory Penziakov---")
    print ("---    Music by Fedor Shaliapin              ---")
    print ("------------------------------------------------")
    print ("---         http://vk/id121006376            ---")
    print ("------------------------------------------------")
    print (" 1: play in full screen.")
    print (" 2: play in a window.")
    screenmode = input('(1-2)')#заводим переменную,чтобы отловить ввод пользователя
    if screenmode == '1': #если он ввёл 1, то запускаем полноэкранный режим, в глобальную переменную screenrect.size
        #заносим FULLSCREEN, и устанавливаем глубину реального цвета
        bestdepth = pygame.display.mode_ok(GameData.screenrect.size, pygame.FULLSCREEN, 32)
        screen = pygame.display.set_mode(GameData.screenrect.size, pygame.FULLSCREEN, bestdepth)
    else:  #если 2,то открываем в минимальном окне
        screen = pygame.display.set_mode(GameData.screenrect.size)

    #Загружаются изображения,принадлежащие спрайтам(танчикам), всё заносится в список класса Tank
    Tank.images = Graphics.load_images('Red_tank_0.bmp','Red_tank_1.bmp','Red_tank_2.bmp','Red_tank_3.bmp','Red_tank_4.bmp','Red_tank_5.bmp',
        'Blue_tank_0.bmp','Blue_tank_1.bmp','Blue_tank_2.bmp','Blue_tank_3.bmp','Blue_tank_4.bmp','Blue_tank_5.bmp',
        'Green_tank_0.bmp','Green_tank_1.bmp','Green_tank_2.bmp','Green_tank_3.bmp','Green_tank_4.bmp','Green_tank_5.bmp',
        'Yellow_tank_0.bmp','Yellow_tank_1.bmp','Yellow_tank_2.bmp','Yellow_tank_3.bmp','Yellow_tank_4.bmp','Yellow_tank_5.bmp',
        'Grey_tank_0.bmp','Grey_tank_1.bmp','Grey_tank_2.bmp','Grey_tank_3.bmp','Grey_tank_4.bmp','Grey_tank_5.bmp',
        'Purple_tank_0.bmp','Purple_tank_1.bmp','Purple_tank_2.bmp','Purple_tank_3.bmp','Purple_tank_4.bmp','Purple_tank_5.bmp')
    TankCopy.images = Tank.images#изображению копий присваиваем сами танчики
    #заносим в список класса пулек танчиков,их изображения
    Bullet.images = Graphics.load_images('Red_bullet.bmp','Blue_bullet.bmp','Green_bullet.bmp','Yellow_bullet.bmp',
                                         'Grey_bullet.bmp','Purple_bullet.bmp')
    #записываем в список класса взрывов, их изображения
    Explosion.images0 = Graphics.load_images('boom-1-0001.png', 'boom-1-0002.png', 'boom-1-0003.png', 'boom-1-0004.png', 'boom-1-0005.png',
                                             'boom-1-0006.png', 'boom-1-0007.png', 'boom-1-0008.png', 'boom-1-0009.png', 'boom-1-0010.png',
                                             'boom-1-0011.png', 'boom-1-0012.png', 'boom-1-0013.png', 'boom-1-0014.png', 'boom-1-0015.png',
                                             'boom-1-0016.png', 'boom-1-0017.png', 'boom-1-0018.png', 'boom-1-0019.png', 'boom-1-0020.png',
                                             'boom-1-0027.png', 'boom-1-0030.png', 'boom-1-0033.png', 'boom-1-0036.png', 'boom-1-0039.png',
                                             'boom-1-0042.png', 'boom-1-0045.png', 'boom-1-0048.png', 'boom-1-0051.png', 'boom-1-0054.png',
                                             'boom-1-0057.png', 'boom-1-0060.png', 'boom-1-0063.png', 'boom-1-0066.png', 'boom-1-0069.png',
                                             'boom-1-0072.png', 'boom-1-0075.png', 'boom-1-0078.png', 'boom-1-0081.png', 'boom-1-0084.png',
                                             'boom-1-0087.png', 'boom-1-0090.png', 'boom-1-0093.png', 'boom-1-0096.png', 'boom-1-0099.png')
    Explosion.images1 = Graphics.load_images('boom-3-0001.png', 'boom-3-0002.png', 'boom-3-0003.png', 'boom-3-0004.png', 'boom-3-0005.png',
                                             'boom-3-0006.png', 'boom-3-0007.png', 'boom-3-0008.png', 'boom-3-0009.png', 'boom-3-0010.png',
                                             'boom-3-0011.png', 'boom-3-0012.png', 'boom-3-0013.png', 'boom-3-0014.png', 'boom-3-0015.png',
                                             'boom-3-0016.png', 'boom-3-0017.png', 'boom-3-0018.png', 'boom-3-0019.png', 'boom-3-0020.png',
                                             'boom-3-0027.png', 'boom-3-0030.png', 'boom-3-0033.png', 'boom-3-0036.png', 'boom-3-0039.png',
                                             'boom-3-0042.png', 'boom-3-0045.png', 'boom-3-0048.png', 'boom-3-0051.png', 'boom-3-0054.png',
                                             'boom-3-0057.png', 'boom-3-0060.png', 'boom-3-0063.png', 'boom-3-0066.png', 'boom-3-0069.png',
                                             'boom-3-0072.png', 'boom-3-0075.png', 'boom-3-0078.png', 'boom-3-0081.png', 'boom-3-0084.png',
                                             'boom-3-0087.png', 'boom-3-0090.png', 'boom-3-0093.png', 'boom-3-0096.png', 'boom-3-0099.png')
    Explosion.images2 = Graphics.load_images('boom-5-0001.png', 'boom-5-0002.png', 'boom-5-0003.png', 'boom-5-0004.png', 'boom-5-0005.png',
                                             'boom-5-0006.png', 'boom-5-0007.png', 'boom-5-0008.png', 'boom-5-0009.png', 'boom-5-0010.png',
                                             'boom-5-0011.png', 'boom-5-0012.png', 'boom-5-0013.png', 'boom-5-0014.png', 'boom-5-0015.png',
                                             'boom-5-0016.png', 'boom-5-0017.png', 'boom-5-0018.png', 'boom-5-0019.png', 'boom-5-0020.png',
                                             'boom-5-0027.png', 'boom-5-0030.png', 'boom-5-0033.png', 'boom-5-0036.png', 'boom-5-0039.png',
                                             'boom-5-0042.png', 'boom-5-0045.png', 'boom-5-0048.png', 'boom-5-0051.png', 'boom-5-0054.png',
                                             'boom-5-0057.png', 'boom-5-0060.png', 'boom-5-0063.png', 'boom-5-0066.png', 'boom-5-0069.png',
                                             'boom-5-0072.png', 'boom-5-0075.png', 'boom-5-0078.png', 'boom-5-0081.png', 'boom-5-0084.png',
                                             'boom-5-0087.png', 'boom-5-0090.png', 'boom-5-0093.png', 'boom-5-0096.png', 'boom-5-0099.png')
    #узнать про термометр
    Thermometer.images = Graphics.load_images('temp_0.bmp','temp_1.bmp','temp_2.bmp','temp_3.bmp','temp_4.bmp','temp_5.bmp')
    #подгрузка изображений респаунов в список класса респаунов
    RespawnPoint.images = Graphics.load_images('respawn_point_0.bmp','respawn_point_1.bmp','respawn_point_2.bmp','respawn_point_3.bmp','respawn_point_4.bmp','respawn_point_5.bmp')
    #загрузка изображения гайм овера в класс гейм овер
    GameOver.images = Graphics.load_images('game_over_0.bmp','game_over_1.bmp' ,'game_over_2.bmp','game_over_3.bmp',
                                           'game_over_4.bmp','game_over_5.bmp','game_over_6.bmp','game_over_7.bmp',
                                           'game_over_8.bmp', 'game_over_9.bmp','game_over_10.bmp','game_over_11.bmp' )
    #занесение в список класса Лого имён изображений логотипа игры
    Logo.images = Graphics.load_images('Tanks_0.bmp','Tanks_1.bmp','Tanks_2.bmp')
    #занесение в список изображений класса Splashscreen изображения заставки
    SplashScreen.image = Graphics.load_image('splash_screen.bmp')
    MenuScreen.images = Graphics.load_images('Menu_0.bmp','Menu_1.bmp','Menu_2.bmp','Menu_3.bmp','Menu_4.bmp')
    CreditScreen.image = Graphics.load_image('credit_screen.bmp')
    #занесение в список изображений класса скорость изображения скорости???
    Gear.images = Graphics.load_images('gear_R.bmp','gear_R.bmp','gear_N.bmp','gear_1.bmp','gear_2.bmp','gear_3.bmp','gear_4.bmp')
    #загружаем картинку опций в класс окна опций
    Options.images = Graphics.load_images('Options_0_0.bmp','Options_0_1.bmp','Options_0_2.bmp','Options_0_3.bmp','Options_0_4.bmp','Options_0_5.bmp','Options_0_6.bmp',
                                          'Options_1_0.bmp','Options_1_1.bmp','Options_1_2.bmp','Options_1_3.bmp',
                                          'Options_2_0.bmp','Options_2_1.bmp','Options_2_2.bmp','Options_2_3.bmp','Options_2_4.bmp',
                                          'Options_3_0.bmp','Options_3_1.bmp','Options_3_2.bmp','Options_3_3.bmp','Options_3_4.bmp',
                                          'Options_4_0.bmp','Options_4_1.bmp','Options_4_2.bmp','Options_4_3.bmp','Options_4_4.bmp',
                                          'Options_5_0.bmp','Options_5_1.bmp','Options_5_2.bmp','Options_5_3.bmp','Options_5_4.bmp',
                                          'Options_6_0.bmp','Options_6_1.bmp','Options_6_2.bmp','Options_6_3.bmp','Options_6_4.bmp','Options_6_5.bmp',
                                          'Options_7_0.bmp',
                                          'Options_8_0.bmp','Options_8_1.bmp')
    #загрузка изображения пустого квадратика в класс данных игры
    GameData.transparant_sprite = Graphics.load_image('transparant_sprite.bmp')

    #украшаем главное окно:
    #заносим в иконку значение функции скэил, которая ставит картинку танчика в положение (x,y)
    icon = pygame.transform.scale(Tank.images[6], (32, 32))
    #помещаем иконку на главное окно
    pygame.display.set_icon(icon)
    #название главного окна
    pygame.display.set_caption('Tanks')
    #делаем невидимым курсор в главном окне
    pygame.mouse.set_visible(0)

    #создаём бэкграунд:сам бэкграунд-плита и лабиринт препятствий
    #загружаем бэкграунд с последнего места игры с помощью функции лоад класса графики
    bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
    #бэкграунд замощает весь экран
    background = pygame.Surface(GameData.screenrect.size)
    #рисуем бэкграунд из двойного буфера
    Graphics.draw_background(background,bgdtile,screen)

    #загрузка музыкального сопровождения
    boom_sound = Soundf.load_sound('boom.wav')
    if pygame.mixer:
        try:
            musics = os.path.join('Sound', 'Soundtrack.wav')
            pl_music = pygame.mixer.Sound(musics)
            pl_music.play(-1)

        except pygame.error:
                print ('Warning, unable to load,')


    # Инициализация спрайтовых групп
    #заводим список танков tanks
    tanks = pygame.sprite.Group()
    #заводим список пуль bullets
    bullets = pygame.sprite.Group()
    #заводим список респаунов
    respawn_points = pygame.sprite.Group()
    #заводим список копий танков
    tank_copies = pygame.sprite.Group()
    #заводим список взрывов
    explosions = pygame.sprite.Group()
    #заводим список окон заставок
    splashscreens = pygame.sprite.Group()

     #заводим список окон меню
    menuscreens = pygame.sprite.Group()

    creditscreens = pygame.sprite.Group()

    #заводим список набранных очков
    scores = pygame.sprite.Group()
    #заводим список гейм оверов
    gameovers = pygame.sprite.Group()
    #заводим список логотипов игры
    logos = pygame.sprite.Group()
    #заводим список опций
    options = pygame.sprite.Group()
    #(визуализация обновлений)делает возможным применение различных функций отрисовки бэкграунда и спрайтов
    all = pygame.sprite.RenderUpdates()

    #назначаем стандартные группы для каждого класса спрайта
    Score.containers = scores, all
    #например,здесь завели список в классе Танк, в котором показаны
    # группы к которым принадлежит тот или иной танк(олл и танкс)
    Tank.containers = tanks, all
    Bullet.containers = bullets, all
    Explosion.containers = explosions, all
    Thermometer.containers = all
    RespawnPoint.containers = respawn_points, all
    GameOver.containers = gameovers, all
    TankCopy.containers = tank_copies, all
    Logo.containers = logos, all
    GameOver.containers = gameovers, all
    SplashScreen.containers = splashscreens, all
    MenuScreen.containers = menuscreens, all
    CreditScreen.containers = creditscreens, all
    Gear.containers = all
    Options.containers = options, all
    NumericalOption.containers = options, all
    StringOption.containers = options, all

    step = 0    # используется в расчёте циклов анимации

    Logo()      # отображает анимированный логотип игры("Forever Tanks")

    # Создание мест восстановления танчиков(помещение спрайтов респаунов в соответствующие координаты под соотв. углом)
    for respawn_point in GameData.battleground[GameData.battlegroundnr].respawnpoints:
        RespawnPoint(respawn_point[0],respawn_point[1],respawn_point[2])

    thermometer = Thermometer() # Отображает нагрев пушки нашего танка
    gear = Gear()               # Отображает скорость нашего игрока

    ###########
    # главное окно
    #бесконечный цикл
    while True:
        # сначала переменной состояние игры из класса GameData присваивается значение экран заставки
        GameData.gamestate = "splash screen"
        #заводим переменную текущего экрана и вначале делаем текущим SplashScreen
        active_screen = SplashScreen()
        #отрисовываем поверх всех спррайтов ландшафт на главенствующее окно
        all.clear(screen, background)
        #стираем танки,копии танков, очки танков, взрывы танков,пули танков
        for tank in tanks:
            tank.kill()
        for tank in tank_copies:
            tank.kill()
        for score in scores:
            score.kill()
        for explosion in explosions:
            explosion.kill()
        for bullet in bullets:
            bullet.kill()

        #зануляем нагрев пушки нашего танчика
        thermometer.temperature = 0
        #прорисовали самый холодный термометр
        thermometer.update()
        #создаём список танков плэера и ботов,соответственно
        tanklist = [Tank(GameData.red, 0, 'Player'),
                    Tank(GameData.blue, 1, 'DefaultBot'),
                    Tank(GameData.green, 2, 'DefaultBot'),
                    Tank(GameData.yellow, 3, 'DefaultBot'),
                    Tank(GameData.grey, 4, 'DefaultBot'),
                    Tank(GameData.purple, 5, 'DefaultBot')]
                    # Параметры 'Player' и 'DefaultBot' не могут изменяться
                    # мы играем за красного танка
                    # ВНИМАНИЕ:ПОРЯДОК танков в вышепривидённом списке ВАЖЕН:
                    # цвет, который определён в GameData, используется как отличительный знак одного из танков

        # прорисовываем спрайты танков и респаунов, убираем окно заставки
        Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
        #ещё один бесконечный цикл для переменных анимаций и прорисовки спрайтов и того, что в окне
        waiting = True
        while waiting:
        #get input
            #отлавливаем событие функцией get()
            for event in pygame.event.get():
                #если кликнули по крестику или нажали комбинацию DOWN + ESCAPE, то закрывается главное окно
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
            # с помощью функции get_pressed() отлавливаем, то что нажал пользователь
            keystate = pygame.key.get_pressed()
            step = step + 1
            #наши переменные циклов анимаций спрайтов и окон обнуляем с некоторого значения
            if step > 4:
                step = 0
                GameData.animstep = GameData.animstep + 1
                if GameData.animstep > 5:
                    GameData.animstep = 0

            # очистка\стирание последних прорисованных спрайтов
            #прорисовываем сверху всех спрайтов ландшафт
            all.clear(screen, background)
            #перерисовываем танки
            tanks.update()
            #перерисовываем копии танков на панели очков
            tank_copies.update()
            #перерисовываем респауны
            respawn_points.update()
            #перерисовываем логотип
            logos.update()
            #рисуем сцену
            dirty = all.draw(screen)
            pygame.display.update(dirty)

            # ограничиваем частоту кадров
            clock.tick(40)
########################
            if keystate[K_SPACE]:
                menu_waiting = True
                #собственно, рисуем окно меню
                for splashscreen in splashscreens:
                    splashscreen.kill()
                #переменной состояние игры из класса GameData присваивается значение экран меню
                GameData.gamestate = "menu screen"
                #заводим переменную текущего экрана и вначале делаем текущим MenuScreen
                active_screen = MenuScreen()

                menucooldown = 0

                while menu_waiting:
                     #отлавливаем событие
                    for event in pygame.event.get():
                        #закрытие окна
                        if event.type == QUIT or \
                            (event.type == KEYDOWN and event.key == K_ESCAPE):
                                return

                    #отливаем нажатие клавиши
                    keystate = pygame.key.get_pressed()
                    if menucooldown == 0:
                        if keystate[K_DOWN]:
                            MenuScreen.count = Graphics.down(MenuScreen.count)
                            menucooldown = GameData.gearcooldown
                        if keystate[K_UP]:
                            MenuScreen.count = Graphics.up(MenuScreen.count)
                            menucooldown = GameData.gearcooldown
                    if keystate[K_RETURN] or keystate[K_KP_ENTER]:

                        if MenuScreen.count == 0:
                            for menuscreen in menuscreens:
                                menuscreen.kill()
                            menu_waiting = False
                            waiting = False
                        elif MenuScreen.count == 1:
                            print('2 players!')
                            menu_waiting = False
                            waiting = False
                        elif MenuScreen.count == 2:
                            print('Enternet!')
                            menu_waiting = False
                            waiting = False
                        elif MenuScreen.count == 3:
                            for menuscreen in menuscreens:
                                menuscreen.kill()
                            for splashscreen in splashscreens:
                                splashscreen.kill()
                            GameData.gamestate = "option screen"
                            #собственно, рисуем окно опций
                            active_screen = Options()
                            bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                            Graphics.draw_background(background, bgdtile, screen, True)
                            #...
                            optionscooldown = 0

                            # прорисовываем спрайты танков и респаунов, вместе с окном опций
                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
                            #пока не закрыто окно опций(за этим следит переменная options_waiting)
                            # изменение игровых опций
                            options_waiting = True
                            while options_waiting:


                                #отливаем нажатие клавиши
                                keystate = pygame.key.get_pressed()
                                #
                                if optionscooldown == 0:

                                    if Options.count == 37:

                                        if keystate[K_RETURN] or keystate[K_KP_ENTER]:

                                            for option in options:
                                                option.kill()
                                            GameData.gamestate = "credits screen"
                                            #собственно, рисуем окно опций
                                            active_screen = CreditScreen()
                                            bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                                            Graphics.draw_background(background, bgdtile, screen, True)
                                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)

                                        if keystate == [K_ESCAPE]:
                                            GameData.gamestate = "option screen"
                                            active_screen = Options()
                                            bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                                            Graphics.draw_background(background, bgdtile, screen, True)

                                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)

                                            for creditscreen in creditscreens:
                                                creditscreen.kill()
                                    if Options.count == 31:
                                        pl_music.stop()
                                    if Options.count == 32:
                                        try:
                                            pl_music.set_volume(0.1)
                                            pl_music.play(-1)
                                        except pygame.error:
                                             print ('Warning, unable to load,')
                                    if Options.count == 33:
                                        try:
                                            pl_music.set_volume(0.3)
                                            pl_music.play(-1)
                                        except pygame.error:
                                             print ('Warning, unable to load,')
                                    if Options.count == 34:
                                        try:
                                            pl_music.set_volume(0.5)
                                            pl_music.play(-1)
                                        except pygame.error:
                                             print ('Warning, unable to load,')
                                    if Options.count == 35:
                                        try:
                                            pl_music.set_volume(0.7)
                                            pl_music.play(-1)
                                        except pygame.error:
                                             print ('Warning, unable to load,')
                                    if Options.count == 36:
                                        try:
                                            pl_music.set_volume(0.9)
                                            pl_music.play(-1)
                                        except pygame.error:
                                             print ('Warning, unable to load,')
                                    if keystate[K_DOWN]:

                                        Options.count = Graphics._down(Options.count)
                                        optionscooldown = GameData.gearcooldown
                                    if keystate[K_UP]:
                                        Options.count = Graphics._up(Options.count)
                                        menucooldown = GameData.gearcooldown
                                    if keystate[K_RIGHT]:

                                        Options.count = Graphics._right(Options.count)

                                        if (Options.count > -1 and Options.count < 6):
                                            GameData._maze = Options.count
                                            if GameData.battlegroundnr < len(GameData.battleground)-1:
                                                GameData.battlegroundnr += 1
                                            else:
                                                GameData.battlegroundnr = 0
                                            #рисуем спрайты
                                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
                                            #рисуем новый ландшафт
                                            bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                                            Graphics.draw_background(background, bgdtile, screen, True)
                                            #переменная нужна,чтобы обновлять анимацию в дочернем окне опций
                                            optionscooldown = GameData.gearcooldown
                                        elif Options.count == 6:
                                            GameData._maze = Options.count
                                            GameData.battlegroundnr = 6
                                            #рисуем спрайты
                                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
                                            #рисуем новый ландшафт
                                            bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                                            Graphics.draw_background(background, bgdtile, screen, True)
                                            #переменная нужна,чтобы обновлять анимацию в дочернем окне опций
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 6 and Options.count < 10):
                                            GameData._difficulty = Options.count
                                            GameData.triggerhappiness += 1
                                            optionscooldown = GameData.gearcooldown


                                        elif Options.count == 10:
                                            GameData._difficulty = Options.count
                                            GameData.triggerhappiness = 30
                                            optionscooldown = GameData.gearcooldown

                                        #если нажата K_UP, то меняй максимальную скорость танчиков в сторону >
                                        elif (Options.count > 10 and Options.count < 15):
                                            GameData._gear_delay = Options.count
                                            GameData.gearcooldown += 1
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 15:
                                            GameData._gear_delay = Options.count
                                            GameData.gearcooldown = 10
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 15 and Options.count < 20):
                                            GameData._ammo_load_time = Options.count
                                            GameData.bulletloadtime += 1
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 20:
                                            GameData._ammo_load_time = Options.count
                                            GameData.bulletloadtime = 10
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 20 and Options.count < 25):
                                            GameData._max_temperature = Options.count
                                            GameData.maxbullets += 5
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 25:
                                            GameData._max_temperature = Options.count
                                            GameData.maxbullets = 30
                                            optionscooldown = GameData.gearcooldown

                                        #если , то меняй  в сторону >
                                        elif (Options.count > 25 and Options.count < 30):
                                            GameData._bullet_speed = Options.count
                                            GameData.bulletspeed += 1
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 30:
                                            GameData._bullet_speed = Options.count
                                            GameData.bulletspeed = 10
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 30 and Options.count < 36):
                                            GameData._volume = Options.count
                                            print('volume')

                                        elif Options.count == 36:
                                            GameData._volume = Options.count
                                            print('volume')

                                        elif Options.count == 37:
                                            GameData._credits = Options.count


                                        elif (Options.count > 37 and Options.count < 39):
                                            GameData._gamepad = Options.count
                                            print('gamepad')

                                        elif Options.count == 39:
                                            GameData._gamepad = Options.count
                                            print('gamepad')

                                    if keystate[K_LEFT]:
                                        Options.count = Graphics._left(Options.count)

                                        if (Options.count > 0 and Options.count < 7):
                                            GameData._maze = Options.count
                                            if GameData.battlegroundnr < len(GameData.battleground)-1:
                                                GameData.battlegroundnr -= 1
                                            else:
                                                GameData.battlegroundnr = 0
                                            #рисуем спрайты
                                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
                                            #рисуем новый ландшафт
                                            bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                                            Graphics.draw_background(background, bgdtile, screen, True)
                                            #переменная нужна,чтобы обновлять анимацию в дочернем окне опций
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 0:
                                            GameData._maze = Options.count
                                            GameData.battlegroundnr = 0
                                            #рисуем спрайты
                                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
                                            #рисуем новый ландшафт
                                            bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                                            Graphics.draw_background(background, bgdtile, screen, True)
                                            #переменная нужна,чтобы обновлять анимацию в дочернем окне опций
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 7 and Options.count < 11):
                                            GameData._difficulty = Options.count
                                            GameData.triggerhappiness -= 1
                                            optionscooldown = GameData.gearcooldown


                                        elif Options.count == 7:
                                            GameData._difficulty = Options.count
                                            GameData.triggerhappiness = 1
                                            optionscooldown = GameData.gearcooldown

                                        #если нажата K_UP, то меняй максимальную скорость танчиков в сторону >
                                        elif (Options.count > 11 and Options.count < 16):
                                            GameData._gear_delay = Options.count
                                            GameData.gearcooldown -= 1
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 11:
                                            GameData._gear_delay = Options.count
                                            GameData.gearcooldown = 1
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 16 and Options.count < 21):
                                            GameData._ammo_load_time = Options.count
                                            GameData.bulletloadtime -= 1
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 16:
                                            GameData._ammo_load_time = Options.count
                                            GameData.bulletloadtime = 1
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 21 and Options.count < 26):
                                            GameData._max_temperature = Options.count
                                            GameData.maxbullets -= 5
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 21:
                                            GameData._max_temperature = Options.count
                                            GameData.maxbullets = 1
                                            optionscooldown = GameData.gearcooldown

                                        #если , то меняй  в сторону >
                                        elif (Options.count > 26 and Options.count < 31):
                                            GameData._bullet_speed = Options.count
                                            GameData.bulletspeed -= 1
                                            optionscooldown = GameData.gearcooldown

                                        elif Options.count == 26:
                                            GameData._bullet_speed = Options.count
                                            GameData.bulletspeed = 1
                                            optionscooldown = GameData.gearcooldown

                                        elif (Options.count > 31 and Options.count < 37):
                                            GameData._volume = Options.count

                                        elif Options.count == 31:
                                            GameData._volume = Options.count

                                        elif Options.count == 37:
                                            GameData._credits = Options.count

                                        elif (Options.count > 38 and Options.count < 40):
                                            GameData._gamepad = Options.count

                                        elif Options.count == 38:
                                            GameData._gamepad = Options.count

                                #отлавливаем событие
                                for event in pygame.event.get():
                                    #закрытие окна
                                    if event.type == QUIT or \
                                        (event.type == KEYDOWN and event.key == K_ESCAPE):


                                        option_waiting = False
                                        #menu_waiting = False
                                        #waiting = False
                                        for menuscreen in menuscreens:
                                            menuscreen.kill()
                                        for splashscreen in splashscreens:
                                            splashscreen.kill()
                                        for option in options:
                                            option.kill()
                                            #GameData.gamestate = "menu screen"
                                            #собственно, рисуем окно опций
                                            #active_screen = MenuScreen()
                                            #bgdtile = Graphics.load_background(GameData.battleground[GameData.battlegroundnr].background, None)
                                            #Graphics.draw_background(background, bgdtile, screen, True)
                                            #Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
                                        waiting = False
                                        #перерисовываем сцену


                                #обновляем анимацию, если пользователь изменил какое-то значение
                                if optionscooldown > 0:
                                    optionscooldown -= 1
                                else:
                                    optionscooldown = 0
                                step = step + 1

                                #в дочернем окне степ и анимстеп тоже нужно обнулять
                                if step > 4:
                                    step = 0
                                    GameData.animstep = GameData.animstep + 1
                                    if GameData.animstep > 5:
                                        GameData.animstep = 0

                                # стираем последние нарисованные спрайты
                                all.clear(screen, background)
                                tanks.update()
                                tank_copies.update()
                                respawn_points.update()
                                logos.update()
                                options.update()
                                #перерисовываем сцену
                                dirty = all.draw(screen)
                                pygame.display.update(dirty)
                                #ограничиваем частоту кадров
                                clock.tick(10)
                                #удаляем все спрайты-опции и активируем окно заставки
                            for option in options:
                                option.kill()
                            Graphics.draw_background(background, bgdtile, screen)
                            active_screen = MenuScreen()
                            # прорисовываем спрайты танков и респаунов, вместе с окном заставок
                            Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, True)
                            #menu_waiting = False
                        elif MenuScreen.count == 4:
                            menu_waiting = False
                            return




                    #обновляем анимацию, если пользователь изменил какое-то значение
                    if menucooldown > 0:
                        menucooldown -= 1
                    else:
                        menucooldown = 0
                    step = step + 1

                    #в дочернем окне степ и анимстеп тоже нужно обнулять
                    if step > 4:
                        step = 0
                        GameData.animstep = GameData.animstep + 1
                        if GameData.animstep > 5:
                            GameData.animstep = 0

                    # стираем последние нарисованные спрайты
                    all.clear(screen, background)
                    tanks.update()
                    tank_copies.update()
                    respawn_points.update()
                    logos.update()
                    menuscreens.update()
                    #перерисовываем сцену
                    dirty = all.draw(screen)
                    pygame.display.update(dirty)
                    #ограничиваем частоту кадров
                    clock.tick(20)

                for menuscreen in menuscreens:
                    menuscreen.kill()

                waiting = False


########################


        # Мы в ИГРЕ
        # делаем все танки и респауны видимыми, с помощью параметра визибл - параметр любого спрайта
        for respawn_point in respawn_points:
            respawn_point.visible = True
        for tank in tanks:
            tank.visible = True
        #переводим состояние игры в режим окна боя
        GameData.gamestate = "fighting"

        # Игрок должен умереть 3 раза - тогда переключается состояние игры на гейм овер
        #(хоть и написписано в презентации "аркадный режим" - пока он не реализован)



        #заводим цикл - пока параметр "число смертей" красного(т.е. нашего) танка меньше десяти, то
        while tanklist[GameData.red].deaths < 3:

            #отлавливаем событие
            for event in pygame.event.get():
                #если нажали красный крестик или комбинацию клавиш KEYDOWN+ESCAPE, то выходим из игры
                if event.type == QUIT:
                    return
                if event.key == K_ESCAPE:
                    GameData.gamestate = "pause"
                    pause_waiting = True
                    while pause_waiting:
                        for event in pygame.event.get():
                        #если нажали красный крестик или комбинацию клавиш KEYDOWN+ESCAPE, то выходим из игры
                            if event.type == QUIT:
                                return
                            if event.key == K_ESCAPE:
                                pause_waiting = False
            #отливаем нажатие клавиши пользователем
            keystate = pygame.key.get_pressed()
            # стираем с экрана последние нарисованные спрайты, это логично, т.к. пользователь нажал клавишу - пора
            #всё перерисовать - т.е. среагировать игре,но тоже верно, если он ничего не нажал
            all.clear(screen, background)

            #определяем столкновение танка с пулями
            #для всех пуль из списка
            for bullet in bullets:

                btest = True  # заводим флажок-переменную, которая предупреждает пересчёт одной и той же пули более одного раза,
                #например, при попадании в танк, если нет этой переменной, то пуля не исчезает, и убивает следующий танк, и т.д.

                #если пуля танка цвета bullet.colour попала в респаун(проверка функцией spritecollide), то убиваем её с экрана
                for respawn_point in pygame.sprite.spritecollide(bullet, respawn_points, 0):
                    if tanklist[bullet.colour].bullets > 0:
                        #танчик может выстрелить ещё одной пулей
                        tanklist[bullet.colour].bullets = tanklist[bullet.colour].bullets - 1
                    bullet.kill()
                    # флажок фолсим
                    btest = False
                    break
                # пока флаг = истина, т.е. пока пуля летит по полю боя
                if btest:
                    #для всех стен
                    for wall in GameData.battleground[GameData.battlegroundnr].walls:
                        #если пуля попала в стену(стена-совокупность квадратиков)
                        if wall.colliderect(bullet.rect):
                            if tanklist[bullet.colour].bullets > 0:
                                #танчик может выстрелить ещё одной пулей
                                tanklist[bullet.colour].bullets = tanklist[bullet.colour].bullets - 1
                            #а ту пулю убиваем
                            bullet.kill()
                            #и делаем невидимой
                            btest = False
                            break
                # пока флаг = истина, т.е. пока пуля летит по полю боя
                if btest:
                    #если пуля попала в один из танков
                    for tank in pygame.sprite.spritecollide(bullet, tanks, 0):
                        #если вет пули не совпал с цветом танка
                        if bullet.colour != tank.colour:
                            #играем музыку взрыва танка
                            boom_sound.play()
                            #на табло очков прибавляем 1 к танку цвета spritecollide
                            tanklist[bullet.colour].kills += 1
                            #Запускаем спрайт взрыва танка
                            Explosion(tank)
                            #взрываем танк
                            tank.explode()
                            #если взорвался танк-бот
                            if tank.colour != GameData.red:   # возвращаем бота к игре с респауна
                                #для i пробегающего значения от 1 до 20
                                for i in range(0,20):
                                  #поведение бота после появления на респауне()здесь он вылазиет из респауна
                                    tank.command_queue.append("up")
                                    tank.command_queue.append("shoot")
                                tank.command_queue.append("flush")
                            #если пуля попала в бота
                            if tanklist[bullet.colour].bullets > 0:
                                #танчик может выстрелить ещё одной пулей
                                tanklist[bullet.colour].bullets = tanklist[bullet.colour].bullets - 1
                            bullet.kill()
                            btest = False
                            break
                #если пуля вылетела за пределы главного окна, то убиваем её, добавляем к очереди
                #танка ещё одну пульку,т.е. понижаем нагрев его пушки(он может выстрелить ещё раз)
                if btest and ((bullet.x < 0) or (bullet.y < 0) or (bullet.x > 800) or (bullet.y > 768)):
                    if tanklist[bullet.colour].bullets > 0:
                        tanklist[bullet.colour].bullets = tanklist[bullet.colour].bullets - 1
                    bullet.kill()

            # Всё, что могут делать танки:
            #для всех танков в списке
            for tank in tanks:
                if tank.gun_cooldown > 0:
                    tank.gun_cooldown = tank.gun_cooldown - 1
                if tank.gear_cooldown > 0:
                    tank.gear_cooldown = tank.gear_cooldown - 1

                if tank.colour != GameData.red:
                    DefaultBot(tank) # AI контролирует все вражеские танки кроме красного
                else:
                    # иначе, отлавливай нажатие плэером кнопок движения и
                    #добавляй в очередь команд красного танчика
                    #двигайся вверх
                    if keystate[K_UP]:
                        #в очередь комманд добавить сдвинуться вверх
                        tank.command_queue.append("up")
                    #двигайся вниз
                    if keystate[K_DOWN]:
                        tank.command_queue.append("down")
                    #двигайся влево
                    if keystate[K_LEFT]:
                        tank.command_queue.append("left")
                    #двигайся вправо
                    if keystate[K_RIGHT]:
                        tank.command_queue.append("right")
                    #остановиться
                    if keystate[K_KP0]:
                        tank.command_queue.append("halt")
                    #стреляй
                    if keystate[K_SPACE]:
                        tank.command_queue.append("shoot")
                    # исправление лагов(если появятся) при выполнении последних комманд(что выше)
                    #пока больше пяти комманд
                    while len(tank.command_queue) > 4:
                        #пользуемся пайпами(трубами),выполняя команды
                        dummy = tank.command_queue.pop(0)

                # комманда только что сдохнувшему танку(появись в respawn_points)
                if len(tank.command_queue) > 0:
                    tank.process_commands(respawn_points)

                tank.move()

            # отображение нагрева пушки(текущее число пуль одного танка на экране)
            #присваиваем переменной thermometer.temperature значение bullets на экране
            thermometer.temperature = tanklist[GameData.red].bullets
            #отображение индикатора передачи скорости красного танчика
            gear.gear = tanklist[GameData.red].gear

            # цикл анимации - нужно поправить используемую modula division
            #самый простой цикл(прибавляем один к переменной цикла анимации)
            step = step + 1
            #обнуляем её после значения пять
            if step > 4:
                step = 0
                #прибавляем один к значению переменной циклов спрайтов
                GameData.animstep = GameData.animstep + 1
                #обнуляем после значения 6
                if GameData.animstep > 5:
                    GameData.animstep = 0

            #апдэйт всех спрайтов
            all.update()

            #рисуй сцену
            dirty = all.draw(screen)
            pygame.display.update(dirty)

            #ограничили частоту кадров
            clock.tick(40)

        #######################
        #активировали окно GameOver
        active_screen = GameOver()
        # прорисовываем спрайты танков и респаунов, вместе с окном GameOver
        Graphics.determine_visibility(respawn_points, tanks, tanklist, active_screen, False)
        #состояние игры = gameover
        GameData.gamestate = "gameover"
        # переменная для бесконечного цикла(видимости окна геймовер)
        waiting = True
        #пока ожидание
        while waiting:
            #отлавливаем событие
            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
            #отлавливаем нажатие клавиши
            keystate = pygame.key.get_pressed()
            #если нажали одну из этих клавиш, то обновляй анимацию вместе со стиранием окна gameover и выходом из игры
            if keystate[K_RETURN] or keystate[K_KP_ENTER]:
                waiting = False
            step = step + 1
            if step > 4:
                step = 0
                GameData.animstep = GameData.animstep + 1
                if GameData.animstep > 5:
                    GameData.animstep = 0
            # апдэйтим спрайты
            all.clear(screen, background)
            scores.update()
            tanks.update()
            tank_copies.update()
            respawn_points.update()
            explosions.update()
            logos.update()
            gameovers.update()

            #обновляем сцену
            dirty = all.draw(screen)
            pygame.display.update(dirty)
            #ограничиваем частоту кадров
            clock.tick(40)

        for gameover in gameovers:
            gameover.kill()

####################
#запуск программы
if __name__ == '__main__': main()
