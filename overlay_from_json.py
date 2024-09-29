import glob
import json
from bs4 import BeautifulSoup

files = map( lambda x: x.replace("\\", "/"), glob.glob('./output/*.json'))

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        print(data)

    with open(file.replace(".json", ""), 'r') as f:
        soup = BeautifulSoup(f, 'xml')
        root = soup.find('svg')

    if type(data.get("elements")) != list:
        data["elements"]=data["elements"].get(list(data.keys())[0])
    for e in data["elements"]:
        if e.get("type") != "text" or e.get("bounds") is None:
            continue
    
        bounds = e.get("bounds")

        root.append(soup.new_tag('rect', x=bounds[0] * data["width"], y=bounds[2] * data["height"], width=(bounds[1] - bounds[0]) * data["width"], height=(bounds[3] - bounds[2]) * data["height"], fill="none", stroke="red", stroke_width="15px"))
        # root.append(soup.new_tag('rect', x=bounds[0], y=bounds[2], width=(bounds[1] - bounds[0]), height=(bounds[3] - bounds[2]), fill="none", stroke="red", stroke_width="10px"))


    with open(file.replace(".json", "_overlay.svg"), 'w') as f:
        f.write(str(soup))

