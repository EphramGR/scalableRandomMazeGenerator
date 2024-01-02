import pygame
import random
import time

#All the pretty factors of 800 numbers
ARR = [2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 80, 100, 160]

#Change this number, but nothing else, 160 max
SIZE = ARR[random.randint(0,13)]

print(SIZE)

#use for more rendomness with bellcurve closer to low less lkely high
#random.randint(2, random.randint(2, random.randint(2,200)))

SCALE = 800/SIZE

ANIMATE = False

WAIT = int((1000/(SIZE*SIZE))/2)

WINDOW = pygame.display.set_mode((SIZE*SCALE, SIZE*SCALE + 100))

IMAGE = pygame.image.load("sprite.png")
IMAGE = IMAGE.convert()
IMAGE = pygame.transform.scale(IMAGE, (SCALE/2, SCALE/2))

IMAGE2 = pygame.image.load("sprite2.png")
IMAGE2 = IMAGE2.convert()
IMAGE2 = pygame.transform.scale(IMAGE2, (SCALE/2, SCALE/2))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

START = random.randint(0,SIZE-1)

RIGHT = 25
LEFT = 25
UP = 25
#Down = leftover

pygame.init()

FONT = pygame.font.Font('freesansbold.ttf', 20)

#print(WAIT, SIZE)

#n, e, s, w
def buildStructure(maze):
	for x in range(SIZE):
		for y in range(SIZE):
			maze.append([])
			for w in range(4):
				maze[(x*SIZE)+y].append(False)

	return maze

def drawMaze(maze):
	WINDOW.fill(BLACK)
	for y in range(SIZE):
		for x in range(SIZE):
			if True in maze[(y*SIZE)+x]:
				if ANIMATE:
					pygame.display.update()
					pygame.time.wait(WAIT)
				pygame.draw.rect(WINDOW, WHITE, (x*SCALE+(SCALE/4)-1, y*SCALE+(SCALE/4)-1, SCALE/2+2, SCALE/2+2))
				if maze[(y*SIZE)+x][0]:
					pygame.draw.rect(WINDOW, WHITE, (x*SCALE+(SCALE/4)-1, y*SCALE-1, SCALE/2+2, SCALE/2+2))
				if maze[(y*SIZE)+x][1]:
					pygame.draw.rect(WINDOW, WHITE, (x*SCALE+(SCALE/2)-1, y*SCALE+(SCALE/4)-1, SCALE/2+2, SCALE/2+2))
				if maze[(y*SIZE)+x][2]:
					pygame.draw.rect(WINDOW, WHITE, (x*SCALE+(SCALE/4)-1, y*SCALE+(SCALE/2)-1, SCALE/2+2, SCALE/2+2))
				if maze[(y*SIZE)+x][3]:
					pygame.draw.rect(WINDOW, WHITE, (x*SCALE-1, y*SCALE+(SCALE/4)-1, SCALE/2+2, SCALE/2+2))

def buildMaze(maze, num):
	maze = buildWin(maze, num)

	maze, win = buildNoise(maze)

	return maze, win

def buildWin(maze, num):
	#This is for future where ir will start where last finished
	start = num
	if num == -1:
		start = START

	current = SIZE*(SIZE-1)+start

	#location of selected path and the way it points back
	maze[current][2] = True
	maze[current].append(2)
	count = 0

	while True:
		count += 1

		if count == SIZE*200:
			print("Bug Handleing")
			maze = bugHandle(maze, current)
			break

		left = False
		right = False
		top = False
		bottem = False

		#If its on the left wall
		modSize = current % SIZE
		if modSize == 0:
			left = True
		#If its on right wall
		elif modSize == SIZE-1:
			right = True

		#If its on top
		if current < SIZE:
			top = True
		#If on bottem
		elif current >= SIZE*(SIZE-1):
			bottem = True

		chance = random.randint(1, 100)

		#print(f"Chance: {chance}, left {left} right{right} up{top} down{bottem}")
		#Right
		if chance <= RIGHT:
			if right:
				continue

			if True in maze[current+1]:
				#print(f"loop at {current+1}")
				continue
			maze[current][1] = True
			maze[current+1][3] = True
			current += 1
			maze[current].append(3)

		#Left
		elif chance <= RIGHT+LEFT:
			if left:
				continue

			if True in maze[current-1]:
				#print(f"loop at {current-1}")
				continue
			maze[current][3] = True
			maze[current-1][1] = True
			current -= 1
			maze[current].append(1)

		#Up
		elif chance <= RIGHT+LEFT+UP:
			if top:
				break

			if True in maze[current-SIZE]:
				#print(f"loop at {current-SIZE}")
				continue
			maze[current][0] = True
			maze[current-SIZE][2] = True
			current = current - SIZE
			maze[current].append(2)
		#Down
		else:
			if bottem:
				continue

			if True in maze[current+SIZE]:
				#print(f"loop at {current+SIZE}")
				continue
			maze[current][2] = True
			maze[current+SIZE][0] = True
			current = current + SIZE
			maze[current].append(0)

		#drawMaze(maze)
		#pygame.time.wait(100)
	
	return maze

def bugHandle(maze, current):
	RorL = True

	stubArr = []

	if current%SIZE >= SIZE/2:
		RorL = False

	while True:
		top = False
		left = False
		right = False

		if current < SIZE:
			top = True

		#If its on the left wall
		modSize = current % SIZE
		if modSize == 0:
			left = True
		#If its on right wall
		elif modSize == SIZE - 1:
			right = True

		chance = random.randint(1, 2)

		if chance == 1:
			if top:
				break

			if True in maze[current-SIZE]:
				for x in range(4):
					if maze[current-SIZE][x] == True:
						#If true is on the thing that points home
						if x == maze[current-SIZE][4]:
							pass
						else:
							maze[current-SIZE][x] = False
							stubArr.append((current-SIZE, x))

			maze[current][0] = True
			maze[current-SIZE][2] = True
			current = current - SIZE
		elif RorL:
			if right:
				continue

			if True in maze[current+1]:
				for x in range(4):
					if maze[current+1][x] == True:
						#If true is on the thing that points home
						if x == maze[current+1][4]:
							pass
						else:
							maze[current+1][x] = False
							stubArr.append((current+1, x))

			maze[current][1] = True
			maze[current+1][3] = True
			current += 1

		else:
			if left:
				continue

			if True in maze[current-1]:
				for x in range(4):
					if maze[current-1][x] == True:
						#If true is on the thing that points home
						if x == maze[current-1][4]:
							pass
						else:
							maze[current-1][x] = False
							stubArr.append((current-1, x))

			maze[current][3] = True
			maze[current-1][1] = True
			current -= 1

		#drawMaze(maze)
		#pygame.time.wait(100)
		
	#print(stubArr)
	for x in range(len(stubArr)):
		#print(maze[stubArr[x][0]][stubArr[x][1]])
		if maze[stubArr[x][0]][stubArr[x][1]] == False:
			if stubArr[x][1] == 0:
				maze[stubArr[x][0]-SIZE][2] = False
			elif stubArr[x][1] == 1:
				maze[stubArr[x][0]+1][3] = False
			elif stubArr[x][1] == 2:
				maze[stubArr[x][0]+SIZE][0] = False
			else:
				maze[stubArr[x][0]-1][1] = False


	return maze

def buildNoise(maze):
	count1 = 0

	while True:
		count1 += 1

		if count1 == SIZE*200:
			break

		current = random.randint(0,SIZE*SIZE-1)

		if not (True in maze[current]):
			continue


		count = 0
		while True:
			count += 1

			if count == int(SIZE*1.5):
				break

			left = False
			right = False
			top = False
			bottem = False

			#If its on the left wall
			modSize = current % SIZE
			if modSize == 0:
				left = True
			#If its on right wall
			elif modSize == SIZE - 1:
				right = True

			#If its on top
			if current < SIZE:
				top = True
			#If on bottem
			elif current >= SIZE*(SIZE-1):
				bottem = True

			chance = random.randint(1, 100)

			#print(f"Chance: {chance}, left {left} right{right} up{top} down{bottem}")
			#Right
			if chance <= RIGHT:
				if right:
					continue

				if True in maze[current+1]:
					#print(f"loop at {current+1}")
					continue
				maze[current][1] = True
				maze[current+1][3] = True
				current += 1
				maze[current].append(3)

			#Left
			elif chance <= RIGHT+LEFT:
				if left:
					continue

				if True in maze[current-1]:
					#print(f"loop at {current-1}")
					continue
				maze[current][3] = True
				maze[current-1][1] = True
				current -= 1
				maze[current].append(1)

			#Up
			elif chance <= RIGHT+LEFT+UP:
				if top:
					continue

				if True in maze[current-SIZE]:
					#print(f"loop at {current-SIZE}")
					continue
				maze[current][0] = True
				maze[current-SIZE][2] = True
				current = current - SIZE
				maze[current].append(2)
			#Down
			else:
				if bottem:
					continue

				if True in maze[current+SIZE]:
					#print(f"loop at {current+SIZE}")
					continue
				maze[current][2] = True
				maze[current+SIZE][0] = True
				current = current + SIZE
				maze[current].append(0)

			#drawMaze(maze)
			#pygame.time.wait(100)
		
	while True:
		num = random.randint(0, SIZE-1)
		if True in maze[num]:
			maze[num][0] = True
			win = num
			break


	return maze, win

def drawPlayer(x, y):
	WINDOW.blit(IMAGE, (x*SCALE+(SCALE/4)-1, y*SCALE+(SCALE/4)))

def drawPlayer2(x, y):
	WINDOW.blit(IMAGE2, (x*SCALE+(SCALE/4)-1, y*SCALE+(SCALE/4)))

def movePlayer(x, y, direction, maze):
	canmove = False
	left = False
	right = False
	top = False
	bottem = False
	won = False

	if not (direction == 2 and x == START and y == SIZE-1):
		#print(x, y, direction)
		if maze[(y*SIZE)+x][direction]:
			canmove = True

	if canmove:
		modSize = (y*SIZE)+x % SIZE
		if modSize == 0:
			left = True
		#If its on right wall
		elif modSize == SIZE-1:
			right = True

		#If its on top
		if (y*SIZE)+x < SIZE:
			top = True
		#If on bottem
		elif (y*SIZE)+x >= SIZE*(SIZE-1):
			bottem = True


		if direction == 0:
			if top:
				won = True
			else:
				y -= 1
		elif direction == 1 and not right:
			x += 1
		elif direction == 2 and not bottem:
			y += 1
		elif direction == 3 and not left:
			x -= 1

	return x, y, won

def update(x, y, x2, y2, maze, point, point2, bestT1, bestT2):
	drawMaze(maze)
	drawPlayer(x, y)
	drawPlayer2(x2, y2)
	drawText(point, point2, bestT1, bestT2)
	pygame.display.update()

def drawText(point, point2, bestT1, bestT2):
	if bestT1 == 100000:
		bestT1 = "N/A"
	if bestT2 == 100000:
		bestT2 = "N/A"

	text = FONT.render(f"Player 1 Points: {point}", True, (123, 175, 212), (0, 0, 0))

	textRect = text.get_rect()
	
	textRect.midleft = (25, 840)

	WINDOW.blit(text, textRect)

	text = FONT.render(f"Player 2 Points: {point2}", True, (255,165,0), (0, 0, 0))

	textRect = text.get_rect()
	
	textRect.midleft = (600, 840)

	WINDOW.blit(text, textRect)

	text = FONT.render(f"Best Time: {bestT1}", True, (123, 175, 212), (0, 0, 0))

	textRect = text.get_rect()
	
	textRect.midleft = (25, 860)

	WINDOW.blit(text, textRect)

	text = FONT.render(f"Best Time: {bestT2}", True, (255,165,0), (0, 0, 0))

	textRect = text.get_rect()
	
	textRect.midleft = (600, 860)

	WINDOW.blit(text, textRect)

def timeUpdate(start, end):
	text = FONT.render("{:.3f}".format(end-start), True, (123, 0, 212), (0, 0, 0))

	textRect = text.get_rect()
	
	textRect.center = (400, 850)

	WINDOW.blit(text, textRect)

	pygame.display.update()

def gameOver(point, point2, bestT1, bestT2):
	WINDOW.fill(BLACK)

	if point > point2:
		winner = "PLAYER 1"
		colour = (123, 175, 212)
	elif point2 > point:
		winner = "PLAYER 2"
		colour = (255,165,0)
	else:
		winner = "NOBODY"
		colour = (150, 150, 150)

	text = FONT.render(f"{winner} WINS!", True, colour, (0, 0, 0))

	textRect = text.get_rect()
	
	textRect.center = (400, 400)

	WINDOW.blit(text, textRect)

	if bestT1 < bestT2:
		time = bestT1
		timeMan = "Player 1"
		colour = (123, 175, 212)
	elif bestT2 < bestT1:
		time = bestT2
		timeMan = "Player 2"
		colour = (255,165,0)
	else:
		if bestT1 == 100000:
			time = "N/A"
		else:
			time = bestT1
		timeMan = "Nobody"
		colour = (150, 150, 150)

	text = FONT.render(f"{timeMan} had the best time with {time} seconds!", True, colour, (0, 0, 0))

	textRect = text.get_rect()
	
	textRect.center = (400, 500)

	WINDOW.blit(text, textRect)

	drawText(point, point2, bestT1, bestT2)

	pygame.display.update()	

	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()


def main():
	maze = []
	start = 0
	end = 0
	bestT1 = 100000
	bestT2 = 100000

	point = 0
	point2 = 0

	maze = buildStructure(maze)

	maze, win = buildMaze(maze, -1)

	#print(maze)
	drawMaze(maze)

	drawText(point, point2, bestT1, bestT2)

	px, py = START, SIZE-1

	px2, py2 = px, py

	drawPlayer(px, py)

	drawPlayer2(px2, py2)

	pygame.display.update()

	start = time.time()

	won = False
	won2 = False

	while True:
		end = time.time()
		timeUpdate(start, end)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver(point, point2, bestT1, bestT2)
			if event.type == pygame.KEYDOWN:
				if event.key== pygame.K_w:
					px, py, won = movePlayer(px, py, 0, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)
				if event.key== pygame.K_a:
					px, py, won = movePlayer(px, py, 3, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)
				if event.key== pygame.K_s:
					px, py, won = movePlayer(px, py, 2, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)
				if event.key== pygame.K_d:
					px, py, won = movePlayer(px, py, 1, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)
				if event.key== pygame.K_UP:
					px2, py2, won2 = movePlayer(px2, py2, 0, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)
				if event.key== pygame.K_LEFT:
					px2, py2, won2 = movePlayer(px2, py2, 3, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)
				if event.key== pygame.K_DOWN:
					px2, py2, won2 = movePlayer(px2, py2, 2, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)
				if event.key== pygame.K_RIGHT:
					px2, py2, won2 = movePlayer(px2, py2, 1, maze)
					update(px, py, px2, py2, maze, point, point2, bestT1, bestT2)


		if won or won2:
			newTime = end-start
			if won:
				if newTime < bestT1:
					bestT1 = round(newTime, 3)
				point += 1
			else:
				if newTime < bestT2:
					bestT2 = round(newTime, 3)
				point2 += 1
			start = time.time()

			won2 = False
			won = False

			maze = []

			maze = buildStructure(maze)

			maze, newwin = buildMaze(maze, win)

			drawMaze(maze)

			drawText(point, point2, bestT1, bestT2)

			drawPlayer(win, SIZE-1)

			drawPlayer2(win, SIZE-1)

			px, py = win, SIZE-1

			px2, py2 = px, py

			pygame.display.update()

			win = newwin


main()