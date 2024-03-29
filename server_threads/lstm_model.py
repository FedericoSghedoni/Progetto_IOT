"""LSTM model that does Energy production forecasting
    Use function 'predict' to use the pre-trained network on new data.
"""
import torch
from torch.utils.data import Dataset
from torch import nn
import numpy as np
torch.manual_seed(42)


class SequenceDataset(Dataset):
    def __init__(self, dataframe, target, sequence_length=48):
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


def predict(x, checkpoint):
    model = energyLSTM()
    model.load_state_dict(checkpoint["params"])
    standard_scaler = checkpoint["standard_scaler"]
    minmax_scaler = checkpoint["minmax_scaler"]

    #print(standard_scaler.mean_, standard_scaler.var_)
    #print(minmax_scaler.data_range_)

    # x deve essere un ndarray (48, 7) con le feature di input
    # (mese, giorno, ora, temeprature, speed, direction, pressure) x 48
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
    input_data = np.array([[1, 1, 0, 18.263, 9.926, 128.0, 1.00048],
                           [1, 1, 1, 18.363, 9.273, 135.0, 0.99979],
                           [1, 1, 2, 18.663, 8.66, 142.0, 0.999592],
                           [1, 1, 3, 18.763, 9.461, 148.0, 0.998309],
                           [1, 1, 4, 18.963, 9.184, 150.0, 0.998507],
                           [1, 1, 5, 19.063, 8.996, 149.0, 0.998507],
                           [1, 1, 6, 19.113, 9.016, 151.0, 0.998211],
                           [1, 1, 7, 19.163, 9.036, 154.0, 0.997815],
                           [1, 1, 8, 19.363, 7.612, 154.0, 1.00028],
                           [1, 1, 9, 19.963, 6.129, 162.0, 1.00295],
                           [1, 1, 10, 20.763, 5.961, 152.0, 1.00048],
                           [1, 1, 11, 21.063, 8.117, 141.0, 1.00068],
                           [1, 1, 12, 21.063, 9.54, 141.0, 0.996926],
                           [1, 1, 13, 20.763, 10.094, 136.0, 1.00028],
                           [1, 1, 14, 20.663, 8.789, 137.0, 0.998801],
                           [1, 1, 15, 20.663, 7.286, 126.0, 0.999986],
                           [1, 1, 16, 20.563, 7.088, 122.0, 0.999591],
                           [1, 1, 17, 20.363, 7.266, 121.0, 0.997715],
                           [1, 1, 18, 20.363, 8.739, 116.0, 0.996334],
                           [1, 1, 19, 20.363, 10.212, 126.0, 0.994952],
                           [1, 1, 20, 20.363, 9.797, 132.0, 0.998406],
                           [1, 1, 21, 20.263, 8.729, 149.0, 1.00048],
                           [1, 1, 22, 20.263, 8.087, 155.0, 0.99821],
                           [1, 1, 23, 20.263, 7.563, 160.0, 0.998703],
                           [1, 2, 0, 20.163, 8.265, 157.0, 0.996432],
                           [1, 2, 1, 19.863, 8.631, 157.0, 0.998999],
                           [1, 2, 2, 19.663, 8.542, 167.0, 0.998802],
                           [1, 2, 3, 19.563, 7.158, 176.0, 0.997914],
                           [1, 2, 4, 19.463, 6.693, 174.0, 0.994952],
                           [1, 2, 5, 19.263, 7.009, 175.0, 0.996335],
                           [1, 2, 6, 19.513, 6.96, 162.0, 0.996433],
                           [1, 2, 7, 19.763, 6.91, 177.0, 0.996432],
                           [1, 2, 8, 19.763, 6.09, 177.0, 0.995643],
                           [1, 2, 9, 20.263, 6.99, 173.0, 0.996926],
                           [1, 2, 10, 21.063, 6.584, 175.0, 0.997518],
                           [1, 2, 11, 22.263, 4.884, 166.0, 1.00048],
                           [1, 2, 12, 22.663, 4.904, 135.0, 0.995937],
                           [1, 2, 13, 21.563, 6.782, 120.0, 0.994655],
                           [1, 2, 14, 20.863, 8.245, 126.0, 0.993964],
                           [1, 2, 15, 21.063, 9.352, 132.0, 0.996432],
                           [1, 2, 16, 21.463, 10.697, 140.0, 0.994457],
                           [1, 2, 17, 21.163, 11.992, 142.0, 0.994457],
                           [1, 2, 18, 20.713, 11.399, 145.0, 0.99426],
                           [1, 2, 19, 20.263, 10.806, 153.0, 0.994162],
                           [1, 2, 20, 19.763, 11.142, 150.0, 0.996432],
                           [1, 2, 21, 19.863, 10.657, 155.0, 0.996334],
                           [1, 2, 22, 19.963, 10.628, 158.0, 0.99436],
                           [1, 2, 23, 19.963, 10.291, 162.0, 0.994853]])

    pred = predict(input_data, torch.load("lstm_parameters.pth"))
    print(pred)




