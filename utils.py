# Resuable utility functions for the project

import svgpathtools
import requests
import json

# Get the bounding box of a path using svgpathtools built-in functions
# Shift is used to keep track of the accumulated position of the path within the groups
def get_path_bbox(path_str, shift=None):
    # Parse the path and calculate its bounding box
    path = svgpathtools.parse_path(path_str)
    bbox = path.bbox()  # Returns (xmin, xmax, ymin, ymax)
    if shift:
        bbox = (bbox[0] + shift[0], bbox[1] + shift[0], bbox[2] + shift[1], bbox[3] + shift[1])
    return bbox

# Output a bounding box for a group of bounding boxes
def combine_bboxes(bbox_list):
    # Combine individual bounding boxes into one bounding box for the group
    xmin = min(b[0] for b in bbox_list)
    xmax = max(b[1] for b in bbox_list)
    ymin = min(b[2] for b in bbox_list)
    ymax = max(b[3] for b in bbox_list)
    return (xmin, xmax, ymin, ymax)

# Find only ids of first degree groups
def get_first_degree_groups(root):
    gs = root.find_all('g', recursive=False)
    res = []
    
    for g in gs:
        id = g.get('id', None)
        if id: res.append(id)

    return res

# Draw rectangle
def add_rect(x,y,width,height, root, soup):
    root.append(soup.new_tag('rect', x=x, y=y, width=width, height=height, fill="none", stroke="black", stroke_width="10px"))

# Recursive function to bound groups of paths
def bound_paths(cur, verbose, root, soup, shift, total_bounds):
    # Shift is used to keep track of the accumulated position of the path within the groups

    children_group = cur.find_all('g', recursive=False)
    if len(children_group) == 0 or not children_group:
        pathsXML = cur.find_all('path')
        if not pathsXML:
            return None

        cur_shift = cur.get('transform', None)
        
        if cur_shift and cur_shift.startswith("matrix"):
            cur_shift = None

        if cur_shift:
            cur_shift = tuple(map(float, cur_shift.replace("translate(", "").replace(")", "").split(",")))
            shift = (shift[0] + cur_shift[0], shift[1] + cur_shift[1])

        bbox_list = [get_path_bbox(path.get('d'), shift) for path in pathsXML]
        for bbox in bbox_list:
            # add_rect(bbox[0], bbox[2], bbox[1] - bbox[0], bbox[3] - bbox[2], root, soup)
            total_bounds.append(bbox)
        return combine_bboxes(bbox_list)


    bbox_list = []
    cur_shift = cur.get('transform', None)

    if cur_shift and cur_shift.startswith("matrix"):
        cur_shift = None

    if cur_shift:
        cur_shift = tuple(map(float, cur_shift.replace("translate(", "").replace(")", "").split(",")))
        shift = (shift[0] + cur_shift[0], shift[1] + cur_shift[1])

        
    for group in children_group:
        bbox = bound_paths(group, verbose, root, soup, shift, total_bounds=total_bounds)


        if not bbox:
            continue
        # add_rect(bbox[0], bbox[2], bbox[1] - bbox[0], bbox[3] - bbox[2], root, soup)
        total_bounds.append(bbox)
        bbox_list.append(bbox)
 
    if not bbox_list:
        return None

    return combine_bboxes(bbox_list)

# Convert an SVG file to a base64 string using a local javascript server
def svg2base64(svg_path):
    with open(svg_path, 'rb') as f:
        res = requests.post(
            'http://localhost:3000/convert',
            files={ "file": f },
            
        )

        return res.text
    