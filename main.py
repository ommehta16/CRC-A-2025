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
import sensors

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

visited = np.zeros(GRID_SIZE).astype(int)
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
for p in procs: p.start()

curr = position(50,50,0,0)

wall_anchor = None

mode = "WANDER"
'''is `"WANDER"`, `"EXPLORE"`, or `"NAVIGATE"` based on the current mode'''

def main():
    global curr, accessible, height
    print("started")

    while wall_anchor == None:
        todo = asyncio.all_tasks()
        asyncio.run(asyncio.wait(*todo,timeout=10))
        check_passive()
        if all(accessible[round(curr.x), round(curr.y)]): break
        visit(curr + OFFSETS[curr.dir])
        wall_anchor = curr
    
    while not wall_on_right(curr):
        asyncio.run(movement.turn(1))
        curr.dir = (curr.dir+1)%4
    mode = "EXPLORE"

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
        
        # OK SO WHAT IVE REALIZED
        # we need to go 3 modes
        # 1. WANDER
        # 2. EXPLORE
        # 3. NAVIGATE
        # 
        # EXPLORE
        # MAKE IT FOLLOW RIGHT WALL HERE!!
        # PSEUDOCODE:
        # check if wall in front
        # yes -->  (
        # check if wall on right
        #   yes --> turn left, continue
        #   no --> turn right, continue
        # )
        # 
        # no --> (
        # check if wall on right
        #   yes --> move forwards
        #   no --> turn right
        # ) 
        #
        ##
        
        if mode == "WANDER":
            ...
        elif mode == "EXPLORE":
            explore()
        else:
            ...

        nxt = curr + OFFSETS[curr.dir]
        if accessible[round(curr.x),round(curr.y),curr.dir] and not visited[round(nxt.x), round(nxt.y)]:
            visit(nxt)
            return
        dir = (curr.dir+1)%4
        while dir != curr.dir:
            nxt = curr+OFFSETS[dir]
            if accessible[round(curr.x),round(curr.y),dir] and not visited[round(nxt.x), round(nxt.y)]:
                visit(nxt)
                return
            dir = (dir+1)%4
        closest_unvisited()
        time.sleep(max(TIME_INCREMENT - float(time.time()-now),0))

def explore():
    raise NotImplementedError()

def check_passive():
    # just check on right and front
    front_distance, right_distance = sensors.get_distances() # type: ignore
    front_color = sensors.get_color() #type: ignore

    front = curr + OFFSETS[curr.dir]

    if max(front_color) < 20: # it is black
        accessible[round(front.x), round(front.y),curr.dir] = False
    elif front_distance < 150: # is it close
        accessible[round(front.x), round(front.y), curr.dir] = False
    else:
        accessible[round(front.x), round(front.y), curr.dir] = True
    
    right = curr + OFFSETS[(curr.dir+1)%4]
    if right_distance < 150:
        accessible[round(right.x), round(right.y), (curr.dir+1)%4] = False
    else:
        accessible[round(right.x), round(right.y), (curr.dir+1)%4] = True


def check_active():
    for _ in range(4):
        asyncio.run(movement.rotate(1))
        check_passive()

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
        
        if visited[round(rn.x), round(rn.y)] == 2:
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

    visit(prev)

def wall_on_right(pos:position)->bool:
    if not accessible[round(pos.x),round(pos.y),(pos.dir + 1)%4]: return True
    return False

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


def update_visitedness(tile:position):
    if visited[round(tile.x), round(tile.y)]: return
    

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
    check_passive()
    visited[tile.x, tile.y] = 1

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