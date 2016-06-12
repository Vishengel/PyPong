import pygame, sys
from pygame.locals import *
import random

FPS = 60

WINDOWWIDTH = 800
WINDOWHEIGHT = 640
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
PADDLEMOVEMENTSPEED = 8
BALLMOVEMENTSPEED = 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def get_sounds():
  sounds = []
  for x in xrange(1,7):
    sounds.append(pygame.mixer.Sound("./Sounds/noot" + str(x) + ".wav"))

  return sounds


def draw_arena():
  DISPLAYSURF.fill(BLACK)
  #pygame.draw.rect(DISPLAYSURF, WHITE, (0,0), (WINDOWWIDTH, WINDOWHEIGHT), LINETHICKNESS * 2)

  pygame.draw.line(DISPLAYSURF, WHITE, (0,0), (WINDOWWIDTH, 0), 2 * LINETHICKNESS)

  pygame.draw.line(DISPLAYSURF, WHITE, (0,WINDOWHEIGHT), (WINDOWWIDTH, WINDOWHEIGHT), 2 * LINETHICKNESS)

  midline_thickness = LINETHICKNESS / 4
  midline_seg_len = WINDOWHEIGHT / 50
  midline_interval = WINDOWHEIGHT / 100

  for y in xrange(LINETHICKNESS + midline_interval, WINDOWHEIGHT - LINETHICKNESS - midline_interval, midline_seg_len + midline_interval):
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH / 2 - midline_thickness / 2), y), ((WINDOWWIDTH / 2 - midline_thickness / 2), y + midline_seg_len), midline_thickness)

def draw_paddle(paddle):
  if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
    paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
  elif paddle.top < LINETHICKNESS:
    paddle.top = LINETHICKNESS

  pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

def draw_ball(ball):
  pygame.draw.rect(DISPLAYSURF, WHITE, ball)

def move_paddle(keys, paddle1, paddle2):
  if keys[K_w]:
    paddle1.y -= PADDLEMOVEMENTSPEED
  if keys[K_s]:
    paddle1.y += PADDLEMOVEMENTSPEED

  if keys[K_UP]:
    paddle2.y -= PADDLEMOVEMENTSPEED
  if keys[K_DOWN]:
    paddle2.y += PADDLEMOVEMENTSPEED

  return paddle1, paddle2

def move_ball(ball, ball_dir_x, ball_dir_y):
  ball.x += ball_dir_x * BALLMOVEMENTSPEED
  ball.y += ball_dir_y * BALLMOVEMENTSPEED
  return ball

def check_paddle_collision(ball, ball_dir_x, paddle1, paddle2):
  if ball_dir_x == -1 and ball.left < paddle1.right and paddle1.top <= ball.top and paddle1.bottom >= ball.bottom:
    ball_dir_x *= -1
  elif ball_dir_x == 1 and ball.right > paddle2.left and paddle2.top <= ball.top and paddle2.bottom >= ball.bottom:
    ball_dir_x *= -1

  return ball_dir_x

def check_edge_collision(ball, ball_dir_y):
  if ball.top <= LINETHICKNESS or ball.bottom >= (WINDOWHEIGHT - LINETHICKNESS):
    ball_dir_y *= -1

  return ball_dir_y

def update_score(ball, score1, score2, made_goal):
  if ball.left <= 0:
    score2 += 1
    made_goal = True
  elif ball.right >= WINDOWWIDTH:
    score1 += 1
    made_goal = True

  return score1, score2, made_goal

def display_score(score1, score2):
  score1_surf = BASICFONT.render("%s" % score1, True, WHITE)
  score1_rect = score1_surf.get_rect()
  score1_rect.topleft = (WINDOWWIDTH / 4 - score1_rect.width / 2, WINDOWHEIGHT / 20)

  score2_surf = BASICFONT.render("%s" % score2, True, WHITE)
  score2_rect = score2_surf.get_rect()
  score2_rect.topleft = (3 * WINDOWWIDTH / 4 - score2_rect.width / 2, WINDOWHEIGHT / 20)

  DISPLAYSURF.blit(score1_surf, score1_rect)
  DISPLAYSURF.blit(score2_surf, score2_rect)

def main():
  pygame.init()
  pygame.mixer.init()
  global DISPLAYSURF
  global BASICFONTSIZE
  global BASICFONT

  DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
  pygame.display.set_caption("Pongu")
  BASICFONTSIZE = 120
  BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

  sounds = get_sounds()

  FPSCLOCK = pygame.time.Clock()

  ball_x = WINDOWWIDTH / 2 - LINETHICKNESS / 2
  ball_y = WINDOWHEIGHT / 2 - LINETHICKNESS / 2

  p1_position = WINDOWHEIGHT / 2 - PADDLESIZE / 2
  p2_position =  WINDOWHEIGHT / 2 - PADDLESIZE / 2

  paddle1 = pygame.Rect(PADDLEOFFSET, p1_position, LINETHICKNESS, PADDLESIZE)
  paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, p2_position, LINETHICKNESS, PADDLESIZE)
  ball = pygame.Rect(ball_x, ball_y, LINETHICKNESS, LINETHICKNESS)

  ball_dir_x = -1
  ball_dir_y = -1

  draw_arena()
  draw_paddle(paddle1)
  draw_paddle(paddle2)
  draw_ball(ball)

  score1 = 0
  score2 = 0

  made_goal = False

  #airhorn = pygame.mixer.Sound("./airhorn.wav")

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      #if event.type == KEYUP:
        #paddle1 = move_paddle(event.key, paddle1)

    draw_arena()
    draw_paddle(paddle1)
    draw_paddle(paddle2)
    draw_ball(ball)

    keys = pygame.key.get_pressed()
    paddle1, paddle2 = move_paddle(keys, paddle1, paddle2)

    ball = move_ball(ball, ball_dir_x, ball_dir_y)
    ball_dir_x = check_paddle_collision(ball, ball_dir_x, paddle1, paddle2)
    ball_dir_y = check_edge_collision(ball, ball_dir_y)

    score1, score2, made_goal = update_score(ball, score1, score2, made_goal)

    if made_goal:
      ball = pygame.Rect(ball_x, ball_y, LINETHICKNESS, LINETHICKNESS)
      random.choice(sounds).play()
      #airhorn.play()

    made_goal = False

    display_score(score1, score2)

    pygame.display.update()
    FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
