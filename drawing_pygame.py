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

# Line map
line_map = []

# Circle variables
#circle_x = 400
#circle_y = 50
#circle_radius = 20
#circle_color = (255, 0, 0)
#circle_speed = 1
#circle_falling = True
 
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
def load_line_map():
    try:
        with open("line_map.txt", "r") as file:
            for line in file:
                start_str, end_str, color_str = line.strip().split(";")
                start_coordinates = tuple(map(int, start_str.split(",")))
                end_coordinates = tuple(map(int, end_str.split(",")))
                color = tuple(map(int, color_str.split(",")))
                line_map.append((start_coordinates, end_coordinates, color))
                pygame.draw.line(drawing_space, color, start_coordinates, end_coordinates, 3)
    except FileNotFoundError:
        pass
def save_line_map():
    with open("line_map.txt", "w") as file:
        for line in line_map:
            start_coordinates, end_coordinates, color = line
            file.write(f"{start_coordinates[0]},{start_coordinates[1]};{end_coordinates[0]},{end_coordinates[1]};{color[0]},{color[1]},{color[2]}\n")
load_line_map()
# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_line_map()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 50 <= mouse_x <= 750 and 50 <= mouse_y <= 550:
                if drawing == False:
                    drawing = True
                    start_pos = mouse_pos
                elif drawing == True:
                    end_pos = mouse_pos
                    pygame.draw.line(drawing_space, current_color, (start_pos[0]-50, start_pos[1]-50), (end_pos[0]-50, end_pos[1]-50), 3)
                    new_start_coordinates = (start_pos[0]-50, start_pos[1]-50)
                    new_end_coordinates = (end_pos[0]-50, end_pos[1]-50)
                    line_map.append((new_start_coordinates, new_end_coordinates, current_color))
                    print(line_map)
                    drawing = False
        elif event.type == pygame.KEYDOWN:
            select_color(event.key)
    #if circle_falling:
        #circle_y += circle_speed
        #if circle_y + circle_radius >= 550:
            #circle_y = 550 - circle_radius
            #circle_y = 50
    screen.fill((200, 200, 200))
    screen.blit(drawing_space, (50, 50))
    screen.blit(color_font_surface, (20, 15))
    screen.blit(current_color_box, (200, 17))
    screen.blit(color_directions_surface, (240, 17))
    #pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

# After looking up information from pygame documentation and checking code through Gemini, my initial ideas recieved pushback.
# I was able to optimize the preview lines I was looking for by taking a suggestion from Gemini to draw the preview lines on the screen, which will be filled over on each new loop.
# This doesn't happen with the drawing space, however, because you are blitting the altered drawing space each iteration
    if drawing:
        pygame.draw.line(screen, current_color, start_pos, mouse_pos, 3)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()