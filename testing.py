import json
import requests
from matplotlib import pyplot as plt
import pandas as pd
import sys

regions = []
region_image_ids = []

COUNTRY = sys.argv[1]
ADMIN_LEVEL = sys.argv[2]

r = requests.get(f"https://www.geoboundaries.org/api/current/gbOpen/{COUNTRY}/{ADMIN_LEVEL}/")
dlPath = r.json()['simplifiedGeometryGeoJSON']
geoBoundary = requests.get(dlPath).json()

#Matplotlib Visualization
fig = plt.figure(1, figsize=(5,5), dpi=90, frameon=False)
axs = fig.add_subplot(111)
#hide x-axis
axs.get_xaxis().set_visible(False)

#hide y-axis 
axs.get_yaxis().set_visible(False)

axs.spines['top'].set_visible(False)
axs.spines['right'].set_visible(False)
axs.spines['bottom'].set_visible(False)
axs.spines['left'].set_visible(False)

#Accounting for Multipolygon Boundaries
for boundary in geoBoundary["features"]:
    if boundary["geometry"]['type'] == "MultiPolygon":
        polys = boundary["geometry"]["coordinates"]
        for poly in polys:
            exterior = poly[0]
            xs, ys = zip(*exterior)
            axs.fill(xs, ys, alpha=1, fc='#0B6623', ec='black')
    else:
        exterior = boundary["geometry"]["coordinates"][0]
        xs, ys = zip(*exterior)
        axs.fill(xs, ys, alpha=1, fc='#0B6623', ec='black')

# individual saved files
counter = 0
for boundary in geoBoundary["features"]:
    props = boundary["properties"]
    if boundary["geometry"]['type'] == "MultiPolygon":
        polys = boundary["geometry"]["coordinates"]
        for poly in polys:
            exterior = poly[0]
            xs, ys = zip(*exterior)
            axs.fill(xs, ys, alpha=1, fc='#800000', ec='black')
    else:
        exterior = boundary["geometry"]["coordinates"][0]
        xs, ys = zip(*exterior)
        axs.fill(xs, ys, alpha=1, fc='#800000', ec='black')

    #image_id2 = props["shapeName"].lower().replace(" ", "_").replace("-","_")
    image_id = COUNTRY.lower() + str(counter)
    regions.append(props["shapeName"])
    region_image_ids.append(image_id)
    
    fig.savefig(COUNTRY + "_" + ADMIN_LEVEL + "/" + image_id + ".png", bbox_inches='tight', pad_inches=0, transparent=True)

    if boundary["geometry"]['type'] == "MultiPolygon":
        polys = boundary["geometry"]["coordinates"]
        for poly in polys:
            exterior = poly[0]
            xs, ys = zip(*exterior)
            axs.fill(xs, ys, alpha=1, fc='#0B6623', ec='black')
    else:
        exterior = boundary["geometry"]["coordinates"][0]
        xs, ys = zip(*exterior)
        axs.fill(xs, ys, alpha=1, fc='#0B6623', ec='black')
    counter +=1

data = {"Region": regions, "Ids": region_image_ids}
df = pd.DataFrame(data)
df.to_csv(COUNTRY + ".csv", index=False)
