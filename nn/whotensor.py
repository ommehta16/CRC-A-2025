import numpy as np
from matplotlib import pyplot as plt
import cv2
import multiprocessing as mp
from PIL import Image
import torch
import time
import math
from multiprocessing import Pool

def conv_1_chnl(chl:np.ndarray,conv:np.ndarray) -> np.ndarray:
    '''
    Convolute one channel using the filter `conv`
    '''
    # a:torch.Tensor = torch.conv1d(torch.tensor(chl),torch.tensor(conv))
    # return a.numpy()
    conv_x = conv.shape[1]
    conv_y = conv.shape[0]
    
    new_chl = np.zeros(chl.shape).astype(int)
    chl = np.pad(chl,(conv_y//2,conv_x//2),'constant',constant_values=(0,0))
    
    for y in range(new_chl.shape[0]): # When convoluting on the CPU, this setup is (almost??) unavoidable. GPU access in python w/o CUDA is annoying though
        for x in range(new_chl.shape[1]):
            curr_block = chl[y:y+conv_y,x:x+conv_x]
            new_chl[y,x] = np.multiply(curr_block,conv).sum()
    
    new_chl = new_chl.clip(0,255)
    return new_chl

def convolute(img_arr: np.ndarray,conv: np.ndarray) -> np.ndarray:
    
    new_img = np.zeros(img_arr.shape).astype(int)
    with Pool() as pool: chnl_list = pool.starmap(conv_1_chnl,[(img_arr[:,:,i],conv) for i in range(3)])
    for i in range(3): new_img[:,:,i] = chnl_list[i] 
    
    new_img = new_img.clip(0,255)
    return new_img

class Blur:
    
    def generate_gauss_kernel(rad,sigma) -> np.ndarray:
        '''Generate a gaussian blur kernel with the specified radius (`rad`) and standard deviation (`sigma`)'''
        arr = np.zeros((2*rad+1,2*rad+1))
        inv_sigma = 1/sigma
        d_squared = lambda x,y: x**2 + y**2
        G = lambda x,y: 0.159154943 * inv_sigma * math.exp(-0.5 * inv_sigma * d_squared(x-rad,y-rad)) # Gaussian function: math from https://en.wikipedia.org/wiki/Gaussian_function
        for y in range(2*rad+1): # loop over the kernel size, set each pixel
            for x in range(2*rad+1):
                arr[x,y] = G(x,y)
                
        return arr/arr.sum()

    def gaussian(img: np.ndarray,radius:float,sigma:float) -> np.ndarray:
        '''Apply a gaussian filter on the specified image (`img`) with the specified radius (`rad`) and standard deviation (`sigma`)'''
        img = convolute(img,Blur.generate_gauss_kernel(radius,sigma)) # Convolute using the gaussian filter
        return img
    

# Takes 36.110 seconds -- That's SLOW
if __name__ == "__main__":
    img_arr = np.array(Image.open("nn/ex.jpg"))

    red = img_arr[:,:,0]
    conv:torch.nn.Conv2d = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, bias=False) 
    conv.weight = torch.nn.Parameter(torch.tensor(
        conv,dtype=torch.float32
    ))
    conv.bias = torch.nn.Parameter(torch.tensor([5],dtype=torch.float32))
    print(conv(red).shape)

    start = time.time()
    new_img_arr = Blur.gaussian(img_arr,16,2)
    end = time.time()
    
    Image.fromarray(np.clip(new_img_arr,0,255).astype(np.uint8)).save("nn/out.png") 

    print(str(end-start) + " seconds")