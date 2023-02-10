from flask import jsonify
from flask import Flask
import os
import sys
from flask import request
import numpy as np
import math
from shapely.geometry import Polygon
import plotting_utils

app = Flask(__name__)

@app.route(f'/generate-garden', methods = ["GET"])
def generate_garden():
    #get parameters
    density = request.args.get('density')
    distribution = request.args.get('distribution')
    beta = request.args.get('beta')
    void_size = request.args.get('void_size')
    void_number = request.args.get('void_number')
    utility_func_exponent = request.args.get('utility_func_exponent')
    symmetry = request.args.get('symmetry')

    #get garden shape
    bmca_coordinates = request.args.get('bmca_coordinates')

    plotting_utils.generate_garden_scatter_and_area() 
