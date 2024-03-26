import pygame
import os
IMG_PLAY = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "play.png")), (200, 200))

IMG_MOUSE = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "mouse.png" )), (100, 100)) 

class Play:
  IMG =IMG_PLAY
  
  def __init__(self):
    self.x = 150
    self.y = 200
    self.width, self.height = self.IMG.get_size()
  def draw(self, picture):
    # Draws the bases on the screen
    picture.blit(self.IMG, (self.x, self.y))  # Draws the first base

  def play_collide(self, mouse_x, mouse_y, mouse):
    mouse_x, mouse_y = mouse.x, mouse.y
    if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
      return True
    return False




class Mouse:
  IMG =IMG_MOUSE

  def __init__(self, x = 200, y = 400):
    self.x = x
    self.y = y
  
  def draw(self, picture):
    # Draws the bases on the screen
    picture.blit(self.IMG, (self.x, self.y))  # Draws the first base
  
  def get_mask(self):
    # Retorna a máscara de colisão do mouse
    return pygame.mask.from_surface(self.IMG)

