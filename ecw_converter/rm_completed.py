#!/usr/bin/env python

import boto3
import os
import subprocess
def id():
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('test-geotiff-img')
    file_list=[]
    for object in my_bucket.objects.all():
        my_file=(os.path.splitext(object.key)[0])
        my_file = str(my_file + ".ecw")
        subprocess.call(["rm","img/ecw/{}".format(my_file)])
        file_list.append(my_file)
    print(file_list)
    return(file_list)
if __name__=='__main__':
    id()
