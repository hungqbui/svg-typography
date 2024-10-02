
# Test file to run the code snippets from main.py and overlay_from_json.py

# import svgpathtools
from utils import *
import bs4 as BeautifulSoups
import requests
import json

# paths, attributes, svg_attributes = svgpathtools.svg2paths2('../svgs/circle.svg')

with open('./svgs/whatislove.svg', "r") as f:
    soup = BeautifulSoups.BeautifulSoup(f, "xml")
    root = soup.find("svg")

print(get_text(root))
