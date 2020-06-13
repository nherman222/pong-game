# pong.py
# Author: Nina Herman
# Date: 01/18/19
# Course: CS1
# Purpose: Create a game of pong. (with extra credit)

from cs1lib import *
import random

HEIGHT_WINDOW = 400
WIDTH_WINDOW = 400
HEIGHT_PADDLE = 50
WIDTH_PADDLE = 41
LEFT_INITIAL_Y = 0
PADDLE_MOVE_AMOUNT = 10
LEFT_MOVE_UP = "a"
LEFT_MOVE_DOWN = "z"
RIGHT_MOVE_UP = "k"
RIGHT_MOVE_DOWN = "m"
QUIT = "q"
START_OVER = " "
RADIUS = 10
STOP = 0
COLOR_INCREMENT = 0.3
LEFT_PADDLE = load_image("pingpong.png")
RIGHT_PADDLE = load_image("pingpongright.png")
WIDTH_WALL = 20
HEIGHT_WALL = 60
left_up_pressed = False
left_down_pressed = False
right_up_pressed = False
right_down_pressed = False
current_y_left = LEFT_INITIAL_Y
current_y_right = HEIGHT_WINDOW - HEIGHT_PADDLE
ballx = WIDTH_WINDOW/2
bally = HEIGHT_WINDOW/2
vx = 3
vy = 3
games = 3
color_ball1 = 0
color_ball2 = 0.2
color_ball3 = 0.5
initial = True
wallx = WIDTH_WINDOW/2 - 10
wally = HEIGHT_WINDOW/4 + 200
game_over = False
new_game = False
right = False
left = False
speed = 3

def set_background():
    set_clear_color(.55, .88, .99)
    clear()

def kpress(k):
    global left_up_pressed, left_down_pressed, right_up_pressed, right_down_pressed, new_game

    if k == LEFT_MOVE_UP:
        left_up_pressed = True

    if k == LEFT_MOVE_DOWN:
        left_down_pressed = True

    if k == RIGHT_MOVE_UP:
        right_up_pressed = True

    if k == RIGHT_MOVE_DOWN:
        right_down_pressed = True

    if k == QUIT:
        cs1_quit()

    if k == START_OVER:
        start_over()
        new_game = True

def krelease(k):
    global left_up_pressed, left_down_pressed, right_up_pressed, right_down_pressed

    if k == LEFT_MOVE_UP:
        left_up_pressed = False

    if k == LEFT_MOVE_DOWN:
        left_down_pressed = False

    if k == RIGHT_MOVE_UP:
        right_up_pressed = False

    if k == RIGHT_MOVE_DOWN:
        right_down_pressed = False

def draw_paddles():
    global current_y_left, current_y_right
    set_fill_color(.9, .6, .5)
    disable_stroke()

    draw_image(RIGHT_PADDLE, WIDTH_WINDOW - WIDTH_PADDLE, current_y_right) #fancy paddles
    draw_image(LEFT_PADDLE, LEFT_INITIAL_Y, current_y_left)

def move_paddles():
    global current_y_left, current_y_right, left_up_pressed, left_down_pressed, right_up_pressed, right_down_pressed

    if left_up_pressed and current_y_left != LEFT_INITIAL_Y: #moves left paddle up
        current_y_left = current_y_left - PADDLE_MOVE_AMOUNT
        draw_paddles()

    if left_down_pressed and current_y_left != HEIGHT_WINDOW - HEIGHT_PADDLE: #moves left paddle down
        current_y_left = current_y_left + PADDLE_MOVE_AMOUNT
        draw_paddles()

    if right_up_pressed and current_y_right != LEFT_INITIAL_Y: #moves right paddle up
        current_y_right = current_y_right - PADDLE_MOVE_AMOUNT
        draw_paddles()

    if right_down_pressed and current_y_right != HEIGHT_WINDOW - HEIGHT_PADDLE: #moves right paddle down
        current_y_right = current_y_right + PADDLE_MOVE_AMOUNT
        draw_paddles()
    else:
        draw_paddles()

def draw_ball():
    global ballx, bally, vx, vy, color_ball1, color_ball2, color_ball3
    disable_stroke()
    set_fill_color(color_ball1, color_ball2, color_ball3)
    draw_circle(ballx, bally, RADIUS)

def change_ball_color():
    global color_ball1, color_ball2, color_ball3

    if color_ball1 >= 1 - COLOR_INCREMENT:  #does't allow color values to be greater than 1
        color_ball1 = 0
    if color_ball2 >= 1 - COLOR_INCREMENT:
        color_ball2 = 0
    if color_ball3 >= 1 - COLOR_INCREMENT:
        color_ball3 = 0

    if color_ball1 <= 1 - COLOR_INCREMENT: #if ball hits paddle, switch color of ball
        color_ball1 = color_ball1 + COLOR_INCREMENT
    if color_ball2 <= 1 - COLOR_INCREMENT:
        color_ball2 = color_ball2 + COLOR_INCREMENT
    if color_ball3 <= 1 - COLOR_INCREMENT:
        color_ball3 = color_ball3 + COLOR_INCREMENT

def move_ball():
    global ballx, bally, vx, vy, color_ball1, color_ball2, color_ball3, initial, game_over, left, right, speed

    if ball_hit_left(): #if ball hits paddle, switch x direction of ball
        vx = speed
        if left:
            random_direction = random.randint(0, 1) #randomly chooses if ball will go up or down after hitting paddle
            if random_direction == 0:
                vy = -speed
            else:
                vy = speed

            left = False
            right = True #if ball is traveling right, doesn't change y movement of ball
            change_ball_color()

    if ball_hit_right(): #same thing for right paddle
        vx = -speed
        if right:
            random_direction = random.randint(0, 1)
            if random_direction == 0:
                vy = -speed
            else:
                vy = speed

            right = False
            left = True
            change_ball_color()

    if ball_hit_bottom() or ball_hit_top(): #if ball hits top or bottom wall, switch y direction of ball
        vy = -vy

    if stop_ball() or collision_wall(): #if ball hits vertical wall, game over
        vx = STOP
        vy = STOP
        set_font_size(30)
        enable_stroke()
        draw_text("GAME OVER", WIDTH_WINDOW/4, HEIGHT_WINDOW/2)
        set_font_size(15)
        draw_text("Press space to start new game!", WIDTH_WINDOW/4 - 10, HEIGHT_WINDOW/2 + 30)

    if not initial:
        ballx = ballx + vx #moves ball in x direction
        bally = bally + vy #moves ball in y direction

def ball_hit_right(): #checks if ball hits right paddle
    global ballx, bally, current_y_right

    if ballx + RADIUS/2 > (WIDTH_WINDOW - WIDTH_PADDLE) and (current_y_right < bally + RADIUS) and (bally - RADIUS < current_y_right + HEIGHT_PADDLE):
        return True
    else:
        return False

def ball_hit_left(): #checks if ball hits left paddle
    global ballx, bally, current_y_left

    if ballx - RADIUS/2 < (WIDTH_WINDOW - WIDTH_WINDOW) + WIDTH_PADDLE and (current_y_left < bally + RADIUS) and (bally - RADIUS < current_y_left + HEIGHT_PADDLE):
        return True
    else:
        return False

def ball_hit_bottom(): #checks if ball hits bottom wall
    global bally

    if bally + RADIUS > HEIGHT_WINDOW:
        return True
    else:
        return False

def ball_hit_top(): #checks if ball hits top wall
    global bally

    if bally - RADIUS < HEIGHT_WINDOW - HEIGHT_WINDOW:
        return True
    else:
        return False

def stop_ball():
    global ballx, game_over

    if ballx + RADIUS >= WIDTH_WINDOW: #if ball hits right wall
        return True

    if ballx - RADIUS <= (WIDTH_WINDOW - WIDTH_WINDOW): #if ball hits left wall
        return True

def draw_wall():
    global wallx, wally
    set_fill_color(0.4, 0.2, 0.2)
    draw_rectangle(wallx, wally, WIDTH_WALL, HEIGHT_WALL)

def collision_wall(): #if ball hits brick wall
    global wallx, wally, game_over, initial

    if not initial:
        if wallx <= ballx + RADIUS <= wallx + WIDTH_WALL and wally <= bally + RADIUS and bally - RADIUS <= wally + HEIGHT_WALL: #ball hits brick wall from left
            return True
        elif wallx <= ballx - RADIUS <= wallx + WIDTH_WALL and wally <= bally + RADIUS and bally - RADIUS <= wally + HEIGHT_WALL: #ball hits brick wall from right
            return True
        else:
            return False

def start_over(): #resets variables to start new game
    global current_y_left, current_y_right, ballx, bally, vx, vy, initial, games, speed

    current_y_left = LEFT_INITIAL_Y
    current_y_right = HEIGHT_WINDOW - HEIGHT_PADDLE
    ballx = WIDTH_WINDOW/2
    bally = HEIGHT_WINDOW/2
    initial = True
    games = games + 0.5 #makes speed of ball faster with every new game
    speed = games

def draw_game():

    global initial, vx, vy, ballx, bally, new_game, right, left, speed
    set_background()

    if initial: #first ball movement
        initialx = random.randint(0, 1) #randomly select direction of x movement
        if initialx == 0:
            vx = -speed
        else:
            vx = speed

        if vx > 0 and vy <= 0:
            vy = speed #makes ball travel down if going to the right so its possible to get the ball

        if vx < 0 and vy >= 0:
            vy = -speed #makes ball travel up if going to the left so its possible to get the ball

        initial = False

        if vx > 0:
            right = True
        if vx < 0:
            left = True

    if not new_game: #welcome screen when opening window
        set_font_size(30)
        set_font("Bradley Hand")
        draw_text("WELCOME TO PONG!", WIDTH_WINDOW / 10, HEIGHT_WINDOW / 3)
        draw_text("Press space to start game!", WIDTH_WINDOW / 12, HEIGHT_WINDOW - 150)

    if new_game: #call functions if game is started
        if not (stop_ball() or collision_wall()): #if game over, paddles and wall disappear
            move_paddles()
            draw_wall()

        draw_ball()
        move_ball()


start_graphics(draw_game, key_press=kpress, key_release=krelease)