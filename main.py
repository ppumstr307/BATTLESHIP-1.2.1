import pygame
import asyncio

# Colors
background_colour =(255,255,255)#(40,194,199)
col = 'black'
color = (219, 112, 147)
color_safe = (146, 179, 240)


# Initializing Pygame
pygame.init()
screen = pygame.display.set_mode((1250,650+25+10)) 
pygame.display.set_caption('Battleship Simulator') 
screen.fill(background_colour) 

font_big = pygame.font.Font('Zector.ttf',75)
font_small = pygame.font.Font('Zector.ttf',25)
header = font_big.render('BATTLESHIP SIMULATOR',True,'black')
font = pygame.font.Font('Zector.ttf', 25)
fonta = pygame.font.Font('Zector.ttf',40)

# Variables
click = 0
info_click = 0


# Drag Variables
rotation_angle = 0
p1_ship_not_placed = True
p2_ship_not_placed = True
show_img = False

cube_size = 50
grid_size = 10
confirm_btn_press_cnt=0

p1_ship_loca = []
p2_ship_loca = []
rectangle_coordinates_list = []
rectangle_coordinates_list1 = []

Store_ship_location = False


# Main Variables
chance=15    
cur_chnc_p1=0
cur_chnc_p2=0

shot_number = 0

switch = True
p1_ships_refined = []
p2_ships_refined = []

hit_squares_p1 = []
hit_squares_p2 = []
miss_squares = []

global p1_ship_des, p2_ship_des
p1_ship_des=0
p2_ship_des=0


# Button Images
play_img = pygame.image.load('Button_Play.jpg').convert_alpha()
play_hov_img = pygame.image.load('Button_Play_Hov.jpg').convert_alpha()

exit_img = pygame.image.load('Button_Exit.jpg').convert_alpha()
exit_hov_img = pygame.image.load('Button_Exit_Hov.jpg').convert_alpha()

info_img = pygame.image.load('Button_Info.jpg').convert_alpha()
info_hov_img = pygame.image.load('Button_Info_Hov.jpg').convert_alpha()

confirm_img = pygame.image.load('Button_Confirm.jpg').convert_alpha()
confirm_hov_img = pygame.image.load('Button_Confirm_Hov.jpg').convert_alpha()

next_img = pygame.image.load('Button_Next.jpg').convert_alpha()
next_hov_img = pygame.image.load('Button_Next_Hov.jpg').convert_alpha()

waiting_img = pygame.image.load('wait.jpg')
ship_a = pygame.image.load('shipa.jpg').convert()
ship_b = pygame.image.load('shipb.jpg').convert()
ship_c = pygame.image.load('shipc.jpg').convert()
ship_d = pygame.image.load('shipd.jpg').convert()


# Renders
text = fonta.render('Hold and drag to insert ships!',True,'black')
text_main1 = font.render('Player 1', True, 'black')
text_main2 = font.render('Player 2', True, 'black')
text_result1 = font_big.render('GAME OVER', True, 'black')
text_result2 = fonta.render('OUT OF AMMUNITIONS', True, 'black')
text_result3_p1 = fonta.render('PLAYER 1 GOT THE MOST HITS', True, 'black')
text_result3_p2 = fonta.render('PLAYER 2 GOT THE MOST HITS', True, 'black')
text_result3_draw = fonta.render('BOTH GOT EQUAL HITS', True, 'black')

text1 = font_small.render('Battleship is a strategy type guessing game for two players. It is played on ruled grids on',True,'black')
text2 = font_small.render("which each player's fleet of warships are marked. The locations of the fleets are concealed ",True,'black')
text3 = font_small.render("from the other player. Players take alternate turns calling 'shots' at the other player's ships,",True,'black')
text4 = font_small.render("and the objective of the game is to destroy the opposing player's fleet. Each player starts",True,'black')
text5 = font_small.render("with 15 units of ammunition which cannot be refilled. Try to hit as many opponent's ships as",True,'black')
text6 = font_small.render('possible under the specified rounds of fire',True,'black')
text0 = font_big.render('INFO',True,'black')

text11 = font_small.render('Each ship occupies some specific number of cells according to the type of ship being placed.',True,'black')
text12 = font_small.render('The types of ships along with their cell size is mentioned below.',True,'black')
text13 = font_small.render('3 Cells',True,'black')
text14 = font_small.render('2 Cells',True,'black')
text15 = font_small.render('5 Cells',True,'black')
text16 = font_small.render('4 Cells',True,'black')


a=font.render('A',True,'black')
b=font.render('B',True,'black')
c=font.render('C',True,'black')
d=font.render('D',True,'black')
e=font.render('E',True,'black')
f=font.render('F',True,'black')
g=font.render('G',True,'black')
h=font.render('H',True,'black')
i=font.render('I',True,'black')
j=font.render('J',True,'black')

a1=font.render('1',True,'black')
a2=font.render('2',True,'black')
a3=font.render('3',True,'black')
a4=font.render('4',True,'black')
a5=font.render('5',True,'black')
a6=font.render('6',True,'black')
a7=font.render('7',True,'black')
a8=font.render('8',True,'black')
a9=font.render('9',True,'black')
a10=font.render('10',True,'black')


# Class Objects
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False


    def draw(self):
        action = False
        hover = False

        try:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                hover = True
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
            else:
                hover = False

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            screen.blit(self.image, (self.rect.x, self.rect.y))
            return action, hover
        
        except:
            pass

class drag_obj:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x, y)
        self.dragging = False
        self.rotation_angle = 0

    def rotate(self):
        # Rotate the image by 90 degrees to the right
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.image = pygame.transform.rotate(self.image, -90)  # Negative angle to rotate right

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            snap_x = (mouse_x // grid_size) * grid_size +1 
            snap_y = (mouse_y // grid_size) * grid_size +1
            self.rect.topleft = (snap_x, snap_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right-click
            if self.rect.collidepoint(event.pos):
                self.rotate()


button_play = Button(520, 200, play_img, 1)
button_exit = Button(520, 500, exit_img, 1)
button_info = Button(520, 350, info_img, 1)
confirm_btn = Button(990, 3, confirm_img, 0.5)
button_next = Button(900, 500, next_img, 1)

# Ships Initial Position
objects_p1 = [drag_obj(87, 625, ship_a),
              drag_obj(952-15, 625, ship_a),
              drag_obj(275-25, 625, ship_b),
              drag_obj(383-25, 625, ship_b),
              drag_obj(493-25, 625, ship_c),
              drag_obj(753-25,625,ship_d)]
              
objects_p2 = [drag_obj(87, 625, ship_a),
              drag_obj(952-15, 625, ship_a),
              drag_obj(275-25, 625, ship_b),
              drag_obj(383-25, 625, ship_b),
              drag_obj(493-25, 625, ship_c),
              drag_obj(753-25,625,ship_d)]
              

running = True

async def main():
    
    global background_colour, col, color, color_safe, click, info_click
    global rotation_angle, p1_ship_not_placed, p2_ship_not_placed, show_img, cube_size, grid_size, confirm_btn_press_cnt
    global p1_ship_loca, p2_ship_loca, rectangle_coordinates_list, rectangle_coordinates_list1, Store_ship_location
    global chance, cur_chnc_p1, cur_chnc_p2, shot_number

    global switch, p1_ships_refined, p2_ships_refined, hit_squares_p1, hit_squares_p2, miss_squares
    global objects_p1, objects_p2, running
    global play_img, play_hov_img, exit_img, exit_hov_img, info_img, info_hov_img, confirm_img, confirm_hov_img, next_img, next_hov_img
    global waiting_img, ship_a, ship_b, ship_c, ship_d
    global text, text_main1, text_main2, text_result1, text_result2, text_result3_p1, text_result3_p2, text_result3_draw
    global text0, text1, textt2, text3, text4, text5, text6, text11, text12, text13, text14, text15, text16
    global a, b, c, d, e, f, g, h, i, j, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10
    global button_exit, button_info, button_next, button_play, confirm_btn
    global p1_ship_des, p2_ship_des
    global ship_list
    
    while running:
        screen.fill(background_colour)
    
        if click == 0:
            if button_play.draw()[1]:
                #print('Hovering on Play')
                button_play = Button(520, 200, play_hov_img, 1)
            else:
                button_play = Button(520, 200, play_img, 1)
    
            if button_exit.draw()[1]:
                #print('Hovering on Exit')
                button_exit = Button(520, 500, exit_hov_img, 1)
            else:
                button_exit = Button(520, 500, exit_img, 1)
    
            if button_info.draw()[1]:
                #print('Hovering on Exit')
                button_info = Button(520, 350, info_hov_img, 1)
            else:
                button_info = Button(520, 350, info_img, 1)
    
            screen.blit(header,(280,50))
            pygame.display.update()
            pygame.display.flip()
    
        if info_click == 1 and click == 'Nil':
            screen.blit(text0, (550, 50))
            screen.blit(text1, (10, 150))
            screen.blit(text2, (10, 200))
            screen.blit(text3, (10, 250))
            screen.blit(text4, (10, 300))
            screen.blit(text5, (10, 350))
            screen.blit(text6, (10, 400))
    
            if button_next.draw()[1]:
                button_next = Button(900, 500, next_hov_img, 1)
            else:
                button_next = Button(900, 500, next_img, 1)
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_next.draw()[0]:
                            info_click += 1
                            click = 'Nil'
                            
        if info_click == 2 and click == 'Nil':
            screen.blit(text0, (550, 50))
            screen.blit(text11,(10,200))
            screen.blit(text12,(10,250))
            screen.blit(text13,(400,365))
            screen.blit(text14,(400,440))
            screen.blit(text15,(400,515))
            screen.blit(text16,(400,590))
    
            screen.blit(ship_a, (40, 350))
            screen.blit(ship_b, (40, 425))
            screen.blit(ship_c, (40, 500))
            screen.blit(ship_d, (40,575))
    
    
            if button_exit.draw()[1]:
                button_exit = Button(900, 500, exit_hov_img, 1)
            else:
                button_exit = Button(900, 500, exit_img, 1)
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_exit.draw()[0]:
                            info_click = 0
                            click = 0
    
        if click == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
                for obj in objects_p1:
                    obj.handle_event(event)
                for obj in objects_p2:
                    obj.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if confirm_btn.draw()[0]:
                        show_img = True
                        confirm_btn_press_cnt+=1
    
                        # Create a list to store the coordinates of the current set of rectangles
                        if p1_ship_not_placed:
                                        
                            current_rectangles = []
                            # Iterate through the objects_p1 and get their coordinates in the specified order
                            for obj in objects_p1:
                                topleft = (obj.rect.topleft[0]-1,obj.rect.topleft[1]-1)
                                topright = (obj.rect.topright[0]-1, obj.rect.topleft[1]-1)
                                bottomleft = (obj.rect.topleft[0]-1, obj.rect.bottomleft[1]-1)
                                bottomright = (obj.rect.bottomright[0]-1,obj.rect.bottomright[1]-1)
                                current_rectangles.append([topleft, topright, bottomleft, bottomright])
    
                            # Append the current set of coordinates to the main list
                            rectangle_coordinates_list.append(current_rectangles)
                            p1_ship_not_placed = False
    
                        else:
                            current_rectangles1 = []
                            # Iterate through the objects_p1 and get their coordinates in the specified order
                            for obj in objects_p2:
                                topleft = (obj.rect.topleft[0]-1,obj.rect.topleft[1]-1)
                                topright = (obj.rect.topright[0]-1, obj.rect.topleft[1]-1)
                                bottomleft = (obj.rect.topleft[0]-1, obj.rect.bottomleft[1]-1)
                                bottomright = (obj.rect.bottomright[0]-1,obj.rect.bottomright[1]-1)
                                current_rectangles1.append([topleft, topright, bottomleft, bottomright])
    
                            # Append the current set of coordinates to the main list
                            rectangle_coordinates_list1.append(current_rectangles1)
                            p2_ship_not_placed = False
    
            if confirm_btn.draw()[1]:
                #print('Hovering on Play')
                confirm_btn = Button(990, 3, confirm_hov_img, 0.5)
            else:
                confirm_btn = Button(990, 3, confirm_img, 0.5)
            
            if confirm_btn_press_cnt == 3:
                click += 1
                Store_ship_location = True
            
            spacing = 564
            txt_spacing = 40
            # text
            screen.blit(text,(300,10))
            screen.blit(a,(txt_spacing,74))
            screen.blit(b,(txt_spacing,74+cube_size))
            screen.blit(c,(txt_spacing,74+(2*cube_size)))
            screen.blit(d,(txt_spacing,74+(3*cube_size)))
            screen.blit(e,(txt_spacing,74+(4*cube_size)))
            screen.blit(f,(txt_spacing,74+(5*cube_size)))
            screen.blit(g,(txt_spacing,74+(6*cube_size)))
            screen.blit(h,(txt_spacing,74+(7*cube_size)))
            screen.blit(i,(txt_spacing,74+(8*cube_size)))
            screen.blit(j,(txt_spacing,74+(9*cube_size)))
    
            screen.blit(a1,(78,spacing))
            screen.blit(a2,(78+cube_size,spacing))
            screen.blit(a3,(78+(2*cube_size),spacing))
            screen.blit(a4,(78+(3*cube_size),spacing))
            screen.blit(a5,(78+(4*cube_size),spacing))
            screen.blit(a6,(78+(5*cube_size),spacing))
            screen.blit(a7,(78+(6*cube_size),spacing))
            screen.blit(a8,(78+(7*cube_size),spacing))
            screen.blit(a9,(78+(8*cube_size),spacing))
            screen.blit(a10,(76+(9*cube_size),spacing))
             
            txt_spacing=txt_spacing+40
            #text2
            screen.blit(a,(txt_spacing+552,72))
            screen.blit(b,(txt_spacing+552,72+cube_size))
            screen.blit(c,(txt_spacing+552,72+(2*cube_size)))
            screen.blit(d,(txt_spacing+552,72+(3*cube_size)))
            screen.blit(e,(txt_spacing+552,72+(4*cube_size)))
            screen.blit(f,(txt_spacing+552,72+(5*cube_size)))
            screen.blit(g,(txt_spacing+552,72+(6*cube_size)))
            screen.blit(h,(txt_spacing+552,72+(7*cube_size)))
            screen.blit(i,(txt_spacing+552,72+(8*cube_size)))
            screen.blit(j,(txt_spacing+552,72+(9*cube_size)))
    
            screen.blit(a1,(78+40+552,spacing))
            screen.blit(a2,(78+40+cube_size+552,spacing))
            screen.blit(a3,(78+40+(2*cube_size)+552,spacing))
            screen.blit(a4,(78+40+(3*cube_size)+552,spacing))
            screen.blit(a5,(78+40+(4*cube_size)+552,spacing))
            screen.blit(a6,(78+40+(5*cube_size)+552,spacing))
            screen.blit(a7,(78+40+(6*cube_size)+552,spacing))
            screen.blit(a8,(78+40+(7*cube_size)+552,spacing))
            screen.blit(a9,(78+40+(8*cube_size)+552,spacing))
            screen.blit(a10,(72+40+(9*cube_size)+552,spacing))
    
            # ... (your other drawing code)
    
            # grid
            for x in range(1, grid_size + 2):
                pygame.draw.line(screen, col, (60, 10 + x * cube_size), (560, 10 + x * cube_size), 2)
                pygame.draw.line(screen, col, (10 + x * cube_size, 60), (10 + x * cube_size, 560), 2)
    
            # grid2
            for x in range(1, grid_size + 2):
                pygame.draw.line(screen, col, (650, 10 + x * cube_size), (1150, 10 + x * cube_size), 2)
                pygame.draw.line(screen, col, (590 + 10 + x * cube_size, 60), (590 + 10 + x * cube_size, 560), 2)
            
    
            if p1_ship_not_placed:
                    
                for obj in objects_p1:
                    obj.update()
                    obj.draw()
            else:
    
                for obj1 in objects_p2:
                    obj1.update()
                    obj1.draw()
    
            if show_img:
                screen.blit(waiting_img, (60, 60))
    
            if confirm_btn_press_cnt >= 2:
                screen.blit(waiting_img,(650,60))
    
            # battleship toggler
            pygame.draw.line(screen, col, (82, 620), (1090, 620), 2)
            pygame.draw.line(screen, col, (82, 680), (1090, 680), 2)
            pygame.draw.line(screen, col, (82, 620), (82, 680), 2)
            pygame.draw.line(screen, col, (268-25, 620), (268-25, 680), 2)
            pygame.draw.line(screen, col, (378-25, 620), (378-25, 680), 2)
            pygame.draw.line(screen, col, (488-25, 620), (488-25, 680), 2)
            pygame.draw.line(screen, col, (747-25, 620), (747-25, 680), 2)
            pygame.draw.line(screen, col, (957-25, 620), (957-25, 680), 2)
            pygame.draw.line(screen, col, (1090, 620), (1090, 680), 2)
    
            pygame.display.update()
            pygame.display.flip()
    
        if Store_ship_location == True:
            for x in rectangle_coordinates_list:
                for ele in x:
                    p1_ship_loca.append(ele)
    
            for x in rectangle_coordinates_list1:
                for ele in x:
                    p2_ship_loca.append(ele)
    
            p1_ships = p1_ship_loca
            p2_ships = p2_ship_loca
            Store_ship_location = False
    
            pygame.display.update()
            pygame.display.flip()
    
        if click == 2:
            for z in range(0, 6):
                len_p1_ship = p1_ships[z][1][0] - p1_ships[z][0][0]
                box_len_p1_ship = len_p1_ship // cube_size
    
                cor = 0
                while cor < (box_len_p1_ship*50):
                    w, s = p1_ships[z][0]
                    col_ = (w+cor) // cube_size
                    row_ = (s) // cube_size
    
                    p1_ships_refined.append((row_, col_))
                    cor += 50
    
            for z in range(0, 6):
                len_p2_ship = p2_ships[z][1][0] - p2_ships[z][0][0]
                box_len_p2_ship = len_p2_ship // cube_size
    
                cor = 0
                while cor < (box_len_p2_ship*50):
                    w, s = p2_ships[z][0]
                    col_ = (w+cor) // cube_size
                    row_ = (s) // cube_size
    
                    p2_ships_refined.append((row_, col_))
                    cor += 50
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        col = x // cube_size
                        row = y // cube_size
    
                        if switch == True:
                            if row >= 1 and col >=1 and row <= 10 and col <= 10:
                                shot_number += 1
                                switch = False
                                
                                if (row, col) in p1_ships_refined:
                                    print('Shot fired at: ',(row, col))
                                    print('Thats a Hit!')
                                    hit_squares_p1.append((row, col))
                                    cur_chnc_p1 += 1
                                    p2_ship_des += 1
                                    print('Ammo Fired by Player 2: ',cur_chnc_p1, 'Units')
                                    print('Ammo left for Player 2: ', (15-cur_chnc_p1), 'Units')
                                    print()
    
                                else:
                                    miss_squares.append((row, col))
                                    cur_chnc_p1 += 1
                                    print('Ammo Fired by Player 2: ',cur_chnc_p1, 'Units')
                                    print('Ammo left for Player 2: ', (15-cur_chnc_p1), 'Units')
                                    print()
                            else:
                                pass
    
                        if switch == False:
                            if row >= 1 and col >=13 and row <= 10 and col <= 22:
                                shot_number += 1
                                switch = True
                                
                                if (row, col) in p2_ships_refined:
                                    print('Shot fired at: ',(row, col))
                                    print('Thats a Hit!')
                                    hit_squares_p2.append((row, col))
                                    cur_chnc_p2 += 1
                                    p1_ship_des += 1
                                    print('Ammo Fired by Player 1: ',cur_chnc_p2, 'Units')
                                    print('Ammo left for Player 1: ', (15-cur_chnc_p2), 'Units')
                                    print()
    
                                else:
                                    cur_chnc_p2 += 1 
                                    miss_squares.append((row, col))
                                    print('Ammo Fired by Player 1: ',cur_chnc_p2, 'Units')
                                    print('Ammo left for Player 1: ', (15-cur_chnc_p2), 'Units')
                                    print()
                            else:
                                pass
                            
    
            # Draw hit and miss squares
            for row, col in hit_squares_p1:
                pygame.draw.rect(screen, color, pygame.Rect(col * cube_size+10, row * cube_size+10, cube_size, cube_size))
            for row, col in hit_squares_p2:
                pygame.draw.rect(screen, color, pygame.Rect(col * cube_size+10, row * cube_size+10, cube_size, cube_size))
            
            for row, col in miss_squares:
                pygame.draw.rect(screen, color_safe, pygame.Rect(col * cube_size+10, row * cube_size+10, cube_size, cube_size))
    
            # Grid 1
            for x in range(1, grid_size + 2):
                pygame.draw.line(screen, col, (60, 10 + x * cube_size), (560, 10 + x * cube_size), 2)
                pygame.draw.line(screen, col, (10 + x * cube_size, 60), (10 + x * cube_size, 560), 2)
    
            # Grid 2
            for x in range(1, grid_size + 2):
                pygame.draw.line(screen, col, (610+50, 10 + x * cube_size), (1110+50, 10 + x * cube_size), 2)
                pygame.draw.line(screen, col, (550+50 + 10 + x * cube_size, 60), (550 +50+ 10 + x * cube_size, 560), 2)
    
            spacing = 564
            txt_spacing = 40
            # Text 1
            screen.blit(text_main1,(240,10))
            screen.blit(a, (txt_spacing, 74))
            screen.blit(b, (txt_spacing, 74 + cube_size))
            screen.blit(c, (txt_spacing, 74 + (2 * cube_size)))
            screen.blit(d, (txt_spacing, 74 + (3 * cube_size)))
            screen.blit(e, (txt_spacing, 74 + (4 * cube_size)))
            screen.blit(f, (txt_spacing, 74 + (5 * cube_size)))
            screen.blit(g, (txt_spacing, 74 + (6 * cube_size)))
            screen.blit(h, (txt_spacing, 74 + (7 * cube_size)))
            screen.blit(i, (txt_spacing, 74 + (8 * cube_size)))
            screen.blit(j, (txt_spacing, 74 + (9 * cube_size)))
    
            screen.blit(text_main2,(850,10))
            screen.blit(a1, (78, spacing))
            screen.blit(a2, (78 + cube_size, spacing))
            screen.blit(a3, (78 + (2 * cube_size), spacing))
            screen.blit(a4, (78 + (3 * cube_size), spacing))
            screen.blit(a5, (78 + (4 * cube_size), spacing))
            screen.blit(a6, (78 + (5 * cube_size), spacing))
            screen.blit(a7, (78 + (6 * cube_size), spacing))
            screen.blit(a8, (78 + (7 * cube_size), spacing))
            screen.blit(a9, (78 + (8 * cube_size), spacing))
            screen.blit(a10, (76 + (9 * cube_size), spacing))
    
            txt_spacing = txt_spacing + 40
            # Text 2
            screen.blit(a, (txt_spacing + 552, 72))
            screen.blit(b, (txt_spacing + 552, 72 + cube_size))
            screen.blit(c, (txt_spacing + 552, 72 + (2 * cube_size)))
            screen.blit(d, (txt_spacing + 552, 72 + (3 * cube_size)))
            screen.blit(e, (txt_spacing + 552, 72 + (4 * cube_size)))
            screen.blit(f, (txt_spacing + 552, 72 + (5 * cube_size)))
            screen.blit(g, (txt_spacing + 552, 72 + (6 * cube_size)))
            screen.blit(h, (txt_spacing + 552, 72 + (7 * cube_size)))
            screen.blit(i, (txt_spacing + 552, 72 + (8 * cube_size)))
            screen.blit(j, (txt_spacing + 552, 72 + (9 * cube_size)))
    
            screen.blit(a1, (78 + 40 + 552, spacing))
            screen.blit(a2, (78 + 40 + cube_size + 552, spacing))
            screen.blit(a3, (78 + 40 + (2 * cube_size) + 552, spacing))
            screen.blit(a4, (78 + 40 + (3 * cube_size) + 552, spacing))
            screen.blit(a5, (78 + 40 + (4 * cube_size) + 552, spacing))
            screen.blit(a6, (78 + 40 + (5 * cube_size) + 552, spacing))
            screen.blit(a7, (78 + 40 + (6 * cube_size) + 552, spacing))
            screen.blit(a8, (78 + 40 + (7 * cube_size) + 552, spacing))
            screen.blit(a9, (78 + 40 + (8 * cube_size) + 552, spacing))
            screen.blit(a10, (72 + 40 + (9 * cube_size) + 552, spacing))
    
            if cur_chnc_p1 == cur_chnc_p2 == chance:
                click +=1
    
            pygame.display.update()
            pygame.display.flip()
    
        if click == 3:
            screen.blit(text_result1,(450,60))
            screen.blit(text_result2,(435,150))
    
            if p1_ship_des > p2_ship_des:
                screen.blit(text_result3_p1,(370,350))
    
            elif p1_ship_des < p2_ship_des:
                screen.blit(text_result3_p2,(370,350))
    
            else:
                screen.blit(text_result3_draw,(430,350))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_play.draw()[0]:
                        click += 1
    
                    if button_exit.draw()[0]:
                        running = False
    
                    if button_info.draw()[0]:
                        info_click += 1
                        click = 'Nil'
        
        pygame.display.update()
        pygame.display.flip()
        await asyncio.sleep(0)
        

asyncio.run(main())