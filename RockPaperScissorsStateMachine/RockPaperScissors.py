from pygame.locals import *
import pygwidgets, pygame, sys, random


def sanaa():
    return 'بسم الله الرحمان الرحيم والصلاة على رسولنا محمد صلى الله عليه وآله وسلم'


if __name__ == "__main__":
    print(sanaa())


def quit_game():
    pygame.quit()
    sys.exit()


WHITE = (255, 255, 255)
ROCK = 'Rock'
PAPER = 'Paper'
SCISSOR = ' Scissors'

STATE_SPLASH = 'Splash'
STATE_PLAYER_CHOICE = 'PlayerChoice'
STATE_SHOW_RESULTS = 'ShowResults'

WIN_WIDTH = 800
WIN_HEIGHT = 600
BG_COLOUR = (90, 90, 90)
FPS = 30

pygame.init()
pygame.display.set_caption('Rock, Paper, Scissor')
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()

player_score = 0
computer_score = 0
state = STATE_SPLASH

rock_paper_scissor_image = pygwidgets.Image(window, (245, 150), 'images/RPS.png')

# Title Images
rock_title_image = pygwidgets.Image(window, (60, 140), 'images/rock_title.png')
paper_title_image = pygwidgets.Image(window, (300, 55), 'images/paper title.png')
scissors_title_image = pygwidgets.Image(window, (590, 140), 'images/scissor title.png')
choose_button = pygwidgets.Image(window, (210, 450), 'images/choose button.png')

#Button Images
start_button = pygwidgets.CustomButton(window, (280, 420), 'images/startButtonUp.png',
                                       'images/startButtonDown.png', 'images/startButtonHighlight.png')
restart_button = pygwidgets.CustomButton(window, (280, 420), 'images/restartButtonUp.png',
                                         'images/restartButtonDown.png', 'images/restartButtonHighlight.png')
rock_button = pygwidgets.CustomButton(window, (20, 220), 'images/RockDown.png',
                                      'images/RockGray.png', 'images/RockOver.png')
paper_button = pygwidgets.CustomButton(window, (280, 140), 'images/PaperDown.png',
                                       'images/PaperGray.png', 'images/PaperOver.png')
scissors_button = pygwidgets.CustomButton(window, (550, 220), 'images/ScissorsDown.png',
                                          'images/ScissorsGray.png', 'images/ScissorsOver.png')
rps_collection_player = pygwidgets.ImageCollection(window, (50, 92),
                                                   {ROCK: 'images/Rock.png',
                                                    PAPER: 'images/Paper.png',
                                                    SCISSOR: 'images/Scissors.png'}, '')
rps_collection_computer = pygwidgets.ImageCollection(window, (520, 92),
                                                     {ROCK: 'images/Rock.png',
                                                      PAPER: 'images/Paper.png',
                                                      SCISSOR: 'images/Scissors.png'}, '')


result_field = pygwidgets.DisplayText(window, (80, 310), 'Choose!', textColor=WHITE,
                                      width=610, justified='center', fontSize=50)

player_score_counter = pygwidgets.DisplayText(window, (35, 415), f'Player Score:{player_score}',
                                              fontSize=50, textColor=WHITE)
computer_score_counter = pygwidgets.DisplayText(window, (420, 415), f'Computer Score:{computer_score}',
                                                fontSize=50, textColor=WHITE)
message_field = pygwidgets.DisplayText(window, (85, 35), 'Welcome to Rock, Paper, Scissors!',
                                       fontSize=50, textColor=WHITE, width=610, justified='center')

state_player_choice_draw_list = [rock_button, paper_button, scissors_button, choose_button, rock_title_image,
                                 paper_title_image, scissors_title_image]
state_show_results_draw_list = [result_field, restart_button, rps_collection_player, message_field,
                                rps_collection_computer, player_score_counter, computer_score_counter]

# Sounds

tie_sound = pygame.mixer.Sound('sounds/push.wav')
winner_sound = pygame.mixer.Sound('sounds/yay.mp3')
looser_sound = pygame.mixer.Sound('sounds/ooh.mp3')
main_game_sound = pygame.mixer.Sound('sounds/game start.mp3')
main_game_sound.play(-1)

rock_title_image.hide()
paper_title_image.hide()
scissors_title_image.hide()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit_game()

        if state == STATE_SPLASH:
            if start_button.handleEvent(event):
                state = STATE_PLAYER_CHOICE

        elif state == STATE_PLAYER_CHOICE:
            player_choice = ''
            if rock_button.handleEvent(event):
                player_choice = ROCK
                rps_collection_player.replace(ROCK)

            elif paper_button.handleEvent(event):
                player_choice = PAPER
                rps_collection_player.replace(PAPER)

            elif scissors_button.handleEvent(event):
                player_choice = SCISSOR
                rps_collection_player.replace(SCISSOR)

            if player_choice != '':
                computer_choice = random.choice((ROCK, PAPER, SCISSOR))
                rps_collection_computer.replace(computer_choice)

                if player_choice == computer_choice:
                    result_field.setValue('Its a Tie!')
                    tie_sound.play()

                elif player_choice == ROCK and computer_choice == SCISSOR:
                    result_field.setValue('Rock breaks Scissors. You win!')
                    player_score += 1
                    winner_sound.play()

                elif player_choice == SCISSOR and computer_choice == PAPER:
                    result_field.setValue('Scissors cuts paper. You win!')
                    player_score += 1
                    winner_sound.play()

                elif player_choice == PAPER and computer_choice == ROCK:
                    result_field.setValue('Paper wraps paper. You win!')
                    player_score += 1
                    winner_sound.play()

                elif player_choice == PAPER and computer_choice == SCISSOR:
                    result_field.setValue('Scissors cuts paper. You loose!')
                    computer_score += 1
                    looser_sound.play()

                elif player_choice == SCISSOR and computer_choice == ROCK:
                    result_field.setValue('Rock breaks Scissors. You loose!')
                    computer_score += 1
                    looser_sound.play()

                elif player_choice == ROCK and computer_choice == PAPER:
                    result_field.setValue('Paper wraps paper. You loose!')
                    computer_score += 1
                    looser_sound.play()

                player_score_counter.setValue(f'Your Score: {str(player_score)}')
                computer_score_counter.setValue(f'CoMpUtEr Score: {str(computer_score)}')
                state = STATE_SHOW_RESULTS

        elif state == STATE_SHOW_RESULTS:
            if restart_button.handleEvent(event):
                state = STATE_PLAYER_CHOICE
        else:
            raise ValueError(f'Unknown value for state {state}')

    if state == STATE_PLAYER_CHOICE:
        mouse_pos = pygame.mouse.get_pos()
        rock_title_image.show() if rock_button.getRect().collidepoint(mouse_pos) else rock_title_image.hide()
        paper_title_image.show() if paper_button.getRect().collidepoint(mouse_pos) else paper_title_image.hide()
        scissors_title_image.show() if scissors_button.getRect().collidepoint(mouse_pos) else scissors_title_image.hide()

    elif state == STATE_SHOW_RESULTS:
        message_field.setValue('You                           Computer')

    window.fill(BG_COLOUR)

    if state == STATE_SPLASH:
        rock_paper_scissor_image.draw(), start_button.draw(), message_field.draw()

    elif state == STATE_PLAYER_CHOICE:
        for drawing_items in state_player_choice_draw_list:
            drawing_items.draw()
        rock_title_image.draw()
    elif state == STATE_SHOW_RESULTS:
        for drawing_items in state_show_results_draw_list:
            drawing_items.draw()

    pygame.display.update()
    clock.tick(30)
