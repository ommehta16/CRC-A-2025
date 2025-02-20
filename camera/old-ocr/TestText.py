import easyocr
import numpy as np
reader = easyocr.Reader(['en'])

def readText(img:np.array) -> str:
    '''returns str or None'''
    txt = reader.readtext(img)
    if (txt is None or len(txt) == 0): return None

    return str(txt[0][1])