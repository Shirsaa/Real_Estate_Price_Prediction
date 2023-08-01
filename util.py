import json
import pickle
import sklearn
import numpy as np
 
def get_location_name():

    global __locations
    global __data_columns
    global __model

    print('loading_saved_artifacts')

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    
    with open("./artifacts/banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)

    print('loading_saved_artifacts_done')

    return __locations



def estimated_price(location, sqft, bath, bhk):

    print('loading_saved_artifacts')

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    
    with open("./artifacts/banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)

    print('loading_saved_artifacts_done')

    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = None

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    x[loc_index] = 1

    return __model.predict([x])[0]


if __name__ == '__main__':
    get_location_name()
    estimated_price()
    print(estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(estimated_price('koramangala', 1000, 3, 3))

