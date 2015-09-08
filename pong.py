#Rice University Introduction to Interactive Programming (python)
#Implementation of classic arcade game Pong
#Produced in codeskulptor and works better in codeskultptor
#Imported simplieguitk to implement GUI components used in codeskulptor

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 700
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT, RIGHT = False, True
ball_vel = [0, 0]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
upkey, downkey = False, False

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[1] = - random.randrange(60, 180)/ 60.0
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/ 60.0
    else:
        ball_vel[0] = - random.randrange(120, 240)/ 60.0
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(random.choice([True, False]))
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
      
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],
                     [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],
                     [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],
                     [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball and determine whether paddle and ball collide    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[0] >= (WIDTH-1)-BALL_RADIUS - PAD_WIDTH: #right
        if abs(paddle2_pos - ball_pos[1]) > HALF_PAD_HEIGHT + BALL_RADIUS/2:		
            spawn_ball(LEFT)
            score1 += 1
        else:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
    
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: #left
        if abs(paddle1_pos - ball_pos[1])> HALF_PAD_HEIGHT + BALL_RADIUS/2:		
            spawn_ball(RIGHT)
            score2 += 1
            return score2
        else:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        
    if ball_pos[1] <= BALL_RADIUS: #up
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS: #down
        ball_vel[1] = - ball_vel[1]   
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    if paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
        
    if paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
   
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], 
                     [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], PAD_WIDTH ,'White') 
    canvas.draw_line([(WIDTH - HALF_PAD_WIDTH), paddle2_pos + HALF_PAD_HEIGHT], 
                     [(WIDTH - HALF_PAD_WIDTH), paddle2_pos - HALF_PAD_HEIGHT], PAD_WIDTH, 'White')
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH*1/4, 80], 50, "Lime")
    canvas.draw_text(str(score2), [WIDTH*3/4, 80], 50, "Magenta")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, downkey, upkey
    if key==simplegui.KEY_MAP["s"]:
        downkey = True
        paddle1_vel = 2
    elif key==simplegui.KEY_MAP["w"]:
        upkey = True
        paddle1_vel = -2
    if key==simplegui.KEY_MAP["down"]:
        downkey = True
        paddle2_vel = 2
    elif key==simplegui.KEY_MAP["up"]:
        upkey = True
        paddle2_vel = -2
def keyup(key):
    global paddle1_vel, paddle2_vel, downkey, upkey
    if key==simplegui.KEY_MAP["s"]:
        downkey = False
        paddle1_vel = 0 if not upkey else -2
    elif key ==simplegui.KEY_MAP["w"]:
        upkey = False
        paddle1_vel = 0 if not downkey else 2
    if key==simplegui.KEY_MAP["down"]:
        downkey = False
        paddle2_vel = 0 if not upkey else -2
    elif key ==simplegui.KEY_MAP["up"]:
        upkey = False
        paddle2_vel = 0 if not downkey else 2
        
def reset():
    new_game()
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", reset)


# start frame
new_game()
frame.start()
reset()
