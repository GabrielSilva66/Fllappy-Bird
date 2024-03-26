import pygame
import os

# Loads the base image and scales it
IMG_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png"))) 

# Class representing the base in the game
class Base:
  SPEED = 5               # Speed at which the base moves to the left
  WIDTH = IMG_BASE.get_width()  # Width of the base image
  IMG = IMG_BASE          # Image of the base

  def __init__(self, y):
    # Initializes a base object
    self.y = y         # Y-coordinate of the base
    self.x1 = 0        # X-coordinate of the first base
    self.x2 = self.WIDTH  # X-coordinate of the second base, starts at the width of the base image

  def move(self):
    # Moves the base to the left
    self.x1 -= self.SPEED 
    self.x2 -= self.SPEED

    # Resets the position of the bases when they go off-screen
    if(self.x1 + self.WIDTH < 0):
      self.x1 = self.x2 + self.WIDTH
    if(self.x2 + self.WIDTH < 0):
      self.x2 = self.x1 + self.WIDTH

  def draw(self, picture):
    # Draws the bases on the screen
    picture.blit(self.IMG, (self.x1, self.y))  # Draws the first base
    picture.blit(self.IMG, (self.x2, self.y))  # Draws the second base 
