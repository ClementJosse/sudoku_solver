import PySimpleGUI as sg
import random
import string
import numpy as np
import time


def isThisNumberAlreadyPlacedInTheGroupAtThesesCoordinates(value,coord_x,coord_y,sudoku_programme):
    
    group_x=int(coord_x/3)*3
    group_y=int(coord_y/3)*3
    a=list()
    for i in range(group_x,group_x+3):
        for j in range(group_y,group_y+3):
            a.append(int(sudoku_programme[i][j]))
            
    return value in a

def isThisNumberAlreadyInHisRow(value,coord_x,sudoku_programme):
    for i in range(9):
        if value == sudoku_programme[coord_x][i]:
            return True
    return False

def isThisNumberAlreadyInHisColomn(value,coord_y,sudoku_programme):
    for i in range(9):
        if value == sudoku_programme[i][coord_y]:
            return True
    return False

def canThisNumberBePlacedAtThesesCoordinates(k,i,j,sudoku_programme):
    # vérification dans le groupe de 9 cases si le nombre que l'on souhaite écrire est déjà présent
    # vérification dans la ligne si le nombre que l'on souhaite écrire est déjà présent
    # vérification dans la colonne si le nombre que l'on souhaite écrire est déjà présent
    
    #print(isThisNumberAlreadyPlacedInTheGroupAtThesesCoordinates(k,i,j,sudoku_programme),isThisNumberAlreadyInHisRow(k,i,sudoku_programme),isThisNumberAlreadyInHisColomn(k,j,sudoku_programme), k)
    
    return isThisNumberAlreadyPlacedInTheGroupAtThesesCoordinates(k,i,j,sudoku_programme)==False and isThisNumberAlreadyInHisRow(k,i,sudoku_programme)==False and isThisNumberAlreadyInHisColomn(k,j,sudoku_programme) == False
                    
def placeThisNumberVisualyAtTheseCoordinates(event,box_y,box_x):
    letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
    g.DrawRectangle((box_x * BOX_SIZE + 5, box_y * BOX_SIZE + 3), (box_x * BOX_SIZE + BOX_SIZE + 5, box_y * BOX_SIZE + BOX_SIZE + 3), fill_color ="#64778D",line_color = None, line_width = None)
    g.draw_text(event,letter_location, font='Arial')

def findSolution(sudoku_initial):
    #print(np.matrix(sudoku_initial))
    nb_retour=0
    sudoku_programme=[ [0]*9 for i in range(9)]
    for i in range(9):
        for j in range(9):
            sudoku_programme[i][j]=sudoku_initial[i][j]

    # trouver les coordonnés de la première case vide en haut a gauche

    
    list_of_dicts = []

    for i in range(9):
        for j in range(9):
            if sudoku_initial[i][j] == 0:
                d = {"i": i, "j": j}
                list_of_dicts.append(d)

    curseur=0
    while(curseur<len(list_of_dicts)):

        #print("case",list_of_dicts[curseur]['i'],list_of_dicts[curseur]['j'],curseur)
        
        i=list_of_dicts[curseur]['i']
        j=list_of_dicts[curseur]['j']

        # pour chaque nombre de 1 à 9 dans la case "disponible" du sudoku_initial :
        print("[Check]",curseur)
        placedValue=False
        for k in range(sudoku_programme[i][j]+1,10):
            print(k)
            #vérification si il est possible de le nombre peut etre placé a ces coordonnées 
            if canThisNumberBePlacedAtThesesCoordinates(k,i,j,sudoku_programme):
                # si c'est possible, on l'écrit dans la case du sudoku_programme et on passe a la suivante
                print("placement ->",k)
                sudoku_programme[i][j]=k
                placeThisNumberVisualyAtTheseCoordinates(k,i,j)
                placedValue=True
                curseur+=1
                print(np.matrix(sudoku_programme))
                break
        
        # si ce n'est pas possible 
        if placedValue == False:
            
            # si on est à la première case il faut juste faire refaire les vérifications du nombre + 1 sans revenir a la case précédente
            if curseur == 0:
                if sudoku_programme[i][j]==10:
                    print("unsolvable :(")
                    break
            # dans le cas général revenir à la case précédente et refaire les vérifications du nombre + 1 du sudoku_programme
            sudoku_programme[i][j]=0
            curseur-=1
            nb_retour+=1
            
    
    print("nombre de retour en arrière:",nb_retour)
    return sudoku
BOX_SIZE = 25

layout = [
    
    [sg.Graph((600, 600), (0, 450), (450, 0), key='-GRAPH-',
              change_submits=True, drag_submits=False)],
    [sg.Button('Solve'), sg.Button('Reset'),sg.Button('Exit')]
]

window = sg.Window('Window Title', layout, finalize=True,return_keyboard_events=True, use_default_focus=False)

g = window['-GRAPH-']



for row in range(9):
    for col in range(9):
        g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
        #g.draw_text('{}'.format(row * 6 + col + 1),
        #            (col * BOX_SIZE + 10, row * BOX_SIZE + 8))


sudoku = [ [0]*9 for i in range(9)]

while True:             # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    mouse = values['-GRAPH-']
    
    if event in (sg.WIN_CLOSED, 'Reset'):
        for i in range(9):
           for j in range(9): 
                g.DrawRectangle((j * BOX_SIZE + 5, i * BOX_SIZE + 3), (j * BOX_SIZE + BOX_SIZE + 5, i * BOX_SIZE + BOX_SIZE + 3), fill_color ="#64778D",line_color = None, line_width = None)
                sudoku[i][j]=0

    if event in (sg.WIN_CLOSED, 'Solve'):
        findSolution(sudoku)
        print("solved :)")

    if event == '-GRAPH-':
        if mouse == (None, None):
            continue
        
        box_x = mouse[0]//BOX_SIZE
        box_y = mouse[1]//BOX_SIZE
        if box_x < 9 and box_y < 9 :
            #g.DrawRectangle((box_x * BOX_SIZE + 5, box_y * BOX_SIZE + 3), (box_x * BOX_SIZE + BOX_SIZE + 5, box_y * BOX_SIZE + BOX_SIZE + 3),line_color = "white", line_width = 1)
            letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
            print("clicked at ",box_x, box_y)
            
            
    if event == "1" or event == "2" or event == "3" or event == "4" or event == "5" or event == "6" or event == "7" or event == "8" or event == "9" or event == "Delete:46" :
        if event == "Delete:46" :
            g.DrawRectangle((box_x * BOX_SIZE + 5, box_y * BOX_SIZE + 3), (box_x * BOX_SIZE + BOX_SIZE + 5, box_y * BOX_SIZE + BOX_SIZE + 3), fill_color ="#64778D",line_color = None, line_width = None)
            sudoku[box_y][box_x]=0
        else :
            g.DrawRectangle((box_x * BOX_SIZE + 5, box_y * BOX_SIZE + 3), (box_x * BOX_SIZE + BOX_SIZE + 5, box_y * BOX_SIZE + BOX_SIZE + 3), fill_color ="#64778D",line_color = None, line_width = None)
            g.draw_text(event,letter_location, font='Arial')
            sudoku[box_y][box_x]=int(event)
        
    #print(event)

window.close()


""" with open('input.txt', 'r') as f:
    sudoku = [[int(num) for num in line.split(' ')] for line in f]

print(sudoku) """