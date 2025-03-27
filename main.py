from sensors import color, distance
from movement import movement, routing
import multiprocessing as mp
import multiprocessing.connection as connection
import time
import numpy as np

# from camera import PiCam as camera
# from camera import PiText as ocr

TIME_INCREMENT:float = 0.5
START:float          = time.time()
MAX_PULL_WAIT:float  = 5

move, tmp = mp.Pipe() #tmp is the other end of the pipe, so we can forget it
move_prc = mp.Process(target=movement.run, args=(tmp, ))
del tmp

GRID_SIZE = (100,100)

floor = np.zeros(GRID_SIZE).astype(int)
height = np.zeros(GRID_SIZE).astype(int)

accessible = np.zeros(GRID_SIZE).astype(int)
'''
`accessible[i][j]` is a bitmask for the cells we cango to directly

bits correspond to lrtb (i.e. `3` = `0011` means we can access `(i-1,j)` and `(i+1, j)`)
'''

def main():
    while True:
        now:float = time.time()
    
        while move.poll() and (time.time()-now < TIME_INCREMENT or now-lastPull >= MAX_PULL_WAIT):
            lastPull = time.time()
            newData = move.recv()
            '''
            get data from move for how far we've gone since last turn (in tiles, preferrably)
            '''

        '''
        ROUTING stuff needs to go here
         - fill in the movement grid based on sensor data
         - repeated BFS --> want to explore the entire grid
         - shouldn't disallow backtracking but discourage it
         - so weighted BFS
        '''

        time.sleep(max(TIME_INCREMENT - float(time.time()-now),0))

if __name__ == "__main__": main()