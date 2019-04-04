#!/usr/bin/env python

from sys import argv
import subprocess
import glob

def run(src_filepath, dst_filepath, area_number):
    #list file names of folder (mypath = folder name)
    import os
    from os import listdir
    from os.path import isfile, join
    #glob_call = str(src_filepath + '/????_6?0??????2018.ecw'
    onlyfiles = glob.glob(src_filepath+'/????_6?{}??????201?.ecw'.format(area_number))
    if not os.path.exists("img/compliant-cog/"):
        os.makedirs("img/compliant-cog/")
    print(onlyfiles)
    #loop through each of these files
    for i in onlyfiles: 
        if i.endswith('2017.ecw') or i.endswith('2018.ecw'):
            #set source
            src = i
            print(src)
            #create destination 
            dst_name = str("{}.tif".format(os.path.splitext(src)[0]))
            dst = str("{}/{}".format(dst_filepath, dst_name.strip('img/ecw/')))
            print(dst)
            #Need something in here to either delete the src file after conversion or to check if dst exists 
            if os.path.isfile(dst):
                print("{} already processed".format(dst))
            else:
                #translate to GeoTiff using src and dst
                print("Starting conversion of {}".format(src))
                subprocess.call(["gdal_translate", "-of", "GTiff", str(src), str(dst), "-co", "TILED=YES", "-co", "COMPRESS=LZW", "-co", "BIGTIFF=YES", "-co", "NUM_THREADS=ALL_CPUS","--config", "GDAL_CACHEMAX","512"])
                print("{} successfully converted".format(src))
                subprocess.call(["gdaladdo", str(dst)])
                subprocess.call(["gdal_translate", "-of", "GTiff", str(dst), str("img/compliant-cog/"+dst_name.strip('img/ecw/')), "-co", "TILED=YES", "-co", "COMPRESS=LZW", "-co", "BIGTIFF=YES", "-co","COPY_SRC_OVERVIEWS=YES", "-co","NUM_THREADS=ALL_CPUS","--config", "GDAL_CACHEMAX","512"])
if __name__ == '__main__':
    run(argv[1], argv[2], argv[3])
