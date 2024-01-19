import pygame
import time

class Image:
    def __init__(self, image, x, y, scale):
        self.Height = image.get_height()
        self.Width = image.get_width()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(self.Width*self.scale), int(self.Height*self.scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def Display(self, Tela):
        Tela.blit(self.image, (self.rect.x, self.rect.y))

class Button:
    def __init__(self, image, x, y, scale):
        self.Height = image.get_height()
        self.Width = image.get_width()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(self.Width*self.scale), int(self.Height*self.scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.toggled = False

        self.FirstContact = 0
        self.NumContacts = 0


    def Action(self, Tela):
        Action = False
        Mouse_Pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(Mouse_Pos): # Se a posição do rato coincidir com a imagem do butão

            if pygame.mouse.get_pressed()[0] == 0: # Se o rato não estiver a clicar dentro da região do butão, então podemos dar reset à qtd de contactos
                self.clicked = False
                self.NumContacts = 0

            if (self.NumContacts == 0): # Verifica se é o primeiro contacto com o butão [e guarda o estado do rato (pressionado ou não)]
                self.FirstContact = (pygame.mouse.get_pressed()[0])

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if (self.FirstContact == 0): # Não entrou na área a clicar
                    self.clicked = True
                    Action = True
                
            self.NumContacts += 1 # Se o Rato se mantiver de cima do butão incrementa-se a qtd de contactos

        else: # Se a posição do rato estiver fora da imagem dá-se reset ao número de contactos
            self.NumContacts = 0

        Tela.blit(self.image, (self.rect.x, self.rect.y))
        return Action

    def Atual_State(self):
        return self.toggled
    
    def Switch_On_Off(self, Tela, On_IMG, Off_IMG):
        if self.Action(Tela):
            
            if self.toggled == False:
                self.__init__(On_IMG, self.rect.x, self.rect.y, self.scale)
                self.toggled = True
            
            elif self.toggled == True:
                self.__init__(Off_IMG, self.rect.x, self.rect.y, self.scale)
                self.toggled = False
            
            time.sleep(0.1)

    def Switch_Image(self, New_Image):
        ''' Only Works for specific transitions between images (Same Image, Different States) '''
        self.__init__(New_Image, self.rect.topleft[0],self.rect.topleft[1] ,self.scale)