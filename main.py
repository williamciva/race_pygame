import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.car import Car
import recursos.config as config
import json


pygame.init()
inicializarBancoDeDados()
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( config.game_resolution ) 
pygame.display.set_caption("Need 4 Python")
icone  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )


## base assets
## cars
red_car = Car("assets/red_car.png", config.game_resolution)
purple_car = Car("assets/purple_car.png", config.game_resolution, "down")
yellow_car = Car("assets/yellow_car.png", config.game_resolution, "down")
blue_car = Car("assets/blue_car.png", config.game_resolution, "down")
enemy_cars = (purple_car, yellow_car, blue_car)

# backgrounds
home_background = pygame.transform.smoothscale(pygame.image.load("assets/home_background.png"), config.game_resolution)


## backgrounds
road_background_1 = pygame.image.load("assets/road_big.png")
road_background_2 = pygame.transform.rotate(pygame.image.load("assets/road_big.png"), 180)


## sounds
pygame.mixer.music.load("assets/nfs_theme.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.fadeout(3000)
pygame.mixer.music.play(-1, fade_ms=2000)

race_car_passing = pygame.mixer.Sound("assets/race_car_passing.mp3")
race_car_passing.set_volume(0.05)


fundoDead = pygame.image.load("assets/fundoDead.png")

explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)


def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            root.destroy()  # Fecha a janela após a entrada válida

    # Criação da janela principal
    root = tk.Tk()
    # # Obter as dimensões da tela
    # largura_tela = root.winfo_screenwidth()
    # altura_tela = root.winfo_screenheight()
    # pos_x = (largura_tela - largura_janela) // 2
    # pos_y = (altura_tela - altura_janela) // 2
    # root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    # root.title("Informe seu nickname")
    # root.protocol("WM_DELETE_WINDOW", obter_nome)

    # # Entry (campo de texto)
    # entry_nome = tk.Entry(root)
    # entry_nome.pack()

    # # Botão para pegar o nome
    # botao = tk.Button(root, text="Enviar", command=obter_nome)
    # botao.pack()

    # # Inicia o loop da interface gráfica
    # root.mainloop()
    
    # if (True):
    #     raise Exception("w: " + str(red_car.width) + " h: " + str(red_car.height))


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
        
            
        tela.fill(branco)
        

        config.map_velocity += 0.007
        config.map_1_postion_y += config.map_velocity
        config.map_2_postion_y += config.map_velocity
        
        
        if(config.map_1_postion_y >= 700):
            config.map_1_postion_y = config.map_2_postion_y-1390
                    
        if(config.map_2_postion_y >= 700):
            config.map_2_postion_y = config.map_1_postion_y-1390
        
            
        tela.blit(road_background_1, (config.map_1_postion_x, config.map_1_postion_y))
        tela.blit(road_background_2, (config.map_2_postion_x, config.map_2_postion_y))        
        tela.blit(red_car.sprite, (red_car.x, red_car.y))
        
        
        enemy_car.y = enemy_car.y + enemy_car.velocity
        if enemy_car.y > red_car.y:
            pontos = pontos + 1
            
            enemy_car = enemy_cars[random.randint(0, len(enemy_cars) - 1)] 
            enemy_car.x = config.enemy_positions_x[random.randint(0, len(config.enemy_positions_x) - 1)]
            enemy_car.y = -240
            enemy_car_velocity = enemy_car_velocity + 1
            enemy_car.velocity = enemy_car_velocity
            
            pygame.mixer.Sound.play(race_car_passing)
        
            

        tela.blit(enemy_car.sprite, (enemy_car.x, enemy_car.y) )
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
    
        
        red_car.colisor_x = list(range(red_car.x, red_car.x + red_car.width))
        red_car.colisor_y = list(range(red_car.y, red_car.y + red_car.height))
        enemy_car.colisor_x = list(range(enemy_car.x, enemy_car.x + enemy_car.width))
        enemy_car.colisor_y = list(range(enemy_car.y, enemy_car.y + enemy_car.height))
        
        
        os.system("cls")
        if  len( list( set(enemy_car.colisor_y).intersection(set(red_car.colisor_y))) ) > dificuldade:
            if len( list( set(enemy_car.colisor_x).intersection(set(red_car.colisor_x))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
        
        pygame.display.update()
        relogio.tick(60)


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
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(home_background, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
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
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        
            
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)


start()