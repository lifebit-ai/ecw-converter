#!/usr/bin/env python

from sys import argv
import subprocess
def run(src_filepath, dst_filepath):
    #list file names of folder (mypath = folder name)
    import os
    from os import listdir
    from os.path import isfile, join
    import subprocess

    onlyfiles = [f for f in listdir(src_filepath) if isfile(join(src_filepath, f))]
    #loop through each of these files
    for i in onlyfiles:
        #set source
        src = i
        print(src)
        #create destination 
        dst_name = str("{}.tif".format(os.path.splitext(src)[0]))
        dst = str("{}/{}".format(dst_filepath, dst_name))
        print(dst)
        #Need something in here to either delete the src file after conversion or to check if dst exists 
        if os.path.isfile(dst):
            print("{} already processed".format(dst))
        else:
            #translate to GeoTiff using src and dst
            print("Starting conversion of {}".format(src))
            subprocess.call(["gdal_translate", "-of", "GTiff", str("{}/{}".format(src_filepath, src)), str(dst)])
if __name__ == '__main__':
    run(argv[1], argv[2])
