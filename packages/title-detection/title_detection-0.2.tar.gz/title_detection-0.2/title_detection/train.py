import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import xgboost as xgb
import pandas as pd
from sklearn.metrics import classification_report
from .model_loader import load_deep_nn_model, load_xgboost_model
from .deep_nn import DeepNNClassifier
from .preprocess import preprocess_data

# Define the dataset class
class TitleDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data.iloc[index]
        features = torch.tensor(row[['IsBold', 'IsItalic', 'IsUnderlined', 'Left', 'Right', 'Top', 'Bottom']].values.astype(float), dtype=torch.float32)
        label = torch.tensor(row['Label'], dtype=torch.long)
        return features, label

def train_models(train_data_path, test_data_path):

    # Load data with a different encoding to avoid UnicodeDecodeError
    train_data = pd.read_csv(train_data_path, encoding='latin1')  # or 'ISO-8859-1'
    test_data = pd.read_csv(test_data_path, encoding='latin1')    # or 'ISO-8859-1'

    # Preprocess data
    train_data, test_data = preprocess_data(train_data), preprocess_data(test_data)

    # Rest of the code...

    # Prepare datasets
    train_dataset = TitleDataset(train_data)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Initialize NN model
    nn_model = DeepNNClassifier(input_size=7, hidden_size1=256, hidden_size2=128, hidden_size3=64, output_size=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(nn_model.parameters(), lr=0.001)
    scheduler = ReduceLROnPlateau(optimizer, 'min', patience=3)

    # Train NN
    for epoch in range(20):
        nn_model.train()
        total_loss = 0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = nn_model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        scheduler.step(total_loss)

    torch.save(nn_model.state_dict(), 'models/deep_nn_classifier.pth')

    # Prepare features for XGBoost
    train_preds = []
    nn_model.eval()
    for inputs, _ in train_loader:
        outputs = nn_model(inputs)
        _, preds = torch.max(outputs, 1)
        train_preds.extend(preds.numpy())

    train_data['NN_Predictions'] = train_preds
    X_train = train_data[['IsBold', 'IsItalic', 'IsUnderlined', 'Left', 'Right', 'Top', 'Bottom', 'NN_Predictions']]
    y_train = train_data['Label']

    # Train XGBoost model
    xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=6)
    xgb_model.fit(X_train, y_train)
    xgb_model.save_model('models/xgboost_model.json')

    print("Models trained and saved!")
