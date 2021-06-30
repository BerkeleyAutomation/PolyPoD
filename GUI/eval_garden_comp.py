import garden_constants
import glob
import numpy as np

images = {}
for np_name in glob.glob('final-gardens-thru_round3-data/*.np[yz]'):
    images[np_name] = np.load(np_name, allow_pickle=True)

for i in images.keys():
    print('key', i)
    c = garden_constants.garden_companionship_score(images[i])
    print('garden_comp_score: ', c)
'''
print('values\n')
for i in images.values():
    print('value', i)
    '''