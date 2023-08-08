# Wordle game
import pygame
import random

# Initialize + SetUp
pygame.init()
screen_width = 540
screen_height = 730
screen = pygame.display.set_mode([screen_width, screen_height])
base_font = pygame.font.Font(None, 100)
pygame.display.set_caption("Tahasin Shadat - Wordle")
user_texts = [''] * 30
guessed_words = []
current_input_rect = 0
letters_typed = 0

# Parse words into dictionary
word_dictionary = {}
with open("words.txt", "r") as file:
    word_list = file.read().splitlines()

for word in word_list:
    word_dictionary[word] = word

random_word = random.choice(word_list)
guesses = 6
global win 
win = False
guessed_letters = [
    [],
    [],
    [],
    [],
    [],
    []
]
green_positions = []
yellow_positions = []
gray_positions = []

def create_input_rect(x, y, size, color, border_color, border_width):
    border_rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, border_color, border_rect)

    input_rect = pygame.Rect(x + border_width, y + border_width, size - 2 * border_width, size - 2 * border_width)
    pygame.draw.rect(screen, color, input_rect)

    return input_rect

def create_board(square_size, border_size, current_row):
    square_color = 'white'
    border_color = 'black'
    start_x = 50
    start_y = 115
    gap = 10
    input_rects = []
    for r in range(6):
        for c in range(5):

            if r <= current_row:  # Only color the current row and previous rows
                if [r, c] in green_positions:
                    square_color = 'green'
                    border_color = 'green'
                elif [r, c] in yellow_positions:
                    square_color = 'yellow'
                    border_color = 'yellow'
                elif [r, c] in gray_positions:
                    square_color = 'gray'
                    border_color = 'gray'
                else:
                    square_color = 'white'
                    border_color = 'black'
            else:
                square_color = 'white'
                border_color = 'black'

            input_rect = create_input_rect(
                start_x,
                start_y,
                square_size,
                square_color,
                border_color,
                border_size
            )
            input_rects.append(input_rect)
            start_x += square_size + gap
        start_y += square_size + gap
        start_x = 50
    
    return input_rects

def is_row_filled(row):
    start_index = 5 * (row - 1)
    end_index = start_index + 5
    for i in range(start_index, end_index):
        if len(user_texts[i]) != 1:
            return False
    return True

def addGuessedWord(guessed_word):
    if len(guessed_words) < 6:
        guessed_words.append(guessed_word)

def storeGuessedWord(row):
    start_index = 5 * (row - 1)
    end_index = start_index + 5
    guessed_word = ''
    for i in range(start_index, end_index):
        guessed_word += user_texts[i]
    addGuessedWord(guessed_word)

def checkWord(guess, row):    
    # guessed_letters = []
    global green_positions, yellow_positions, gray_positions, win
    
    # for i in range(5):
    #     if guess[i] in random_word:
    #         guessed_letters[row-1].append(guess[i])

    if guess == random_word:
        win = True

    for i in range(5):
        if guess[i] == random_word[i]:
            green_positions.append([row - 1, i])
        elif guess[i] in random_word:
            yellow_positions.append([row - 1, i])
        else:
            gray_positions.append([row - 1, i])

def show_popup_message(message, duration=1000):
    font = pygame.font.Font(None, 40)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    # Create a rectangle for the background
    rect_width = text.get_width() + 20
    rect_height = text.get_height() + 20
    rect = pygame.Rect(
        screen_width // 2 - rect_width // 2,
        screen_height // 2 - rect_height // 2,
        rect_width,
        rect_height,
    )
    pygame.draw.rect(screen, (255, 255, 255), rect)  # Draw the black rectangle
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(duration)

def name_and_tracker(guesses):

    base_font = pygame.font.Font(None, 75)
    text_surface = base_font.render('Wordle', True, 'black')
    screen.blit(text_surface, (185, 20))

    base_font = pygame.font.Font(None, 35)
    text_surface = base_font.render('By: Tahasin Shadat', True, 'black')
    screen.blit(text_surface, (155, 70))

    base_font = pygame.font.Font(None, 50)
    text_surface = base_font.render('Attempts: ' + str(guesses), True, 'black')
    screen.blit(text_surface, (175, 675))

active = True
row = 1
input_rects = create_board(80, 5, row - 1)
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(user_texts[current_input_rect]) > 0:
                    user_texts[current_input_rect] = user_texts[current_input_rect][:-1]
                elif current_input_rect % 5 != 0:
                    current_input_rect -= 1
                    user_texts[current_input_rect] = user_texts[current_input_rect][:-1]

            else:
                # Check if the event is a letter (A-Z or a-z)
                if event.unicode.isalpha() and len(user_texts[current_input_rect]) < 1:
                    user_texts[current_input_rect] += event.unicode

                if len(user_texts[current_input_rect]) == 1:
                    current_input_rect += 1
                    if current_input_rect >= (5 * row):
                        current_input_rect = 5 * row - 1

            if is_row_filled(row) and event.key == pygame.K_RETURN:
                guesses -= 1
                enter_pressed = True
                storeGuessedWord(row)
                checkWord(guessed_words[row-1], row)

                if win == True:
                    show_popup_message('You guessed the word!', 10000)
                    running = False
                
                else:
                    if row != 6:
                        row += 1
                    # print(guessed_words)

    screen.fill((255, 246, 237))

    create_board(80, 5, row - 1)

    for i, text in enumerate(user_texts):
        upper_user_text = text.upper()
        text_surface = base_font.render(upper_user_text, True, 'black')

        if i == current_input_rect:
            pygame.draw.rect(screen, pygame.Color('lightskyblue3'), input_rects[i])

        screen.blit(text_surface, (input_rects[i].x + 10, input_rects[i].y + 5))

    name_and_tracker(guesses)

    if guesses == 0 and not win:
        show_popup_message(f'You Lost, the word was {random_word}!', 10000)
        running = False

    pygame.display.update()

pygame.quit()
