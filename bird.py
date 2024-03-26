import pygame
import os

# Load bird images and scale them
IMG_BIRD = [
  pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
  pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png" ))),
  pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))) 
]

class Bird:
  # Class variable to store bird images
  IMG = IMG_BIRD

  # Parameters for rotation
  ROTATE_MAX = 25
  ROTATE_SPEED = 20
  ANIMATION_TIME = 5

  def __init__(self, x, y):
    # Initialize the Bird object
    self.x = x              # x-coordinate position
    self.y = y              # y-coordinate position
    self.angle = 0          # Angle of rotation for the bird
    self.speed = 0          # Vertical speed of the bird
    self.height = self.y    # Initial height of the bird
    self.time = 0           # Time since last jump
    self.count_img = 0      # Counter for bird animation frames
    self.img = self.IMG[0]  # Initial bird image

  def jump(self):
    # Make the bird jump
    self.speed = -10.5      # Vertical velocity
    self.time = 0           # Reset time since last jump
    self.height = self.y    # Update the initial height
  
  def move(self):
    # Move the bird
    # Calculate vertical displacement using the "suvat" equations
    self.time += 1
    move = 1.5 * (self.time**2) + self.speed * self.time

    # Limit the maximum vertical speed and apply displacement
    if move > 16:
      move = 16
    elif move < 0:
      move -= 2
    self.y += move

    # Adjust the bird's angle of rotation
    if move < 0 or self.y < (self.height + 30):
      if self.angle < self.ROTATE_MAX:
        self.angle = self.ROTATE_MAX
    else:
      if self.angle > -90:
        self.angle -= self.ROTATE_SPEED + 20
  
  def draw(self, picture):
    # Draw the bird on the screen
    self.count_img += 1

    # Update bird image for animation
    if self.count_img < self.ANIMATION_TIME:
      self.img = self.IMG[0]
    elif self.count_img < self.ANIMATION_TIME * 2:
      self.img = self.IMG[1]
    elif self.count_img < self.ANIMATION_TIME * 3:
      self.img =  self.IMG[2]
    elif self.count_img < self.ANIMATION_TIME * 4:
      self.img =  self.IMG[1]
    elif self.count_img >= self.ANIMATION_TIME * 4 + 1:
      self.img =  self.IMG[0]
      self.count_img = 0

    # Apply special animation if the bird is falling
    if self.angle <= -80:
      self.img = self.IMG[1]
      self.count_img = self.ANIMATION_TIME * 2

    # Draw the rotated bird image on the screen
    image_rotate = pygame.transform.rotate(self.img, self.angle)
    pos_center_img = self.img.get_rect(topleft=(self.x, self.y)).center
    rectangle = image_rotate.get_rect(center=pos_center_img)
    picture.blit(image_rotate, rectangle.topleft)

  def get_mask(self):
    # Get the collision mask for the bird
    return pygame.mask.from_surface(self.img)
