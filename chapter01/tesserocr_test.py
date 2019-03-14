#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/3 10:24
software: PyCharm
description: 
'''

import tesserocr
from PIL import Image

image = Image.open('image.png')
print(tesserocr.image_to_text(image))