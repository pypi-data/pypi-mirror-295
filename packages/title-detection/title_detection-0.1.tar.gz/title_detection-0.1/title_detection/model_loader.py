import torch
import xgboost as xgb
from .deep_nn import DeepNNClassifier

def load_deep_nn_model(path):
    # Define the model architecture (match it to your saved model)
    model = DeepNNClassifier(input_size=7, hidden_size1=128, hidden_size2=64, hidden_size3=32, output_size=2)
    
    # Load the model's state dictionary (weights)
    model.load_state_dict(torch.load(path))
    
    # Return the model ready for inference
    return model

def load_xgboost_model(path):
    # Load the XGBoost model
    model = xgb.XGBClassifier()
    model.load_model(path)
    
    # Return the XGBoost model ready for inference
    return model
