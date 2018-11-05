"""
Acknowlegement:
@ Script Created on May 3rd 2016
@ Author: Weixing Zhang
@ Purpose: Calculate the true four corners of a remote sensing imagery
@ python 2.76
@ Required modules: gdal, os.path, numpy, and argparse

I learned and gained a lot of help from Python community. Thank you!
I share this script mainly because back then, I could not find a easy-to-use Python script to
calculate the true four corners of a remote sensing imagery, which would exclude the blank areas.

@Prerequirement
Install gdal module
(1) Download gdal if you don't have it installed on your Machine (http://www.lfd.uci.edu/~gohlke/pythonlibs/)
(2) After downloaded gdal.whl, open your command prompt, type "cd /Downloads directory"
(3) type "pip install xxxx.whl"
"""


"""
How to use:
(1) COMMANDLINE: 
python true4corners.py C:\sample_NDVI.tif

(2) import as a module

import true4corners
rs_img_path = r"C:\sample_NDVI.tif"
info_image = true4corners.true4corner(rs_img_path) # is a list of image ID, x1, ... 

OUTPUT FORMAT
Image ID: 1030010084969100 
x1: 72.1315
y1: 142.123
x2: 73.141
y2: 142.123
x3: 73.141
y3: 140.512
x4:  72.1315
y4:  140.512
Date: 2018-09-10
Image Cloud: 0%
Sensor: WV02

"""

# import required modules
import os, os.path
from osgeo import gdal
import numpy as np
from gdalconst import *


def locate_center_edge(raster,edge,rows,cols):
    if edge == "up":
        for i in xrange(0,rows):
            input_array = raster.ReadAsArray(0,i,cols,1).flatten()
            if np.argwhere(input_array!=0).shape[0] != 0:
                break
            else:
                continue
    
    elif edge == "right":
        for i in xrange(0,rows):
            input_array = raster.ReadAsArray(cols-1-i,0,1,rows).flatten()
            if np.argwhere(input_array!=0).shape[0] != 0:
                break
            else:
                continue
    
    elif edge == "down":
        for i in xrange(0,rows):
            input_array = raster.ReadAsArray(0,rows-1-i,cols,1).flatten()
            if np.argwhere(input_array!=0).shape[0] != 0:
                break
            else:
                continue
    
    elif edge == "left":
        for i in xrange(0,rows):
            input_array = raster.ReadAsArray(i,0,1,rows).flatten()
            if np.argwhere(input_array!=0).shape[0] != 0:
                break
            else:
                continue   

    avail_array = np.argwhere(input_array!=0)
    sort_array = np.sort(avail_array.flatten())
    center = np.median(sort_array)
    return center


def info(img_path):
    img_name = img_path.split(os.sep)[-1]
    img_sensor = img_name.split("_")[0]
    img_date_year = img_name.split("_")[1][0:4]
    img_date_month = img_name.split("_")[1][4:6]
    img_date_day = img_name.split("_")[1][6:8]
    
    img_date_f1 = img_date_month+"/"+img_date_day+"/"+img_date_year
    img_date_f2 = img_date_year+"-"+img_date_month+"-"+img_date_day
    
    img_id = str(img_name.split("_")[2])+"-"+str(img_name.split("_")[3])
    
    return [img_id,img_date_f1,img_date_f2,img_sensor]


def true4corner(img_path):
    # read image
    img_info = info(img_path)
    src = gdal.Open(img_path)
    
    # extract image information
    proj = src.GetProjection()
    rows_input = src.RasterYSize
    cols_input = src.RasterXSize
    bands_input = src.RasterCount
    
    # create empty grid cell
    transform = src.GetGeoTransform()
    
    # ulx, uly is the upper left corner
    ulx, x_resolution, _, uly, _, y_resolution  = transform
    lrx = ulx + (src.RasterXSize * x_resolution)
    lry = uly + (src.RasterYSize * y_resolution)
    
    # get the 1st band
    band_1_raster = src.GetRasterBand(1)
    
    # locate the center of the edge with available pixels
    up_edge_cnt = locate_center_edge(band_1_raster,"up",rows_input,cols_input)
    right_edge_cnt = locate_center_edge(band_1_raster,"right",rows_input,cols_input)
    down_edge_cnt = locate_center_edge(band_1_raster,"down",rows_input,cols_input)
    left_edge_cnt = locate_center_edge(band_1_raster,"left",rows_input,cols_input)
        
    # final result
    up_xy = [ulx + (up_edge_cnt * x_resolution), uly]
    right_xy = [lrx, uly + (right_edge_cnt * y_resolution)]
    down_xy = [ulx + (down_edge_cnt * x_resolution), lry]
    left_xy = [ulx, uly + (left_edge_cnt * y_resolution)]
    
    # return the four corners x and y
    """
    OUTPUT FORMAT
    Image ID: 1030010084969100 
    x1: 72.1315
    y1: 142.123
    x2: 73.141
    y2: 142.123
    x3: 73.141
    y3: 140.512
    x4:  72.1315
    y4:  140.512
    Date: 2018-09-10
    Image Cloud: 0%
    Sensor: WV02
    """
    return [img_info[0],
            up_xy[0],
            up_xy[1],
            right_xy[0],
            right_xy[1],
            down_xy[0],
            down_xy[1],
            left_xy[0],
            left_xy[1],
            img_info[1],
            img_info[2],
            "unknown",
            img_info[3]]
