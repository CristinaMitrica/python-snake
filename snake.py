
#Versión Nueva =)
#snake+ premium enterprise

#region Librerias
from abc import ABC, abstractmethod
import datetime
import random
import keyboard
import os
import time
#endregion

#region Manzana

class Objeto(ABC): #Abstract no usado aun
    def __init__(self, aspecto, posicionX, posicionY, puntuacionADar):
        self.aspecto = aspecto
        self.puntuacionADar = puntuacionADar
        self.posicionX = posicionX
        self.posicionY = posicionY

    #Elige y posiciona al objeto en la matriz del Background 
    def Respawn(self, bg):
        newPosX, newPosY = random.randint(0, bg.height - 1), random.randint(0, bg.width - 1)

        #Comprueba si la posición esta vacia
        while bg.IsEmpty(newPosX, newPosY) != True:
            newPosX, newPosY = random.randint(0, bg.height - 1), random.randint(0, bg.width - 1)
        
        self.posicionX, self.posicionY = newPosX, newPosY
        bg.mtx[newPosX][newPosY] = self.aspecto

    #Cuando Snake toca al objeto es llamada
    def IsEaten(self, bg, puntuacionTotal):
        self.Respawn(bg)
        return puntuacionTotal + self.puntuacionADar

class ObjetoBueno(Objeto):
    def __init__(self, aspecto,posicionX, posicionY, puntuacionADar = 5):
        super().__init__(aspecto, posicionX, posicionY, puntuacionADar)

class ObjetoMalo(Objeto):
    def __init__(self, aspecto, posicionX, posicionY, puntuacionADar = -5):
        super().__init__(aspecto, posicionX, posicionY, puntuacionADar)
#endregion

#region Snake
class Snake:
    lastPositions = []
    def __init__(self, posicionX, posicionY, aspectoCabeza='🔶', aspectoCola='⬛', longitud=3, vidas = 3):
        self.posicionX = posicionX
        self.posicionY = posicionY
        self.aspectoCabeza = aspectoCabeza
        self.aspectoCola = aspectoCola
        self.longitud = longitud
        self.__vidas = vidas
        self.lastDirection = 0

    @property
    def GetVidas(self):
        return self.__vidas
    
    @GetVidas.setter
    def SetVidas(self, nuevaVida):
        self.__vidas = nuevaVida

#endregion

#region Background
class Background:
    mtx = []
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.PrintBackground()


    def StartBackground(self):
        self.mtx = [['⬜' for i in range(self.width)] for a in range(self.height)]

    def PrintBackground(self):
        for i in self.mtx:
            for a in i:
                print(a, end='')
            print()

    #Devuelve si la posicion esta vacia
    def IsEmpty(self, posX, posY):
        if self.mtx[posX][posY] == '⬜':
            return True
        return False
#endregion

#region Game
class Game:

    def __init__(self, bg, snake, goodItem, badItem, puntuacionTotal = 0):
        self.bg = bg
        self.snake = snake
        self.goodItem = goodItem
        self.badItem = badItem
        self.puntuacionTotal = puntuacionTotal

    #El unico personaje que se mueve es el Snake, aqui solo accederá cuando esta colisione con algo
    #En función haya colisionado con qué, irá hacia un sitio u otro
    def CheckColisions(self):
            colorToCheck = self.bg.mtx[self.snake.posicionX][self.snake.posicionY]
            if colorToCheck != '⬜':
                if colorToCheck == '⬛':
                    self.snake.SetVidas = self.snake.GetVidas - 1
                elif colorToCheck == '🌞':
                    self.puntuacionTotal = self.goodItem.IsEaten(self.bg, self.puntuacionTotal)
                    self.snake.SetVidas = self.snake.GetVidas + 1
                elif colorToCheck == '🥦':
                    self.puntuacionTotal = self.badItem.IsEaten(self.bg, self.puntuacionTotal)
                    self.snake.SetVidas = self.snake.GetVidas - 1

    #Se llama antes de el juego para inicializar/reinicializar variables
    def StartGame(self):  
        for i in range(6):
            self.snake.lastPositions.append([4, 14 - i])

        self.bg.StartBackground()
        
        self.bg.mtx[self.snake.posicionX][self.snake.posicionY] = self.snake.aspectoCabeza
        for i in self.snake.lastPositions:
            self.bg.mtx[i[0]][i[1]] = self.snake.aspectoCola
        
        self.goodItem.Respawn(self.bg)
        self.badItem.Respawn(self.bg)

        self.bg.PrintBackground()

    #Bucle del juego
    def onGame(self):
        tecla_presionada = False
        while True:
            if tecla_presionada:
                #Restart
                os.system('cls' if os.name == 'nt' else 'clear')
                self.bg.StartBackground()
                self.bg.mtx[self.goodItem.posicionX][self.goodItem.posicionY] = self.goodItem.aspecto
                self.bg.mtx[self.badItem.posicionX][self.badItem.posicionY] = self.badItem.aspecto
                
                #Cola
                self.snake.lastPositions.insert(0, [self.snake.posicionX, self.snake.posicionY])
                
                while len(self.snake.lastPositions) >= self.snake.GetVidas:
                    self.snake.lastPositions = self.snake.lastPositions[:-1]

                for i in self.snake.lastPositions:
                    self.bg.mtx[i[0]][i[1]] = self.snake.aspectoCola

                #Movement
                #LastDirection Tiene que no permitir en la direccion contraria a la que se ha avanzado
                #Ej: si va hacia arriba, que no deje ir hacia abajo...
                if keyboard.is_pressed('d') and self.snake.lastDirection != 1:
                    if self.snake.posicionY + 1 < self.bg.width:
                        self.snake.posicionY += 1
                        self.snake.lastDirection = 3
                elif keyboard.is_pressed('w') and self.snake.lastDirection != 2:
                    if self.snake.posicionX > 0:
                        self.snake.posicionX -= 1
                        self.snake.lastDirection = 4
                elif keyboard.is_pressed('a') and self.snake.lastDirection != 3:
                    if self.snake.posicionY > 0:
                        self.snake.posicionY -= 1
                        self.snake.lastDirection = 1
                elif keyboard.is_pressed('s') and self.snake.lastDirection != 4:
                    if self.snake.posicionX + 1 < self.bg.height:
                        self.snake.posicionX += 1
                        self.snake.lastDirection = 2
                    
                self.CheckColisions()

                self.bg.mtx[self.snake.posicionX][self.snake.posicionY] = self.snake.aspectoCabeza            
                for i in self.snake.lastPositions:
                    self.bg.mtx[i[0]][i[1]] = self.snake.aspectoCola

                self.bg.PrintBackground()
                print('Puntuación:', self.puntuacionTotal)
                print('Vidas:', self.snake.GetVidas)

                time.sleep(0.2)
                
            if keyboard.is_pressed('d') or keyboard.is_pressed('w') or keyboard.is_pressed('a') or keyboard.is_pressed('s'):
                tecla_presionada = True
            else:
                tecla_presionada = False
                time.sleep(0.2)
#endregion

class Classification:
    def __init__(self):
        pass

    def print_classification(self):
        try:
            with open('.\classification.txt', 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print('No se encuentra el archivo "classification.txt" en la ubicación actual.')

    def add_user_classification(self, name, punctuation):
        date_time = datetime.datetime.now()
        date_time_formated = date_time.strftime('%Y-%m-%d %H:%M:%S')
        
        user_entry_classification = f'fecha: {date_time_formated}: nombre: {name} - puntuación: {punctuation}\n'
        try:
            with open('.\classification.txt', 'a') as f:
                f.write(user_entry_classification)
                print(f'Entrada agregada: {user_entry_classification}')
        except FileNotFoundError:
            print('No se encuentra el archivo "classification.txt" en la ubicación actual.')
       
class Menu: 
    def __init__(self):
        pass

    def print_menu(self):
        print('\nMenú:')
        print('1. Jugar partida')
        print('2. Ver clasificación')
        print('3. Salir')
    
    def init_menu(self):
        while True:
            self.print_menu()
            opcion = input('Seleccione una operación (1/2/3): ')

            if opcion == '1':
                g = Game(Background(20, 10), Snake(4, 15), ObjetoBueno('🌞', random.randint(0, 9), random.randint(0, 19)), ObjetoMalo('🥦', random.randint(0, 9), random.randint(0, 19)))
                g.StartGame()
                g.onGame()
                pass

            elif opcion == '2':
                classification = Classification()
                classification.print_classification()

            elif opcion == '3':
                break

            else:
                input('Opción no existe, introduce una opción correcta: ')

menu = Menu()
menu.init_menu()