import pygame
from pygame import *
import time
import random
import sqlite3
import sys

from pygame import event
from pygame.constants import QUIT

pygame.init()
dis_width = 600 
dis_height = 400

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

playername=""

snake_block=10
snake_speed=15
font_style = pygame.font.SysFont("calibri",25)
score_font = pygame.font.SysFont("comicsanms", 35)

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by DravockSoftware')

clock = pygame.time.Clock()
def Your_score(score):
    value = score_font.render( playername + " 's Score " + str(score),True,yellow)
    dis.blit(value,[0,0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0],x[1],snake_block,snake_block])
def message (msg,color):
    mesg=font_style.render(msg,True,color)
    dis.blit(mesg,[dis_width/6,dis_height/3])
def menue_screen():
    global playername
    print("menü_screen gestartet ")
    menue_active=True
    name=""
    playername=""
    clock=pygame.time.Clock()
    firstreturn = False
    while menue_active == True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("menu beendet")
                menue_active= False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if not firstreturn:
                        playername=name
                        name=""
                        print(playername)
                        firstreturn=True
                    else:
                        main_game()
                else :
                    name += event.unicode
            elif event.type == pygame.QUIT:
                return

        dis.fill(blue)

        willkommens_text = font_style.render("Willkommen bei Snake", True, black)
        dis.blit(willkommens_text, [175, 25])
        namenseingabe =font_style.render("Bitte Geben Sie hier ihren Namen ein",True,black)  
        dis.blit(namenseingabe,[100,100])      
        block = font_style.render(name, True, white)
        dis.blit(block, [225,205])
        pygame.draw.rect(dis, black, [175,200,250,40], width=1)

        if firstreturn ==True :
            playernmedis =font_style.render("Hallo " + str(playername) + "!" ,True,black)  
            dis.blit(playernmedis,[225,300])
            anzeige2=font_style.render("Drücken Sie 'Enter' um das Spiel zu Starten",True,black)
            dis.blit(anzeige2,[75,325])

        pygame.display.flip()
        clock.tick()
    pygame.quit()
    quit()
def main_game():
    print("game run gestartet")
    print(playername)
    game_active= True
    direction_closed =""
    x1 =dis_width/2
    y1= dis_height/2

    x1_change = 0
    y1_change = 0

    snake_list=[]
    length_of_snake= 1

    foodx=round(random.randrange(0,dis_width-snake_block)/10)*10
    foody=round(random.randrange(0, dis_height-snake_block)/10)*10

    while game_active == True :
        dis.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_active=False
                print("Gamerun beendet")
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction_closed!="left":
                    x1_change = -snake_block
                    y1_change = 0
                    direction_closed="right"
                elif event.key == pygame.K_RIGHT and direction_closed !="right":
                    x1_change = snake_block
                    y1_change = 0
                    direction_closed="left"
                elif event.key == pygame.K_UP and direction_closed !="up":
                    y1_change = -snake_block
                    x1_change = 0
                    direction_closed="down"
                elif event.key == pygame.K_DOWN and direction_closed !="down":
                    y1_change = snake_block
                    x1_change = 0
                    direction_closed="up"
                elif event.key == pygame.K_SPACE:
                    pause()
                print(direction_closed)
                
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_active = False
            game_over()
        
        x1 += x1_change
        y1 += y1_change
        
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_Head:
                game_active = False
                game_over()
            
        our_snake(snake_block, snake_list)
        Your_score(length_of_snake - 1)

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
        
        pygame.display.update()
        clock.tick(snake_speed)
def game_over():
    print("Game over Screen gestartet")
    clock=pygame.time.Clock()
    game_over_screen=True
    while game_over_screen == True :
        dis.fill(blue) 
        for event in pygame.event.get ():
            if  event.type== pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("game over screen beendet")
                game_over_screen=False

            elif event.type == pygame.KEYDOWN and event.key== pygame.K_SPACE:
                main_game()
            elif event.type== pygame.KEYDOWN and event.key == pygame.K_RETURN:
                menue_screen()
            elif event.type == pygame.KEYDOWN and event.key ==pygame.K_BACKSPACE:
                highscoreliste()

        gameoveranzeige=font_style.render("Game Over ! ", True , black)
        dis.blit(gameoveranzeige,[250,50])
        playagainanzeige=font_style.render("Noch eine runde ? Drücke 'SPACE' Taste",True,black)
        dis.blit(playagainanzeige,[100,150])
        newgameanzeige=font_style.render("Neuer Spieler? Drücke 'ENTER' Taste ",True,black)
        dis.blit(newgameanzeige,[100,200])
        highscorelistanzeige=font_style.render("Bestenliste ansehen? Drücke 'H' Taste",True,black)
        dis.blit(highscorelistanzeige,[100,250])
        quitgameanzeige=font_style.render("Spiel beenden -  Drücke 'ESC' Taste",True,black)
        dis.blit(quitgameanzeige,[100,300])        
        pygame.display.flip()
        clock.tick()
    pygame.quit()
    quit()
def pause():
    loop = 1
    game_pause_message = font_style.render("PAUSED", 500, 150)
    game_pause_message = font_style.render("Press Space to continue", 500, 250)
    while loop:
        dis.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_SPACE:
                    dis.fill((0, 0, 0))
                    loop = 0
        pygame.display.update()
        text = font_style.render("Pause", True, green)
        dis.blit(text, [270, 190])
def highscoreliste():
    print("highscore liste gestartet")
    clock=pygame.time.Clock()
    highscorelist_active =True
    while highscorelist_active==True:
        dis.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                highscorelist_active=False
                print("Highscore Screen beendet")
                pygame.quit()
                sys.exit()
        highscoreanzeige=font_style.render("Highscore Liste",True,black)
        dis.blit(highscoreanzeige,[200,50])
        pygame.display.flip()
        clock.tick()

menue_screen()