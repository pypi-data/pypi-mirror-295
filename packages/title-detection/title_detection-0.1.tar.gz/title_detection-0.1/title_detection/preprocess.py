import pandas as pd
import numpy as np

# Preprocessing function to format the data for inference
def preprocess_data(data_point):
    # Example data_point dictionary
    # {'IsBold': 1, 'IsItalic': 0, 'IsUnderlined': 0, 'Left': 50, 'Right': 100, 'Top': 200, 'Bottom': 250}

    # Extracting the values from the input dictionary
    features = [data_point['IsBold'], data_point['IsItalic'], data_point['IsUnderlined'],
                data_point['Left'], data_point['Right'], data_point['Top'], data_point['Bottom']]

    # Converting the feature list to a numpy array
    processed_features = np.array(features, dtype=float)

    return processed_features
