import pygame
import os
import random

PICTURE_WIDHT = 500
PICTURE_HEIGHT = 800

IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png" ))) 
IMG_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png"))) 
IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) 
IMG_BIRD = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
  pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png" ))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))) 
]

pygame.font.init()
FONT_POINT = pygame.font.SysFont('arial', 50)

class Bird:
  IMG = IMG_BIRD

  # rotação
  ROTATE_MAX = 25
  ROTATE_SPEED = 20
  ANIMATION_TIME = 5

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.angle = 0
    self.speed = 0
    self.height = self.y
    self.time = 0
    self.count_img = 0
    self.img = self.IMG[0]

  def jump(self):
    self.speed = -10.5
    self.time = 0
    self.height = self.y
  
  def move(self):
    #Calcular o deslocamneto
    self.time += 1
    move = 1.5 * (self.time**2) + self.speed * self.time

    #restringei o deslocamento
    if move > 16: move = 16
    elif move < 0: move -= 2
    self.y += move

    #Angulo do pássaro
    if(move < 0 or self.y < (self.height + 50)):
      if(self.angle < self.ROTATE_MAX):
        self.angle = self.ROTATE_MAX
    else:
      if(self.angle < -90):
        self.angle -= self.ROTATE_SPEED
  
  def draw(self, picture):
    #definição e qual imagem usar do pasaro

    self.count_img += 1

    if(self.count_img < self.ANIMATION_TIME ):
      self.img = self.IMG[0]
    elif(self.count_img < self.ANIMATION_TIME*2):
      self.img = self.IMG[1]
    elif(self.count_img < self.ANIMATION_TIME*3):
      self.img =  self.IMG[2]
    elif(self.count_img < self.ANIMATION_TIME*4):
      self.img =  self.IMG[1]
    elif(self.count_img >= self.ANIMATION_TIME*4+1):
      self.img =  self.IMG[0]
      self.count_img = 0

  
    # se o passaro estiver caindo, não pode bater asa
    if(self.angle <= -80):
      self.img = self.IMG[1]
      self.count_img = self.ANIMATION_TIME*2

    #desenhar imagem
    image_rotate = pygame.transform.rotate(self.img, self.angle)
    pos_center_img = self.img.get_rect(topleft=(self.x, self.y)).center
    rectangle = image_rotate.get_rect(center=pos_center_img)
    picture.blit(image_rotate, rectangle.topleft)

  def get_mask(self):
    return pygame.mask.from_surface(self.img)



class Pipe:
  DISTANCE = 200
  SPEED = 5

  def __init__(self, x):
    self.x = x
    self.heigt = 0
    self.pos_base = 0
    self.pos_top = 0
    self.PIPE_BASE = IMG_PIPE
    self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, False, True)
    self.pass_pipe = False
    self.define_height()

  def define_height(self):
    self.heigt = random.randrange(50, 450)
    self.pos_top = self.heigt - self.PIPE_TOP.get_height()
    self.pos_base = self.heigt + self.DISTANCE

  def move(self):
    self.x -= self.SPEED
  
  def draw(self, picture):
    picture.blit(self.PIPE_TOP, (self.x, self.pos_top))
    picture.blit(self.PIPE_BASE, (self.x, self.pos_base))

  def collide(self, bird):
    bird_mask = bird.get_mask()
    top_mask = pygame.mask.from_surface(self.PIPE_TOP)
    base_mask = pygame.mask.from_surface(self.PIPE_BASE)
    
    distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
    distance_base = (self.x - bird.x, self.pos_base - round(bird.y))

    top_point = bird_mask.overlap(top_mask, distance_top)
    base_point = bird_mask.overlap(base_mask, distance_base)

    if(base_point or top_point):
      return True
    else:
      return False


class Base:
  SPEED = 5
  WIDTH = IMG_BASE.get_width()
  IMG = IMG_BASE

  def __init__(self, y):
    self.y = y
    self.x1 = 0
    self.x2 = self.WIDTH

  def move(self):
    self.x1 -= self.SPEED 
    self.x2 -= self.SPEED

    if(self.x1 + self.WIDTH < 0):
      self.x1 = self.x2 + self.WIDTH
    if(self.x2 + self.WIDTH < 0):
      self.x2 = self.x1 + self.WIDTH

  def draw(self, picture):
    picture.blit(self.IMG, (self.x1, self.y))
    picture.blit(self.IMG, (self.x2, self.y))


def draw_picture(picture, birds, pipes, base, points):
  picture.blit(IMG_BACKGROUND, (0,0))

  for bird in birds:
    bird.draw(picture)
  
  for pipe in pipes:
    pipe.draw(picture)

  text = FONT_POINT.render(f"Points: {points}", 1, (255,255,255))
  picture.blit(text, (PICTURE_WIDHT - 10 - text.get_width(), 10))
  base.draw(picture)

  pygame.display.update()





    

def main():
  birds = [Bird(230, 350)]
  base = Base(730)
  pipes = [Pipe(700)]
  picture = pygame.display.set_mode((PICTURE_WIDHT, PICTURE_HEIGHT))
  points = 0
  clock = pygame.time.Clock()
  end_game = False


  while(not end_game):
    clock.tick(30)

    for event in pygame.event.get():
      if(event.type == pygame.KEYDOWN):
        if(event.key == pygame.K_SPACE):
          for bird in  birds:
            bird.jump()
      if (event.type == pygame.QUIT):
        end_game == True
        pygame.quit()
        quit()
    
    for bird in birds:
      bird.move()
    base.move()

    add_pipe = False
    remove_pipes = []
    for pipe in pipes:
      for i, bird in enumerate(birds):
        if(pipe.collide(bird)):
          bird.pop(i)
        if(not pipe.pass_pipe and bird.x > pipe.x):
          pipe.pass_pipe = True
          add_pipe = True
      pipe.move()
      if(pipe.x + pipe.PIPE_TOP.get_width() < 0):
        remove_pipes.append(pipe) 

    if(add_pipe):
      points += 1
      pipes.append(Pipe(600))
    for pipe in remove_pipes:
      pipes.remove(pipe)

    for i, bird in enumerate(birds):
      if(bird.y + bird.img.get_height() > base.y or bird.y < 0):
        birds.pop(i)
        
    draw_picture(picture, birds, pipes, base, points)



if __name__ == "__main__":
  main()  # Chama a função principal se o script for executado diretamente



