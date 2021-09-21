import pygame
import time
import random
import sqlite3
import sys
from pygame import *
from sqlite3.dbapi2 import SQLITE_SELECT
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
score1=0

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
    global playername ,score1
    print("menü_screen gestartet ")
    menue_active=True
    name=""
    playername=""
    clock=pygame.time.Clock()
    firstreturn = False
    while menue_active == True :
        dis.fill(blue)        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("menu beendet")
                menue_active= False
                sys.exit()
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
    global playername , score1
    print("game run gestartet")
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
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
                print("direction closed: ",direction_closed)
                
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_active = False
            game_over()
        
        x1 += x1_change
        y1 += y1_change
        
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        # snake_body=[]
        # snake_body.append(x1)
        # snake_body.append(y1)
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
        score1=length_of_snake-1

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

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                menue_screen()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
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
    print("pause")
    while loop:
        dis.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    
                    loop = 0
        game_pause_message = font_style.render("PAUSED", True, black)
        dis.blit(game_pause_message,[225,150])
        game_pause_message1 = font_style.render("Press 'Space' to continue", True,black)
        dis.blit(game_pause_message1,[150,175])
        pygame.display.update()
        clock.tick()
def highscoreliste():
    verbindung=sqlite3.connect("Highscoreliste.db")
    cursor=verbindung.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS highscore(user VARCHAR(255), punkte INT (255)) ")

    einmaleingabe =0
    print("highscore liste gestartet")
    clock=pygame.time.Clock()
    highscorelist_active =True
    if highscorelist_active== True:
        sortiert=cursor.execute("SELECT * from highscore ORDER BY punkte DESC").fetchall()
        print(sortiert)
    while highscorelist_active==True:
        dis.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                highscorelist_active=False
                print("Highscore Screen beendet")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if score1 >sortiert[9][1] and einmaleingabe < 1:
                    print("Highscore saved")
                    cursor.execute("""
                    INSERT INTO highscore VALUES(?,?)
                    """,(playername,score1))
                    verbindung.commit()
                    verbindung.close()
                    einmaleingabe+=1
                else:
                    menue_screen()   
        highscoreanzeige=font_style.render("Highscore Liste",True,black)
        dis.blit(highscoreanzeige,[200,50])

        sortiertanzeige1user=font_style.render("1."+str(sortiert[0][0]),True,yellow)
        dis.blit(sortiertanzeige1user,[150,100])
        sortiertanzeige1score=font_style.render(str(sortiert[0][1]),True,yellow)
        dis.blit(sortiertanzeige1score,[350,100])

        sortiertanzeige2user=font_style.render("2."+str(sortiert[1][0]),True,black)
        dis.blit(sortiertanzeige2user,[150,125])
        sortiertanzeige2score=font_style.render(str(sortiert[1][1]),True,black)
        dis.blit(sortiertanzeige2score,[350,125])

        sortiertanzeige3user=font_style.render("3."+str(sortiert[2][0]),True,black)
        dis.blit(sortiertanzeige3user,[150,150])
        sortiertanzeige3score=font_style.render(str(sortiert[2][1]),True,black)
        dis.blit(sortiertanzeige3score,[350,150])

        sortiertanzeige4user=font_style.render("4."+str(sortiert[3][0]),True,black)
        dis.blit(sortiertanzeige4user,[150,175])
        sortiertanzeige4score=font_style.render(str(sortiert[3][1]),True,black)
        dis.blit(sortiertanzeige4score,[350,175])

        sortiertanzeige5user=font_style.render("5."+str(sortiert[4][0]),True,black)
        dis.blit(sortiertanzeige5user,[150,200])
        sortiertanzeige5score=font_style.render(str(sortiert[4][1]),True,black)
        dis.blit(sortiertanzeige5score,[350,200])

        sortiertanzeige6user=font_style.render("6."+str(sortiert[5][0]),True,black)
        dis.blit(sortiertanzeige6user,[150,225])
        sortiertanzeige6score=font_style.render(str(sortiert[5][1]),True,black)
        dis.blit(sortiertanzeige6score,[350,225])

        sortiertanzeige7user=font_style.render("7."+str(sortiert[6][0]),True,black)
        dis.blit(sortiertanzeige7user,[150,250])
        sortiertanzeige7score=font_style.render(str(sortiert[6][1]),True,black)
        dis.blit(sortiertanzeige7score,[350,250])

        sortiertanzeige8user=font_style.render("8."+str(sortiert[7][0]),True,black)
        dis.blit(sortiertanzeige8user,[150,275])
        sortiertanzeige8score=font_style.render(str(sortiert[7][1]),True,black)
        dis.blit(sortiertanzeige8score,[350,275])

        sortiertanzeige9user=font_style.render("9."+str(sortiert[8][0]),True,black)
        dis.blit(sortiertanzeige9user,[150,300])
        sortiertanzeige9score=font_style.render(str(sortiert[8][1]),True,black)
        dis.blit(sortiertanzeige9score,[350,300])

        sortiertanzeige10user=font_style.render("10."+str(sortiert[9][0]),True,black)
        dis.blit(sortiertanzeige10user,[150,325])
        sortiertanzeige10score=font_style.render(str(sortiert[9][1]),True,black)
        dis.blit(sortiertanzeige10score,[350,325])
        pygame.display.flip()
        clock.tick()
menue_screen()