import pygame
import random
import os
import recursos.config as config
from recursos.car import Car
from recursos.funcoes import escreverDados
import recursos.interface as interface


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(config.game_resolution) 
pygame.display.set_caption("Need 4 Python")


# icons
icone  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)

## cars
red_car = Car("assets/red_car.png", config.game_resolution)
purple_car = Car("assets/purple_car.png", config.game_resolution, "down")
yellow_car = Car("assets/yellow_car.png", config.game_resolution, "down")
blue_car = Car("assets/blue_car.png", config.game_resolution, "down")
enemy_cars = (purple_car, yellow_car, blue_car)


# backgrounds
home_background = pygame.transform.smoothscale(pygame.image.load("assets/home_background.png"), config.game_resolution)
endgame_background = pygame.transform.smoothscale(pygame.image.load("assets/car_crashed.png"), config.game_resolution)

road_background_1 = pygame.image.load("assets/road_big.png")
road_background_2 = pygame.transform.rotate(pygame.image.load("assets/road_big.png"), 180)


## sounds
pygame.mixer.music.load("assets/nfs_theme.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.fadeout(3000)
pygame.mixer.music.play(-1, fade_ms=2000)

race_car_passing = pygame.mixer.Sound("assets/race_car_passing.mp3")
race_car_passing.set_volume(0.05)

crashSound = pygame.mixer.Sound("assets/crash.mp3")
crashSound.set_volume(0.2)


## fonts
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)


def play():
    move_x_red_car  = 0
    move_y_red_car  = 0
    enemy_car = enemy_cars[random.randint(0, len(enemy_cars) - 1)] 
    enemy_car.x = config.enemy_positions_x[random.randint(0, len(config.enemy_positions_x) - 1)]
    enemy_car.y = -100
    enemy_car.velocity = 5
    enemy_car_velocity = enemy_car.velocity
    pontos = 0
    dificuldade  = 30
        
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and (evento.key == pygame.K_RIGHT or evento.key == pygame.K_d):
                move_x_red_car = 15
            elif evento.type == pygame.KEYDOWN and (evento.key == pygame.K_LEFT or evento.key == pygame.K_a):
                move_x_red_car = -15
            elif evento.type == pygame.KEYUP and (evento.key == pygame.K_RIGHT or evento.key == pygame.K_d):
                move_x_red_car = 0
            elif evento.type == pygame.KEYUP and (evento.key == pygame.K_LEFT or evento.key == pygame.K_a):
                move_x_red_car = 0
            elif evento.type == pygame.KEYDOWN and (evento.key == pygame.K_UP or evento.key == pygame.K_w):
                move_y_red_car = -15
            elif evento.type == pygame.KEYDOWN and (evento.key == pygame.K_DOWN or evento.key == pygame.K_s):
                move_y_red_car = 15
            elif evento.type == pygame.KEYUP and evento.key == (pygame.K_UP or evento.key == pygame.K_w):
                move_y_red_car = 0
            elif evento.type == pygame.KEYUP and evento.key == (pygame.K_DOWN or evento.key == pygame.K_s):
                move_y_red_car = 0
                
        red_car.x = red_car.x + move_x_red_car            
        red_car.y = red_car.y + move_y_red_car            
        
        if red_car.x < config.road_limit_x[0]:
            red_car.x = config.road_limit_x[0]
        elif red_car.x > config.road_limit_x[1]:
            red_car.x = config.road_limit_x[1]
            
        if red_car.y < 0 :
            red_car.y = 15
        elif red_car.y > 473:
            red_car.y = 463
                

        config.map_velocity += 0.007
        config.map_1_postion_y += config.map_velocity
        config.map_2_postion_y += config.map_velocity
        
        
        if(config.map_1_postion_y >= config.game_resolution[1]):
            config.map_1_postion_y = config.map_2_postion_y-1390
                    
        if(config.map_2_postion_y >= config.game_resolution[1]):
            config.map_2_postion_y = config.map_1_postion_y-1390
        
        
        enemy_car.y = enemy_car.y + enemy_car.velocity
        if enemy_car.y > config.game_resolution[1]:
            pontos = pontos + 1
            
            enemy_car = enemy_cars[random.randint(0, len(enemy_cars) - 1)] 
            enemy_car.x = config.enemy_positions_x[random.randint(0, len(config.enemy_positions_x) - 1)]
            enemy_car.y = int(enemy_car.resolution[1] * -1)
            enemy_car_velocity = enemy_car_velocity + 1
            enemy_car.velocity = enemy_car_velocity
            
            pygame.mixer.Sound.play(race_car_passing)
        
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, config.white)
    
        
        red_car.colisor_x = list(range(red_car.x, red_car.x + red_car.width))
        red_car.colisor_y = list(range(red_car.y, red_car.y + red_car.height))
        enemy_car.colisor_x = list(range(enemy_car.x, enemy_car.x + enemy_car.width))
        enemy_car.colisor_y = list(range(enemy_car.y, enemy_car.y + enemy_car.height))
        
        
        os.system("cls")
        if  len( list( set(enemy_car.colisor_y).intersection(set(red_car.colisor_y))) ) > dificuldade:
            if len( list( set(enemy_car.colisor_x).intersection(set(red_car.colisor_x))   ) )  > dificuldade:
                escreverDados(interface.name, pontos)
                dead()
                
        
        ## render
        window.fill(config.white)    
        window.blit(road_background_1, (config.map_1_postion_x, config.map_1_postion_y))
        window.blit(road_background_2, (config.map_2_postion_x, config.map_2_postion_y))        
        window.blit(red_car.sprite, (red_car.x, red_car.y))
        window.blit(enemy_car.sprite, (enemy_car.x, enemy_car.y) )
        window.blit(texto, (15,15))
        
        
        pygame.display.update()
        clock.tick(60)


def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    interface.input_name()
                    play()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        window.fill(config.white)
        window.blit(home_background, (0,0) )

        startButton = pygame.draw.rect(window, config.white, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, config.black)
        window.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(window, config.white, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, config.black)
        window.blit(quitTexto, (25,62))
        
        pygame.display.update()
        clock.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crashSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    interface.dead_window()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    play()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        
            
            
        window.fill(config.white)
        window.blit(endgame_background, (0,0) )

        
        startButton = pygame.draw.rect(window, config.white, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, config.black)
        window.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(window, config.white, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, config.black)
        window.blit(quitTexto, (25,62))


        pygame.display.update()
        clock.tick(60)