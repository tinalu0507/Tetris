#!/usr/bin/python
from Tkinter import *
import random

def run(rows, cols):
	root=Tk()
	global canvas
	canvas=Canvas(root, width=cols*30+60, height=rows*30+60)
	canvas.pack()
	root.resizable(width=0, height=0)
	class Struct: pass
	canvas.data=Struct()
	canvas.data.rows=rows
	canvas.data.cols=cols
	init()
	root.bind("<Key>", keyPressed)
	if canvas.data.isGameOver==False and canvas.data.pause==False:
		timerFired()
	root.mainloop()

def init():
	canvas.data.isGameOver=False
	canvas.data.pause=False
	canvas.data.instructions=False
	emptyColor="LightSeaGreen"
	canvas.data.time=0
	global board
	board=[]
	for row in range(canvas.data.rows):
		board.append([])
		for col in range(canvas.data.cols):
			board[row].append(emptyColor)
	canvas.data.emptyColor=emptyColor
	 # pre-load a few cells with known colors for testing purposes
	#board[0][0] = "red" # top-left is red
	#board[0][canvas.data.cols-1] = "white" # top-right is white
	#board[canvas.data.rows-1][0] = "green" # bottom-left is green
	#board[canvas.data.rows-1][canvas.data.cols-1] = "gray" # bottom-right is gray
	iPiece = [
    [ True,  True,  True,  True]
  ]
  
	jPiece = [
    [ True, False, False ],
    [ True, True,  True]
  ]
  
	lPiece = [
    [ False, False, True],
    [ True,  True,  True]
  ]
  
	oPiece = [
    [ True, True],
    [ True, True]
  ]
  
	sPiece = [
    [ False, True, True],
    [ True,  True, False ]
  ]
  
	tPiece = [
    [ False, True, False ],
    [ True,  True, True]
  ]

	zPiece = [
    [ True,  True, False ],
    [ False, True, True]
  ]
	tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
	tetrisPieceColors = [ "red", "magenta", "pink", "cyan", "green", "orange", "blue", "purple", "yellow"]
	canvas.data.tetrisPieces= tetrisPieces
	canvas.data.tetrisPieceColors = tetrisPieceColors
	newFallingPiece()
	canvas.data.score=0

	

def drawGame():
 	canvas.create_rectangle(0, 0, canvas.data.cols*30+60, canvas.data.rows*30+60, fill="MediumAquamarine")
 	drawBoard()
 	drawFallingPiece()

def drawBoard():
 	for row in range(canvas.data.rows):
 		for col in range(canvas.data.cols):
 			drawCell(row, col, board[row][col])

def drawCell(row, col, color):
	canvas.create_rectangle(col*30+30 , row*30+30, col*30+60, row*30+60, fill=color, outline="DarkCyan", width=2)
 	#canvas.create_rectangle(col*20+25, row*20+25, row*20+35, row*20+35, fill=board[row][col])

def drawmenu():
	canvas.create_rectangle(0, 0, canvas.data.cols*30+60, canvas.data.rows*30+60, fill="MediumAquamarine")
	canvas.create_text(canvas.data.cols*15, canvas.data.rows*7, text="Teris!", anchor=SW, fill="DarkOliveGreen", font="Perisa 24 italic")
	canvas.create_text(canvas.data.cols*6, canvas.data.rows*13, text="Please choose a level", anchor=SW, fill="DarkOliveGreen", font="Perisa 24 italic")
	canvas.create_text(canvas.data.cols*12, canvas.data.rows*15, text="1\Beginner", anchor=SW, fill="DarkOliveGreen", font="Perisa 18 italic")
	canvas.create_text(canvas.data.cols*12, canvas.data.rows*15+15, text="2\Intermediate", anchor=SW, fill="DarkOliveGreen", font="Perisa 18 italic")
	canvas.create_text(canvas.data.cols*12, canvas.data.rows*15+30, text="3\Advanced", anchor=SW, fill="DarkOliveGreen", font="Perisa 18 italic")

def redrawAll(canvas):
	canvas.delete(ALL)
	if canvas.data.isGameOver==True:
		drawGame()
		canvas.create_rectangle(60,150,300,300,fill="LightSeaGreen", outline="DarkCyan")
		canvas.create_text(canvas.data.cols*15-30, canvas.data.rows*15, text="Game Over", anchor=SW, fill="DarkOliveGreen", font="Perisa 24 italic")
		canvas.create_text(canvas.data.cols*15-40, canvas.data.rows*15+30, text="press r to restart", anchor=SW, fill="DarkOliveGreen", font="Perisa 18 italic")
	else:
		removeFullRows()
		drawGame()
		drawScore()
	if canvas.data.pause==True:
		drawPausescreen()
	if canvas.data.pause==True:
		placeinstructions()
	

def newFallingPiece():
	fallingPiece=canvas.data.tetrisPieces[random.randint(0, len(canvas.data.tetrisPieces)-1)]
	fallingPieceColor=canvas.data.tetrisPieceColors[random.randint(0, len(canvas.data.tetrisPieceColors)-1)]
	fallingPieceRows=len(fallingPiece)
	fallingPieceCols=len(fallingPiece[0])
	fallingPieceRow=0
	fallingPieceCol=canvas.data.cols/2-fallingPieceCols/2
	canvas.data.fallingPieceCol=fallingPieceCol
	canvas.data.fallingPieceRow=fallingPieceRow
	canvas.data.fallingPieceRows=fallingPieceRows
	canvas.data.fallingPieceCols=fallingPieceCols
	canvas.data.fallingPiece=fallingPiece
	canvas.data.fallingPieceColor=fallingPieceColor


def drawFallingPiece():
	for row in range(canvas.data.fallingPieceRows):
		for col in range(canvas.data.fallingPieceCols):
			if canvas.data.fallingPiece[row][col]==True:
				drawCell(canvas.data.fallingPieceRow+row, canvas.data.fallingPieceCol+col, canvas.data.fallingPieceColor)
	#offset fallingPieceCol fallingPieceRow

def keyPressed(event):
	key = event.keysym
	if canvas.data.isGameOver==False and canvas.data.pause==False:
		if key=="Left":
			moveFallingPiece(canvas, 0, -1)
		elif key=="Right":
			moveFallingPiece(canvas, 0, +1)
		elif key=="Down":
			moveFallingPiece(canvas, +1, 0)
		elif key=="Up":
			rotateFallingPiece()
		elif key=="space":
			droptothebottom()
		elif key=="p":
			canvas.data.pause=True
	if canvas.data.pause==True:
		if key=="c":
			canvas.data.pause=False
			canvas.data.instructions=False
	if key=="1":
		canvas.data.time=1000
		canvas.data.isGameOver=False
	if key=="2":
		canvas.data.time=750
		canvas.data.isGameOver=False
	if key=="3":
		canvas.data.time=500
		canvas.data.isGameOver=False
	if key=="r":
		init()
	redrawAll(canvas)

def moveFallingPiece(canvas, drow, dcol):
	canvas.data.fallingPieceRow+=drow
	canvas.data.fallingPieceCol+=dcol
	if fallingPieceIsLegal(canvas) ==False:
		canvas.data.fallingPieceRow-=drow
		canvas.data.fallingPieceCol-=dcol
		return False
	return True

def fallingPieceIsLegal(canvas):
	for i in range(canvas.data.fallingPieceRows):
		for j in range(canvas.data.fallingPieceCols):
			if canvas.data.fallingPiece[i][j]==True:
				if i+canvas.data.fallingPieceRow >= canvas.data.rows or i+canvas.data.fallingPieceRow <0 :
					return False
				elif j+canvas.data.fallingPieceCol >= canvas.data.cols or j+canvas.data.fallingPieceCol < 0:
					return False
				elif board[i+canvas.data.fallingPieceRow][j+canvas.data.fallingPieceCol]!=canvas.data.emptyColor:
					return False
	return True

def fallingPieceCenter():
	row=canvas.data.fallingPieceRow + canvas.data.fallingPieceRows/2
	col=canvas.data.fallingPieceCol + canvas.data.fallingPieceCols/2
	return (row, col)

def rotateFallingPiece():
	OldPiece=canvas.data.fallingPiece
	OldRow=canvas.data.fallingPieceRow
	OldCol=canvas.data.fallingPieceCol
	OldRows=canvas.data.fallingPieceRows
	OldCols=canvas.data.fallingPieceCols
	NewPiece=[]
	for i in range(len(OldPiece[0])):
		NewPiece.append([])
		for j in range (len(OldPiece)):
			NewPiece[i].append(OldPiece[j][len(OldPiece[0])-i-1])
	(oldCenterRow, oldCenterCol)=fallingPieceCenter()
	c=canvas.data.fallingPieceRows
	canvas.data.fallingPieceRows=canvas.data.fallingPieceCols
	canvas.data.fallingPieceCols=c
	(newCenterRow, newCenterCol)=fallingPieceCenter()
	canvas.data.fallingPieceRow +=(oldCenterRow - newCenterRow)
	canvas.data.fallingPieceCol +=(oldCenterCol - newCenterCol)
	canvas.data.fallingPiece=NewPiece
	if fallingPieceIsLegal(canvas) ==False:
		canvas.data.fallingPiece=OldPiece
		canvas.data.fallingPieceRow=OldRow
		canvas.data.fallingPieceCol=OldCol
		canvas.data.fallingPieceRows=OldRows
		canvas.data.fallingPieceCols=OldCols

def timerFired():
	if canvas.data.isGameOver==False and canvas.data.pause==False:
		if moveFallingPiece(canvas,+1,0)==False:
			placeFallingPiece()
			newFallingPiece()
			if fallingPieceIsLegal(canvas)==False:
				canvas.data.isGameOver=True
	redrawAll(canvas)
	delay = 750
	canvas.after(delay, timerFired)

def placeFallingPiece():
	for row in range(canvas.data.fallingPieceRows):
		for col in range(canvas.data.fallingPieceCols):
			if canvas.data.fallingPiece[row][col]==True:
				board[canvas.data.fallingPieceRow+row][canvas.data.fallingPieceCol+col]=canvas.data.fallingPieceColor

def removeFullRows():
	counter=0
	oldRow=canvas.data.rows-1
	newRow=canvas.data.rows-1
	while oldRow>=0:
		result=False
		for col in range(0, canvas.data.cols): 
			if board[oldRow][col]==canvas.data.emptyColor:
				result=True
		if result==True:
			for j in range(0, canvas.data.cols):
				board[newRow][j]=board[oldRow][j]
			newRow-=1
		else:
			counter+=1
		oldRow-=1
	#for row in range(0, counter):
		#for col in range(0, canvas.data.cols):
			#board[row][col]=canvas.data.emptyColor
	canvas.data.score+=counter**2

def drawScore():
	canvas.create_text(60, 20, text="Score:"+ str(canvas.data.score), fill="DarkOliveGreen", font="Ariel 16")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*30+40, text="press r to restart, p to pause and see instructions", fill="DarkOliveGreen")

def drawPausescreen():
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15+30, text="press c to continue", fill="purple")

def droptothebottom():
	while moveFallingPiece(canvas,+1,0)==True:
		moveFallingPiece(canvas,+1,0)

def placeinstructions():
	canvas.create_rectangle(60,150,300,300,fill="LightSeaGreen", outline="DarkCyan")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15-60, text="Up: rotate the piece", fill="DarkOliveGreen")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15-45, text="Left: move the piece to the left", fill="DarkOliveGreen")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15-30, text="Right: move the piece to the right", fill="DarkOliveGreen")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15-15, text="Space: drop the piece to the bottom", fill="DarkOliveGreen")
	canvas.create_text(canvas.data.cols*15+30, canvas.data.rows*15+15, text="press c to continue", fill="grey")

run(15,10)