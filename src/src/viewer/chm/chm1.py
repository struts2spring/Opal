#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from PIL import Image
import urlparse
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

class CHMFile:
    def __init__(self, file_name):
        self.chmfile = chm.CHMFile()
        self.chmfile.LoadCHM(file_name)

    def create_thumb(self, out_file):       
        image = None
        area = 0 # cover will propably be the biggest image from home page

        iui = self.chmfile.ResolveObject(self.chmfile.home) 
        home = self.chmfile.RetrieveObject(iui[1])[1] # get home page (as html)
        tree = BeautifulSoup(home)
        for img in tree.find_all('img'):
            src_attr =  urlparse.urljoin(self.chmfile.home, img.get('src'))
            chm_image = self.chmfile.ResolveObject(src_attr)
            png_data = self.chmfile.RetrieveObject(chm_image[1])[1] # get image (as raw data)

            png_img = Image.open(StringIO(png_data))
            new_width, new_height = png_img.size
            new_area = new_width * new_height 
            if(new_area > area and new_width > 50 and new_height > 50): # to ensure image is at least 50x50
                area = new_area
                image = png_img
        if image:
            image.save(out_file, format="PNG")


if __name__ == '__main__':
    import sys
    chm = CHMFile('1.chm')
    chm.create_thumb('2.png')