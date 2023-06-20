from flask import jsonify
from flask import Flask
import os
from flask_cors import CORS
import sys
from flask import request
import numpy as np
import math
from shapely.geometry import Polygon
import plotting_utils
import generate_test_gardens
import bmca_utils
import tempfile
from flask import send_file

app = Flask(__name__)
CORS(app)


num_trials = 1
num_gardens_to_generate = 1
data = None
cylinder_nt = 70
generate_plotly=False
save_plotly=True
save_2d=False



@app.route(f'/get_parameters', methods = ["POST"])
def get_parameters():
    garden = {}
    
    #get parameters
    request_json = request.get_json()
    garden['density'] = request_json.get('density', 0.75)
    garden['coordinates'] = request_json.get('coordinates', [])
    garden['num_plants'] = request_json.get('num_plants', 0)
    garden['num_each_plant'] = request_json.get('num_each_plant', [])
    garden['distribution'] = 'even'
    garden['beta'] = request_json.get('beta', 0.2)
    garden['void_size'] = request_json.get('void_size', 15)
    garden['void_number'] = request_json.get('void_number', 2)
    garden['utility_func_exponent'] = request_json.get('utility_func_exponent', ['same', -6])
    garden['symmetry'] = request_json.get('symmetry', 'neither')
    
    
    # garden["density"] = request.args.get('density')
    # garden["distribution"] = request.args.get('distribution')
    # garden["beta"] = request.args.get('beta')
    # garden["void_size"] = request.args.get('void_size')
    # garden["void_number"] = request.args.get('void_number')
    # garden["utility_func_exponent"] = request.args.get('utility_func_exponent')
    # garden["symmetry"] = request.args.get('symmetry')
    # garden["coordinates"] = request.args.get('coordinates')
    # garden["num_each_plant"] = np.full(9, 2) #change later

    #take user inputs
    garden = generate_test_gardens.add_d_to_garden(garden)
    print(garden)

    fig, ax = plotting_utils.generate_garden_scatter_and_area(d=garden['d'], image_id='abc', num_images=1,
                                                        cylinder_nt=cylinder_nt, data=None,
                                                        generate_plotly=generate_plotly, garden=garden,
                                                        save_plotly=save_plotly, save_2d=save_2d)
    with tempfile.NamedTemporaryFile(suffix='.png') as f:
        fig.savefig(f.name)
        return send_file(f.name, mimetype='image/gif')

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8000, debug = False)

    
