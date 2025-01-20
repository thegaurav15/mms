import os
from PIL import Image
import shutil
from math import floor

def createJpg(img, maxsize, output):
    img.convert('L').save(output,  optimize=True, quality=55)     #first pass
    size = os.path.getsize(output)    #get the saved file size
    pass_counter = 1
    
    h, w = img.height, img.width    #resolution for first pass
    while size > maxsize:          #applying successive passes
        h, w = floor(h * 0.95), floor(w * 0.95)
        img.convert('L').resize((w, h)).save(output,  optimize=True, quality=55)
        size = os.path.getsize(output)
        pass_counter = pass_counter + 1
    
    print(output, pass_counter)
    
def createTif(img, maxsize, output):
    img.convert('1').save(output,  optimize=True)     #first pass
    size = os.path.getsize(output)    #get the saved file size
    pass_counter = 1
    
    h, w = img.height, img.width    #resolution for first pass
    while size > maxsize:          #applying successive passes
        h, w = floor(h * 0.95), floor(w * 0.95)
        img.convert('1').resize((w, h)).save(output,  optimize=True)
        size = os.path.getsize(output)
        pass_counter = pass_counter + 1
    
    print(output, pass_counter)