from sensors import color, distance
import multiprocessing as mp
import multiprocessing.connection as connection
import time
import numpy as np
import heapq
from position import position
from movement import movement
import asyncio
from collections import deque
import sys

TIME_INCREMENT:float = 0.5
START:float          = time.time()
MAX_PULL_WAIT:float  = 5

# move, tmp = mp.Pipe() #tmp is the other end of the pipe, so we can forget it
# move_prc = mp.Process(target=movement.run, args=(tmp, ))
# del tmp

GRID_SIZE = (100,100)

floor = np.zeros(GRID_SIZE).astype(int)
height = np.zeros(GRID_SIZE).astype(int)

OFFSETS = [
    [0,1],
    [1,0],
    [0,-1],
    [-1,0],
]

visited = np.zeros(GRID_SIZE).astype(bool)
accessible = np.zeros((GRID_SIZE[0],GRID_SIZE[1],4)).astype(bool)
'''
`accessible[i][j]` tells us which directions we can go from cell (i,j)

`accessible[i][j][0]` --> right\n
`accessible[i][j][1]` --> bottom\n
`accessible[i][j][2]` --> left\n
`accessible[i][j][3]` --> top\n

so if `accessible[i][j][2]` and `accessible[i][j][3]`, we can access `(i,j-1)` and `(i-1,j)`
'''


curr = position(50,50,0,0)


def main():
    while True:
        now:float = time.time()
    

        '''
        ROUTING stuff needs to go here
         - fill in the movement grid based on sensor data
         - repeated BFS --> want to explore the entire grid
         - shouldn't disallow backtracking but discourage it
         - so weighted BFS --> literally just djikstra what :sob:
        '''

        # what do we want to do -- explore or ??

        time.sleep(max(TIME_INCREMENT - float(time.time()-now),0))

def closest_unvisited():
    global curr, accessible, height

    # BFS for closest unvisited

    bfs:deque[position] = deque()

    bfs.appendleft(curr)
    seen = set()
    came_from:dict[position, position] = dict()

    to_visit = None
        
    while len(bfs):
        rn = bfs.pop()
        
        if visited[round(rn.x), round(rn.y)]:
            to_visit = rn
        for dir in range(4):
            nxt = rn + OFFSETS[dir]
            seen.add(nxt)
            if accessible[round(rn.x), round(rn.y), dir]:
                came_from[nxt] = rn
                bfs.appendleft(nxt)
    
    if to_visit == None:
        go_home() 

def go_home():
    # bfs for shortest path home
    

    # execute shortest path home

    print("home!")
    sys.exit(0)


def nextMove():
    global curr, accessible, height
    x, y = round(curr.x), round(curr.y)
    nxt = curr + OFFSETS[curr.dir]
    if accessible[x,y,curr.dir] and not visited[round(nxt.x), round(nxt.y)]:
        asyncio.create_task(movement.move_one_tile())
        visited[round(nxt.x), round(nxt.y)] = True
        return
    dir = (curr.dir+1)%4
    while dir != curr.dir:
        nxt = curr+OFFSETS[dir]
        if accessible[x,y,dir] and not visited[round(nxt.x), round(nxt.y)]:
            asyncio.create_task(movement.rotate(dir - curr.dir))
            time.sleep(0.01) #hopefully figures out the rotation
            asyncio.create_task(movement.move_one_tile())
            visited[round(nxt.x), round(nxt.y)] = True
            return
        dir = (dir+1)%4
    closest_unvisited()
    
    



if __name__ == "__main__": main()
