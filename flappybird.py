"""
Flappy Bird Game
Author: Gabriel Victor da Silva
Date: 25/03/2024
"""
import pygame
import os

from pipe import Pipe
from base import Base
from bird import Bird
from begin import Play
from begin import Mouse

# Definition of the game image dimensions
PICTURE_WIDHT = 500
PICTURE_HEIGHT = 800

# Initializes the font to display points on the screen
pygame.font.init()
FONT_POINT = pygame.font.SysFont('arial', 50)

# Loads and resizes the background image of the game
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png" ))) 


# Function to draw the game image, birds, pipes, base, and points on the screen
def draw_picture(picture, birds, pipes, base, points):
  picture.blit(IMG_BACKGROUND, (0,0))  # Draws the game background

  # Draws the birds on the screen
  for bird in birds:
    bird.draw(picture)
  
  # Draws the pipes on the screen
  for pipe in pipes:
    pipe.draw(picture)

  # Renders and draws the text of the points on the screen
  text = FONT_POINT.render(f"Points: {points}", 1, (255,255,255))
  picture.blit(text, (PICTURE_WIDHT - 10 - text.get_width(), 10))
  
  # Draws the base on the screen
  base.draw(picture)

  # Updates the screen
  pygame.display.update()

def def_begin(picture):
  play = Play()
  mouse = Mouse()
  end_begin = False
  pygame.display.set_caption("teste")

  while(not end_begin):

    for event in pygame.event.get():
      if(event.type == pygame.QUIT):
        end_begin == True
        pygame.quit()
        quit()
        
      mouse_pos = pygame.mouse.get_pos()
      mouse_x, mouse_y = mouse_pos
      mouse = Mouse(mouse_x-42, mouse_y-30)

      if(play.play_collide(mouse_x-42, mouse_y-30, mouse)):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Verifica se o botão esquerdo foi pressionado)
          end_begin = True

    draw_begin(picture, play, mouse)

def draw_begin(picture, play, mouse):
  picture.blit(IMG_BACKGROUND, (0,0))  # Draws the game background
  base = Base(650)  

  play.draw(picture)
  base.draw(picture)
  mouse.draw(picture)
    

  # Updates the screen
  pygame.display.update()

def reset_game():
  # Reinicializa as variáveis do jogo com seus valores iniciais
  new_bird = Bird(230, 350)   # Cria um novo pássaro na posição inicial
  new_base = Base(650)        # Cria uma nova base na posição inicial
  new_pipe = Pipe(700)        # Cria um novo cano na posição inicial
  return new_bird, new_base, new_pipe




# Main function of the game
def main():
  birds = [Bird(230, 350)]                                            # Creates a bird at the initial position
  base = Base(650)                                                    # Creates the game base
  pipes = [Pipe(700)]                                                 # Creates a pipe at the initial position
  picture = pygame.display.set_mode((PICTURE_WIDHT, PICTURE_HEIGHT))  # Sets up the game screen
  points = 0                                                          # Initializes the player's points
  clock = pygame.time.Clock()                                         # Initializes the game clock
  end_game = False                                                    # Defines the end game condition

  beggining = True

  # Main game loop
  while(not end_game):
    clock.tick(30)  # Limits the game to 30 frames per second

    if(beggining): 
      def_begin(picture) 
      beggining = False

    # Checks pygame events
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):  # Checks if the player closed the game
        end_game == True
        pygame.quit()
        quit()
      if(event.type == pygame.KEYDOWN):  # Checks if the player pressed a key
        if(event.key == pygame.K_SPACE):  # Checks if the player pressed the space key
          for bird in birds:  # Makes the bird jump
            bird.jump()
    
    # Moves the birds
    for bird in birds:
      bird.move()
    
    # Moves the game base
    base.move()

    add_pipe = False        # Variable to add a new pipe
    remove_pipes = []       # List of pipes to remove

    # Moves and checks collision with pipes
    for pipe in pipes:
      for i, bird in enumerate(birds):
        if(pipe.collide(bird)):  # Checks if there was a collision between the bird and the pipe
          birds.pop(i)           # Removes the bird from the game
          birds = [Bird(230, 350)]                                           
          base = Base(650)                                                    
          pipes = [Pipe(700)] 
          beggining = True
          points = 0  


        if(not pipe.pass_pipe and bird.x > pipe.x):  # Checks if the bird passed through the pipe
          pipe.pass_pipe = True
          add_pipe = True
      pipe.move()  # Moves the pipe
      if(pipe.x + pipe.PIPE_TOP.get_width() < 0):  # Removes the pipes that went off-screen
        remove_pipes.append(pipe) 

    # Adds a new pipe to the game
    if(add_pipe):
      points += 1
      pipes.append(Pipe(600))
    
    # Removes the pipes that went off-screen
    for pipe in remove_pipes:
      pipes.remove(pipe)

    # Checks if the bird touched the ground or went off-screen
    for i, bird in enumerate(birds):
      if(bird.y + bird.img.get_height() > base.y):
        birds.pop(i)
        birds = [Bird(230, 350)]                                           
        base = Base(650)                                                    
        pipes = [Pipe(700)] 
        beggining = True
        points = 0  
        
    # Draws the game image
    draw_picture(picture, birds, pipes, base, points)

# Starts the game if the script is executed directly
if __name__ == "__main__":
  main()
