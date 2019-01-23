# True-4-corners-of-a-Remote-sensing-imagery
Locate the true 4 corners of a remote sensing imagery

NOTE:
This is originally designed for processing WorldView-2 images.
Please feel free to modify the script as needed. 

Acknowlegement:
<li>   @ Script Created on November 5th 2018</li>
<li>   @ Author: Weixing Zhang</li>
<li>   @ Purpose: Calculate the true four corners of a remote sensing imagery</li>
<li>   @ python 2.76</li>
<li>   @ Required modules: gdal, os.path, numpy, and argparse</li>

I learned and gained a lot of help from Python community. Thank you!
I share this script mainly because back then, I could not find a easy-to-use Python script to
calculate the true four corners of a remote sensing imagery, which would exclude the blank areas.

@Prerequirement
Install gdal module
(1) Download gdal if you don't have it installed on your Machine (http://www.lfd.uci.edu/~gohlke/pythonlibs/)
(2) After downloaded gdal.whl, open your command prompt, type "cd /Downloads directory"
(3) type "pip install xxxx.whl"

How to use the script:
1. cmd: 
>python true4corners.py C:\sample_NDVI.tif

2. import the script as a module
'''
import true4corners
rs_img_path = r"C:\sample_NDVI.tif"
info_image = true4corners.true4corner(rs_img_path) # is a list of image ID, x1, ... 
'''

OUTPUT FORMAT
'''
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
'''
