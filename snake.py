#snake+ premium enterprise

#region Librerias
from abc import ABC, abstractmethod
import random
import keyboard
import os
import time
#endregion

#region Manzana

class Objeto(ABC): #Abstract no usado aun
    puntuacion = 0
    posicionX = 0
    posicionY = 0
    def _init_(self, aspecto, posicionX, posicionY, puntuacion):
        self.aspecto = aspecto
        self.puntuacion = puntuacion
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
        return puntuacionTotal + self.puntuacion

class ObjetoBueno(Objeto):
    def _init_(self, aspecto,posicionX, posicionY, puntuacion = 5):
        super()._init_(aspecto, posicionX, posicionY, puntuacion)

class ObjetoMalo(Objeto):
    def _init_(self, aspecto, posicionX, posicionY, puntuacion = -5):
        super()._init_(aspecto, posicionX, posicionY, puntuacion)
#endregion

#region Snake
class Snake:
    lastPositions = []
    def _init_(self, posicionX, posicionY, aspectoCabeza='🔶', aspectoCola='⬛', longitud=3, vidas = 3, puntuacionTotal = 0):
        self.posicionX = posicionX
        self.posicionY = posicionY
        self.aspectoCabeza = aspectoCabeza
        self.aspectoCola = aspectoCola
        self.longitud = longitud
        self.__vidas = vidas
        self.puntuacionTotal = puntuacionTotal

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
    def _init_(self, width, height):
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

    def _init_(self, bg, snake, goodItem, badItem):
        self.bg = bg
        self.snake = snake
        self.goodItem = goodItem
        self.badItem = badItem

    #El unico personaje que se mueve es el Snake, aqui solo accederá cuando esta colisione con algo
    #En función haya colisionado con qué, irá hacia un sitio u otro
    def CheckColisions(self):
            colorToCheck = self.bg.mtx[self.snake.posicionX][self.snake.posicionY]
            if colorToCheck != '⬜':
                if colorToCheck == '⬛':
                    pass
                elif colorToCheck == '🌞':
                    a = self.goodItem.IsEaten(self.bg, 0)
                elif colorToCheck == '🥦':
                    a = self.badItem.IsEaten(self.bg, 0)

    #Se llama antes de el juego para inicializar/reinicializar variables
    def StartGame(self):  
        for i in range(4):
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


                #lastMoveX = snake.posicionX
                #lastMoveY = snake.posicionY

                #Movement
                if keyboard.is_pressed('d'):
                    if self.snake.posicionY + 1 < self.bg.width:
                        self.snake.posicionY += 1
                elif keyboard.is_pressed('w'):
                    if self.snake.posicionX > 0:
                        self.snake.posicionX -= 1
                elif keyboard.is_pressed('a'):
                    if self.snake.posicionY > 0:
                        self.snake.posicionY -= 1
                elif keyboard.is_pressed('s'):
                    if self.snake.posicionX + 1 < self.bg.height:
                        self.snake.posicionX += 1

                #Cola
                #for i in snake.lastPositions:
                #    auxX = i[0]
                #    auxY = i[1]

                self.CheckColisions()

                self.bg.mtx[self.snake.posicionX][self.snake.posicionY] = self.snake.aspectoCabeza            
                for i in self.snake.lastPositions:
                    self.bg.mtx[i[0]][i[1]] = self.snake.aspectoCola

                self.bg.PrintBackground()
                print('Puntuación: 0')
                print('Vidas: 4')

                time.sleep(0.2)
                
            if keyboard.is_pressed('d') or keyboard.is_pressed('w') or keyboard.is_pressed('a') or keyboard.is_pressed('s'):
                tecla_presionada = True
            else:
                tecla_presionada = False
                time.sleep(0.2)
#endregion

g = Game(Background(20, 10), Snake(4, 15), ObjetoBueno('🌞', random.randint(0, 9), random.randint(0, 19)), ObjetoMalo('🥦', random.randint(0, 9), random.randint(0, 19)))

g.StartGame()
g.onGame()