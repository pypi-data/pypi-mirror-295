import pandas as pd

def preprocess_data(data):
    # Convert boolean-like columns from strings to integers
    bool_columns = ['IsBold', 'IsItalic', 'IsUnderlined']
    for col in bool_columns:
        data[col] = data[col].replace({'TRUE': 1, 'FALSE': 0}).astype(int)

    # Convert positional columns to numeric
    positional_columns = ['Left', 'Right', 'Top', 'Bottom']
    data[positional_columns] = data[positional_columns].apply(pd.to_numeric, errors='coerce')
    
    # Handle any remaining NaN values
    data.fillna(0, inplace=True)
    
    return data
