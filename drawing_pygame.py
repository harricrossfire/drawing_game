# Respective libraries
import pygame, sys

# Init commands
pygame.init()
clock = pygame.time.Clock()

# States
drawing = False
start_pos = None

# Color options (I eventually want to make this more rubust, but we're going to stick to primary colors because it's like 12:00 and my wife wants to watch the Amazing Digital Circus with me).
color_options = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]

# This is the game ui
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Line Drawing Game")
color_font = pygame.font.Font(None, 36)
color_font_surface = color_font.render("Current Color:", True, (0, 0, 0))
color_directions_font = pygame.font.Font(None, 24)
color_directions_surface = color_directions_font.render("(Press Z to cycle previous color, X to cycle next color)", True, (0, 0, 0))
drawing_space = pygame.Surface((700, 500))
drawing_space.fill((255, 255, 255))
current_color_box = pygame.Surface((20, 20))
current_color = color_options[0]
current_color_box.fill(current_color)
 
# Color selection function
def select_color(key):
    global current_color
    current_color_index = color_options.index(current_color)
    if key == pygame.K_x:
        if current_color_index == len(color_options) - 1:
            current_color = color_options[0]
        else:
            current_color = color_options[current_color_index + 1]
    elif key == pygame.K_z:
        if current_color_index == 0:
            current_color = color_options[len(color_options) - 1]
        else:
            current_color = color_options[current_color_index - 1]
    current_color_box.fill(current_color)
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
        elif event.type == pygame.KEYDOWN:
            select_color(event.key)
    screen.fill((200, 200, 200))
    screen.blit(drawing_space, (50, 50))
    screen.blit(color_font_surface, (20, 15))
    screen.blit(current_color_box, (200, 17))
    screen.blit(color_directions_surface, (240, 17))

# After looking up information from pygame documentation and checking code through Gemini, my initial ideas recieved pushback.
# I was able to optimize the preview lines I was looking for by taking a suggestion from Gemini to draw the preview lines on the screen, which will be filled over on each new loop.
# This doesn't happen with the drawing space, however, because you are blitting the altered drawing space each iteration
    if drawing:
        pygame.draw.line(screen, current_color, start_pos, mouse_pos, 3)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()