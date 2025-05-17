import numpy as np
class position:
    def __init__(self, x:float=0,y:float=0,z:float=0,dir=0):
        self.x = x
        self.y = y
        self.z = z
        self.dir = dir

    @staticmethod
    def from_array(arr):
        try:
            nums = np.asarray(arr).astype(float)

            if len(nums) == 1: return position(dir=nums[0])
            if len(nums) == 3: return position(nums[0],nums[1],nums[2])
            if len(nums) == 4: return position(nums[0],nums[1],nums[2],nums[3])
        except: pass
        raise TypeError()

    def as_array(self) -> np.ndarray:
        return np.asarray([self.x, self.y, self.z, self.dir])
    
    def copy(self):
        return position(self.x,self.y,self.z,self.dir)
    
    def strict_equals(self, other):        
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z) and (self.dir == other.dir)
    
    def coords(self) -> tuple[int,int,int]:
        return (round(self.x), round(self.y), round(self.z))


    def __add__(self, other):
        new = self.copy()
        if isinstance(other, position):
            new.x += other.x
            new.y += other.y
            new.z += other.z
            return new
        try:
            to_add = np.asarray(other)
            if len(to_add.shape) != 1: raise ValueError(f"how {len(to_add.shape)}D matrix to vector??")

            new.x += to_add[0]
            new.y += to_add[1]
            if len(to_add) >= 3: new.z += to_add[2]
            return new
        except: raise TypeError(f"you give {type(other)} i no like")
    
    def __sub__(self, other):
        new = self.copy()
        if isinstance(other, position):
            new.x -= other.x
            new.y -= other.y
            new.z -= other.z
            return new
        try:
            to_sub = np.asarray(other)
            if len(to_sub.shape) != 1: raise ValueError(f"Cannot subtract {len(to_sub.shape)}D matrix with vector")
            
            new.x -= to_sub[0]
            new.y -= to_sub[1]
            if len(to_sub) >= 3: new.z += to_sub[2]
            return new
        except: raise TypeError(f"you give {type(other)} i no like")
    
    def __mul__(self,other):
        new = self.copy()
        if isinstance(other, position):
            new.x*=other.x
            new.y*=other.y
            new.z*=other.z
            return new
        try:
            to_mul = np.asarray(other)
            if len(to_mul.shape) != 1: raise ValueError(f"Cannot multiply {len(to_mul.shape)}D matrix with vector")

            if to_mul.shape[0] == 1:
                new.x*=to_mul[0]
                new.y*=to_mul[0]
                new.z*=to_mul[0]
            elif to_mul.shape[0] == 3:
                new.x *= to_mul[0]
                new.y *= to_mul[1]
                new.z *= to_mul[2]
            else: raise ValueError(f"Cannot multiply by a vector of length {to_mul.shape[0]}")
            return new
        except: raise TypeError(f"you give {type(other)} i no like")
    
    def __div__(self,other):
        new = self.copy()
        try:
            if isinstance(other, position):
                new.x/=other.x
                new.y/=other.y
                new.z/=other.z
                return new
        except ZeroDivisionError as err: raise err
        try:
            to_div = np.asarray(other)
            if len(to_div.shape) != 1: raise ValueError(f"Cannot divide a {len(to_div.shape)}D matrix with vector.")
            if to_div.shape[0] == 1:
                new.x/=to_div[0]
                new.y/=to_div[0]
                new.z/=to_div[0]
            elif to_div.shape[0] == 3:
                new.x /= to_div[0]
                new.y /= to_div[1]
                new.z /= to_div[2]
            else: raise ValueError("Cannot divide by a vector of that length")
            return new
        except Exception as e: raise e
    
    def __eq__(self, other):
        '''Checks location but NOT direction'''
        if isinstance(other, position):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            try:
                to_cmp = np.asarray(other)
                return bool(to_cmp[0] == self.x and to_cmp[1] == self.y and to_cmp[2] == self.z)
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

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __len__(self):
        return 3