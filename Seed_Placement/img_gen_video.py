import pickle
import os
from pathlib import Path
import gzip
from seed_solver import compute_scores
# from final_find import NUM_SEEDS, GARDEN_SIZE

# REAL_GARDEN_WIDTH = 137 #in cm
NUM_SEEDS = 25
GARDEN_SIZE = 150
NUM_PIXELS = 100


PLANT_SIZE = {
 'borage': 29, #(60,5) 
 'sorrel': 9,
 'cilantro': 12,
 'radicchio': 24,#29
 'kale': 35, #35
 'green_lettuce': 16, #(18,1)
 'red_lettuce': 13,#15
 'arugula': 21, #(25,1)
 'swiss_chard': 27, #31
 'turnip': 31 #33
}


PLANTS = ['kale', 'green_lettuce', 'red_lettuce', 'cilantro', 'swiss_chard', 'borage', 'sorrel', 'radicchio', 'arugula', 'turnip']

# SAME_RELATIONSHIP_VALUE
SRV = 1.0

PLANTS_RELATION = {
        "borage":       {"borage": SRV, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 1.0, "arugula": 0.0, "swiss_chard": 1.0, "turnip": 0.0},
        "sorrel":       {"borage": 0.0, "sorrel": SRV,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": 0.0, "swiss_chard": 0.0, "turnip": 0.0},
        "cilantro":     {"borage": -1.0, "sorrel": 0.0,  "cilantro": SRV, "radicchio": 0.0, "kale": -1.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": 0.0, "swiss_chard": 0.0, "turnip": 0.0},
        "radicchio":    {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": SRV, "kale": 0.0, "green_lettuce":-1.0, "red_lettuce":-1.0, "arugula": 0.0, "swiss_chard":-1.0, "turnip": 0.0},
        "kale":         {"borage": -1.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 1.0, "kale": SRV, "green_lettuce": -1.0, "red_lettuce": -1.0, "arugula": -1.0, "swiss_chard": 0.0, "turnip": 0.0},
        "green_lettuce":{"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": SRV, "red_lettuce": -1.0, "arugula": 0.0, "swiss_chard": -1.0, "turnip": 0.0},
        "red_lettuce":  {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": -1.0, "kale": -1.0, "green_lettuce": -1.0, "red_lettuce": SRV, "arugula": 0.0, "swiss_chard": 0.0, "turnip": 0.0},
        "arugula":      {"borage": 0.0, "sorrel": 1.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 1.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": SRV, "swiss_chard": 0.0, "turnip": 0.0},
        "swiss_chard":  {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": 0.0, "swiss_chard": SRV, "turnip": 0.0},
        "turnip":       {"borage": 0.0, "sorrel": 0.0,  "cilantro": 0.0, "radicchio": 0.0, "kale": 0.0, "green_lettuce": 0.0, "red_lettuce": 0.0, "arugula": 1.0, "swiss_chard": 1.0, "turnip": SRV}
}

COLORS = [(0.1137, 0.2588, 0.8510), (0.4275, 0.8667, 0.6941), (0.5098, 0.2784, 0.8549), (0.2, 0.4784, 0.3765), (0.9333, 0.3804, 0.3725), (0.9467, 0.6863, 0.2431), (0.9294, 0.2, 0.2412), (0.7333, 0.6980, 0.0934), (0.3059, 0.4667, 0.1255), (0.8196, 0.2863, 0.6510), (0.9333, 0.3804, 0.3725)]
RATIO = 1
from PIL import Image, ImageDraw, ImageFont


CANVAS_SIZE = 5

def draw_image(labels, points):
    im = Image.new("RGB", (GARDEN_SIZE*CANVAS_SIZE,GARDEN_SIZE*CANVAS_SIZE), (255,255,255))
    dr = ImageDraw.Draw(im)
    for i in range(len(points)):
        if points.shape == (NUM_SEEDS,):
            t = points
            points = labels
            labels = t
        [x,y] = points[i]
        l = labels[i]
        type = PLANTS[l]
        r = PLANT_SIZE[type]
        color = COLORS[l]
        color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        fill = (color[0] + round((255-color[0])*2/4), color[1]+round((255-color[1])*2/4), color[2]+round((255-color[2])*2/4))
        dr.ellipse(((x-r)*CANVAS_SIZE,(y-r)*CANVAS_SIZE,(x+r)*CANVAS_SIZE,(y+r)*CANVAS_SIZE), outline=color, width=4) #fill=fill
        dr.ellipse((x*CANVAS_SIZE-3,y*CANVAS_SIZE-3,x*CANVAS_SIZE+3,y*CANVAS_SIZE+3), color)
        #dr.ellipse(((x-r)*CANVAS_SIZE,(y-r)*CANVAS_SIZE,(x+r)*CANVAS_SIZE,(y+r)*CANVAS_SIZE), fill=color, outline=color, width=1)
        # dr.ellipse((x*CANVAS_SIZE-3,y*CANVAS_SIZE-3,x*CANVAS_SIZE+3,y*CANVAS_SIZE+3), (40,40,40))

    return im

dirpath = "data_img/"
paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
for fname in paths:
    fname = str(fname)
    if fname == 'data_img/.DS_Store' or fname[:14] == dirpath + "trial":
        continue
    with open(fname, "rb") as f:
        [labels, points] = pickle.load(f)
    print(fname)
    print("SCORE: ", compute_scores(points, labels, NUM_SEEDS))
    overlap_im = draw_image(labels, points)
    overlap_im.save(fname+".png")
