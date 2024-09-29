from svgpathtools import svg2paths2, parse_path, wsvg, Path, Line
import glob
from bs4 import BeautifulSoup
from utils import *
from llvmapi import detect_object

files = map( lambda x: x.replace("\\", "/"), glob.glob('./svgs/*.svg'))

for file in files:

    # Read the SVG file and parse
    with open(file, 'r') as f:
        soup = BeautifulSoup(f, 'xml')
        root = soup.find('svg')

    # Get the binary representation of the current SVG file
    binaryImage = svg2base64(file)

    # Parse the SVG file to get the paths, attributes and SVG attributes using svgpathtools
    paths, attributes, svg_attributes = svg2paths2(file)
    width = float(svg_attributes['width'].replace("px", ""))
    height = float(svg_attributes['height'].replace("px", ""))

    # Write the binary representation of the SVG file to a text file
    filename = file.split("/")[-1]
    with open(f"./binImgs/binary-{filename}.txt", "w") as f:
        f.write(binaryImage)

    # Get the ids of the outmost groups in the SVG file
    first = get_first_degree_groups(root)

    # Keep track of the total bounds of the elements in the SVG file
    total_bounds = []

    # If there are no groups in the SVG file, bound the paths directly
    if not first:
        bounds = bound_paths(root, filename=="", root=root, soup=soup, shift=(0,0), total_bounds=total_bounds)
    else:
        for g in first:
            element = root.find('g', id=g)

            # Bound the paths in the group with depth-first search
            bounds = bound_paths(element, filename=="", root=root, soup=soup, shift=(0,0), total_bounds=total_bounds)

    # Remove duplicate bounding boxes (tuples are hashable) NOTE: not sure why there are duplicates
    total_bounds = list(set(total_bounds))

    # Draw the bounding boxes of the elements in the SVG file
    for bbox in total_bounds:
        add_rect(bbox[0], bbox[2], bbox[1] - bbox[0], bbox[3] - bbox[2], root, soup)

    # Experimenting with prompting scaled bounds
    scaled_bounds = [(b[0] / width, b[1] / width, b[2] / height, b[3] / height ) for b in total_bounds]


    # Detect the objects in the SVG file using the LLVM API
    # res = detect_object(binaryImage, scaled_bounds)
    res = detect_object(binaryImage, total_bounds)

    print("Vision detecting...")

    data = {
        "width": width,
        "height": height,
        "elements": res
    }

    json_res = json.dumps(data, indent=4)

    # Write the JSON responses to a file
    with open(f'./output/{filename}.json', 'w') as f:
        f.write(json_res)

    print("Vision done")

    # Write the SVG file with the bounding boxes of the elements
    with open("./output/" + filename, 'w') as f:
        f.write(str(soup))
    