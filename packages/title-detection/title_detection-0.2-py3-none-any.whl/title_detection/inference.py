import xgboost as xgb
import torch
import pandas as pd
from .model_loader import load_deep_nn_model, load_xgboost_model

def predict_title(input_data):
    # Load models
    nn_model, xgb_model = load_deep_nn_model('models/deep_nn_classifier.pth'), load_xgboost_model('models/xgboost_model.json')
    
    # Prepare the input for the neural network
    nn_input = torch.tensor([[
        input_data['IsBold'],
        input_data['IsItalic'],
        input_data['IsUnderlined'],
        input_data['Left'],
        input_data['Right'],
        input_data['Top'],
        input_data['Bottom']
    ]], dtype=torch.float32)
    
    nn_model.eval()
    with torch.no_grad():
        nn_output = nn_model(nn_input)
        _, nn_pred = torch.max(nn_output, 1)
    
    # Prepare the input for XGBoost
    xgb_input = pd.DataFrame([{
        'IsBold': input_data['IsBold'],
        'IsItalic': input_data['IsItalic'],
        'IsUnderlined': input_data['IsUnderlined'],
        'Left': input_data['Left'],
        'Right': input_data['Right'],
        'Top': input_data['Top'],
        'Bottom': input_data['Bottom'],
        'NN_Predictions': nn_pred.item()
    }])
    
    # XGBoost prediction
    xgb_pred = xgb_model.predict(xgb.DMatrix(xgb_input))

    # Convert probability to binary class
    xgb_pred = (xgb_pred > 0.5).astype(int)

    # Return the binary prediction as an integer
    return int(xgb_pred)

