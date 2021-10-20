import sys
import os
from array import *

class Sudoku(object):
    path = ''
    isOpen = False
    board = [[0 for i in range(9)] for j in range (9)]
    
    
    def printBoard(self):
        print("Printing board:")
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end = ' ')
            print('')
    
    
    def loadBoard(self, path):
        if(path == None):
            print("loadBoard: no 'file' argument given, terminating.")
            return 0
        
        print("Loading file.")
        file = open(path, 'r')
        lines = file.readlines()
        
        row = 0
        for line in lines:
            line = line.strip()
            
            col = 0
            for a in line:
                self.board[row][col] = int(a)
                col+=1
  
            row += 1
            

        print("Done. Closing " + path)
        file.close()
        return True
    
    
    def possibleValues(board, row, col):
        usedValues = 
    
    def _solve(self, board):
        blank_row = -1
        blank_col = -1
        
        for i in range(9):
            for j in range(9):
                if board[j][j] == 0 :
                    blank_row = i
                    blank_col = j
                    break
            if blank_row != -1:
                break
        
        if blank_row == -1:
            self.printBoard()
            # write board
            return True
    
    def solve(self):
        self._solve(self.board)
    
    
    def __init__(self, path=''):
        if(os.path.exists(path) == False):
            print("File '" + path + "' does not exist.")
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
        

def main():
    # if(len(sys.argv) != 2):
    #     print("No arguments given.")
    #     print("Usage:\n$ python sudoku.py [file path]")
    #     return 0
    
    #sudoku = Sudoku(sys.argv[1])
    sudoku = Sudoku("test.txt")
    sudoku.printBoard()
    
    return 0


if __name__ == "__main__":
    main()

# steps:
# read command line arg
# print command line arg
# read file
# print file content
# turn content into board data
# print board data in a readable manner
