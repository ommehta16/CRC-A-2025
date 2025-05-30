print("starting...")
from multiprocessing import Process, Queue, Event, set_start_method
from FinalCode.Camera import producer
from FinalCode.DetectRectColor import detector
import time
import numpy as np
from position import position
from movement import movement, output
import asyncio
from collections import deque
import sensors
import sys
import RPi.GPIO as GPIO
import traceback

TIME_INCREMENT:float = 0.5
START:float          = time.time()
MAX_PULL_WAIT:float  = 5

GRID_SIZE = (100,100,2)

OFFSETS = [
    [0,1],
    [1,0],
    [0,-1],
    [-1,0],
]

water = set()

HOME = position(50,50,0,0)

visited = np.zeros(GRID_SIZE).astype(int)
accessible = np.zeros((GRID_SIZE[0],GRID_SIZE[1],GRID_SIZE[2],4)).astype(int)
'''
`accessible[i][j][k][dir]` tells us what's accessible from cell (i,j,k) in direction dir:
RBTL (0R, 1B, 2L, 3T)

-1 --> not checked\n
0 --> not accessible\n
1 --> accessible
'''

accessible-=1



frame_queue     = Queue(maxsize=5)
annotated_queue = Queue(maxsize=5)
color_queue = Queue()
stop_event      = Event()
procs = [
    Process(target=producer, args=(frame_queue, stop_event)),
    Process(target=detector, args=(frame_queue, color_queue, stop_event)),
    # Process(target=consumer, args=(annotated_queue, color_queue, stop_event)),
]
for p in procs: p.start()

curr = position(50,50,0,0)
ramps:set[position] = set()
'''
A RAMP IS BASICALLY JUST AN ELEVATOR
so if position A is a ramp, B (a w/ opposite z) is its corresponding part on the other floor
they exist on different floors
and A and B are only accessible from 1 side each (the side we explored to them from)
'''

wall_anchor = None

mode = "WANDER"
'''is `"WANDER"`, `"EXPLORE"`, or `"NAVIGATE"` based on the current mode'''
nav_tgt = None

def main():
    global curr, accessible, wall_anchor, mode
    print("started")

    while wall_anchor == None:

        visit(curr + OFFSETS[curr.dir])
        if all(accessible[curr.coords()]!=0): continue
        # keep looking unless theres DEFINITELY a wall here
        # This allows initial exploration to be faster (basically just moving in a straight line
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
        if sensors.get_button(): return #close if the button is pressed
        if not color_queue.empty():
            color=color_queue.get() # the color is _only_ important for debug purposes
            if color=="red":
                deploy_kit(2)
            elif color=="yellow":
                deploy_kit(1)
            elif color=="green":
                deploy_kit(0)
            asyncio.run(movement.stop())

        
        if mode == "WANDER": wander()
        elif mode == "EXPLORE": explore()
        elif mode == "NAVIGATE":
            navigate()
            if curr == HOME:
                print("it's over!")
                return
            mode = "WANDER"
        elif mode == "END": return
        else: raise Exception("bruh?")
        time.sleep(max(TIME_INCREMENT - float(time.time()-now),0))

def navigate():
    print("navigate")
    global curr, accessible, mode, nav_tgt
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
        
        if rn == nav_tgt:
            to_visit = rn
            break
        for dir in range(4):
            nxt = rn + OFFSETS[dir]
            if nxt in seen: continue
            seen.add(nxt)
            if accessible[(*rn.coords(), dir)] == 1:
                came_from[nxt] = rn
                bfs.appendleft(nxt)

        if rn in ramps:
            tmp = rn.copy()
            tmp.z = int(not bool(round(rn.z)))
            bfs.appendleft(tmp)
    if to_visit == None:
        check_active()
        print("NO PATH FOUND")
        mode = "WANDER"
        return
    

    path:list[position] = []
    while not to_visit.strict_equals(curr):
        path.append(to_visit)
        to_visit = came_from[to_visit]

    while len(path): #TODO should we nav direct or ??
        visit(path[-1])
        path.pop()

def wander():
    print("wander")
    global curr, accessible, mode, wall_anchor

    # BFS for closest unvisited
    bfs:deque[position] = deque()

    bfs.appendleft(curr)
    seen = set()
    came_from:dict[position, position] = dict()

    to_visit = None
    
    while len(bfs):
        rn = bfs.pop() # current node in BFS
        
        if visited[rn.coords()] == 0 or visited[rn.coords()] == 1:

            # if we haven't OR have only partially seen it
            to_visit = rn
            break
        for dir in range(4):
            nxt = rn + OFFSETS[dir]
            if nxt in seen: continue
            seen.add(nxt)
            if accessible[(*rn.coords(),dir)] == 1: # directly accessible
                came_from[nxt] = rn
                bfs.appendleft(nxt)
        if rn in ramps: # accessible via elevator = ramp
            nxt = rn.copy()
            nxt.z = int(not bool(round(rn.z)))
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

    while not rn.strict_equals(curr):
        prev = rn
        rn = came_from[rn]
    EXPLORE_OPP = visited[prev.coords()]==0 and not all(accessible[prev.coords()]==1)

    if EXPLORE_OPP:
        mode="EXPLORE"
        wall_anchor=prev
    visit(prev)

def explore():
    print("explore")
    '''Follow right wall'''

    global mode, wall_anchor
    assert wall_anchor != None

    nxt = curr.copy()
    if not wall_right(curr): nxt.dir = (nxt.dir+1)%4 # turn right if we can
    else:
        if wall_front(curr): nxt.dir = (nxt.dir-1 + 4)%4
        else: nxt += OFFSETS[curr.dir]
    if nxt == wall_anchor:
        mode = "WANDER"
        wall_anchor = None
        return
    visit(nxt)

def check_passive():
    print("check passive")
    global accessible
    # just check on right and front
    front_distance, right_distance = sensors.get_distances()
    front_color = sensors.get_color()
    
    assert front_color and front_distance and right_distance
    front = curr + OFFSETS[curr.dir]
    def rgb_to_hsv(rgb:tuple):
        r,g,b = rgb
        r/=255; g/=255; b/=255
        hue = -1
        delta = max(r,g,b)-min(r,g,b)+0.0001
        if max(r,g,b) == r: hue = ((g-b)/delta) % 6
        elif max(r,g,b) == g: hue = ((b-r)/delta)+2
        else: hue=((r-g)/delta)+4
        hue *= 60
        sat = (max(r,g,b)-min(r,g,b))/(max(r,g,b)+0.0001)

        return hue,sat, max(r,g,b)
    
    h,s,v = rgb_to_hsv(front_color)
    if h<=250 and 200<=h and s>0.5 and v>0.5:
        water.add(front)
    if max(front_color) < 20: # it is black
        accessible[(*curr.coords(),curr.dir)] = 0
        accessible[(*front.coords(),(2+curr.dir)%4)] = 0
        print("front black")
    elif front_distance < 150: # is it close
        accessible[(*curr.coords(), curr.dir)] = 0
        accessible[(*front.coords(), (2+curr.dir)%4)] = 0
        print("front too close")
    else:
        accessible[(*curr.coords(), curr.dir)] = 1
        accessible[(*front.coords(), (2+curr.dir)%4)] = 1
    right = curr + OFFSETS[(curr.dir+1)%4]
    print("front accessible")
    if right_distance < 150:
        accessible[(*curr.coords(), (curr.dir+1)%4)] = 0
        accessible[(*right.coords(), (curr.dir+3)%4)] = 0
        print("right too close")
    else:
        accessible[(*curr.coords(), (curr.dir+1)%4)] = 1
        accessible[(*right.coords(), (curr.dir+3)%4)] = 1
        print("right accessible")

def check_active():
    print("check active")
    for _ in range(4):
        tgt = curr.copy()
        tgt.dir = (curr.dir+1)%4
        visit(tgt)

def wall_right(pos:position)->bool:
    print("wall right")
    if accessible[(*pos.coords(),(pos.dir + 1)%4)] != 1: return True
    return False

def wall_front(pos:position)->bool:
    print("wall front")
    if accessible[(*pos.coords(),pos.dir)] != 1: return True
    return False

def go_home():
    print("go home")
    global mode, nav_tgt
    nav_tgt = HOME
    mode = "NAVIGATE"

def visit(dest:position):
    print("visit")
    '''
    go to the location `tile` and update accessibility accordingly
    `tile` must be 1 move away (meaning any rotation and up to 1 tile of movement)
    '''
    global curr

    # `vec_to` is an integer vector for how many tiles we need to move
    vec_to = position.from_array(dest.coords())-position.from_array(curr.coords())

    if abs(vec_to.x) + abs(vec_to.y) > 1: raise ValueError(f"Target [{dest}] is too far from [{curr}]")

    if vec_to.x ==0 and vec_to.y ==0: necessary_dir = dest.dir
    else: necessary_dir = OFFSETS.index([round(vec_to.x),round(vec_to.y)])
    
    if necessary_dir != curr.dir: # we have to rotate
        rot_amt = (necessary_dir - curr.dir+4)%4
        if rot_amt == 3: rot_amt = -1
        asyncio.run(movement.rotate(rot_amt))
        curr.dir = necessary_dir
        time.sleep(0.01)
    check_passive()
    update_visitedness(curr)
    
    if vec_to.x ==0 and vec_to.y ==0: return
    
    # do the actual movement
    start = curr.copy()
    delta_height = asyncio.run(movement.move_tiles(1))
    # ^ as a proportion of 25cm
    
    # curr is now the state AFTER the move
    curr.x = dest.x
    curr.y = dest.y

    # check with the original z initially
    check_passive()
    update_visitedness(curr)
    curr.z += delta_height
    # ^^ if we realize that we did a ramp, these get overwritten

    if curr in water:
        print("IM SO WET RN")
        time.sleep(5)

    # Ramp Detection
    if round(curr.z) != round(start.z):
        print(f'''
            WARNING: Moved to floor {curr.z} (delta_height = {delta_height}) 
            from floor {start.z}. Expected floor {dest.z}
        ''')

        ramps.add(curr.copy())
        ramps.add(start.copy())

# Accessibility for the start of the ramp (on 'start_state_before_move' floor)
        accessible[(*start.coords(), start.dir)] = 0
        accessible[(*start.coords(), (start.dir + 1) % 4)] = 0
        accessible[(*start.coords(), (start.dir + 3) % 4)] = 0
        accessible[(*start.coords(), (start.dir + 2) % 4)] = 1
        update_visitedness(start)
        
        # Accessibility for the end of the ramp (on 'curr' floor, robot facing curr.dir)
        accessible[(*curr.coords(), curr.dir)] = 1
        accessible[(*curr.coords(), (curr.dir+1)%4)] = 0
        accessible[(*curr.coords(), (curr.dir+3)%4)] = 0
        accessible[(*curr.coords(), (curr.dir+2)%4)] = 0
        update_visitedness(curr)

def update_visitedness(tile:position):
    print("update visitedness")
    global visited

    if all(accessible[tile.coords()]!=-1): visited[tile.coords()] = 2 # All directions checked (are 0 or 1)
    elif any(accessible[tile.coords()]!=-1): visited[tile.coords()] = 1 # Some directions checked
    else: visited[tile.coords()] = 0 # No directions checked

def deploy_kit(n):
    print("deploy kit")
    for i in range(n):
        output.eject()
    
    asyncio.run(output.blink())

def reset():
    print("reset")
    global mode, accessible, visited, ramps
    mode = "WANDER"
    sensors.blink(10,0.1)
    time.sleep(10)
    # accessible = np.zeros((GRID_SIZE[0],GRID_SIZE[1],GRID_SIZE[2],4)).astype(int)
    # accessible-=1
    # visited = np.zeros(GRID_SIZE).astype(int)
    sensors.blink(10,0.1)
    ramps = set()
    print("SHIT")

if __name__ == "__main__":
    try:
        try: set_start_method("spawn")
        except: pass
        print("wow so cool")
        sensors.initialize_sensors()
        sensors.blink(2)
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        stop_event.set()
    finally:
        print("Exiting, joining processes...")
        GPIO.cleanup()
        stop_event.set() # Ensure all processes are signalled to stop
        for p in procs:
            if p.is_alive():
                p.join(timeout=2) # Wait for processes to finish
            if p.is_alive():
                print(f"Process {p.name} did not terminate, killing.")
                p.kill() # Force kill if join times out
        print("All processes joined.")

    
#     try:
#         try:
#             set_start_method("spawn")  # Required for Picamera2 multiprocessing
#         except RuntimeError: 
#             pass
#         sensors.blink(2)
#         while True:
#             try: main()
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 traceback.print_exc()
#                 stop_event.set()
            
#             while True:
#                 print("enters")
#                 if sensors.get_button():
#                     print("restarting...")
#                     sensors.blink(1,0.1)
#                     reset()
#                     sensors.blink(1,0)
#                     break
#                 sensors.blink(1,0)
#                 time.sleep(0.5)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         import traceback
#         traceback.print_exc()
#         stop_event.set()
#     finally:
#         print("Exiting, joining processes...")
#         GPIO.cleanup()
#         stop_event.set() # Ensure all processes are signalled to stop
#         for p in procs:
#             if p.is_alive():
#                 p.join(timeout=2) # Wait for processes to finish
#             if p.is_alive():
#                 print(f"Process {p.name} did not terminate, killing.")
#                 p.kill() # Force kill if join times out
#         print("All processes joined.")

#         sensors.blink(1,0)
#         time.sleep(0.5)

# print("Exiting, joining processes...")
# GPIO.cleanup()
# stop_event.set() # Ensure all processes are signalled to stop
# for p in procs:
#     if p.is_alive():
#         p.join(timeout=2) # Wait for processes to finish
#     if p.is_alive():
#         print(f"Process {p.name} did not terminate, killing.")
#         p.kill() # Force kill if join times out
# print("All processes joined.")
