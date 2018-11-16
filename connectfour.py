import pgzrun
from abc import ABC
import math

HEIGHT = 600
WIDTH = 800

class Field(ABC):
    def __init__(self):
        # Field initialisation: Which Players turn? How many cell have the Field? Which cells are yellow, red?
        self._actPlayer = True
        self._cells = [None] * 42  # array will be filled with True(Yellow)  False(Red)
        self._yellow = []  # array with cells numbers with yellow coins
        self._red = []  # array with cells numbers with red coins

    def getCells(self):  # [] _cells
        # returns current cells array
        return self._cells

    def getActPlayer(self):  # bool _actPlayer
        # returns current Player
        return self._actPlayer

    def _changePlayer(self): # from True to Fals
        # changes current Player
        self._actPlayer = not self._actPlayer

    def _dropCoin(self, column):
        # Sets coin by given column:
        # coin falls until he hits another coin(if) or the ground(elif)
        # _cells, _red, _yellow will be filled

        for x in range(1, 6):
            cell = column + x * 7

            if self._cells[cell] != None and self._cells[column] == None:  # until he hits another coin
                self._cells[cell - 7] = self.getActPlayer()
                if self.getActPlayer():
                    self._yellow.append(cell - 7)
                else:
                    self._red.append(cell - 7)
                self._changePlayer()
                break  # code outside for-loop

            elif x == 5 and self._cells[column] == None:  # until he hits the ground
                self._cells[cell] = self.getActPlayer()
                if self.getActPlayer():
                    self._yellow.append(cell)
                else:
                    self._red.append(cell)
                self._changePlayer()
                break  # code outside for-loop

    def _checkWinner(self):
        # Checks if there are four equal coins in a row according to the last set coin
        # returns Winner(True=Yellow, False=Red) if there is one

        # steps describes the difference between two cells to be in one line:
        # horizontal: 1 vertically: 7 diagonal_up: 6 diagonal_down: 8
        steps = [1, 7, 6, 8]

        # get last added coin and its position
        if len(self._red) == 0 and len(self._yellow) == 0:
            return
        elif self.getActPlayer():
            lastPos = self._red[len(self._red) - 1]         # last droped position
        else:
            lastPos = self._yellow[len(self._yellow) - 1]   # last droped position
        actCells = self._cells

        for i in steps:
            win = 1
            for x in range(1, 5):
                if lastPos + (i * x) < 42 and actCells[lastPos + (i * x)] == actCells[lastPos]:
                    # check if all cells in one row (horizontal)
                    if i == 1 and math.floor((lastPos + (i * x)) / 7) == math.floor(lastPos / 7):
                        win = win + 1
                    # check if all cells in successive rows
                    elif math.floor((lastPos + (i * x)) / 7) == math.floor(lastPos / 7) + x:
                        win = win + 1
                    else:
                        break
                else:
                    break
                if win == 4:
                    return actCells[lastPos]

            for x in range(1, 5):
                if lastPos - (i * x) > -1 and actCells[lastPos - (i * x)] == actCells[lastPos]:
                    if i == 1 and math.floor((lastPos - (i * x)) / 7) == math.floor(lastPos / 7):
                        win = win + 1
                    elif math.floor((lastPos - (i * x)) / 7) == math.floor(lastPos / 7) - x:
                        win = win + 1
                    else:
                        break
                else:
                    break
                if win == 4:
                    return actCells[lastPos]

    def _check4Row(self):
        firstCol = [7, 14, 21, 28, 35]
        lastCol = [6, 13, 20, 27, 34]
        if self.getActPlayer():
            lastPos = self._red[len(self._red) - 1]         # last droped position
        else:
            lastPos = self._yellow[len(self._yellow) - 1]   # last droped position
        actCells = self._cells
        anzahl  = 1

        while actCells[lastPos] == actCells[lastPos+1] and actCells[lastPos+1] not in firstCol:
            anzahl = anzahl + 1
            if anzahl == 4:
                return Winner

        while actCells[lastPos] == actCells[lastPos-1] and actCells[lastPos-1] not in lastCol:
            anzahl = anzahl + 1
            if anzahl == 4:
                return Winner
        return NoWinner


class GUI(Field):

    def __init__(self):
        Field.__init__(self)
        self._restart = Actor('restart', (40, 40))

    def _drawRed(self, cell):
        # draws a red coin in given cell
        y = 6 - math.ceil((cell + 1) / 7)
        x = cell - math.floor((cell) / 7) * 7
        rball = Actor('rball')
        rball.pos = (190 + x * 70, 600 - 100 - 30 - 70 * y)
        rball.draw()

    def _drawYellow(self, cell):
        # draws a yellow coin in given cell
        y = 6 - math.ceil((cell + 1) / 7)
        x = cell - math.floor((cell) / 7) * 7
        yball = Actor('yball')
        yball.pos = (190 + x * 70, 600 - 100 - 30 - 70 * y)
        yball.draw()

    def draw(self):
        # draws cell with current status

        # draw white screen
        screen.fill((200, 255, 255))

        # draw empty cells
        blue = 0, 50, 200
        box = Rect((150, 60), (HEIGHT - 100, 450))
        screen.draw.filled_rect(box, blue)

        # coin width = 60, space between = 10, startX = 190, startY = 470
        for y in range(0, 6):
            for x in range(0, 7):
                wball = Actor('wball')
                wball.pos = (150+10+30 + x * (60+10), HEIGHT - (90+10+30) - (60+10) * y)
                wball.draw()

        # draw coin appending to given cell
        for x in self._yellow:
            self._drawYellow(x)

        for x in self._red:
            self._drawRed(x)

        # give message if there is a winner
        if self._checkWinner() == False:
            screen.draw.text("Red won", (300, 10), color='red', background='yellow')
            self._restart.draw()
        elif self._checkWinner() == True:
            screen.draw.text("Yellow won", (300, 10), color='yellow', background='red')
            self._restart.draw()

    def clicked(self, pos):
        # as long as there is no winner add a coin to a column by clicking the column
        if self._checkWinner() != False and self._checkWinner() != True:
            for x in range(0, 7):
                if pos[1] > 85 and pos[1] < 600:  # column
                    if pos[0] > 160 + x * 70 and pos[0] < 220 + x * 70:
                        self._dropCoin(x)
        else:
            if self._restart.collidepoint(pos):
                self.__init__()

class KI(Field, opColor):
    _dropCoin
    

a = GUI()


def draw():
    a.draw()


def on_mouse_down(pos):
    a.clicked(pos)


pgzrun.go()
