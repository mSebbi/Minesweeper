import pygame
import os
from time import sleep
from random import random



class Piece():
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb
        self.gedrueckt = False
        self.flagged = False

    def getHasBomb(self):
        return self.hasBomb

    def getgedrueckt(self):
        return self.gedrueckt

    def getFlagged(self):
        return self.flagged

    def setNeighbors(self, nachbar):
        self.nachbar = nachbar
        self.setNumAround()

    def setNumAround(self):
        self.numAround = 0
        for piece in self.nachbar:
            if (piece.getHasBomb()):
                self.numAround += 1

    def getNumAround(self):
        return self.numAround

    def toggleFlag(self):
        self.flagged = not self.flagged

    def click(self):
        self.gedrueckt = True

    def getNeighbors(self):
        return self.nachbar


class Board():
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.verloren = False
        self.anzgedrueckt = 0
        self.anznichtBomben = 0
        self.setBoard()

        
    def setBoard(self):
        self.board = []
        for reihe in range(self.size[0]):
            reihe = []
            for col in range(self.size[1]):
                hasBomb = random() < self.prob
                if (not hasBomb):
                    self.anznichtBomben += 1
                piece = Piece(hasBomb)
                reihe.append(piece)
            self.board.append(reihe)
        self.setNeighbors()

    def setNeighbors(self):
        for reihe in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.getPiece((reihe, col))
                nachbar = self.getListOfNeighbors((reihe, col))
                piece.setNeighbors(nachbar)

    def getListOfNeighbors(self, index):
        nachbar = []
        for reihe in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBounds = reihe < 0 or reihe >= self.size[0] or col < 0 or col >= self.size[1]
                same = reihe == index[0] and col == index[1]
                if (same or outOfBounds):
                    continue
                nachbar.append(self.getPiece((reihe, col)))
        return nachbar

    def getSize(self):
        return self.size

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, piece, flag):
        if (piece.getgedrueckt() or (not flag and piece.getFlagged())):
            return
        if (flag):
            piece.toggleFlag()
            return
        piece.click()
        if (piece.getHasBomb()):
            self.verloren = True
            return
        self.anzgedrueckt += 1
        if (piece.getNumAround() != 0):
            return
        for neighbor in piece.getNeighbors():
            if (not neighbor.getHasBomb() and not neighbor.getgedrueckt()):
                self.handleClick(neighbor, False)

    def getverloren(self):
        return self.verloren

    def getWon(self):
        return self.anznichtBomben == self.anzgedrueckt

class Game():
	def __init__(self, board, screenSize):
		self.board = board
		self.screenSize = screenSize
		self.pieceSize = self.screenSize[0] // self.board.getSize() [1], self.screenSize[1] // self.board.getSize()[0]
		self.loadImages()

	def run(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.screenSize)
		running = True
		while running:
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					running = False
				if (event.type == pygame.KEYDOWN):
					if (event.key == pygame.K_q):
						running = False
				if (event.type == pygame.MOUSEBUTTONDOWN):
					position = pygame.mouse.get_pos()
					rightClick = pygame.mouse.get_pressed()[2]
					self.handleClick(position, rightClick)
			self.draw()
			pygame.display.flip()
			if (self.board.getWon()):
				sleep(3)
				running = False

		pygame.QUIT()

	def draw(self):
		topLeft = (0, 0)
		for reihe in range(self.board.getSize() [0]):
			for col in range(self.board.getSize()[1]):
				piece = self.board.getPiece((reihe, col))
				image = self.getImage(piece)
				self.screen.blit(image, topLeft)
				topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
			topLeft = 0, topLeft[1] + self.pieceSize[1]

	def loadImages(self):
		self.images = {}
		for fileName in os.listdir("images"):
			if (not fileName.endswith(".png")):
				continue
			image = pygame.image.load(r"images/" + fileName)
			image = pygame.transform.scale(image, self.pieceSize)
			self.images[fileName.split(".") [0]] = image

	def getImage(self, piece):
		string = None
		if (piece.getgedrueckt()):
			string = "bomb-at-clicked-block" if piece.getHasBomb() else str(piece.getNumAround())
		else:
			string = "flag" if piece.getFlagged() else "empty-block"
		return self.images[string]

	def handleClick(self, position, rightClick):
		if (self.board.getverloren()):
			return
		index = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]
		piece = self.board.getPiece(index)
		self.board.handleClick(piece, rightClick)

        
if __name__ == '__main__':
    size = (9,9)
    prob = 0.1
    board = Board(size, prob)
    screenSize = (800, 800)
    game = Game(board, screenSize)
    game.run()
