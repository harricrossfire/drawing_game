# Respective libraries
import pygame, sys

# Init commands
pygame.init()
clock = pygame.time.Clock()

# States
drawing = False
start_pos = None

# This is the game ui
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Line Drawing")
drawing_space = pygame.Surface((700, 500))
drawing_space.fill((255, 255, 255))
current_color_box = pygame.Surface((50, 50))
current_color = (0, 0, 0)
 
# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 50 <= mouse_x <= 750 and 50 <= mouse_y <= 550:
                if drawing == False:
                    drawing = True
                    start_pos = mouse_pos
                elif drawing == True:
                    end_pos = mouse_pos
                    pygame.draw.line(drawing_space, current_color, (start_pos[0]-50, start_pos[1]-50), (end_pos[0]-50, end_pos[1]-50), 3)
                    drawing = False
    screen.fill((200, 200, 200))
    screen.blit(drawing_space, (50, 50))

# After looking up information from pygame documentation and checking code through Gemini, my initial ideas recieved pushback.
# I was able to optimize the preview lines I was looking for by taking a suggestion from Gemini to draw the preview lines on the screen, which will be filled over on each new loop.
# This doesn't happen with the drawing space, however, because you are blitting the altered drawing space each iteration
    if drawing:
        pygame.draw.line(screen, current_color, start_pos, mouse_pos, 3)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()