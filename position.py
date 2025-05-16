import numpy as np
class position:
    def __init__(self, x:float=0,y:float=0,z:float=0,dir=0):
        self.x = x
        self.y = y
        self.z = z
        self.dir = dir
    
    def copy(self):
        return position(self.x,self.y,self.z,self.dir)

    def __add__(self, other):
        new = self.copy()
        try:
            to_add = np.asarray(other)
            if len(to_add.shape) != 1: raise TypeError(f"how {len(to_add.shape)}D matrix to vector??")

            new.x += to_add[0]
            new.y += to_add[1]
            new.z += to_add[2]
            return new
        except: raise TypeError(f"you give {type(other)} i no like")
    
    def __sub__(self, other):
        new = self.copy()
        try:
            to_add = np.asarray(other)
            if len(to_add.shape) != 1: raise TypeError(f"how {len(to_add.shape)}D matrix to vector??")

            new.x -= to_add[0]
            new.y -= to_add[1]
            new.z -= to_add[2]
            return new
        except: raise TypeError(f"you give {type(other)} i no like")
    
    def __mul__(self,other):
        new = self.copy()
        try:
            to_add = np.asarray(other)
            if len(to_add.shape) != 1: raise TypeError(f"how {len(to_add.shape)}D matrix to vector??")

            if to_add.shape[0] == 1:
                new.x*=to_add[0]
                new.y*=to_add[0]
                new.z*=to_add[0]
            else:
                new.x *= to_add[0]
                new.y *= to_add[1]
                new.z *= to_add[2]
            return new
        except: raise TypeError(f"you give {type(other)} i no like")
    
    def __div__(self,other):
        new = self.copy()
        try:
            to_add = np.asarray(other)
            if len(to_add.shape) != 1: raise TypeError(f"how {len(to_add.shape)}D matrix to vector??")

            if to_add.shape[0] == 1:
                new.x/=to_add[0]
                new.y/=to_add[0]
                new.z/=to_add[0]
            else:
                new.x /= to_add[0]
                new.y /= to_add[1]
                new.z /= to_add[2]
            return new
        except Exception as e: raise e
    
    def __eq__(self, other):
        if type(other) == position:
            return self.x == other.x and self.y == other.y and self.z == other.z and self.dir == other.dir
        else:
            try:
                to_add = np.asarray(other)
                return to_add[0] == self.x and to_add[1] == self.y and to_add[2] == self.z
            except: return False

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}) @ {self.dir}"
    
    def __getitem__(self,idx:int):
        if idx >= 3: raise IndexError()
        return [self.x,self.y,self.z][idx]
    
    def __setitem__(self,idx:int,value:float):
        if idx >= 3: raise IndexError()
        if idx==0: self.x = value
        if idx==1: self.y = value
        if idx==2: self.z = value