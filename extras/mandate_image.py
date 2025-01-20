import os
from PIL import Image
import shutil
from math import floor
import tempfile

MAXSIZE = 100000

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

def makeJpg(file):
    img = Image.open(file)
    output = tempfile.TemporaryFile()
    img.convert('L').save(output, format="JPEG",  optimize=True, quality=75)     #first pass
    size = output.tell()    #get the saved file size
    pass_counter = 1
    
    x = 0
    while size > MAXSIZE:          #applying successive passes
        w, h = floor(img.width * (1-x)), floor(img.height * (1-x))
        img.convert('L').resize((w, h)).save(output, format='JPEG', optimize=True, quality=55)
        size = output.tell()
        x = x + 4/100
        pass_counter += 1
    
    print(output, pass_counter)
    return output

def makeTif(file):
    img = Image.open(file)
    output = tempfile.TemporaryFile()
    img.convert('1').save(output, format="TIFF",  optimize=True)     #first pass
    size = output.tell()    #get the saved file size
    pass_counter = 1
    
    x = 0
    while size > MAXSIZE:          #applying successive passes
        x = x + 4/100
        w, h = floor(img.width * (1-x)), floor(img.height * (1-x))
        img.convert('1').resize((w, h)).save(output, format="TIFF",  optimize=True)
        size = output.tell()
        pass_counter += 1
    
    print(output, pass_counter)
    return output
    
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