import numpy as np
import pandas as pd

def get_duration(index:dict):

    """
    Function that takes as input the index of syllables, their starting point and end point. The index should be a dictionary
    where each key is a syllable, and the values are: Recording, startframe and endframe.

    It returns a dictionary where each syllable is a key and each value is a pandas df with the following properties:
    - recording: name of the recording
    - StartFrame
    - EndFrame
    - Duration: duration of that syllable in that recoding
    """
    index_diff = {}

    for key in index.keys():
        ind_arr = np.asanyarray(index[key])
        dif = ind_arr[:, 2].astype('int') - ind_arr[:, 1].astype('int')
        dif = np.reshape(dif, (dif.shape[0], 1))
        ind_arr = np.hstack((ind_arr, dif))
        index_diff[key] = pd.DataFrame(ind_arr, columns=['Recording', 'StartFrame', 'EndFrame', 'Duration'])
    return index_diff

