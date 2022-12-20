import pygame
import sys
import random

""" 
import pygame - This provides access to the pygame framework and imports all functions of pygame.

pygame.init() - This is used to initialize all the required module of the pygame.

pygame.display.set_mode((width, height)) - This is used to display a window of the desired size. 
The return value is a Surface object which is the object where we will perform graphical operations.

pygame.event.get()- This is used to empty the event queue. If we do not call this, the window messages will 
start to pile up and, the game will become unresponsive in the opinion of the operating system.

pygame.QUIT - This is used to terminate the event when we click on the close button at the corner of the window.

The pygame blit is the process to render the game object onto the surface, and this process is called blitting. 
When we create the game object, we need to render it. If we don't render the game objects and run the program, 
then it will give the black window as an output.

Blitting is one of the slowest operations in any game so, we need to be careful to not to blit much onto the screen in every frame. 
The primary function used in blitting is blit()

pygame.Surface.convert_alpha: It creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format with per-pixel alpha. If no surface is given, the new surface will be optimized for blitting to the current display.




"""

def game_floor():
    screen.blit(floor_base,(floor_x_pos,600))
    screen.blit(floor_base,(floor_x_pos+400,600))
    # print("Floor is Building")

def check_collision(pipes):
    #check collison with pipes
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            return False
    #check floor is not hit
    if bird_rect.top<=-150 or bird_rect.bottom>=600:
        die_sound.play()
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height) #replace with a random
    top_pipe=pipe_surface.get_rect(midbottom=(399,random_pipe_pos-200))
    bottom_pipe=pipe_surface.get_rect(midtop=(399,random_pipe_pos))
    return bottom_pipe,top_pipe
 
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=625:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
    
# import pygame - This provides access to the pygame framework and imports all functions of pygame.
pygame.init()
clock=pygame.time.Clock()

#vars(Variables)
gravity=0.25
bird_movement=0
screen=pygame.display.set_mode((400,650))

background= pygame.image.load("Flappy_Bird_Game/sprites/background-day.png").convert()
background=pygame.transform.scale(background,(400,650)) #Scales the background to fit the assigned window

bird=pygame.image.load("Flappy_Bird_Game/sprites/bluebird-midflap.png").convert_alpha()# Convert means converting   it into a string
# bird=pygame.transform.scale2x(bird)
bird_rect=bird.get_rect(center=(100,250)) # To detect collisons

floor_base = pygame.image.load("Flappy_Bird_Game/sprites/base.png").convert()#SInce it is not a transparent image
floor_base=pygame.transform.scale2x(floor_base)
floor_x_pos=0

message = pygame.image.load("Flappy_Bird_Game/sprites/message.png").convert_alpha()#SInce it is not a transparent image
message=pygame.transform.scale2x(message)
game_over_react= message.get_rect(center=(200,325))

#building pipes
pipe_surface= pygame.image.load("Flappy_Bird_Game/sprites/pipe-green.png")
pipe_surface=pygame.transform.scale(pipe_surface,(50,500))
pipe_list=[]
pipe_height=[280,350,450]

SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200) #This means spawning the pipe every 1200 frames

flap_sound=pygame.mixer.Sound('Flappy_Bird_Game/flappy_bird_assets/audio/wing.wav')
die_sound=pygame.mixer.Sound('Flappy_Bird_Game/flappy_bird_assets/audio/die.wav')

game_active=True
while True:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active:
                bird_movement=0
                bird_movement-=8
                flap_sound.play()
            if event.key==pygame.K_SPACE and game_active==False:
                bird_rect.center=(100,325)
                bird_movement=0
                pipe_list.clear()
                game_active=True
        if event.type==SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe()) #append does not work
            print(pipe_list)
            # print("Pipe Created")
        

    screen.blit(background,(0,0)) # Adds the image to our full game (0,0) symbolises the top left hand corner
    
    if game_active:
        bird_movement+=gravity
        bird_rect.centery+=bird_movement
        
        screen.blit(bird,bird_rect) # Adds the image to our full game (0,0) symbolises the top left hand corner
        
        #Draw pipes
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        # Check for Collision
        game_active=check_collision(pipe_list)
    else:
        screen.blit(message,game_over_react)
    #Create Floor
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos<=-400:
        floor_x_pos=0
        
    pygame.display.update()
    clock.tick(120)# Added to slow down the function