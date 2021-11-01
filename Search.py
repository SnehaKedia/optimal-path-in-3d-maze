from collections import deque
import queue
from queue import PriorityQueue
import math

class Agent:
    def __init__(self):
        self.searchAlgorithm = ''
        self.dimensions = None
        self.entranceGrid = None
        self.exitGrid = None
        # self.numberOfGrids = 0
        self.gridsDict = {}
        self.operationsList = [(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), 
                               (0, 0, -1), (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
                               (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1), (0, 1, 1),
                               (0, 1, -1), (0, -1, 1), (0, -1, -1)]
        self.operationsCost = [0, 10, 10, 10, 10, 10, 10, 14, 14, 14, 14, 14, 14, 14,14, 14, 14, 14, 14]
        
    def createAgent(self, fileName):
        info = []
        with open(fileName, 'r') as file:
            for line in file.readlines():
                info.append(line.rstrip())
        file.close()
        
        self.searchAlgorithm = info[0]
        self.dimensions = tuple(map(int, info[1].split(' ')))
        self.entranceGrid = tuple(map(int, info[2].split(' ')))
        self.exitGrid = tuple(map(int, info[3].split(' ')))
        if (not self.checkBoundary(self.entranceGrid)) or (not self.checkBoundary(self.exitGrid)):
            self.outputFail()
            return
        # self.numberOfGrids = int(info[4])
        for i in range(5, len(info)):
            line = list(map(int, info[i].split(' ')))
            # print("list: ", line)
            key = (line[0], line[1], line[2])
            if not self.checkBoundary(key):
                continue
            self.gridsDict[key] = line[3:]
        # print(self.gridsDict)
        agent.selectAlgorithm()
        
    def selectAlgorithm(self):
        
        if len(self.gridsDict) == 0:
            self.outputFail()
            return
        
        if self.searchAlgorithm == "BFS":
            parent = self.bfsPath()
        
        elif self.searchAlgorithm == "UCS":
            parent = self.ucsPath()
        
        elif self.searchAlgorithm == "A*":
            parent = self.aStarPath()
            
        # print("Parent: ", parent)
        if parent == "No Path Found":
            self.outputFail()
        else:
            path, totalCost = self.getPathAndCost(parent)
            self.outputSuccess(path, totalCost)
        return
        
    def checkBoundary(self, gridLocation):
        if (0 <= gridLocation[0] < self.dimensions[0]) and (0 <= gridLocation[1] < self.dimensions[1]) and (0 <= gridLocation[2] < self.dimensions[2]):
            return True
        return False
    
    def bfsPath(self):
        reachedExit = False
        ## visited[grid] = parentNode
        visited = {agent.entranceGrid: None}
        queue = deque()
        queue.append(agent.entranceGrid)
        
        while queue:
            currentGrid = queue.popleft()
            if currentGrid == agent.exitGrid:
                reachedExit = True
                break
                
            for action in self.gridsDict[currentGrid]:
                operation = self.operationsList[action]
                neighbor = (currentGrid[0] + operation[0], currentGrid[1] + operation[1], currentGrid[2] + operation[2])
                # neighbor = tuple(map(sum, zip(grid, self.operationsList[action])))
                if checkBoundary(neighbor) and neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = currentGrid
                    
        if reachedExit:
            return visited
        else:
            return "No Path Found"
        
    def ucsPath(self):
        reachedExit = False
        ## visited[grid] = (cost, parentNode, actionToReach)
        visited = {agent.entranceGrid: (0, None, 0)}
        
        priorQueue = PriorityQueue()
        ## priorQueue.get() -> (cost, currentGrid)
        priorQueue.put((0, agent.entranceGrid))
        
        while not priorQueue.empty():
            # print("priorQueue: ", priorQueue.queue)
            currentCost, currentGrid = priorQueue.get()
            # print("currentGrid: ", currentGrid)
            if currentGrid == agent.exitGrid:
                reachedExit = True
                break
                
            for action in self.gridsDict[currentGrid]:
                operation = self.operationsList[action]
                neighbor = (currentGrid[0] + operation[0], currentGrid[1] + operation[1], currentGrid[2] + operation[2])
                newCost = currentCost + self.operationsCost[action]
                # print("Neighbor: ", neighbor, "newCost: ", newCost)
                if checkBoundary(neighbor) and ((neighbor not in visited) or (visited[neighbor][0] > newCost)):
                    priorQueue.put((newCost, neighbor))
                    visited[neighbor] = (newCost, currentGrid, action)
                    
        if reachedExit:
            return visited
        else:
            return "No Path Found"
        
    def heuristicEuclidean(self, grid1, grid2):
        ax, ay, az = grid1[0], grid1[1], grid1[2]
        bx, by, bz = grid2[0], grid2[1], grid2[2]
        
        heuristic = int(math.sqrt(((ax-bx)**2) + ((ay-by)**2) + ((az-bz)**2)))
        # print("heuristic: ", heuristic, "for (", ax, ay, az, ") and (", bx, by, bz, ")" )
        return heuristic
    
    def heuristicManhattan(self, grid1, grid2):
        ax, ay, az = grid1[0], grid1[1], grid1[2]
        bx, by, bz = grid2[0], grid2[1], grid2[2]
        
        sums = abs(ax-bx) + abs(ay-by) + abs(az-bz)
        heuristic = int(10 * (sums/2))
        return heuristic
        
    def aStarPath(self):
        reachedExit = False
        ## visited[grid] = (cost, parentNode, actionToReach)
        visited = {agent.entranceGrid: (0, None, 0)}
        
        priorQueue = PriorityQueue()
        ## priorQueue.get() -> (cost, parentHeuristic, currentGrid)
        priorQueue.put((0, 0, agent.entranceGrid))
        
        while not priorQueue.empty():
            # print("priorQueue: ", priorQueue.queue)
            currentCost, parentHeuristic, currentGrid = priorQueue.get()
            # print("currentGrid: ", currentGrid, "currentCost: ", currentCost, "parentHeuristic: ", parentHeuristic)
            currentCost = currentCost - parentHeuristic
            if currentGrid == agent.exitGrid:
                reachedExit = True
                break
                
            for action in self.gridsDict[currentGrid]:
                operation = self.operationsList[action]
                neighbor = (currentGrid[0] + operation[0], currentGrid[1] + operation[1], currentGrid[2] + operation[2])
                neighborHeuristic = self.heuristicManhattan(neighbor, self.exitGrid)
                newCost = currentCost + self.operationsCost[action] + neighborHeuristic
                # print("Neighbor: ", neighbor, "newCost: ", newCost)
                if checkBoundary(neighbor) and ((neighbor not in visited) or (visited[neighbor][0] > newCost)):
                    priorQueue.put((newCost, neighborHeuristic, neighbor))
                    visited[neighbor] = (newCost-neighborHeuristic, currentGrid, action)
                    
        if reachedExit:
            return visited
        else:
            return "No Path Found"
    
    def getPathAndCost(self, parent):
        path = []
        currentGrid = agent.exitGrid
        
        if self.searchAlgorithm == "BFS":
            totalCost = 0
            while currentGrid != agent.entranceGrid:
                totalCost += 1
                path.insert(0, (currentGrid, 1))
                currentGrid = parent[currentGrid]
            path.insert(0, (agent.entranceGrid, 0))
            
        else:
            totalCost = parent[agent.exitGrid][0]
            while currentGrid != agent.entranceGrid:
                costOfStep = self.operationsCost[parent[currentGrid][2]]
                path.insert(0, (currentGrid, costOfStep))
                currentGrid = parent[currentGrid][1]
            path.insert(0, (agent.entranceGrid, 0))
              
        # print("Path: ", path)
        # print("TotalCost: ", totalCost)
        
        return path, totalCost
        
    
    def outputSuccess(self, path, totalCost):
        with open("output.txt", "w+") as file:
            file.write(str(totalCost))
            file.write("\n")
            file.write(str(len(path)))
            file.write("\n")
            for i in range(len(path)):
                step = path[i]
                location = step[0]
                value = step[1]
                file.write(" ".join([str(location[0]), str(location[1]), str(location[2]), str(value)]))
                if i != (len(path)-1):
                    file.write("\n")
        file.close()
        return
    
    def outputFail(self):
        with open("output.txt", "w+") as file:
            file.write("FAIL")
        file.close()
        return
        

if __name__ == '__main__':
    import time
    import filecmp
    import os
    start = time.time()
    fileName = os.getcwd()+'/customInput1.txt'
    test_outfile = os.getcwd()+'/output11.txt'
    
    agent = Agent()
    # fileName = "input5.txt"
    agent.createAgent(fileName)
    
    end = time.time()
    print("TOTAL TIME: ", (end-start))
    print(filecmp.cmp('output.txt', test_outfile))
