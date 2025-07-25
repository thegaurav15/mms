import os
from PIL import Image
import shutil
from math import floor
import tempfile
from io import BytesIO

MAXSIZE = 100000

def makeJpg(file):
    img = Image.open(file)
    output = BytesIO()
    img.convert('L').save(output, format="JPEG",  optimize=True, quality=75)     #first pass
    size = output.tell()    #get the saved file size
    pass_counter = 1
    
    x = 0
    while size > MAXSIZE:          #applying successive passes
        output.close()
        output = BytesIO()
        w, h = floor(img.width * (1-x)), floor(img.height * (1-x))
        img.convert('L').resize((w, h)).save(output, format='JPEG', optimize=True, quality=55)
        size = output.tell()
        x = x + 4/100
        pass_counter += 1
    
    print(output, pass_counter)
    output.seek(0)
    yield output.read()

def makeTif(file):
    img = Image.open(file)
    output = BytesIO()
    img.convert('1').save(output, format="TIFF",  optimize=True)     #first pass
    size = output.tell()    #get the saved file size
    pass_counter = 1
    
    x = 0
    while size > MAXSIZE:          #applying successive passes
        output.close()
        output = BytesIO()
        x = x + 4/100
        w, h = floor(img.width * (1-x)), floor(img.height * (1-x))
        img.convert('1').resize((w, h)).save(output, format="TIFF",  optimize=True)
        size = output.tell()
        pass_counter += 1
    
    print(output, pass_counter)
    output.seek(0)
    yield output.read()
