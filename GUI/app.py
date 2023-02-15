from flask import jsonify
from flask import Flask
import os
import sys
from flask import request
import numpy as np
import math
from shapely.geometry import Polygon
import plotting_utils
import generate_test_gardens
import bmca_utils
from flask import send_file

app = Flask(__name__)


num_trials = 1
num_gardens_to_generate = 1
data = None
cylinder_nt = 70
generate_plotly=False
save_plotly=True
save_2d=False



@app.route(f'/get_parameters', methods = ["GET"])
def get_parameters():
    garden = {}
    
    #get parameters
    # garden["density"] = request.args.get('density')
    # garden["distribution"] = request.args.get('distribution')
    # garden["beta"] = request.args.get('beta')
    # garden["void_size"] = request.args.get('void_size')
    # garden["void_number"] = request.args.get('void_number')
    # garden["utility_func_exponent"] = request.args.get('utility_func_exponent')
    # garden["symmetry"] = request.args.get('symmetry')
    # garden["coordinates"] = request.args.get('coordinates')
    # garden["num_each_plant"] = np.full(9, 2) #change later

    # #dummy values
    garden["coordinates"] = [[100, 100], [200, 100], [200, 200], [300, 200], [300, 100], [400, 100], [400, 400],[250, 250], [250, 400], [100, 400], [100, 300], [175, 250], [100, 200], [100, 100]]
    garden["density"] = 0.75
    garden["distribution"] = 'even'
    garden["beta"] = 0.2
    garden["void_size"] = 15
    garden["void_number"] = 2
    garden["utility_func_exponent"] = ['same', -6]
    garden["symmetry"] = 'neither'
    garden["num_each_plant"] = np.full(3, 1) #change later
    garden = generate_test_gardens.add_d_to_garden(garden)
    print(garden)

    fig, ax = plotting_utils.generate_garden_scatter_and_area(d=garden['d'], image_id='abc', num_images=1,
                                                        cylinder_nt=cylinder_nt, data=None,
                                                        generate_plotly=generate_plotly, garden=garden,
                                                        save_plotly=save_plotly, save_2d=save_2d)
    path = os.path.abspath("app.py")
    fig.savefig(os.path.join(path, 'test.png'))
    return send_file('test.png', mimetype='image/gif')

    
if __name__ == "__main__":
    app.run(port = 8000, debug = True)

    
