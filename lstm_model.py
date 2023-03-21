"""LSTM model that does Energy production forecasting
    Use function 'predict' to use the pre-trained network on new data.
"""
import torch
from torch.utils.data import Dataset
from torch import nn
import numpy as np
torch.manual_seed(42)


class SequenceDataset(Dataset):
    def __init__(self, dataframe, target, sequence_length=16):
        self.features = [c for c in dataframe.columns if c != 'index' and c != target]
        self.target = target
        self.sequence_length = sequence_length

        self.y = torch.tensor(dataframe[self.target].values).float()
        self.X = torch.tensor(dataframe[self.features].values).float()

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, i):
        if i >= self.sequence_length - 1:
            i_start = i - self.sequence_length + 1
            x = self.X[i_start:(i + 1), :]
        else:
            padding = self.X[0].repeat(self.sequence_length - i - 1, 1)
            x = self.X[0:(i + 1), :]
            x = torch.cat((padding, x), 0)

        return x, self.y[i]


class energyLSTM(nn.Module):
    def __init__(self, num_features = 7, hidden_units = 3):
        super().__init__()
        self.num_features = num_features  # this is the number of features
        self.hidden_units = hidden_units
        self.num_layers = 1

        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_units,
            batch_first=True,
            num_layers=self.num_layers
        )

        self.linear = nn.Linear(in_features=self.hidden_units, out_features=1)

    def forward(self, x):
        batch_size = x.shape[0]
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_units).requires_grad_()
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_units).requires_grad_()

        _, (hn, _) = self.lstm(x, (h0, c0))
        out = self.linear(hn[0]).flatten()  # First dim of Hn is num_layers, which is set to 1 above.

        return out


def predict(x):
    model = energyLSTM()
    checkpoint = torch.load("lstm_parameters.pth")
    model.load_state_dict(checkpoint["params"])
    standard_scaler = checkpoint["standard_scaler"]
    minmax_scaler = checkpoint["minmax_scaler"]

    #print(standard_scaler.mean_, standard_scaler.var_)
    #print(minmax_scaler.data_range_)

    # x deve essere un vettore (16, 7) con le feature di input
    # (mese, giorno, ora, temeprature, speed, direction, pressure) x16
    x = standard_scaler.transform(x)
    x = torch.tensor(x).float()
    x = torch.unsqueeze(x, dim=0)

    model.eval()
    with torch.no_grad():
        prediction = model(x)
        #print(prediction)
        prediction = np.array(prediction).reshape(-1, 1)
        prediction = minmax_scaler.inverse_transform(prediction)

    return prediction


if __name__ == '__main__':
    input_data = np.array([[17, 4, 6, 21.213, 10.9, 150.1, 0.998],
                           [17, 4, 9, 21.213, 10.9, 150.1, 0.998],
                           [17, 4, 12, 21.213, 10.9, 150.1, 0.998],
                           [17, 4, 15, 21.213, 10.9, 150.1, 0.998],
                           [17, 4, 18, 21.213, 10.9, 150.1, 0.998],
                           [17, 4, 21, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 0, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 3, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 6, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 9, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 12, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 15, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 18, 21.213, 10.9, 150.1, 0.998],
                           [17, 5, 21, 21.213, 10.9, 150.1, 0.998],
                           [17, 6, 0, 21.213, 10.9, 150.1, 0.998],
                           [17, 6, 3, 21.213, 10.9, 150.1, 0.998]])

    pred = predict(input_data)
    #print(pred)




