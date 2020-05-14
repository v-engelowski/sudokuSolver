import numpy as np
import pyautogui as py
from time import sleep
import cv2
import pytesseract
import os
import shutil
import threading

try:
        os.mkdir("Sudoku//img") #creates dir to store screenshots
except:
        print("Creation failed, directory probably already exists")

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"       #location of the "tesseract.exe" which is used to extract text from an image to a string

py.PAUSE = 0.001 #delay for py.* commands

yRows = [265,320,375,430,485,540,595,655,710]   #x and y coordinaets pointing to the middle of the tile
xRows = [390,445,500,555,610,665,720,775,830]

yBox = [241,296,352,408,462,517,573,627,682]    #x and y coordinates for the upper left most corner of a tile
xBox = [364,419,474,530,584,639,695,749,804]

grid = [[None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None]]    #9x9 sudoku grid


def getGrid():  #takes a screenshot of every tile and converts it to string
        global grid

        py.hotkey("alt","tab")  #switch windows to the puzzle
        sleep(0.25)     #wait before taking screenshot

        index = 0

        for y in yBox:
                for x in xBox:
                        py.screenshot("Sudoku//img//grid" + str(index) + ".png",(x,y,53,53))    #takes a screenshot in specified region (x,y,width,depth) and saves it as "grid.."
                        index = index + 1

        py.hotkey("alt","tab")  #switch back to this window

        threads = []

        for i in range(9):
                t = threading.Thread(target=scanImgThread, args=(i,))
                threads.append(t)
        
        for i in threads:
                i.start()
        
        for i in threads:
                i.join()

        #sleep(0.25)
        py.hotkey("alt","tab")  #switch back to the puzzle
        sleep(0.25)


def scanImgThread(row):
                global grid
                ind = row * 9

                for j in range(0,9):      #i and j are the numbers used to wirte to the grid array. i=0 and j=0 is the very first entry, i=0 and j=1 is the second entry of the first row and so on..
                        img = cv2.imread("Sudoku//img//grid" + str(ind) + ".png")
                        text = pytesseract.image_to_string(img,lang="eng", config ="--psm 10")  #--psm 10 determines that the whole file is one character

                        if text == "":  #if the text is empty, it's empty, therefor 0
                                grid[row][j] = 0
                        else:
                                grid[row][j] = int(text)

                        ind = ind + 1
                        os.system("cls")
                        print(np.matrix(grid))  #prints the grid to show the user the progress


def checkGrid(y,x,n):
        global grid

        for i in range(0,9):
                if grid[y][i] == n:     #if the number n already exists in the row or collumn = False
                        return False

        for i in range(0,9):    #see above
                if grid[i][x] == n:
                        return False

        x0 = (x//3) * 3
        y0 = (y//3) * 3

        for i in range(0,3):    #check if n is in 3x3 grid
                for j in range(0,3):
                        if grid[y0 + i][x0+ j] == n:    #if it is, False
                                return False

        return True


def solveGrid():        #moves the mouse to each tile, clicks it, and inputs the number that is supposed to go there
        i = -1

        for y in yRows:
                i = i + 1
                j = 0
                for x in xRows:
                        number = str(grid[i][j])        #reads the number that goes there

                        j = j + 1
                        py.moveTo(x,y)
                        py.leftClick()
                        py.press(number)        #inputs number


def solve():
        global grid

        for y in range(9):
                for x in range(9):
                        if grid[y][x] == 0:     #if the spot on the grid is empty
                                for n in range(1,10):   #check if "n" fits by calling checkGrid()
                                        if checkGrid(y,x,n):    #if it does, write it down
                                                grid[y][x] = n
                                                solve()         #restart this funtion until all spots are filels
                                                grid[y][x] = 0  #if it doesn't fit, go back one step and input another number

                                return
        print(np.matrix(grid))  #prints the solution for the puzzle
        solveGrid()     #then calls to solve the grid for you


def main():
        global grid
        getGrid()
        os.system("cls")
        print("Solving")
        solve()

main()

print("Done")
input = input("Delete images? y/n\n")

if input.lower() == "y":
        print("removing files..")
        shutil.rmtree("Sudoku//img")    #removes images and directory

print("Program finished")