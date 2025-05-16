print("starting...")
# from sensors import color, distance
import multiprocessing as mp

from multiprocessing import Process, Queue, Event, set_start_method
from FinalCode.Camera import producer
from FinalCode.DetectRectColor import detector, consumer
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
`accessible[i][j]` tells us which directions we can go from cell (i,j) in RBTL (0R, 1B, 2L, 3T)

so if `accessible[i][j][2]` and `accessible[i][j][3]`, we can access `(i,j-1)` and `(i-1,j)`
'''

set_start_method("spawn")  # Required for Picamera2 multiprocessing

frame_queue     = Queue(maxsize=5)
annotated_queue = Queue(maxsize=5)
color_queue = Queue()
stop_event      = Event()
procs = [
    Process(target=producer, args=(frame_queue, stop_event)),
    Process(target=detector, args=(frame_queue, annotated_queue, stop_event)),
    Process(target=consumer, args=(annotated_queue, color_queue, stop_event)),
]
for p in procs:
    p.start()

curr = position(50,50,0,0)

def main():
    print("started")
    while True:
        todo = asyncio.all_tasks()
        asyncio.run(asyncio.wait(*todo,timeout=10)) # finish up any outstanding tasks from previous move here
        now:float = time.time()
        # grab color data from consumer here
        while not color_queue.empty():
            nxt = color_queue.get()
            print(nxt)
            asyncio.run(movement.stop())
            deploy_kit() #TODO NOT IMPLEMENTED YET!!!
        next_move()
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
            break
        for dir in range(4):
            nxt = rn + OFFSETS[dir]
            if nxt in seen: continue
            seen.add(nxt)
            if accessible[round(rn.x), round(rn.y), dir]:
                came_from[nxt] = rn
                bfs.appendleft(nxt)
    
    if to_visit == None:
        go_home()
        return
    
    # now we go to to_visit :)
    rn = came_from[to_visit]
    prev = to_visit

    while rn != curr:
        prev = rn
        rn = came_from[rn]

    # go from `curr` to `prev`
    vec_to = prev-curr

    necessary_dir = OFFSETS.index([round(vec_to.x),round(vec_to.y)])

    asyncio.create_task(movement.rotate(necessary_dir-curr.dir))
    time.sleep(0.01)
    asyncio.create_task(movement.move_tiles(1))

def go_home():
    # bfs for shortest path home

    global curr, accessible, height

    # BFS to home

    bfs:deque[position] = deque()

    bfs.appendleft(curr)
    seen = set()
    came_from:dict[position, position] = dict()

    to_visit = None
        
    while len(bfs):
        rn = bfs.pop() # where we "are" rn in bfs
        
        if (rn.x,rn.y) == (50,50):
            to_visit = rn
            break
        for dir in range(4):
            nxt = rn + OFFSETS[dir]
            if nxt in seen: continue
            seen.add(nxt)
            if accessible[round(rn.x), round(rn.y), dir]:
                came_from[nxt] = rn
                bfs.appendleft(nxt)
    
    assert to_visit != None

    path:list[position] = []
    while to_visit != curr:
        path.append(to_visit)
        to_visit = came_from[to_visit]

    while len(path):
        visit(path[-1])
        curr = path[-1]
        path.pop()

    print("home!")
    sys.exit(0)


def next_move():
    global curr, accessible, height
    x, y = round(curr.x), round(curr.y)
    nxt = curr + OFFSETS[curr.dir]
    if accessible[x,y,curr.dir] and not visited[round(nxt.x), round(nxt.y)]:
        visit(nxt)
        return
    dir = (curr.dir+1)%4
    while dir != curr.dir:
        nxt = curr+OFFSETS[dir]
        if accessible[x,y,dir] and not visited[round(nxt.x), round(nxt.y)]:
            visit(nxt)
            return
        dir = (dir+1)%4
    closest_unvisited()

def visit(tile:position):
    '''
    go to the adjacent location `tile` and update accessibility accordingly
    '''
    if (tile - curr).as_array().sum() > 1: raise ValueError("too far")

    vec_to = tile-curr
    necessary_dir = OFFSETS.index([round(vec_to.x),round(vec_to.y)])
    
    if necessary_dir != curr.dir:
        asyncio.run(movement.rotate(necessary_dir - curr.dir))
        time.sleep(0.01)
    asyncio.run(movement.move_tiles(1))
    visited[tile.x, tile.y] = True

def deploy_kit():
    print("kit is being deployed")

    # bruh

    start = time.time()

    while (time.time() - start <= 6): # we're supposed to go for 5 but... 
        
        '''blinky blinky'''

if __name__ == "__main__":
    try:
        main()
    except:
        stop_event.set()
    finally:
        for p in procs: p.join()