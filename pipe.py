import pygame
import random
import os

# Loads the pipe image and scales it
IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) 

# Class representing the pipes in the game
class Pipe:
  DISTANCE = 200  # Distance between pipes
  SPEED = 5       # Speed at which pipes move to the left

  def __init__(self, x):
    # Initializes a pipe object
    self.x = x             # X-coordinate of the pipe
    self.heigt = 0         # Height of the pipe
    self.pos_base = 0      # Position of the base of the pipe
    self.pos_top = 0       # Position of the top of the pipe
    self.PIPE_BASE = IMG_PIPE  # Image of the base of the pipe
    self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, False, True)  # Image of the top of the pipe
    self.pass_pipe = False  # Flag indicating if a bird passed through the pipe
    self.define_height()    # Defines the height of the pipe

  def define_height(self):
    # Defines a random height for the pipe
    self.heigt = random.randrange(50, 450)
    self.pos_top = self.heigt - self.PIPE_TOP.get_height()  # Calculates the position of the top of the pipe
    self.pos_base = self.heigt + self.DISTANCE             # Calculates the position of the base of the pipe

  def move(self):
    # Moves the pipe to the left
    self.x -= self.SPEED
  
  def draw(self, picture):
    # Draws the pipe on the screen
    picture.blit(self.PIPE_TOP, (self.x, self.pos_top))   # Draws the top part of the pipe
    picture.blit(self.PIPE_BASE, (self.x, self.pos_base)) # Draws the base part of the pipe

  def collide(self, bird):
    # Checks for collision between a bird and the pipe
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
