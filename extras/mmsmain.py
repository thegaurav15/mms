import os
from PIL import Image
import shutil
from math import floor
import datetime
import csv
from mandate_image import createJpg, createTif
from mandate_xml import createXml

os.chdir('D:\\Out mandates\\2025-01-17')
from mandate_xml import createXml

print('CWD: ' + os.getcwd() + '\n')

#SETTINGS
EXTENSIONS = ['png', 'jpg', 'jpeg', 'tif', 'tiff']
MAX_SIZE = 100000 #Bytes
NAME_PREFIX = 'MMS-CREATE-HGBX-HGBX344857-' + datetime.datetime.today().strftime('%d%m%Y') + '-10'
ORIGINAL_IMAGES = 'original'
OUTPUT_FOLDER = 'final images and XML'
CSV_FILE = '_CSV.csv'

originals = os.listdir(ORIGINAL_IMAGES) #get a list of original files
originals = sorted(originals)

if not os.path.exists(OUTPUT_FOLDER): #create output folder
        os.mkdir(OUTPUT_FOLDER)

file = open(CSV_FILE)
dictReader = csv.DictReader(file)
for row in dictReader:
    for e in EXTENSIONS:
        filename = row['sno'].zfill(2) + '.' + e
        try:
            originals.remove(filename)
        except ValueError:
            print('No file with name: ' + filename)
        else:
            print('File found: ' + filename)        #image file with right extension found
            break
        
    img = Image.open(ORIGINAL_IMAGES + '/' + filename)
        
    #JPEG
    output_file = OUTPUT_FOLDER + '/' + NAME_PREFIX + row['sno'].zfill(4) + '_detailfront.jpg'
    createJpg(img, MAX_SIZE, output_file)
    
    #TIF
    output_file = OUTPUT_FOLDER + '/' + NAME_PREFIX + row['sno'].zfill(4) + '_front.tif'
    createTif(img, MAX_SIZE, output_file)
    
    #XML
    output_file = OUTPUT_FOLDER + '/' + NAME_PREFIX + row['sno'].zfill(4) + '-INP.xml'
    ref = 'HGBXMMS' + datetime.datetime.today().strftime('%d%m%Y') + row['sno'].zfill(3)
    createXml(output_file, ref, row)
    print('XML Created: ' + output_file + ' with Ref: ' + ref + '\n')