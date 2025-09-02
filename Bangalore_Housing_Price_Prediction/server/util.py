import json
import pickle
import numpy as np

__data_columns = None
__locations = None
__model = None


def get_estimated_price(location, sqft, bath, balcony, bhk):
    try:
        loc_index = __data_columns.index(location)
    except:
        loc_index = -1

    inputs = np.zeros(len(__data_columns))
    inputs[0] = sqft
    inputs[1] = bath
    inputs[2] = balcony
    inputs[3] = bhk
    if loc_index >= 0:
        inputs[loc_index] = 1

    print("Model is predicting")
    return round(__model.predict([inputs])[0],2)

def get_locations():
    return __locations

def load_saved_artifacts():
    print("Loading artifacts...")
    global __data_columns, __locations, __model
    with open('./artifacts/Housing_Data_Columns.json', 'rb') as data_col:
        __data_columns = json.load(data_col)['data_columns']
        __locations = __data_columns[4:]

    with open('./artifacts/bangalore_housing_price_prediction_model.pickle', 'rb') as model_bhp:
        __model = pickle.load(model_bhp)

    print("Loaded artifacts...")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_estimated_price("1st block jayanagar",1000,2,1,2))
