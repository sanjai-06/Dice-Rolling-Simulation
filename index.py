import pygame
import time

from button import Button
from const import POINTS_TO_WIN, SCORE_STOP
from const import TURN_HUMAN, TURN_BOT
from const import FONT_SIZE, WIN_FONT_SIZE
from mechanics import roll_dice


import random
from datetime import datetime


random.seed(time.time())



WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60



BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


pygame.init()


screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Dice Roll Game')
clock = pygame.time.Clock()



def print_human_stats(human_total, human_turn_score, screen, font):
    text = f'HUMAN\nTotal score: {human_total}\nTurn score: {human_turn_score}'
    offset = 0

    for line in text.split('\n'):
        rendered = font.render(line, 1, BLACK)
        screen.blit(rendered, (50, 100+4*offset))
        offset += FONT_SIZE




def print_bot_stats(bot_total, bot_turn_score, screen, font):
    text = f'BOT\nTotal score: {bot_total}\nTurn score: {bot_turn_score}'
    offset = 0

    for line in text.split('\n'):
        rendered = font.render(line, 1, BLACK)
        screen.blit(rendered, (600, 100+4*offset))
        offset += FONT_SIZE



def load_dice_images(path):
    dct = dict()
    for i in range(1, 7):
        img = pygame.image.load(f'{path}dice{i}.png').convert()

        dct[i] = img
    
    return dct





def game():
    
    winner_font = pygame.font.Font('resources/font/consola.ttf', 40)
    status_font = pygame.font.Font('resources/font/consola.ttf', FONT_SIZE)
    dice_imgs = load_dice_images('resources/img/')

    
    human_total, bot_total = 0, 0
    human_turn_score, bot_turn_score = 0, 0 
    turn = TURN_HUMAN
    current_dice = 1

    
    bot_times_thrown = 0  

    
    button_roll = Button(300, 400, 200, 50, color=GREEN, text='Roll')
    button_hold = Button(300, 500, 200, 50, color=BLUE, text='Hold')
    
    
    running = True
    while running:
       
        screen.fill(WHITE)
        
        button_roll.draw(screen)
        button_hold.draw(screen)
       
        print_human_stats(human_total, human_turn_score, screen, status_font)
        print_bot_stats(bot_total, bot_turn_score, screen, status_font)
        
      
        
        time.sleep(0.4) 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if turn == TURN_HUMAN:   
                
                    if button_roll.isOver(event.pos):
                       
                        score = roll_dice()  
                        human_turn_score += score   
                        current_dice = score       

                        if score == SCORE_STOP:   
                            human_turn_score = 0  
                            screen.blit(dice_imgs[current_dice], (350, 100))
                            pygame.display.flip()
                            time.sleep(0.5)
                            turn = TURN_BOT       

                    
                    if button_hold.isOver(event.pos):
                        
                        human_total += human_turn_score  
                        human_turn_score = 0      
                        turn = TURN_BOT  

       
        if turn == TURN_BOT:  
            
           
            difference = bot_total - human_total

            
            if difference >= -30:   
                if bot_turn_score < 20 and bot_times_thrown < 4: 
                    score = roll_dice()   
                    bot_times_thrown += 1  
                    bot_turn_score += score  
                    current_dice = score    

                    
                    if score == SCORE_STOP:
                        bot_turn_score = 0   
                        bot_times_thrown = 0   
                        turn = TURN_HUMAN   

                
                else:
                    bot_total += bot_turn_score  
                    bot_turn_score = 0   
                    bot_times_thrown = 0  
                    turn = TURN_HUMAN   

            
            else:
                if bot_turn_score < human_total/2 and bot_times_thrown < 6:
                    score = roll_dice()   
                    bot_times_thrown += 1  
                    bot_turn_score += score  
                    current_dice = score

                    
                    if score == SCORE_STOP:
                        bot_turn_score = 0 
                        bot_times_thrown = 0
                        turn = TURN_HUMAN
                
                
                else:
                    bot_total += bot_turn_score  
                    bot_turn_score = 0  
                    bot_times_thrown = 0  
                    turn = TURN_HUMAN   

            
        screen.blit(dice_imgs[current_dice], (350, 100))
        
        

        
        if human_total >= POINTS_TO_WIN:
            turn = 'no one'
            text = 'Winner is HUMAN'
            rendered = winner_font.render(text, 1, BLACK)
            screen.blit(rendered, (225, 300))
        elif bot_total + bot_turn_score >= POINTS_TO_WIN:
            bot_total += bot_turn_score
            bot_turn_score = 0
            turn = 'no one'
            text = 'Winner is BOT'
            rendered = winner_font.render(text, 1, BLACK)
            screen.blit(rendered, (225, 300))





        clock.tick(FPS)
        pygame.display.flip()



game()
