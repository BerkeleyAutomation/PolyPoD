import pickle
import os
import plotly_test as pt
import time

directory = "datasets/dataset5"
for entry in os.scandir(directory):
    if (entry.path.endswith("data") and entry.is_file()):
        x = pickle.load(open(entry.path, 'rb'))
        g_data = x['data']
        new_filename = entry.path + "_no_voids"
        pt.plotly_test(pt.single_values['y_eye_mult'],
                       pt.single_values['z_ratio'],
                       pt.single_values['h_mult'],
                       pt.single_values['color_dict'],
                       cylinder_nt=70,
                       data=g_data, plant_labels=False, save=True,
                       where_to_save=new_filename, void_size=0)
        time.sleep(5)