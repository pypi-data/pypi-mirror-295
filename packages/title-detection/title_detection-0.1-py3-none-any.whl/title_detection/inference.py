import torch
from .model_loader import load_deep_nn_model, load_xgboost_model

def predict_title(input_data):
    # Load the models
    nn_model = load_deep_nn_model('models/deep_nn_classifier.pth')
    xgb_model = load_xgboost_model('models/xgboost_model.json')

    # Extract features from the input data dictionary and convert to a tensor
    features = [
        input_data['IsBold'],
        input_data['IsItalic'],
        input_data['IsUnderlined'],
        input_data['Left'],
        input_data['Right'],
        input_data['Top'],
        input_data['Bottom']
    ]
    
    # Convert features to a tensor and add batch dimension
    nn_input = torch.tensor(features, dtype=torch.float32).unsqueeze(0)  # Adding batch dimension
    
    # Predict using the neural network
    nn_model.eval()
    with torch.no_grad():
        nn_prediction = nn_model(nn_input)
        _, nn_pred_label = torch.max(nn_prediction, 1)
    
    # Combine the NN prediction with the original features for XGBoost
    combined_features = features + [nn_pred_label.item()]

    # Predict using XGBoost
    xgb_pred = xgb_model.predict([combined_features])

    return xgb_pred[0]
