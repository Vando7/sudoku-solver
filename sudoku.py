import sys
import os
from array import *
import threading


class Sudoku(object):
    path = ''
    isOpen = False
    board = [[0 for i in range(10)] for j in range(10)]


    def printBoard(self):
        if self.isOpen == False:
            print("No board loaded.")
            return
        self._printBoard(self.board)


    def _printBoard(self, board):
        for i in range(9):
            for j in range(9):
                if(j % 3 == 0 and j != 0):
                    print("| ", end='')
                print(board[i][j], end=' ')

            print('')
            if(i % 3 == 2 and i != 8):
                for j in range(21):
                    if(j == 6 or j == 14):
                        print('+', end='')
                    else:
                        print('-', end='')
                print('')


    def loadBoard(self, path):
        if(path == None):
            print("loadBoard: no 'file' argument given, closing.")
            return

        print("Loading file.")
        file = open(path, 'r')
        lines = file.readlines()

        row = 0
        for line in lines:
            line = line.strip()

            col = 0
            for a in line:
                self.board[row][col] = int(a)
                col += 1

            row += 1

        print("Done. Closing " + path)
        file.close()
        return True


    def cellValues(self, board):
        if self.isOpen == False:
            print("No board loaded.")
            return

        cells = [[0 for i in range(9)] for i in range(9)]

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    cells[i][j] = self.possibleValues(board, i, j)
                else:
                    cells[i][j] = []

        return cells


    def fillHiddenSingles(self, board):
        if self.isOpen == False:
            print("No board loaded.")
            return

        cells = self.cellValues(board)

        # Fill hidden singles per column
        cellChanged = True
        while cellChanged:
            cellChanged = False

            for i in range(9):
                countEncounters = [0 for z in range(10)]
                for j in range(9):
                    for k in range(len(cells[j][i])):
                        countEncounters[cells[j][i][k]] += 1+1-1

                hiddenSingles = []
                for j in range(10):
                    if countEncounters[j] == 1:
                        hiddenSingles.append(j)

                for value in hiddenSingles:
                    for j in range(9):
                        if(value in cells[j][i]):
                            board[j][i] = value
                            cells = self.cellValues(board)
                            cellChanged = True

        # Fill hidden singles per column
        cellChanged = True
        while cellChanged:
            cellChanged = False

            for j in range(9):
                countEncounters = [0 for z in range(10)]
                for i in range(9):
                    for k in range(len(cells[j][i])):
                        countEncounters[cells[j][i][k]] += 1

                hiddenSingles = []
                for i in range(10):
                    if countEncounters[i] == 1:
                        hiddenSingles.append(i)

                for value in hiddenSingles:
                    for i in range(9):
                        if(value in cells[j][i]):
                            board[j][i] = value
                            cells = self.cellValues(board)
                            cellChanged = True

        return


    def possibleValuesCol(self, board, col, usedValuesCol):
        for i in range(0, 9):
            if(board[i][col] != 0):
                usedValuesCol[board[i][col]] = 1
                
    
    def possibleValuesRow(self, board, row, usedValuesRow):
        for i in range(0, 9):
            if(board[row][i] != 0):
                usedValuesRow[board[row][i]] = 1


    def possibleValuesSqu(self, board, row, col, usedValuesSqu):
        quadrantRow = 1
        quadrantCol = 1

        if(row < 3):
            quadrantRow = 0
        if(row > 5):
            quadrantRow = 2
        quadrantRow *= 3

        if(col < 3):
            quadrantCol = 0
        if(col > 5):
            quadrantCol = 2
        quadrantCol *= 3

        for i in range(quadrantRow, quadrantRow+3):
            for j in range(quadrantCol, quadrantCol+3):
                if(board[i][j] != 0):
                    usedValuesSqu[board[i][j]] = 1


    def possibleValues(self, board, row, col):
        if self.isOpen == False:
            print("No board loaded.")
            return
        
        usedValuesRow = [0 for i in range(10)] #self.possibleValuesRow(board, row)
        usedValuesCol = [0 for i in range(10)] #self.possibleValuesCol(board, col)
        usedValuesSqu = [0 for i in range(10)] #self.possibleValuesSquare(board,row,col)
        
        thRow = threading.Thread(target=self.possibleValuesRow, args=(board, row, usedValuesRow))
        thCol = threading.Thread(target=self.possibleValuesCol, args=(board, col, usedValuesCol))
        thSqu = threading.Thread(target=self.possibleValuesSqu, args=(board, row, col, usedValuesSqu))
        
        thRow.start()
        thCol.start()
        thSqu.start()
        
        thRow.join()
        thCol.join()
        thSqu.join()
        
        usedValues = [0 for i in range(10)]
        for i in range(10):
            if(usedValuesRow[i]     == 1 or 
               usedValuesCol[i]     == 1 or 
               usedValuesSqu[i]     == 1):
                usedValues[i] = 1

        result = []
        for i in range(1, 10):
            if(usedValues[i] == 0):
                result.append(i)

        return result


    def _solve(self, board):
        if self.isOpen == False:
            print("No board loaded.")
            return

        blankRow = -1
        blankCol = -1

        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j] == 0:
                    blankRow = i
                    blankCol = j
                    break

            if blankRow != -1:
                break

        if blankRow == -1:
            print("Solved board:")
            self._printBoard(board)
            self.writeBoard()
            return True

        allowedValues = self.possibleValues(board, blankRow, blankCol)

        for i in range(0, len(allowedValues)):
            board[blankRow][blankCol] = allowedValues[i]

            if(self._solve(board)):
                return True

            board[blankRow][blankCol] = 0

        return False


    def solve(self):
        if self.isOpen == False:
            print("No board loaded.")
            return
        self._solve(self.board)


    def smart_solve(self):
        if self.isOpen == False:
            print("No board loaded.")
            return

        self.fillHiddenSingles(self.board)
        self._solve(self.board)


    def __init__(self, path=''):
        if(os.path.exists(path) == False):
            print("File '" + path + "' does not exist.")
            print("Note: make sure you've written the file extension as well.")
            return

        if(os.path.isdir(path)):
            print("File '" + path + "' is directory, not file.")
            return

        print("File '" + path + "' opened successfully.")

        if(self.loadBoard(path) == False):
            print("File '" + path + "' does not have exactly 9 lines.")
            return

        self.isOpen = True
        self.path = path


    def writeBoard(self):
        inputFileName = self.path.split('.')[0]
        print('\nWriting result to ' + inputFileName + '-solved.txt')

        resultFile = open(inputFileName + '-solved.txt', 'w')
        for i in range(9):
            for j in range(9):
                resultFile.write(str(self.board[i][j]))
            resultFile.write("\n")
        resultFile.close()
        print("Done, closing.")


def main():
    if(len(sys.argv) != 2):
        print("No arguments given.")
        print("Usage:\n$ python sudoku.py [file path]")
        return 0

    sudoku = Sudoku(sys.argv[1])

    if(sudoku.isOpen == False):
        return

    print("Input board:\n")
    sudoku.printBoard()
    print("\nSolving . . . \n")
    sudoku.smart_solve()

    return 0


if __name__ == "__main__":
    main()
