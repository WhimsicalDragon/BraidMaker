""" This program is used to draw braid diagrams given a braid diagram.
"""

import time
import pyautogui as mouse

#mouse.PAUSE = 1 #This is to slow down movement between steps if needed

global drawSpeed
drawSpeed = 0.5 #0.5 is effective, but painfully slow to watch...

braid = input("Enter a braid word:")

braid = braid.replace("[","")
braid = braid.replace("]","")

braid = braid.split(",")

for i in range(len(braid)):
    braid[i] = int(braid[i])

print(braid)
size = 1
for i in range(len(braid)):
    if size < (abs(braid[i]) + 1):
        size = (abs(braid[i]) + 1)

#Iniates the start of a braid
def startBraid(size):
    visual = []
    for i in range(size):
        visual.append('|')
        visual.append(' ')
    del visual[-1]
    visual = [visual]
    return visual

#Prints a braid neatly
def printBraid(visual):
    for i in visual:
        line = ""
        for q in i:
            line = line + q
        print(line)

#Adds a no crossing section to the braid
def noCross(visual):
    #The last elem should always have no crossings as it is the start of the braid
    visual.insert(0,visual[-1])
    return visual

#Creates a crossing that cause overstrand to move left and cross over the adjacent strand
#
# | |
# /-\  
# | |
#
#The - represent a negative write crossing
def leftOver(visual,overStrand,size):
    if overStrand == 0:
        raise Exception("There is an issue with the braid word given. Braid word asks to cross leftmost strand over another strand in the left direction. This cannot happen!")
    line = []
    for i in range(size-1):
        if i+1 != overStrand:
            line.append('|')
            line.append(' ')
        else:
            line.append('/')
            line.append('-')
            line.append('\\')
            line.append(' ')

    del line[-1]
    print(line)
    visual.insert(0,line)
    return visual
        
#Creates a crossing that cause overstrand to move right and cross over the adjacent strand
#
# | |
# /+\  
# | |
#
#The + represent a positive writhe crossing
def rightOver(visual,overStrand,size):
    if overStrand == size:
        raise Exception("There is an issue with the braid word given. Braid word asks to cross rightmost strand over another strand in the right direction. This cannot happen!")
    line = []

    for i in range(size - 1):
        if i+1 != overStrand:
            line.append('|')
            line.append(' ')
        else:
            line.append('/')
            line.append('+')
            line.append('\\')
            line.append(' ')

    del line[-1]
    visual.insert(0,line)
    return visual

#Generates the visual braid given the braid word
def genBraid(braid,visual,size):
    for i in braid:
        if i < 0:
            visual = leftOver(visual,abs(i),size)
        else:
            visual = rightOver(visual,abs(i),size)
    return visual


#Sets up the starting mouse position
def mouseSetup():
    pos = False
    while pos == False:
        x = int(input("Enter mouse starting x position:"))
        y = int(input("Enter mouse starting y position:"))
        mouse.moveTo(x,y)
        pos = input("Enter 1 if position is acceptable:")
        if pos == '1':
            pos = True
        else:
            pos = False
    loc = (x,y)
    return loc

#Draws a left diagonal
def drawLeftDiag(x,y,spacing,length,toggle):
    global drawSpeed

    if toggle == True:
        mouse.keyDown('shift')

    mouse.moveTo(x,y)
    mouse.dragTo(x + spacing,y - length,button='left',duration=drawSpeed)
    mouse.keyUp('shift')
    return

#Draws a right diagonal
def drawRightDiag(x,y,spacing,length,toggle):

    if toggle == True:
        mouse.keyDown('shift')

    mouse.moveTo(x,y)
    mouse.dragTo(x - spacing,y - length,button='left',duration=drawSpeed)
    mouse.keyUp('shift')
    return

#Draws a vertical line
def drawNoCross(x,y,length):
    global drawSpeed

    mouse.moveTo(x,y)
    mouse.dragTo(x,y - length,button='left',duration=drawSpeed)
    return

#Leverages the other draw functions to draw a braid using the visual array as instructions
def drawBraid(loc,visual,spacing,length):
    x = loc[0]
    y = loc [1]

    visual.reverse()

    for i in range(len(visual)):
        for j in range(len(visual[i])):
            toggle = False
            if visual[i][j] == '|':
                drawNoCross(x,y,length)
                x = x + spacing
            #Left
            elif visual[i][j] == '/':

                if visual[i][j+1] == '-':
                    toggle = True

                drawLeftDiag(x,y,spacing,length,toggle)
                x = x + spacing

            #Right
            elif visual[i][j] == '\\':
                if visual[i][j-1] == '+':
                    toggle = True
                drawRightDiag(x,y,spacing,length,toggle)
                x = x + spacing
            else:
                pass
        y = y - length
        x = loc[0]

def connectStrands(loc,visual,spacing,length):
    x = loc[0]
    y = loc [1]

    for i in range(len(visual)):
        for j in range(len(visual[i])):

            if visual[i][j] != ' ' and visual[i][j] != '+' and visual[i][j] != '-':
                drawNoCross(x,y,length)
                x = x + spacing
        y = y - length
        x = loc[0]

visual = startBraid(size)


print("Your braid!")
printBraid(genBraid(braid,visual,size))
print(braid)

loc = mouseSetup()
print("It will take approximately " + str(len(visual)*size*0.5) + " seconds to draw this braid.") #KLO Tends to lose crossing information if you go too fast, so we have to be slow with our drawing
time.sleep(5) #Short timeout to switch to KLO
drawBraid(loc,visual,50,25)
connectStrands(loc,visual,50,25)

