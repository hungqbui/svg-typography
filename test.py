
# Test file to run the code snippets from main.py and overlay_from_json.py

import svgpathtools
from utils import *
import bs4 as BeautifulSoups
import requests
import json

paths, attributes, svg_attributes = svgpathtools.svg2paths2('../svgs/circle.svg')

rects = []
for path in paths:
    bbox = path.bbox()
    rect = svgpathtools.parse_path(f'M {bbox[0]} {bbox[2]} L {bbox[1]} {bbox[2]} L {bbox[1]} {bbox[3]} L {bbox[0]} {bbox[3]} Z')
    rects.append(rect)

paths.extend(rects)

svgpathtools.wsvg(paths, filename='./output.svg')

print(svg2base64('../svgs/circle.svg'))