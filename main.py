from sensors import color, distance
# from movement. import movement, routing
import multiprocessing as mp
import multiprocessing.connection as connection
import time
import numpy as np
import heapq

# from camera import PiCam as camera
# from camera import PiText as ocr

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

accessible = np.zeros((GRID_SIZE[0],GRID_SIZE[1],4)).astype(bool)
'''
`accessible[i][j]` tells us which directions we can go from cell (i,j)

`accessible[i][j][0]` --> right
`accessible[i][j][1]` --> bottom
`accessible[i][j][2]` --> left
`accessible[i][j][3]` --> top

so if `accessible[i][j][2]` and `accessible[i][j][3]`, we can access `(i,j-1)` and `(i-1,j)`
'''

'''
OK FOR MESSAGES

We're just going to send in json format bc im lazy af

{
    "variable": value,
    "error": "none"
}

if no error ^^

if there is some error, 

{
    "error": anything other than none
}

the error only rly exists if we're doing requests... we probs aren't anyways, BUT leave error there just in case

'''

curr = (50,50)
direction = [0,1]
height = 0

def main():
    while True:
        now:float = time.time()
    
        # while move.poll() and (time.time()-now < TIME_INCREMENT or now-lastPull >= MAX_PULL_WAIT):
        #     lastPull = time.time()
        #     newData = move.recv()
        #     '''
        #     get data from move for how far we've gone since last turn (in tiles, preferrably)
        #     '''

        #     # newData is literally just the delta height lol

        #     if type(newData) != int:
        #         print("tf is tjis?")
        #         continue

        #     delta_height = newData

        '''
        ROUTING stuff needs to go here
         - fill in the movement grid based on sensor data
         - repeated BFS --> want to explore the entire grid
         - shouldn't disallow backtracking but discourage it
         - so weighted BFS --> literally just djikstra what :sob:
        '''

        # DJIKSTRA HERE

        a = []
        heapq.heapify(a)

        # what do we want to do -- explore or ??

        # move.send({"turn":"right"})
        time.sleep(max(TIME_INCREMENT - float(time.time()-now),0))

if __name__ == "__main__": main()