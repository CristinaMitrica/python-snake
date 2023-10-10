import sqlite3
conn = sqlite3.connect("mi_base_de_datos.db")
cursor = conn.cursor()
cursor.execute('DROP TABLE classifications')

# Crear una tabla (si no existe)
cursor.execute('''CREATE TABLE IF NOT EXISTS classifications (
    id INTEGER PRIMARY KEY,
    date TEXT,
    name TEXT,
    punctuation INTEGER
)''')



# Confirmar los cambios en la base de datos
conn.commit()

# Insertar datos en la tabla
data_to_insert = [
    ('2023-10-10 18:08:36', 'Juan Pérez', 30),
    ('2023-10-08 18:08:36', 'Maria Pérez', 50),
    ('2023-10-09 18:08:36', 'Miguel Pérez', 120)
]
cursor.executemany("INSERT INTO classifications (date, name, punctuation) VALUES (?, ?, ?)", data_to_insert)
# Confirmar los cambios
conn.commit()




#Versión Nueva =)
#snake+ premium enterprise

#region Librerias
from abc import ABC, abstractmethod
import datetime
from functools import reduce
import random
import keyboard
import os
import time
#endregion

#region Manzana

class Objeto(ABC): #Abstract no usado aun
    def __init__(self, skin, posX, posY, scoreGiven):
        self.skin = skin
        self.scoreGiven = scoreGiven
        self.posX = posX
        self.posY = posY

    #Elige y posiciona al objeto en la matriz del Background 
    def respawn(self, bg):
        newPosX, newPosY = random.randint(0, bg.height - 1), random.randint(0, bg.width - 1)

        #Comprueba si la posición esta vacia
        while bg.isEmpty(newPosX, newPosY) != True:
            newPosX, newPosY = random.randint(0, bg.height - 1), random.randint(0, bg.width - 1)
        
        self.posX, self.posY = newPosX, newPosY
        bg.mtx[newPosX][newPosY] = self.skin

    #Cuando Snake toca al objeto es llamada
    @abstractmethod
    def isEaten(self, bg, totalScore):
        pass

class ObjetoBueno(Objeto):
    randomRanges = (0, 2)

    def __init__(self, skin,posX, posY, scoreGiven = 5):
        super().__init__(skin, posX, posY, scoreGiven)

    def isEaten(self, bg, totalScore):
        self.respawn(bg)
        return totalScore + int(self.scoreGiven*random.randint(self.randomRanges[0], self.randomRanges[1]))
    
class ObjetoMalo(Objeto):
    def __init__(self, skin, posX, posY, scoreGiven = -5):
        super().__init__(skin, posX, posY, scoreGiven)

    def isEaten(self, bg, totalScore):
        self.respawn(bg)
        return totalScore + self.scoreGiven
#endregion

#region Snake
class Snake:
    lastPositions = []
    def __init__(self, posX, posY, headSkin='🔶', tailSkin='⬛', length=3, lifes=6):
        self.posX = posX
        self.posY = posY
        self.headSkin = headSkin
        self.tailSkin = tailSkin
        self.longitud = length
        self.__lifes = lifes
        self.lastDirection = 0

    @property
    def getLifes(self):
        return self.__lifes
    
    @getLifes.setter
    def setLifes(self, newLife):
        self.__lifes = newLife
#endregion

#region Background
class Background:
    mtx = []
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.printBackground()

    def startBackground(self):
        self.mtx = [['⬜' for i in range(self.width)] for a in range(self.height)]

    def printBackground(self):
        for i in self.mtx:
            for a in i:
                print(a, end='')
            print()

    #Devuelve si la posicion esta vacia
    def isEmpty(self, posX, posY):
        if self.mtx[posX][posY] == '⬜':
            return True
        return False
#endregion

#region Game
class Game:
    def __init__(self, bg, snake, goodItem, badItem, totalScore = 0):
        self.bg = bg
        self.snake = snake
        self.goodItem = goodItem
        self.badItem = badItem
        self.totalScore = totalScore
        self.gameStarted = False

    #El unico personaje que se mueve es el Snake, aqui solo accederá cuando esta colisione con algo
    #En función haya colisionado con qué, irá hacia un sitio u otro
    def checkColisions(self):
            colorToCheck = self.bg.mtx[self.snake.posX][self.snake.posY]
            if colorToCheck != '⬜':
                if colorToCheck == '⬛':
                    self.snake.setLifes = self.snake.getLifes - 1
                elif colorToCheck == '🌞':
                    self.totalScore = self.goodItem.isEaten(self.bg, self.totalScore)
                    self.snake.setLifes = self.snake.getLifes + 1
                elif colorToCheck == '🥦':
                    self.totalScore = self.badItem.isEaten(self.bg, self.totalScore)
                    self.snake.setLifes = self.snake.getLifes - 1

    #Se llama antes de el juego para inicializar/reinicializar variables
    def startGame(self):  
        self.gameStarted = True
        for i in range(6):
            self.snake.lastPositions.append([4, 14 - i])

        self.bg.startBackground()
        
        self.bg.mtx[self.snake.posX][self.snake.posY] = self.snake.headSkin
        for i in self.snake.lastPositions:
            self.bg.mtx[i[0]][i[1]] = self.snake.tailSkin
        
        self.goodItem.respawn(self.bg)
        self.badItem.respawn(self.bg)

        self.bg.printBackground()

    #Bucle del juego
    def onGame(self):
        keyPressed = False
        sameMove = False
        while self.gameStarted:
            if keyPressed:
                #Restart
                os.system('cls' if os.name == 'nt' else "printf '\033c'")

                self.bg.startBackground()
                self.bg.mtx[self.goodItem.posX][self.goodItem.posY] = self.goodItem.skin
                self.bg.mtx[self.badItem.posX][self.badItem.posY] = self.badItem.skin
                
                #Cola
                if self.snake.lastPositions[0] and sameMove is False:
                    self.snake.lastPositions.insert(0, [self.snake.posX, self.snake.posY])
                    
                    while len(self.snake.lastPositions) >= self.snake.getLifes:
                        self.snake.lastPositions = self.snake.lastPositions[:-1]

                    for i in self.snake.lastPositions:
                        self.bg.mtx[i[0]][i[1]] = self.snake.tailSkin

                #Movement
                #LastDirection Tiene que no permitir en la direccion contraria a la que se ha avanzado
                #Ej: si va hacia arriba, que no deje ir hacia abajo...
                if keyboard.is_pressed('d'):
                    if self.snake.lastDirection != 1:
                        if self.snake.posY + 1 < self.bg.width:
                            self.snake.posY += 1
                            self.snake.lastDirection = 3
                            sameMove = False
                    else:
                        sameMove = True
                elif keyboard.is_pressed('w'):
                    if self.snake.lastDirection != 2:
                        if self.snake.posX > 0:
                            self.snake.posX -= 1
                            self.snake.lastDirection = 4
                            sameMove = False
                    else:
                        sameMove = True                        
                elif keyboard.is_pressed('a'):
                    if  self.snake.lastDirection != 3:
                        if self.snake.posY > 0:
                            self.snake.posY -= 1
                            self.snake.lastDirection = 1
                            sameMove = False
                    else:
                        sameMove = True
                elif keyboard.is_pressed('s'):
                    if self.snake.lastDirection != 4:    
                        if self.snake.posX + 1 < self.bg.height:
                            self.snake.posX += 1
                            self.snake.lastDirection = 2
                            sameMove= False
                    else:
                        sameMove = True
                    
                self.checkColisions()

                for i in self.snake.lastPositions:
                    self.bg.mtx[i[0]][i[1]] = self.snake.tailSkin
                self.bg.mtx[self.snake.posX][self.snake.posY] = self.snake.headSkin  
                self.bg.printBackground()
                print('puntuacion:', self.totalScore)
                print('Vidas:', self.snake.getLifes - 1)
                
                if self.snake.getLifes <= 1 or self.totalScore >= 100:
                    if self.snake.getLifes <= 1:
                        print('Game Over 💀')
                    else:
                        print('You Win 🎉')
                    userName = input('Introduce tu nombre ')

                    if userName == ' ':
                        userName == 'lostName'

                    classification = Classification()
                    classification.addUserClassification(userName, self.totalScore)
                    self.gameStarted = False
                
                time.sleep(0.2)
                
            if keyboard.is_pressed('d') or keyboard.is_pressed('w') or keyboard.is_pressed('a') or keyboard.is_pressed('s'):
                keyPressed = True
            else:
                keyPressed = False
                time.sleep(0.2)
#endregion

#region OffGame
class Classification:
    def getClassifications(self): 
        # Consultar datos
        cursor.execute("SELECT * FROM classifications")
        # Recuperar los resultados
        classifications = cursor.fetchall()
        return classifications

    def getClassificationFromTxt(self):
        classification = ''
        try:
            with open('./classification.txt', 'r') as f:
                classification = f.read()
        except FileNotFoundError:
            print('No se encuentra el archivo "classification.txt" en la ubicación actual.')
            print('Para mostrar la clasificación, debes jugar al menos 1 vez.')
        return classification

    def printClassification(self):  
        classifications = self.mapClassifications() 
        for classification in classifications:
            print(f'id: {classification["id"]}, fecha: {classification["date"]}, nombre: {classification["name"]}, puntuacion: {classification["punctuation"]}')
  
   
    def addUserClassification(self, name, punctuation):
        dateTime = datetime.datetime.now()
        dateTimeFormated = dateTime.strftime('%Y-%m-%d %H:%M:%S')
        userEntryClassification = f'fecha: {dateTimeFormated}, nombre: {name}, puntuacion: {punctuation}\n'
        try:
            with open('./classification.txt', 'a') as f:
                f.write(userEntryClassification)
            print(f'Entrada agregada: {userEntryClassification}')
        except FileNotFoundError:
            print('No se encuentra el archivo "classification.txt" en la ubicación actual.')

    def mapClassifications(self):
        classifications = self.getClassifications()
        formatted_classifications = list(map(lambda x: {'id': x[0], 'date': x[1], 'name': x[2], 'punctuation': x[3]}, classifications))
        return formatted_classifications

    def getHigherScores(self):
        mapClassification = self.mapClassifications()
        higherScores = list(filter(lambda x: int(x['punctuation']) >= 100, mapClassification))

        for i in higherScores:
            print(f'{i["name"]} - {i["punctuation"]}')

    def calculateMeanPunctuations(self):
        map_classification = self.mapClassifications()
        sum_punctuations = reduce(lambda x, y: x + int(y['punctuation']), map_classification, 0)
        length_punctuations = len(map_classification) if len(map_classification) > 0 else 1
        mean_punctuations = int(sum_punctuations) / int(length_punctuations)
        print(f'Media de las puntuaciones: {mean_punctuations:.2f}')

    def getUsers(self):
        mapClassification = self.mapClassifications()
        users = list(map(lambda x: x['name'], mapClassification))
        uniqueUsernames = set(users)

        print('Lista de jugadores: ',)
        for i in uniqueUsernames:
            print(i)
  
class Menu: 
    def __init__(self):
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        
    def printMenu(self):
        print('\nBienvenido al juego del Snake:')
        print('\nMenú:')
        print('1. Jugar partida')
        print('2. Ver clasificación')
        print('3. Mostrar jugadores puntuacion superior a 100')
        print('4. Mostrar media puntos todos los jugadores')
        print('5. Mostrar lista jugadores')
        print('6. Instrucciones del juego')
        print('7. Salir')
    
    def initMenu(self):
        while True:
            self.printMenu()
            opcion = input('\nSeleccione una operación (1/2/3/4/5/6/7): ')
            classification = Classification()
            if opcion == '1':
                g = Game(Background(20, 10), Snake(4, 15), ObjetoBueno('🌞', random.randint(0, 9), random.randint(0, 19)), ObjetoMalo('🥦', random.randint(0, 9), random.randint(0, 19)))
                g.startGame()
                g.onGame()
            elif opcion == '2':
                classification.printClassification()

            elif opcion == '3':
                classification.getHigherScores()

            elif opcion == '4':
                classification.calculateMeanPunctuations()

            elif opcion == '5':
                classification.getUsers()

            elif opcion == '6':
                print(
                    '\nInstrucciones del juego:\n'
                    '🐍 El juego consiste en mover la serpiente con las teclas ''a'', ''w'', ''s'' y ''d''.\n'
                    '💗 Empiezas con 5 vidas.\n'
                    '- Al comer un sol, se aumenta la vida 1 punto y la puntuación de 0 a 10 puntos aleatoriamente.\n'
                    '- Al comer un brócoli, se reduce la vida 1 punto y la puntuación de 5 a 10 puntos aleatoriamente, y la cola de la serpiente disminuye.\n'
                    '- Al chocar contra las paredes, pierdes 1 vida = pierdes 1 punto de la cola.\n'
                    '- Si te cruzas con la cabeza encima de la cola, pierdes 1 vida = pierdes 1 punto de la cola.\n'
                    '💀 Pierdes al quedarte sin vidas.\n'
                    '🎉 Ganas al superar los 100 puntos.\n'
                )

            elif opcion == '7':
                conn.close()
                break

            else:
                input('Opción no existe, introduce una opción correcta: ')
#endregion

menu = Menu()
menu.initMenu()