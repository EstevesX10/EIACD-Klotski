import heapq
import time
from copy import deepcopy
from os import system

import pygame

from Button import Button
from Constants import (
    BG_COLOR,
    BLACK,
    BLANK_COLOR,
    BLUE,
    BOARD_DOWN,
    BORDER_COLOR,
    CIRCLE_COLOR,
    EXTERIOR_BORDER_COLOR,
    MAX_DEPTH_SEARCH,
    N_COLS,
    N_ROWS,
    OTHER_BORDER,
    OTHER_COLOR,
    RED_BORDER,
    RED_COLOR,
    SQSIZE,
    WHITE,
)

''' Main Class of our Game '''
class Level:
    def __init__(self, Red_Squares: list[tuple], Other_Squares: list[list[tuple]], Objective: list[tuple], Tests=[True,True,True,True,True,True]):
        self.matrix = [[0]*N_COLS for _ in range(N_ROWS)]
        self.moves = {"Up":(-1,0), "Down":(1,0), "Left":(0,-1), "Right":(0,1)}
        
        # Parameters to save all the pieces and the objective
        self.red = Red_Squares
        self.others = Other_Squares
        self.objective = Objective
        self.objective.sort()
        
        self.completed = self.Is_Over()
        # In order to save the times, steps to the solution and nodes explored of all the search algorithms
        self.Tests = Tests
        self.Times = [0,0,0,0,0,0]
        self.Steps = [0,0,0,0,0,0]
        self.Nodes_Explored = [0,0,0,0,0,0]
        
        # In order to save the movements/pieces history
        self.move_history = []
        self.red_history = []
        self.others_history = []

        # Updates the matrix with the pieces coordenates
        self.Update_Matrix()
        
        # Saves Initial Positions for the Reset Method
        self.inicial_red = deepcopy(Red_Squares)
        self.initial_others = deepcopy(Other_Squares)
        self.initial_matrix = deepcopy(self.matrix)
        self.inicial_Tests = deepcopy(Tests)
    
    @property
    def _level(self):
        return "\n".join("\t".join(map(str, r)) for r in self.matrix)

    def __hash__(self):
        red_tuple = str(self.red)
        other_tuple = str(sorted(tuple(i) for i in self.others))
        return hash((red_tuple, other_tuple))
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        else:
            return NotImplemented

    def __repr__(self):
        return f"<Level: \n{self._level}>\n"

    def Update_Matrix(self):
        ''' Atualiza a Matriz Tendo em conta as Posições Atuais das Peças '''
        # Dá -se reset à matriz e colocam-se as novas peças
        self.matrix = [[0]*N_COLS for _ in range(N_ROWS)]

        for (x,y) in self.red:
            self.matrix[x][y] = 1
        
        for piece in self.others:
            for (x,y) in piece:
                self.matrix[x][y] = -1

    def Show_Matrix(self):
        '''For Debugging purposes only'''
        print(self.matrix)
        print(f"red: {self.red} || others: {self.others}")

    '''  Main Movements -> Methods '''

    def Valid_Move(self, piece:list[tuple], move):
        ''' Verifies if a certain move is Valid '''
        if move == "Up":
            for (x,y) in piece:
                if not ((x > 0) and (self.matrix[x - 1][y] == 0 or (x-1, y) in piece)):
                    return False
        elif move == "Down":
            for (x,y) in piece:
                if not ((x+1 < N_ROWS) and (self.matrix[x + 1][y] == 0 or (x+1, y) in piece)):
                    return False
        elif move == "Left":
            for (x,y) in piece:
                if not ((y > 0) and (self.matrix[x][y-1] == 0 or (x, y-1) in piece)):
                    return False
        elif move == "Right":
            for (x,y) in piece:
                if not ((y+1 < N_COLS) and (self.matrix[x][y+1] == 0 or (x, y+1) in piece)):
                    return False
        return True
    
    def Make_Move(self, piece:list[tuple], move):
        ''' Makes a Move given a certain piece '''
        if self.Valid_Move(piece, move):
            piece_value = 0
            (x_move, y_move) = self.moves[move]
            
            if self.matrix[piece[0][0]][piece[0][1]] == 1:
                piece_value = 1
            elif self.matrix[piece[0][0]][piece[0][1]] == -1:
                piece_value = -1
            
            # New Position of Pieces
            New_Pieces = []

            for (x,y) in piece:
                if piece_value == 1 or piece_value == -1:
                    New_Pieces.append((x+x_move, y+y_move))
                
            if piece_value == 1:
                self.red = New_Pieces
            elif piece_value == -1:
                self.others.remove(piece)
                self.others.append(New_Pieces)
            
            self.red.sort()
            self.others.sort()

            self.Update_Matrix()
            self.move_history.append(self.matrix)

    ''' Search -> New State Methods '''

    def New_States(self):
        ''' Creates the New Possible states of the board '''
        New_States = []

        if self.Valid_Move(self.red, "Up"):
            aux = deepcopy(self)
            aux.Make_Move(self.red, "Up")
            New_States.append(aux)
        if self.Valid_Move(self.red, "Left"):
            aux = deepcopy(self)
            aux.Make_Move(self.red, "Left")
            New_States.append(aux)
        if self.Valid_Move(self.red, "Down"):
            aux = deepcopy(self)
            aux.Make_Move(self.red, "Down")
            New_States.append(aux)
        if self.Valid_Move(self.red, "Right"):
            aux = deepcopy(self)
            aux.Make_Move(self.red, "Right")
            New_States.append(aux)

        for piece in self.others:
            if self.Valid_Move(piece, "Up"):
                aux = deepcopy(self)
                aux.Make_Move(piece, "Up")
                New_States.append(aux)
            if self.Valid_Move(piece, "Left"):
                aux = deepcopy(self)
                aux.Make_Move(piece, "Left")
                New_States.append(aux)
            if self.Valid_Move(piece, "Down"):
                aux = deepcopy(self)
                aux.Make_Move(piece, "Down")
                New_States.append(aux)
            if self.Valid_Move(piece, "Right"):
                aux = deepcopy(self)
                aux.Make_Move(piece, "Right")
                New_States.append(aux)
        
        return New_States

    ''' Draw Matrix -> Methods '''

    def Show_Border_Pieces(self, screen, color, border_width):
        ''' Dada uma Cor é atribuiída uma borda para cada peça '''
        
        for (x,y) in self.red:
            # De Forma a que os contornos ficassem bem, estes foram feitos antes das linhas pretas de forma a que estas façam o devido acerto
            if (x + 1 < N_ROWS and self.matrix[x+1][y] != 1) or x + 1 == N_ROWS: # BAIXO - CONTORNOS
                pygame.draw.line(screen,RED_BORDER,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN - border_width), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN - border_width), border_width + 1)
            if (y + 1 < N_COLS and self.matrix[x][y+1] != 1) or y + 1 == N_COLS: # DIREITA - CONTORNOS
                pygame.draw.line(screen,RED_BORDER,(1.5*SQSIZE + y*SQSIZE + SQSIZE - border_width, .9*SQSIZE + x*SQSIZE + BOARD_DOWN + border_width - 1), (1.5*SQSIZE + y*SQSIZE + SQSIZE - border_width, .9*SQSIZE + x*SQSIZE +  SQSIZE + BOARD_DOWN), border_width + 1)
            
            if (x > 0 and self.matrix[x-1][y] != 1) or x == 0: # CIMA
                pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), border_width)
            if (y > 0 and self.matrix[x][y-1] != 1) or y == 0: # ESQUERDA
                pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN), border_width)
            if (y + 1 < N_COLS and self.matrix[x][y+1] != 1) or y + 1 == N_COLS: # DIREITA
                pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE +  SQSIZE + BOARD_DOWN), border_width)
            if (x + 1 < N_ROWS and self.matrix[x+1][y] != 1) or x + 1 == N_ROWS: # BAIXO
                pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN), border_width)

        for piece in self.others:
            for (x,y) in piece:
                if (x + 1 < N_ROWS and (self.matrix[x+1][y] != -1 or (x+1,y) not in piece)) or x + 1 == N_ROWS: # BAIXO - CONTORNOS
                    pygame.draw.line(screen,OTHER_BORDER,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN - border_width), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN - border_width), border_width + 1)
                if (y + 1 < N_COLS and (self.matrix[x][y+1] != -1 or (x,y+1) not in piece)) or y + 1 == N_COLS: # DIREITA - CONTORNOS
                    pygame.draw.line(screen,OTHER_BORDER,(1.5*SQSIZE + y*SQSIZE + SQSIZE - border_width, .9*SQSIZE + x*SQSIZE + BOARD_DOWN + border_width - 1), (1.5*SQSIZE + y*SQSIZE + SQSIZE - border_width, .9*SQSIZE + x*SQSIZE +  SQSIZE + BOARD_DOWN), border_width + 1)
            
                if (x > 0 and (self.matrix[x-1][y] != -1 or (x-1,y) not in piece)) or x == 0: # CIMA
                    pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), border_width)
                if (x + 1 < N_ROWS and (self.matrix[x+1][y] != -1 or (x+1,y) not in piece)) or x + 1 == N_ROWS: # BAIXO
                    pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN), border_width)
                if (y > 0 and (self.matrix[x][y-1] != -1 or (x,y-1) not in piece)) or y == 0: # ESQUERDA
                    pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + SQSIZE + BOARD_DOWN), border_width)
                if (y + 1 < N_COLS and (self.matrix[x][y+1] != -1 or (x,y+1) not in piece)) or y + 1 == N_COLS: # DIREITA
                    pygame.draw.line(screen,color,(1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN), (1.5*SQSIZE + y*SQSIZE + SQSIZE, .9*SQSIZE + x*SQSIZE +  SQSIZE + BOARD_DOWN), border_width)
    
    def Draw_Matrix(self, screen):
        ''' Shows the Board within the game's graphical interface '''
        screen.fill(BG_COLOR)

        # Creates the Border Around the Board
        pygame.draw.rect(screen,EXTERIOR_BORDER_COLOR, (1.5*SQSIZE - (BOARD_DOWN/2), .9*SQSIZE - (BOARD_DOWN/2) + BOARD_DOWN, SQSIZE*N_COLS + BOARD_DOWN, SQSIZE*N_ROWS + BOARD_DOWN),0,10)
        pygame.draw.rect(screen,BORDER_COLOR, (1.5*SQSIZE - (BOARD_DOWN/4), .9*SQSIZE - (BOARD_DOWN/4) + BOARD_DOWN, SQSIZE*N_COLS + (BOARD_DOWN/2), SQSIZE*N_ROWS + BOARD_DOWN - (BOARD_DOWN/2)),0,5)    

        for x in range(N_ROWS):
            for y in range(N_COLS):
                if self.matrix[x][y] == 1:
                    pygame.draw.rect(screen,RED_COLOR,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN , SQSIZE, SQSIZE))
                
                elif self.matrix[x][y] == -1:
                    pygame.draw.rect(screen,OTHER_COLOR,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN , SQSIZE, SQSIZE))

                elif self.matrix[x][y] == 0:
                    pygame.draw.rect(screen,BLANK_COLOR,(1.5*SQSIZE + y*SQSIZE, .9*SQSIZE + x*SQSIZE + BOARD_DOWN , SQSIZE, SQSIZE))

        # Creates Simple Circles to mark the objective position
        for (x,y) in self.objective:
            if self.matrix[x][y] == 0: # Big Circle
                pygame.draw.circle(screen, CIRCLE_COLOR, (1.5*SQSIZE + y*SQSIZE + SQSIZE/2, .9*SQSIZE + x*SQSIZE + SQSIZE/2 + BOARD_DOWN), SQSIZE/8, 100)
            elif self.matrix[x][y] == -1: # Small Circle
                pygame.draw.circle(screen, CIRCLE_COLOR, (1.5*SQSIZE + y*SQSIZE + SQSIZE/2, .9*SQSIZE + x*SQSIZE + SQSIZE/2 + BOARD_DOWN), 5, 20)
            
        self.Show_Border_Pieces(screen, BLACK, 3)

    def Write(self, font, text, size, color, bg_color, bold, pos, screen):
        ''' Writes Text into the Screen '''
        letra = pygame.font.SysFont(font, size, bold)
        frase = letra.render(text, 1, color, bg_color)
        screen.blit(frase, pos)

    ''' Update Movement ->  Methods '''

    def Pixels_to_Coordenates(self, Position:tuple):
        ''' Converte a Posição do Rato numa Posição da Matriz '''
        y = (Position[0] - 1.5*SQSIZE)//SQSIZE
        x = (Position[1] - .9*SQSIZE - BOARD_DOWN)//SQSIZE
        return (x,y)

    def Clicked_Piece(self,Mouse_Pos:tuple):
        ''' Finds the Piece that was clicked on '''
        (x,y) = self.Pixels_to_Coordenates(Mouse_Pos)
        
        if (x,y) in self.red:
            return self.red

        for piece in self.others:
            if (x,y) in piece:
                return piece
        return None

    def Movement_Dir(self, Initial:tuple=(0,0), Final:tuple=(0,0)):
        ''' Dadas as Coordenadas de 2 Posições, facilmente se obtém o vetor com a direção da peça '''
        xi,yi = self.Pixels_to_Coordenates(Initial)
        xf,yf = self.Pixels_to_Coordenates(Final)
        x = xf-xi
        y = yf-yi
        return (x,y)

    def Vetor_To_Movement(self, piece:list[tuple], vetor:tuple=(0,0)):
        ''' Translates the Movement vector into an actual move of the piece '''
        (move_x, move_y) = vetor
        
        if move_x >= 1:
            self.Make_Move(piece, "Down")
            move_x -= 1
        
        elif move_x <= -1:
            self.Make_Move(piece, "Up")
            move_x += 1
        
        elif move_y >= 1:
            self.Make_Move(piece, "Right")
            move_y -= 1

        elif move_y <= -1:
            self.Make_Move(piece, "Left")
            move_y += 1
        
        return (move_x,move_y)

    ''' Game Changing Methods '''

    def Is_Over(self):
        ''' Verifies if the level has reached an objective state'''
        for (x,y) in self.objective:
            if self.matrix[x][y]!=1:
                return False
        return True
    
    def Reset_Level(self):
        ''' Resets the current Level '''
        self.__init__(self.inicial_red, self.initial_others, self.objective, self.inicial_Tests)

    def Print_Solving(self, screen, wait_time):
        ''' Escreve em Ambiente Gráfico 'Solving...' '''
        solving_step = 0
        pos = (270,30)
        
        if solving_step == 0:
            self.Write('Arial', " Solving .   ", 40, WHITE, None, False, pos, screen)
            solving_step += 1
            time.sleep(wait_time)
            pygame.display.update()
        if solving_step == 1:
            self.Write('Arial', " Solving ..  ", 40, WHITE, None, False, pos, screen)
            solving_step += 1
            time.sleep(wait_time)
            pygame.display.update()
        if solving_step == 2:
            self.Write('Arial', " Solving ... ", 40, WHITE, None, False, pos, screen)
            time.sleep(wait_time)
            pygame.display.update()

    def Get_Solution(self, Node):
        ''' Returns a List of Nodes with the Moves towards a solution'''
        Res_Nodes = []
        while(Node.parent != None):
            Res_Nodes.insert(0, Node)
            Node = Node.parent
        return Res_Nodes

    def Show_Solution(self, Node, screen):
        ''' Solves the Problem within the graphical application '''
        Res_Nodes = self.Get_Solution(Node)
        for node in Res_Nodes:
            self.red = node.state.red
            self.others = node.state.others
            
            self.Update_Matrix()
            
            self.move_history.append(self.matrix)
            self.Draw_Matrix(screen)
            
            pygame.display.update()
            self.Print_Solving(screen, .3)
            time.sleep(.1)
        
        return True

    def Solve_It(self, screen):
        ''' Solves the Level with a certain search algorithm '''
        # goal, nodes = A_Star_Search_Node(self, h1)
        goal, nodes = A_Star_Search_Node(self, h2)        
        self.Show_Solution(goal, screen)
        return True

    def Get_Functions_Specs(self):
        ''' Adds the Specifications of all Funtions '''
        if self.Tests[0]:
            start = time.time()
            res, nodes_explored = Bfs_Node(self)
            end = time.time()
            self.Times[0] = round(end-start,3)
            self.Steps[0] = len(self.Get_Solution(res))
            self.Nodes_Explored[0] = nodes_explored

        if self.Tests[1]:
            start = time.time()
            res, nodes_explored = Limited_Iterative_Deepening_Node(self, MAX_DEPTH_SEARCH)
            end = time.time()
            self.Times[1] = round(end-start,3)
            self.Steps[1] = len(self.Get_Solution(res))
            self.Nodes_Explored[1] = nodes_explored
        
        if self.Tests[2]:
            start = time.time()
            res, nodes_explored = Greedy_Search_Node(self, h1)
            end = time.time()
            self.Times[2] = round(end-start,3)
            self.Steps[2] = len(self.Get_Solution(res))
            self.Nodes_Explored[2] = nodes_explored
        
        if self.Tests[3]:
            start = time.time()
            res, nodes_explored = Greedy_Search_Node(self, h2)
            end = time.time()
            self.Times[3] = round(end-start,3)
            self.Steps[3] = len(self.Get_Solution(res))
            self.Nodes_Explored[3] = nodes_explored
        
        if self.Tests[4]:
            start = time.time()
            res, nodes_explored = A_Star_Search_Node(self, h1)
            end = time.time()
            self.Times[4] = round(end-start,3)
            self.Steps[4] = len(self.Get_Solution(res))
            self.Nodes_Explored[4] = nodes_explored
        
        if self.Tests[5]:
            start = time.time()
            res, nodes_explored = A_Star_Search_Node(self, h2)
            end = time.time()
            self.Times[5] = round(end-start,3)
            self.Steps[5] = len(self.Get_Solution(res))
            self.Nodes_Explored[5] = nodes_explored

    def Run(self, Screen):
        ''' Initialize Pygame '''

        self.Get_Functions_Specs()

        ''' Buttons In Level '''
        Home_IMG = pygame.image.load('Assets/Home.png').convert_alpha()
        Home_Button = Button(Home_IMG, 50, 670, .15)

        Reset_ING = pygame.image.load('Assets/Reload.png').convert_alpha()
        Reset_Button = Button(Reset_ING, 230, 670, .15)

        Solve_IMG = pygame.image.load('Assets/Solve.png').convert_alpha()
        Solve_Button = Button(Solve_IMG, 400, 670, .15)

        Analyse_IMG = pygame.image.load('Assets/Analyse.png').convert_alpha()
        Analyse_Button = Button(Analyse_IMG, 550, 670, .15)

        Back_IMG = pygame.image.load('Assets/Back.png').convert_alpha()
        Back_Button = Button(Back_IMG, 50, 675, .15)

        ''' Run Loop '''
        Level_Menu = "Game"
        run = True
        flag = 0
        while run:
            
            if Level_Menu == "Game":
                self.Draw_Matrix(Screen)
                
                if Home_Button.Action(Screen):
                    # Goes Back to the Levels
                    pygame.time.wait(70)
                    run = False
                    
                if Reset_Button.Action(Screen):
                    self.Reset_Level()
                    system('cls')
                    print("\n\t#----------------------------------------------#")
                    print("\t| Please Wait while the level is being Reseted |")
                    print("\t#----------------------------------------------#")
                    self.Get_Functions_Specs()
                    system('cls')
                    print("\n\t#-----------------------------#")
                    print("\t| Reset Succeded -> Try Again |")
                    print("\t#-----------------------------#")

                if Solve_Button.Action(Screen):
                    if not self.completed:
                        self.Solve_It(Screen)
                    else:
                        print(" -> Already DONE ")

                if Analyse_Button.Action(Screen):
                    Level_Menu = "Analyse"

                # Atualiza se já chegou ao estado final
                self.completed = self.Is_Over()
                if self.Is_Over():
                    self.Write('Arial', " Congratulations !!! ", 30, WHITE, None, True, (234,20), Screen)
                    self.Write('Arial' , f" < Done in {len(self.move_history)} Steps > ", 25, WHITE, None, False, (254,60), Screen)
                    
            elif Level_Menu == "Analyse":
                Screen.fill(BG_COLOR)
                self.Write('Arial', " Algorithms Efficiency ", 40, WHITE, None, True, (180,40), Screen)
                
                self.Write('Arial',f" Algorithm ",35, BLUE, WHITE, False, (40,130), Screen)
                self.Write('Arial',f" Steps ",35, BLUE, WHITE, False, (210,130), Screen)
                self.Write('Arial',f" Nodes Explored ",35, BLUE, WHITE, False, (330,130), Screen)
                self.Write('Arial',f" Time ",35, BLUE, WHITE, False, (580,130), Screen)
                
                x_alg = 30
                x_steps = 235
                x_nodes_explored = 420
                x_time = 580
                
                y = 220
                y_interval = 80

                if self.Tests[0]:
                    aux = 20
                    self.Write('Arial',f" BFS ",25, WHITE, None, False, (x_alg+50,y-aux), Screen)
                    self.Write('Arial',f" {self.Steps[0]} ",30, WHITE, None, False, (x_steps,y-aux), Screen)
                    self.Write('Arial',f" {self.Nodes_Explored[0]} ",30, WHITE, None, False, (x_nodes_explored,y-aux), Screen)
                    self.Write('Arial',f" {self.Times[0]}s ",30, WHITE, None, False, (x_time,y-aux), Screen)
                    y += y_interval - 2*aux

                if self.Tests[1]:
                    self.Write('Arial',f" Itr Deepening ",25, WHITE, None, False, (x_alg+10,y), Screen)
                    self.Write('Arial',f" {self.Steps[1]} ",30, WHITE, None, False, (x_steps,y), Screen)
                    self.Write('Arial',f" {self.Nodes_Explored[1]} ",30, WHITE, None, False, (x_nodes_explored,y), Screen)
                    self.Write('Arial',f" {self.Times[1]}s ",30, WHITE, None, False, (x_time,y), Screen)
                    y += y_interval - 20
                
                if self.Tests[2]:
                    aux = 10
                    self.Write('Arial',f" Greedy Search ",25, WHITE, None, False, (x_alg+5,y), Screen)
                    self.Write('Arial',f" (H1) ",25, WHITE, None, False, (x_alg+55,y+30), Screen)
                    self.Write('Arial',f" {self.Steps[2]} ",30, WHITE, None, False, (x_steps,y+aux), Screen)
                    self.Write('Arial',f" {self.Nodes_Explored[2]} ",30, WHITE, None, False, (x_nodes_explored,y+aux), Screen)
                    self.Write('Arial',f" {self.Times[2]}s ",30, WHITE, None, False, (x_time,y+aux), Screen)
                    y += y_interval
                
                if self.Tests[3]:
                    aux = 10
                    self.Write('Arial',f" Greedy Search ",25, WHITE, None, False, (x_alg+5,y), Screen)
                    self.Write('Arial',f" (H2) ",25, WHITE, None, False, (x_alg+55,y+30), Screen)
                    self.Write('Arial',f" {self.Steps[3]} ",30, WHITE, None, False, (x_steps,y+aux), Screen)
                    self.Write('Arial',f" {self.Nodes_Explored[3]} ",30, WHITE, None, False, (x_nodes_explored,y+aux), Screen)
                    self.Write('Arial',f" {self.Times[3]}s ",30, WHITE, None, False, (x_time,y+aux), Screen)
                    y += y_interval
                
                if self.Tests[4]:
                    aux = 10
                    self.Write('Arial',f" A* Algorithm ",25, WHITE, None, False, (x_alg+15,y), Screen)
                    self.Write('Arial',f" (H1) ",25, WHITE, None, False, (x_alg+55,y+30), Screen)
                    self.Write('Arial',f" {self.Steps[4]} ",30, WHITE, None, False, (x_steps,y+aux), Screen)
                    self.Write('Arial',f" {self.Nodes_Explored[4]} ",30, WHITE, None, False, (x_nodes_explored,y+aux), Screen)
                    self.Write('Arial',f" {self.Times[4]}s ",30, WHITE, None, False, (x_time,y+aux), Screen)
                    y += y_interval
                
                if self.Tests[5]:
                    aux = 10
                    self.Write('Arial',f" A* Algorithm ",25, WHITE, None, False, (x_alg+15,y), Screen)
                    self.Write('Arial',f" (H2) ",25, WHITE, None, False, (x_alg+55,y+30), Screen)
                    self.Write('Arial',f" {self.Steps[5]} ",30, WHITE, None, False, (x_steps,y+aux), Screen)
                    self.Write('Arial',f" {self.Nodes_Explored[5]} ",30, WHITE, None, False, (x_nodes_explored,y+aux), Screen)
                    self.Write('Arial',f" {self.Times[5]}s ",30, WHITE, None, False, (x_time,y+aux), Screen)
                    y += y_interval

                if Back_Button.Action(Screen):
                    Level_Menu = "Game"
                    time.sleep(.1)
                
            ''' Event Loop '''
            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Initial_pos = event.pos
                    clicked_piece = self.Clicked_Piece(Initial_pos)
                
                # De forma a impedir erros ao transitar do menu dos Modos para o Nivel é importante que ao dar MOUSEBUTTONUP não dê logo trigger ao cálculo do movimento
                if event.type == pygame.MOUSEBUTTONUP and flag == 0:
                    flag = 1

                elif event.type == pygame.MOUSEBUTTONUP and flag == 1:
                    Final_pos = event.pos
                    move_vec = self.Movement_Dir(Initial_pos, Final_pos)
                    if clicked_piece:
                        while(move_vec != (0,0)):
                            move_vec = self.Vetor_To_Movement(clicked_piece, move_vec)

                if event.type == pygame.QUIT:
                    exit()
            
            pygame.display.update()
        system('cls')

''' TreeNode Class -> Used with Search Algorithms '''
class TreeNode:
    def __init__(self, state:Level, parent=None):
        self.state = state
        self.children = []
        self.parent = parent

    def Add_Child(self, child):
        child.parent = self
        self.children.append(child)

''' Search Algorithms '''

def Bfs_Node(initial_state:Level):
    ''' Breadth-First Search Algorithm using TreeNodes '''
    root = TreeNode(initial_state, None)
    queue = [root]
    visited = []
    nodes_explored = 0

    while queue:
        node = queue.pop(0)
        if node.state in visited: continue
        visited.append(node.state)
        
        if node.state.Is_Over():
            return node, nodes_explored
        
        nodes_explored += 1
        for new_state in node.state.New_States():
            if new_state not in visited:
                child = TreeNode(new_state, node)
                queue.append(child)
    return None, None

def Current_Depth(node:TreeNode):
    ''' Returns the Current Depth of a given Node '''
    depth = 0
    while node.parent != None:
        depth += 1
        node = node.parent
    return depth

def Limited_Iterative_Deepening_Node(initial_state:Level, Depth_limit:int):
    ''' Limited Iterative Deepening Search using TreeNodes '''
    # Para obter uma Iterative Deepening bastaria considerar a Profundidade Limite igual a infinito
    current_depth = 1
    nodes_explored = 0

    while current_depth < Depth_limit:
        root = TreeNode(initial_state, None)
        stack = [root]
        visited = set()

        while stack:
            current = stack.pop(0)
            if current.state in visited: continue
            visited.add(current.state)

            if current.state.Is_Over():
                return current, nodes_explored

            nodes_explored += 1

            # De forma a inserir os nós de forma correta usou-se uma variável auxiliar 'i'
            i = 0
            for new_state in current.state.New_States():
                if new_state not in visited:
                    child = TreeNode(new_state, current)
                    stack.insert(i,child)
                    i+=1

        current_depth += 1
    return None, None

def h1(state:Level):
    ''' Returns the manhattan distance from current position to it's final one'''
    final_pos = state.objective
    current_pos = state.red
    current_pos.sort()
    total = 0

    for i in range(len(final_pos)):
        dx = abs(current_pos[i][0] - final_pos[i][0])
        dy = abs(current_pos[i][1] - final_pos[i][1])
        total +=  dx + dy
        
    return total

def Check_Others_Piece(state:Level, pos:tuple):
    ''' Checks if in a certain positon of the board there is a 'others' piece '''
    return state.matrix[pos[0]][pos[1]] == -1

def Adjacent_Piece(state:Level, move:tuple):
    ''' Given a Move, this function verifies if there is an adjacent block in the move's direction'''
    if move[0] != 0 and move[1] != 0:
        (move_x, move_y) = (move[0]//abs(move[0]), move[1]//abs(move[1]))
    elif move[0] == 0 and move[1] != 0:
        (move_x, move_y) = (0, move[1]//abs(move[1]))
    elif move[0]!= 0 and move[1] == 0:
        (move_x, move_y) = (move[0]//abs(move[0]),0)
    else: # (move_x, move_y) = (0,0) -> The Piece does not move
        return False

    for (x,y) in state.red:
        if(Check_Others_Piece(state, (x+move_x,y+move_y))):
            return True
    return False

def h2(state:Level):
    ''' Similar to 'h1' but this function takes into consideration possible pieces that might block red's piece movement '''
    final = state.objective
    initial = state.red
    initial.sort()
    total = 0
    for i in range(len(final)):
        move = (final[i][0] - initial[i][0],
                final[i][1] - initial[i][1])
        
        dx = abs(move[0])
        dy = abs(move[1])
        
        if Adjacent_Piece(state, move):
            total +=  10*(dx + dy)
        else:
            total += dx+dy
        
    return total

def Greedy_Search_Node(initial_state:Level, heuristic):
    ''' Greedy-Search Algorithm using TreeNodes '''
    setattr(TreeNode, "__lt__", lambda self, other: heuristic(self.state) < heuristic(other.state))
    root = TreeNode(initial_state, None)
    states = [root]
    visited = set()
    nodes_explored = 0

    while states:
        current = heapq.heappop(states)
        if current.state in visited: continue
        visited.add(current.state)

        if current.state.Is_Over():
            return current, nodes_explored

        nodes_explored += 1

        for new_state in current.state.New_States():
            if (new_state not in visited):
                child = TreeNode(new_state, current)
                heapq.heappush(states, child)
    
    return None, None

def A_Star_Search_Node(initial_state:Level, heuristic):
    ''' A* Search Algorithm using TreeNodes '''
    return Greedy_Search_Node(initial_state, lambda state: (heuristic(state) + len(state.move_history) - 1))
