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

height = np.zeros(GRID_SIZE).astype(int)

OFFSETS = [
    [0,1],
    [1,0],
    [0,-1],
    [-1,0],
]

HOME = position(50,50,0)

visited = np.zeros(GRID_SIZE).astype(int)
accessible = np.zeros((GRID_SIZE[0],GRID_SIZE[1],4)).astype(int)
'''
`accessible[i][j]` tells us which directions we can go from cell (i,j) in RBTL (0R, 1B, 2L, 3T)

so if `accessible[i][j][2]` and `accessible[i][j][3]`, we can access `(i,j-1)` and `(i-1,j)`

-1 --> not checked\n
0 --> not accessible\n
1 --> accessible
'''

accessible-=1

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
nav_tgt = None

def main():
    global curr, accessible, height
    print("started")

    while wall_anchor == None:
        
        visit(curr + OFFSETS[curr.dir])
        if all(accessible[round(curr.x), round(curr.y)]!=0): continue
        wall_anchor = curr
    
    while not wall_right(curr):
        nxt=curr.copy()
        nxt.dir = (nxt.dir+1)%4
        visit(nxt)
    check_active()
    mode = "EXPLORE"

    while True:
        now:float = time.time()
        # grab color data from consumer here
        while not color_queue.empty():
            print(color_queue.get()) # the color is _only_ important for debug purposes
            asyncio.run(movement.stop())
            deploy_kit() #TODO NOT IMPLEMENTED YET!!!
        
        if mode == "WANDER":
            wander()
        elif mode == "EXPLORE":
            explore()
        elif mode == "NAVIGATE":
            navigate()
            if curr.as_array() == HOME:
                print("it's over!")
                return
            mode = "WANDER"
        elif mode == "END": return
        else: raise Exception("bruh?")
        time.sleep(max(TIME_INCREMENT - float(time.time()-now),0))

def navigate():
    global curr, accessible, height, mode, nav_tgt
    if not nav_tgt:
        check_active()
        mode = "WANDER"
        return
    # BFS to home

    bfs:deque[position] = deque()

    bfs.appendleft(curr)
    seen = set()
    came_from:dict[position, position] = dict()

    to_visit = None
        
    while len(bfs):
        rn = bfs.pop() # where we "are" rn in bfs
        
        if rn.as_array() == nav_tgt:
            to_visit = rn
            break
        for dir in range(4):
            nxt = rn + OFFSETS[dir]
            if nxt in seen: continue
            seen.add(nxt)
            if accessible[round(rn.x), round(rn.y), dir] == 1:
                came_from[nxt] = rn
                bfs.appendleft(nxt)
    if to_visit == None:
        print("NO PATH FOUND")
        mode = "WANDER"
        return
    

    path:list[position] = []
    while to_visit != curr.as_array():
        path.append(to_visit)
        to_visit = came_from[to_visit]

    while len(path): #TODO should we nav direct or ??
        visit(path[-1])
        curr = path[-1]
        path.pop()

def wander():
    global curr, accessible, height, mode, wall_anchor

    # BFS for closest unvisited
    bfs:deque[position] = deque()

    bfs.appendleft(curr)
    seen = set()
    came_from:dict[position, position] = dict()

    to_visit = None
    
    while len(bfs):
        rn = bfs.pop()
        
        if visited[round(rn.x), round(rn.y)] == 0 or visited[round(rn.x), round(rn.y)] == 1:
            # if we haven't OR have only partially seen it
            to_visit = rn
            break
        for dir in range(4):
            nxt = rn + OFFSETS[dir]
            if nxt in seen: continue
            seen.add(nxt)
            if accessible[round(rn.x), round(rn.y), dir] == 1:
                came_from[nxt] = rn
                bfs.appendleft(nxt)
    
    if to_visit == None:
        go_home()
        return
    
    if to_visit == curr:
        check_active()
        return
    # now we go to to_visit :)
    rn = came_from[to_visit]
    prev = to_visit

    while rn != curr:
        prev = rn
        rn = came_from[rn]
    if visited[round(prev.x),round(prev.y)] == 0 and not all(accessible[round(prev.x),round(prev.y)]==1):
        mode="EXPLORE"
        wall_anchor=prev

    visit(prev)

def explore():
    '''Follow right wall'''

    global mode, wall_anchor
    assert wall_anchor != None

    nxt = curr.copy()
    if not wall_right(curr): nxt.dir = (nxt.dir+1)%4 # turn right if we can
    else:
        if wall_front(curr): nxt.dir = (nxt.dir-1 + 4)%4
        else: nxt += OFFSETS[curr.dir]
    if nxt == wall_anchor.as_array():
        mode = "WANDER"
        wall_anchor = None
        return
    visit(nxt)

def check_passive():
    # just check on right and front
    front_distance, right_distance = sensors.get_distances()
    front_color = sensors.get_color()
    assert front_color and front_distance and right_distance
    front = curr + OFFSETS[curr.dir]

    if max(front_color) < 20: # it is black
        accessible[round(curr.x), round(curr.y),curr.dir] = 0
        accessible[round(front.x), round(front.y),(2+curr.dir)%4] = 0
    elif front_distance < 150: # is it close
        accessible[round(curr.x), round(curr.y), curr.dir] = 0
        accessible[round(front.x), round(front.y), (2+curr.dir)%4] = 0
    else:
        accessible[round(curr.x), round(curr.y), curr.dir] = 1
        accessible[round(front.x), round(front.y), (2+curr.dir)%4] = 1
    
    right = curr + OFFSETS[(curr.dir+1)%4]
    if right_distance < 150:
        accessible[round(curr.x), round(curr.y), (curr.dir+1)%4] = 0
        accessible[round(right.x), round(right.y), (curr.dir+3)%4] = 0
    else:
        accessible[round(curr.x), round(curr.y), (curr.dir+1)%4] = 1
        accessible[round(right.x), round(right.y), (curr.dir+3)%4] = 1


def check_active():
    for _ in range(4):
        asyncio.run(movement.rotate(1))
        curr.dir = (curr.dir+1)%4
        check_passive()

def wall_right(pos:position)->bool:
    if accessible[round(pos.x),round(pos.y),(pos.dir + 1)%4] != 1: return True
    return False

def wall_front(pos:position)->bool:
    if accessible[round(pos.x),round(pos.y),pos.dir] != 1: return True
    return False

def go_home():
    global mode, nav_tgt
    nav_tgt = HOME
    mode = "NAVIGATE"    
    navigate()

    print("home!")
    mode = "END"

def visit(tile:position):
    global curr
    '''
    go to the location `tile` and update accessibility accordingly
    `tile` must be 1 move away (meaning any rotation and up to 1 tile of movement)
    '''
    vec_to = tile-curr
    if abs(vec_to.x) + abs(vec_to.y) > 1: raise ValueError("too far")

    if vec_to.x ==0 and vec_to.y ==0: necessary_dir = curr.dir
    else: necessary_dir = OFFSETS.index([round(vec_to.x),round(vec_to.y)])
    
    if necessary_dir != curr.dir:
        asyncio.run(movement.rotate(necessary_dir - curr.dir))
        curr.dir = necessary_dir
        time.sleep(0.01)
    asyncio.run(movement.move_tiles(1))
    check_passive()
    curr = tile
    update_visitedness(curr)

def update_visitedness(tile:position):
    global visited

    x, y, z = map(round,[tile.x, tile.y, tile.z])

    if all(accessible[x,y]!=-1): visited[x,y] = 2 # All directions checked (are 0 or 1)
    elif any(accessible[x,y]!=-1): visited[x,y] = 1 # Some directions checked
    else: visited[x,y] = 0


def deploy_kit():
    print("kit is being deployed")
    # bruh

    start = time.time()

    while (time.time() - start <= 6): # we're supposed to go for 5 but... 
        
        '''blinky blinky'''

if __name__ == "__main__":
    try: main()
    except: stop_event.set()
    finally:
        for p in procs: p.join()