from Button import Button
from Level import *
from Constants import (
    WIDTH,
    HEIGHT,
    BLACK,
    BLUE,
    WHITE,
)

import pygame

''' Game Interface '''
class Game:
    def __init__(self,  Menu="Main"):
        self.menu = Menu

    def Write_On_Screen(self, font, text, size, color, bg_color, bold, pos, screen):
        letra = pygame.font.SysFont(font, size, bold)
        frase = letra.render(text, 1, color, bg_color)
        screen.blit(frase, pos)

    def Run(self):
        
        pygame.init()
        Screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Klotski')
        Icon = pygame.image.load('Assets/Icon.png').convert_alpha()
        pygame.display.set_icon(Icon)

        ''' Main Menu '''
        Main_Menu_IMG = pygame.image.load('Assets/Klotski_BG.png').convert_alpha()
        Main_Menu = Button(Main_Menu_IMG, -330,0,.75)

        Start_IMG = pygame.image.load('Assets/Start.png').convert_alpha()
        Start_Button = Button(Start_IMG, 340, 350, .55)

        ''' Modes Menu '''
        Easy_IMG = pygame.image.load('Assets/Easy.png').convert_alpha()
        Easy_Button = Button(Easy_IMG, 250, 160, .4)

        Hard_IMG = pygame.image.load('Assets/Hard.png').convert_alpha()
        Hard_Button = Button(Hard_IMG, 250, 400, .4)

        Options_IMG = pygame.image.load('Assets/Options.png').convert_alpha()
        Options_Button = Button(Options_IMG, 600, 30, .15)

        Back_IMG = pygame.image.load('Assets/Back.png').convert_alpha()
        Back_Button = Button(Back_IMG, 50, 675, .15)

        Exit_IMG = pygame.image.load('Assets/Exit.png').convert_alpha()
        Exit_Button = Button(Exit_IMG, 530, 650, .25)

        ''' Options Menu '''
        How_To_Play_IMG = pygame.image.load('Assets/How_To_Play.png').convert_alpha()
        How_To_Play_Button = Button(How_To_Play_IMG, 300, 130, .2)
        
        How_To_Play_1_IMG = pygame.image.load('Assets/HowToPlay_1.png').convert_alpha()
        How_To_Play_1 = Button(How_To_Play_1_IMG, 120, 425, .4)
        How_To_Play_2_IMG = pygame.image.load('Assets/HowToPlay_2.png').convert_alpha()
        How_To_Play_2 = Button(How_To_Play_2_IMG, 420, 425, .4)
        How_To_Play_Arrow_IMG = pygame.image.load('Assets/Arrow.png').convert_alpha()
        How_To_Play_Arrow = Button(How_To_Play_Arrow_IMG, 300, 470, .2)

        Algoritms_IMG = pygame.image.load('Assets/Algorithms.png').convert_alpha()
        Algoritms_Button = Button(Algoritms_IMG, 300, 330, .2)

        Credits_IMG = pygame.image.load('Assets/Credits.png').convert_alpha()
        Credits_Button = Button(Credits_IMG, 315 , 530, .15)

        ''' EXTRA IMAGES '''
        Work_IMG = pygame.image.load('Assets/Work.png').convert_alpha()
        Work_Button = Button(Work_IMG, 480, 480, .25)

        ''' LEVELS IMAGES '''
        L1_IMG = pygame.image.load('Assets/Levels/1.png').convert_alpha()
        L2_IMG = pygame.image.load('Assets/Levels/2.png').convert_alpha()
        L3_IMG = pygame.image.load('Assets/Levels/3.png').convert_alpha()
        L4_IMG = pygame.image.load('Assets/Levels/4.png').convert_alpha()
        L5_IMG = pygame.image.load('Assets/Levels/5.png').convert_alpha()
        L6_IMG = pygame.image.load('Assets/Levels/6.png').convert_alpha()
        L7_IMG = pygame.image.load('Assets/Levels/7.png').convert_alpha()
        L8_IMG = pygame.image.load('Assets/Levels/8.png').convert_alpha()

        L1_DONE_IMG = pygame.image.load('Assets/Levels/1_Done.png')
        L2_DONE_IMG = pygame.image.load('Assets/Levels/2_Done.png')
        L3_DONE_IMG = pygame.image.load('Assets/Levels/3_Done.png')
        L4_DONE_IMG = pygame.image.load('Assets/Levels/4_Done.png')
        L5_DONE_IMG = pygame.image.load('Assets/Levels/5_Done.png')
        L6_DONE_IMG = pygame.image.load('Assets/Levels/6_Done.png')
        L7_DONE_IMG = pygame.image.load('Assets/Levels/7_Done.png')
        L8_DONE_IMG = pygame.image.load('Assets/Levels/8_Done.png')

        ''' Levels '''
        L1_Easy_Button = Button(L1_IMG, 60,180,.2)
        L2_Easy_Button = Button(L2_IMG, 220,180,.2)
        L3_Easy_Button = Button(L3_IMG, 380,180,.2)
        L4_Easy_Button = Button(L4_IMG, 540,180,.2)
        L5_Easy_Button = Button(L5_IMG, 60, 320,.2)
        L6_Easy_Button = Button(L6_IMG, 220,320,.2)
        L7_Easy_Button = Button(L7_IMG, 380,320,.2)
        L8_Easy_Button = Button(L8_IMG, 540,320,.2)
        
        L1_Hard_Button = Button(L1_IMG, 60,180,.2)
        L2_Hard_Button = Button(L2_IMG, 220,180,.2)
        L3_Hard_Button = Button(L3_IMG, 380,180,.2)
        L4_Hard_Button = Button(L4_IMG, 540,180,.2)
        L5_Hard_Button = Button(L5_IMG, 60, 320,.2)
        L6_Hard_Button = Button(L6_IMG, 220,320,.2)
        L7_Hard_Button = Button(L7_IMG, 380,320,.2)
        L8_Hard_Button = Button(L8_IMG, 540,320,.2)
        
        ''' Switches '''
        Switch_OFF_IMG = pygame.image.load('Assets/Off.png').convert_alpha()
        Switch_ON_IMG = pygame.image.load('Assets/On.png').convert_alpha()
        
        Bfs_Switch = Button(Switch_OFF_IMG, 100, 230, .2)
        Itr_Deep_Switch = Button(Switch_OFF_IMG, 100, 350, .2)
        Greedy_Search_H1_Switch = Button(Switch_OFF_IMG, 100, 470, .2)
        
        Greedy_Search_H2_Switch = Button(Switch_OFF_IMG, 400, 230, .2)
        A_Star_H1_Switch = Button(Switch_OFF_IMG, 400, 350, .2)
        A_Star_H2_Switch = Button(Switch_OFF_IMG, 400, 470, .2)

        # Inicializa o Estado de Análise dos Algoritmos a ser usados
        Algorithms = [Bfs_Switch.Atual_State(), Itr_Deep_Switch.Atual_State(), Greedy_Search_H1_Switch.Atual_State(), Greedy_Search_H2_Switch.Atual_State(),A_Star_H1_Switch.Atual_State(), A_Star_H2_Switch.Atual_State()]
        
        ''' Menu Variables '''
        Menu = "Main"
        run = True
        while run:

            if Menu == "Main":
                Main_Menu.Action(Screen)
                pygame.draw.rect(Screen, BLACK, (373, 230, 250, 90))
                self.Write_On_Screen('Arial', " Klotski ", 80, BLUE, WHITE, True, (363, 220), Screen)
                if Start_Button.Action(Screen):
                    Menu = "Modes"

            elif Menu == "Modes":
                Screen.fill(BLUE)
                self.Write_On_Screen('Arial', " MODES ", 80, WHITE, None, True ,(210,30), Screen)
                if Options_Button.Action(Screen):
                    Menu = "Options"
                if Easy_Button.Action(Screen):
                    Menu = "Easy_Mode"
                if Hard_Button.Action(Screen):
                    Menu = "Hard_Mode"
                if Back_Button.Action(Screen):
                    Menu = "Main"
                if Exit_Button.Action(Screen):
                    run = False

            elif Menu == "Options":
                Screen.fill(BLUE)
                self.Write_On_Screen('Arial'," Options ", 80, WHITE, None, True, (210,30), Screen)
                self.Write_On_Screen('Arial', ' How To Play ', 40, BLUE, WHITE, False, (250,250), Screen)
                self.Write_On_Screen('Arial', ' Algorithms To Test ', 40, BLUE, WHITE, False, (220, 450), Screen)
                self.Write_On_Screen('Arial', ' Credits ', 40, BLUE, WHITE, False, (290,620), Screen)
                if How_To_Play_Button.Action(Screen):
                    Menu = "How_To_Play"
                if Algoritms_Button.Action(Screen):
                    Menu = "Algorithms"
                if Credits_Button.Action(Screen):
                    Menu = "Credits_Page"
                if Back_Button.Action(Screen):
                    Menu = "Modes"
                if Exit_Button.Action(Screen):
                    run = False

            elif Menu == "How_To_Play":
                Screen.fill(BLUE)
                self.Write_On_Screen('Arial'," How to Play ", 70, WHITE, None, True, (170,50), Screen)
                self.Write_On_Screen('Arial', f" The goal is to ", 30, BLUE, WHITE, False, (260,165), Screen)
                self.Write_On_Screen('Arial', f" bring the red block to ", 30, BLUE, WHITE, False, (220,210), Screen)
                self.Write_On_Screen('Arial', f" the final position ", 30, BLUE, WHITE, False, (245,255), Screen)
                self.Write_On_Screen('Arial', f" (small red circles) ", 30, BLUE, WHITE, False, (240,300), Screen)
                self.Write_On_Screen('Arial', f" in as few steps as possible ", 30, BLUE, WHITE, False, (190,345), Screen)

                How_To_Play_Arrow.Action(Screen)
                How_To_Play_1.Action(Screen)
                How_To_Play_2.Action(Screen)

                if Back_Button.Action(Screen):
                    Menu = "Options" 
                
                if Exit_Button.Action(Screen):
                    run = False

            elif Menu == "Algorithms":
                Screen.fill(BLUE)
                self.Write_On_Screen('Arial'," Algorithms to Test ", 60, WHITE, None, True, (140,35), Screen)
                pygame.draw.line(Screen, WHITE, (348,165), (348,585), 5)

                self.Write_On_Screen('Arial'," Breath-First Search ", 30, WHITE, None, True, (80,200), Screen)
                if Bfs_Switch.Switch_On_Off(Screen, Switch_ON_IMG, Switch_OFF_IMG):
                    print("BFS")
                
                self.Write_On_Screen('Arial'," Iterative Deepening ", 30, WHITE, None, True, (80,320), Screen)
                if Itr_Deep_Switch.Switch_On_Off(Screen, Switch_ON_IMG, Switch_OFF_IMG):
                    print("ITERATIVE DEEPENING")
                
                self.Write_On_Screen('Arial'," Greedy Search (H1) ", 30, WHITE, None, True,(80,440), Screen)
                if Greedy_Search_H1_Switch.Switch_On_Off(Screen, Switch_ON_IMG, Switch_OFF_IMG):
                    print("GREEDY SEARCH - H1")
                
                self.Write_On_Screen('Arial'," Greedy Search (H2) ", 30, WHITE, None, True,(380,200), Screen)
                if Greedy_Search_H2_Switch.Switch_On_Off(Screen, Switch_ON_IMG, Switch_OFF_IMG):
                    print("GREEDY SEARCH - H2")
                
                self.Write_On_Screen('Arial'," A* Algorithm (H1) ", 30, WHITE, None, True, (380,320), Screen)
                if A_Star_H1_Switch.Switch_On_Off(Screen, Switch_ON_IMG, Switch_OFF_IMG):
                    print("A STAR ALGORITHM")
                
                self.Write_On_Screen('Arial'," A* Algorithm (H2) ", 30, WHITE, None, True, (380,440), Screen)
                if A_Star_H2_Switch.Switch_On_Off(Screen, Switch_ON_IMG, Switch_OFF_IMG):
                    print("A STAR ALGORITHM - H2")

                # Atualiza os Algoritmos a Testar
                Algorithms = [Bfs_Switch.Atual_State(), Itr_Deep_Switch.Atual_State(), Greedy_Search_H1_Switch.Atual_State(), Greedy_Search_H2_Switch.Atual_State(),A_Star_H1_Switch.Atual_State(), A_Star_H2_Switch.Atual_State()]

                if Back_Button.Action(Screen):
                    Menu = "Options" 
                
                if Exit_Button.Action(Screen):
                    run = False
            
            elif Menu == "Credits_Page":
                Screen.fill(BLUE)
                self.Write_On_Screen('Arial'," Credits ", 80, WHITE, None, True, (215,50), Screen)
                self.Write_On_Screen('Arial', " Klotski's Implementation using Python ", 40, BLUE, WHITE, False, (65,175), Screen)
                self.Write_On_Screen('Arial', " Developed by: ", 40, WHITE, None, True, (65,250), Screen)
                self.Write_On_Screen('Arial', " - Gonçalo Esteves, up202203947 ", 30, WHITE, None, False, (90,310), Screen)
                self.Write_On_Screen('Arial', " - Mariana Gomes, up202206615 ", 30, WHITE, None, False, (90,360), Screen)
                self.Write_On_Screen('Arial', " Under Guidance of: ", 40, WHITE, None, True, (65,430), Screen)
                self.Write_On_Screen('Arial', " - Professor Luís Paulo Reis ", 30, WHITE, None, False, (90,490), Screen)
                
                Work_Button.Action(Screen)

                if Back_Button.Action(Screen):
                    Menu = "Options" 
                
                if Exit_Button.Action(Screen):
                    run = False

            elif Menu == "Easy_Mode":
                Screen.fill(BLUE)
                self.Write_On_Screen('Arial'," Easy Mode ", 80, WHITE, None, True, (170,50), Screen)

                if L1_Easy_Button.Action(Screen):
                    red_piece = [(0,0),(0,1),(1,0),(1,1)]
                    other_pieces = []
                    obj = [(3,2),(3,3),(4,2),(4,3)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L1_Easy_Button.Switch_Image(L1_DONE_IMG)
                
                if L2_Easy_Button.Action(Screen):
                    red_piece = [(0,0),(0,1),(1,0),(1,1)]
                    other_pieces = [[(2,0),(2,1)]]
                    obj = [(3,2),(3,3),(4,2),(4,3)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L2_Easy_Button.Switch_Image(L2_DONE_IMG)

                if L3_Easy_Button.Action(Screen):
                    red_piece = [(0,0),(0,1),(1,0),(1,1)]
                    other_pieces = [[(2,1),(2,2)]]
                    obj = [(3,2),(3,3),(4,2),(4,3)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L3_Easy_Button.Switch_Image(L3_DONE_IMG)
                
                if L4_Easy_Button.Action(Screen):
                    red_piece = [(0,0),(0,1),(1,0),(1,1)]
                    other_pieces = [[(2,0),(2,1)],[(2,2),(2,3)]]
                    obj = [(3,2),(3,3),(4,2),(4,3)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L4_Easy_Button.Switch_Image(L4_DONE_IMG)
                
                if L5_Easy_Button.Action(Screen):
                    red_piece = [(3,2),(3,3),(4,2)]
                    other_pieces = [[(0,2),(1,1),(1,2)],[(2,2)],[(2,3)]]
                    obj = [(0,0),(0,1),(1,0)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L5_Easy_Button.Switch_Image(L5_DONE_IMG)
                
                if L6_Easy_Button.Action(Screen):
                    red_piece = [(0,1),(1,1),(1,2)]
                    other_pieces = [[(2,1)],[(2,2)],[(2,3)],[(2,0),(3,0),(3,1),(4,1)]]
                    obj = [(3,2),(4,2),(4,3)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L6_Easy_Button.Switch_Image(L6_DONE_IMG)
                
                if L7_Easy_Button.Action(Screen):
                    red_piece = [(0,0),(0,1)]
                    other_pieces = [[(1,0),(1,1),(2,0)], [(3,1),(3,2),(3,3),(2,3)]]
                    obj = [(2,1),(2,2)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L7_Easy_Button.Switch_Image(L7_DONE_IMG)
                
                if L8_Easy_Button.Action(Screen):
                    red_piece = [(0,2),(0,3),(1,2),(1,3)]
                    other_pieces = [[(2,0)], [(4,2)], [(2,1),(2,2),(3,2)]]
                    obj = [(3,0),(4,0),(3,1),(4,1)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L8_Easy_Button.Switch_Image(L8_DONE_IMG)

                if Back_Button.Action(Screen):
                    Menu = "Modes" 
                
                if Exit_Button.Action(Screen):
                    run = False
            
            elif Menu == "Hard_Mode":
                Screen.fill(BLUE)
                self.Write_On_Screen('Arial'," Hard Mode ", 80, WHITE, None, True, (170,50), Screen)

                if L1_Hard_Button.Action(Screen):
                    red_piece = [(1,1),(1,2),(2,1),(2,2)]
                    other_pieces = [[(0,1),(0,2)], [(1,0),(2,0)], [(3,1),(3,2)], [(1,3),(2,3)]]
                    obj = [(3,1),(3,2),(4,1),(4,2)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L1_Hard_Button.Switch_Image(L1_DONE_IMG)
                
                if L2_Hard_Button.Action(Screen):
                    red_piece = [(0,0),(0,1),(1,0),(1,1)]
                    other_pieces = [[(2,2)],[(0,2),(1,2)],[(2,0),(2,1)]]
                    obj = [(3,2),(3,3),(4,2),(4,3)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L2_Hard_Button.Switch_Image(L2_DONE_IMG)

                if L3_Hard_Button.Action(Screen):
                    red_piece = [(0,0)]
                    other_pieces = [[(0,1),(1,0),(1,1)], [(0,2),(1,2)], [(2,2)], [(2,0),(2,1)]]
                    obj = [(4,3)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L3_Hard_Button.Switch_Image(L3_DONE_IMG)
                
                if L4_Hard_Button.Action(Screen):
                    red_piece = [(0,1),(0,2),(1,1),(1,2)]
                    other_pieces = [[(0,0),(1,0)], [(2,0)], [(2,1),(2,2)], [(2,3)], [(0,3),(1,3)]]
                    obj = [(3,1),(3,2),(4,1),(4,2)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L4_Hard_Button.Switch_Image(L4_DONE_IMG)
                
                if L5_Hard_Button.Action(Screen):
                    red_piece = [(0,1),(0,2),(1,1),(1,2)]
                    other_pieces = [[(0,0)], [(1,0)], [(2,0)], [(3,0)], [(4,0)], [(2,1)], [(2,2)], [(2,3)], [(0,3)], [(1,3)], [(3,1)], [(3,2)], [(3,3)], [(4,3)]]
                    obj = [(3,1),(3,2),(4,1),(4,2)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L5_Hard_Button.Switch_Image(L5_DONE_IMG)
                
                if L6_Hard_Button.Action(Screen):
                    red_piece = [(0,1),(0,2),(1,1),(1,2)]
                    other_pieces = [[(0,0)], [(1,0)], [(2,0)], [(3,0)], [(4,0)], [(2,1), (2,2)], [(3,1),(3,2)], [(0,3)], [(1,3)], [(2,3)], [(3,3)], [(4,3)]]
                    obj = [(3,1),(3,2),(4,1),(4,2)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L6_Hard_Button.Switch_Image(L6_DONE_IMG)
                
                if L7_Hard_Button.Action(Screen):
                    red_piece = [(0,0),(0,1),(1,0),(1,1)]
                    other_pieces = [[(0,2),(0,3)], [(1,2),(1,3)], [(2,2),(2,3)], [(2,0),(2,1)], [(3,0),(4,0)], [(3,3),(4,3)]]
                    obj = [(3,1),(3,2),(4,1),(4,2)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L7_Hard_Button.Switch_Image(L7_DONE_IMG)
                
                if L8_Hard_Button.Action(Screen):
                    red_piece = [(0,1),(0,2),(1,1),(1,2)]
                    other_pieces = [[(0,0)],[(1,0)], [(2,0),(3,0)], [(4,0)], [(2,1)], [(2,2)], [(3,1), (3,2)], [(0,3)], [(1,3)], [(2,3), (3,3)], [(4,3)]]
                    obj = [(3,1),(3,2),(4,1),(4,2)]
                    Level_ = Level(red_piece, other_pieces, obj, Algorithms)
                    Level_.Run(Screen)
                    if Level_.completed:
                        L8_Hard_Button.Switch_Image(L8_DONE_IMG)

                if Back_Button.Action(Screen):
                    Menu = "Modes"
                
                if Exit_Button.Action(Screen):
                    run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()
        
Play = Game()
Play.Run()
