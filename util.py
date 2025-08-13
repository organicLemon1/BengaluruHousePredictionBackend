import os
import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    """Return estimated price for given features"""
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def load_saved_artifacts():
    """Load model and column info from artifacts folder"""
    global __data_columns, __locations, __model

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Load column info
    with open(os.path.join(BASE_DIR, "artifacts", "columns.json"), "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    # Load trained model
    if __model is None:
        with open(os.path.join(BASE_DIR, "artifacts", "bangalore_house_prices_model.pickle"), "rb") as f:
            __model = pickle.load(f)

    print("Artifacts loaded successfully!")

def get_location_names():
    """Return all locations"""
    if __locations is None:
        return []
    return __locations

def get_data_columns():
    """Return all column names"""
    return __data_columns

# For testing locally
if __name__ == '__main__':
    load_saved_artifacts()
    print("Locations:", get_location_names())
    print("Sample predictions:")
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('Ejipura', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
