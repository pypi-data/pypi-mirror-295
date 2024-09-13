import torch
import xgboost as xgb
from .deep_nn import DeepNNClassifier

def load_deep_nn_model(path):
    model = DeepNNClassifier(input_size=7, hidden_size1=256, hidden_size2=128, hidden_size3=64, output_size=2)
    model.load_state_dict(torch.load(path))
    model.eval()
    return model


def load_xgboost_model(path):
    model = xgb.Booster()
    model.load_model(path)
    return model
