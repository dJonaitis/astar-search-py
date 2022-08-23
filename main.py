import pygame
import colorspy as color
from queue import PriorityQueue

#change the size variable to change how many squares (size^2 will be total amount of squares)
size = 20
#change the dimensions variable to resize pygame window
dimensions = 600
window = pygame.display.set_mode((dimensions, dimensions))
pygame.display.set_caption("Pathfinding algorithm (A*)")

class Node:
    def __init__(self, row, col, dimensions, totalRows):
        self.row = row
        self.col = col
        self.x = row * dimensions
        self.y = col * dimensions
        self.dimensions = dimensions
        self.color = color.white
        self.neighbors = []
        self.totalRows = totalRows
    
    def getPos(self):
        return self.row, self.col
    def closed(self):
        return self.color == color.red
    def open(self):
        return self.color == color.lawn_green
    def wall(self):
        return self.color == color.black
    def startPoint(self):
        return self.color == color.yellow
    def endPoint(self):
        return self.color == color.pink

    def reset(self):
        self.color = color.white
    def setClosed(self):
        self.color = color.red
    def setOpen(self):
        self.color = color.lawn_green
    def setWall(self):
        self.color = color.black
    def setStartPoint(self):
        self.color = color.yellow
    def setEndPoint(self):
        self.color = color.pink
    def setPath(self):
        self.color = color.blue
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.dimensions, self.dimensions))
    def getNeighbors(self, grid):
        self.neighbors = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].wall(): #down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 - 1 and not grid[self.row - 1][self.col].wall(): #up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].wall(): #right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].wall(): #left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def createGrid(rows, dimensions):
    grid = []
    gap = dimensions // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def drawGrid(window, rows, dimensions):
    gap = dimensions // rows
    for i in range(rows):
        pygame.draw.line(window, color.dark_gray, (0, i * gap), (dimensions, i * gap)) 
        for j in range(rows):
            pygame.draw.line(window, color.dark_gray, (j * gap, 0), (j * gap, dimensions))

def getPath(lastNode, current, draw):
    while current in lastNode:
        current = lastNode[current]
        current.setPath()
        draw()

def aStar(draw, grid, startPoint, endPoint):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, startPoint))
    lastNode = {}
    gScore = {node: float("inf") for row in grid for node in row}
    gScore[startPoint] = 0
    fScore = {node: float("inf") for row in grid for node in row}
    fScore[startPoint] = heuristic(startPoint.getPos(), endPoint.getPos())

    openSetHash = {startPoint}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == endPoint:
            getPath(lastNode, endPoint, draw)
            endPoint.setEndPoint()
            return True
        for neighbor in current.neighbors:
            tempGScore  = gScore[current] + 1
            if tempGScore < gScore[neighbor]:
                lastNode[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + heuristic(neighbor.getPos(), endPoint.getPos())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.setOpen()

        draw()
        if current != startPoint:
            current.setClosed()

def heuristic(point1, point2):
    #using manhattan distance
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1-x2) + abs(y1-y2)


def draw(window, grid, rows, dimensions):
    window.fill(color.white)
    for row in grid:
        for node in row:
            node.draw(window)
    drawGrid(window, rows, dimensions)
    
    pygame.display.update()

def clickPos(pos, rows, dimensions):
    gap = dimensions // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row,col

def main(window, dimensions):
    rows = size
    grid = createGrid(rows, dimensions)
    startPoint = None
    endPoint = None
    run = True
    started = False
    
    while run:
        draw(window, grid, rows, dimensions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = clickPos(position, rows, dimensions)
                node = grid[row][col]
                if not startPoint and node != endPoint:
                    startPoint = node
                    startPoint.setStartPoint()
                elif not endPoint and node != startPoint:
                    endPoint = node
                    endPoint.setEndPoint()
                elif (node != endPoint) and (node != startPoint):
                    node.setWall()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = clickPos(position, rows, dimensions)
                node = grid[row][col]
                node.reset()
                if node == startPoint:
                    startPoint = None
                elif node == endPoint:
                    endPoint = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not started:
                    for row in grid:
                        for node in row:
                            node.getNeighbors(grid)
                    aStar(lambda: draw(window, grid, rows, dimensions), grid, startPoint, endPoint)
                if event.key == pygame.K_BACKSPACE:
                    startPoint = None
                    endPoint = None
                    grid = createGrid(rows, dimensions)
    
    pygame.quit()

main(window, dimensions)