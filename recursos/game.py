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
icon  = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

## cars
red_car = Car("assets/red_car.png", config.game_resolution)
purple_car = Car("assets/purple_car.png", config.game_resolution)
yellow_car = Car("assets/yellow_car.png", config.game_resolution)
blue_car = Car("assets/blue_car.png", config.game_resolution)
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
font_small = pygame.font.SysFont("arial", 12)
font = pygame.font.SysFont("arial", 22)
font_big = pygame.font.SysFont("arial", 72)


## filters
filter = pygame.Surface(config.game_resolution, pygame.SRCALPHA)

filter_transparent = filter
filter_transparent.fill(config.black_transparent)

filter_transparent_2 = filter
filter_transparent.fill(config.black_transparent_2)

    

def start():
    menu(home_background)


def menu(background):    
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    
    center_position_x_start = (config.game_resolution[0] - larguraButtonStart) / 2
    center_position_y_start = ((config.game_resolution[1] - alturaButtonStart) / 2) - 10


    center_position_x_quit = (config.game_resolution[0] - larguraButtonQuit) / 2
    center_position_y_quit = ((config.game_resolution[1] + alturaButtonQuit) / 2) + 10


    startTexto = font.render("Iniciar Game", True, config.black)
    start_text_width , start_text_height = startTexto.get_size()
    center_position_x_start_text = center_position_x_start + (larguraButtonStart - start_text_width) / 2
    center_position_y_start_text = center_position_y_start + (alturaButtonStart - start_text_height) / 2
    
    
    quitTexto = font.render("Sair do Game", True, config.black)
    quit_text_width , quit_text_height = quitTexto.get_size()
    center_position_x_quit_text = center_position_x_quit + (larguraButtonQuit - quit_text_width) / 2
    center_position_y_quit_text = center_position_y_quit + (alturaButtonQuit - quit_text_height) / 2


    
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
        window.blit(background, (0,0))
        window.blit(filter_transparent_2, (0, 0))

        startButton = pygame.draw.rect(window, config.white, (center_position_x_start, center_position_y_start, larguraButtonStart, alturaButtonStart), border_radius=15)
        window.blit(startTexto, (center_position_x_start_text, center_position_y_start_text))
        
        quitButton = pygame.draw.rect(window, config.white, (center_position_x_quit, center_position_y_quit, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        window.blit(quitTexto, (center_position_x_quit_text, center_position_y_quit_text))
        
        pygame.display.flip()
        clock.tick(60)


def play():
    move_x_red_car  = 0
    move_y_red_car  = 0
    enemy_car = enemy_cars[random.randint(0, len(enemy_cars) - 1)] 
    
    position = random.randint(0, len(config.enemy_positions_x) - 1)
    if position % 2 == 0:
        enemy_car.setRotation("down")
    else:
        enemy_car.setRotation("up")
    enemy_car.x = config.enemy_positions_x[position]
    
    enemy_car.y = -100
    enemy_car.velocity = 5
    enemy_car_velocity = enemy_car.velocity
    pontos = 0
    count_cars = 0
    dificuldade  = 30
    
    is_paused = False
    pause = False
    
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
            elif evento.type == pygame.KEYDOWN and evento.key == (pygame.K_SPACE):
                if is_paused:
                    is_paused = False
                    pause = False
                else:
                    is_paused = True
                    pause = True
                
                                
               
        if is_paused:
            if pause:  
                window.blit(filter_transparent, (0, 0))

                texto_pause = font_big.render("PAUSE", True, config.white)
                texto_rect = texto_pause.get_rect(center=(config.game_resolution[0] // 2, config.game_resolution[1] // 2))
                window.blit(texto_pause, texto_rect)
                
                pause = False
        
        
        else:    
            red_car.x = red_car.x + move_x_red_car            
            red_car.y = red_car.y + move_y_red_car
            enemy_car.y = enemy_car.y + enemy_car.velocity            
            
            
            if red_car.x < config.road_limit_x[0]:
                red_car.x = config.road_limit_x[0]
            elif red_car.x > config.road_limit_x[1]:
                red_car.x = config.road_limit_x[1]
                
                
            if red_car.y < 0 :
                red_car.y = 10
            elif red_car.y > 473:
                red_car.y = 463
                    

            config.map_velocity += 0.007
            config.map_1_postion_y += config.map_velocity
            config.map_2_postion_y += config.map_velocity
            
            
            if(config.map_1_postion_y >= config.game_resolution[1]):
                config.map_1_postion_y = config.map_2_postion_y-1390
                        
            if(config.map_2_postion_y >= config.game_resolution[1]):
                config.map_2_postion_y = config.map_1_postion_y-1390
            
            
            if enemy_car.y > red_car.y and count_cars == pontos:
                pontos += 1
                pygame.mixer.Sound.play(race_car_passing)
                
            
            if enemy_car.y > config.game_resolution[1]:
                count_cars += 1              
                enemy_car = enemy_cars[random.randint(0, len(enemy_cars) - 1)] 
                
                position = random.randint(0, len(config.enemy_positions_x) - 1)
                if position % 2 == 0:
                    enemy_car.setRotation("down")
                else:
                    enemy_car.setRotation("up")
                enemy_car.x = config.enemy_positions_x[position]
    
                enemy_car.y = int(enemy_car.resolution[1] * -1)
                enemy_car_velocity = enemy_car_velocity + 1
                enemy_car.velocity = enemy_car_velocity
            
            
            text_points = font.render("Pontos: " + str(pontos), True, config.white)
            text_points_width = (text_points.get_size()[0]) + 60
            
            text_pause = font_small.render("Press Space to Pause Game", True, config.white)
            text_pause_width = (text_points.get_size()[0])
            
            label_width = text_points_width + text_pause_width + 52
            label_point = pygame.Surface((label_width, 35), pygame.SRCALPHA)
            pygame.draw.rect(label_point, config.black_transparent_2, (0, 0, label_width, 35))
        
            
            red_car.colisor_x = list(range(red_car.x, red_car.x + red_car.width))
            red_car.colisor_y = list(range(red_car.y, red_car.y + red_car.height))
            enemy_car.colisor_x = list(range(enemy_car.x, enemy_car.x + enemy_car.width))
            enemy_car.colisor_y = list(range(enemy_car.y, enemy_car.y + enemy_car.height))
            
            
            if  len( list( set(enemy_car.colisor_y).intersection(set(red_car.colisor_y))) ) > dificuldade:
                if len( list( set(enemy_car.colisor_x).intersection(set(red_car.colisor_x))   ) )  > dificuldade:
                    
                    pygame.mixer.Sound.play(crashSound)

                    escreverDados(interface.name, pontos)
                    interface.dead_window()
                    
                    menu(endgame_background)

            
            ## render
            window.fill(config.white)    
            window.blit(road_background_1, (config.map_1_postion_x, config.map_1_postion_y))
            window.blit(road_background_2, (config.map_2_postion_x, config.map_2_postion_y))        
            window.blit(red_car.sprite, (red_car.x, red_car.y))
            window.blit(enemy_car.sprite, (enemy_car.x, enemy_car.y) )
            window.blit(label_point, (5, 11))
            window.blit(text_points, (15,15))
            window.blit(text_pause, (text_points_width, 25))
        
        
        pygame.display.flip()
        clock.tick(60)