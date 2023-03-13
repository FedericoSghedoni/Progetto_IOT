import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch import nn
torch.manual_seed(42)


def init_dataframe(df):
    # modify Time values
    hour_col = []

    for i in range(df['Time'].size):
        if df['Time'][i].split(' ')[1] == 'pm':
            h = df['Time'][i].split(':')[0]
            h = int(h) + 12
        else:
            h = df['Time'][i].split(':')[0]
            h = int(h)
        hour_col = np.append(hour_col, h)

    df = df.drop('Time', axis=1)
    df.insert(1, 'Time', hour_col.astype(int))

    # mantain only 3h values
    hour_vals = [0, 3, 6, 9, 12, 15, 18, 21]
    df = df[df['Time'].isin(hour_vals)]
    df = df.reset_index()

    # modify Date values
    month_col = []
    day_col = []
    for i in range(df['Date'].size):
        month_col = np.append(month_col, df['Date'][i].split(' ')[1])
        day_col = np.append(day_col, df['Date'][i].split(' ')[0])
    df = df.drop('Date', axis=1)
    df.insert(0, 'Day', day_col.astype(int))
    df.insert(0, 'Month', month_col.astype(int))

    # normalization
    ss = StandardScaler()
    mms = MinMaxScaler()
    ct = ColumnTransformer([
        ('input_normalization', ss, [c for c in df.columns if c != 'index' and c != 'System power generated | (kW)']),
        ('target_normalization', mms, ['System power generated | (kW)'])
    ])

    df = pd.DataFrame(ct.fit_transform(df), columns=[c for c in df.columns if c != 'index'])

    return df, ss, mms


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


class ShallowRegressionLSTM(nn.Module):
    def __init__(self, num_features, hidden_units):
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


def train_model(data_loader, model, loss_function, optimizer, losses):
    num_batches = len(data_loader)
    total_loss = 0
    model.train()

    for X, y in data_loader:
        output = model(X)
        loss = loss_function(output, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / num_batches
    losses.append(avg_loss)
    print(f"Train loss: {avg_loss}")


def test_model(data_loader, model, loss_function, losses):
    num_batches = len(data_loader)
    total_loss = 0

    model.eval()
    with torch.no_grad():
        for X, y in data_loader:
            output = model(X)
            total_loss += loss_function(output, y).item()

    avg_loss = total_loss / num_batches
    losses.append(avg_loss)
    print(f"Test loss: {avg_loss}")


def predict(data_loader, model):
    output = torch.tensor([])
    model.eval()
    with torch.no_grad():
        for X, _ in data_loader:
            y_star = model(X)
            output = torch.cat((output, y_star), 0)

    return output


if __name__ == '__main__':
    dataframe = pd.read_csv("TurbineDatabase.csv")

    num_features = 7
    sequence_length = 8
    batch_size = 2
    target = 'System power generated | (kW)'
    learning_rate = 0.001
    num_hidden_units = 3

    dataframe = dataframe.iloc[:-sequence_length]
    dataframe, ss, mms = init_dataframe(dataframe)

    test_head = dataframe.index[int(0.8*len(dataframe))]
    df_train = dataframe.loc[:test_head, :]
    df_test = dataframe.loc[test_head:, :]

    train_dataset = SequenceDataset(
        df_train,
        target=target,
        sequence_length=sequence_length
    )

    test_dataset = SequenceDataset(
        df_test,
        target=target,
        sequence_length=sequence_length
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model = ShallowRegressionLSTM(num_features=num_features, hidden_units=num_hidden_units)
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # test_losses = []
    # print("Untrained test\n--------")
    # test_model(test_loader, model, loss_function, test_losses)
    # print()

    train_losses = []
    test_losses = []

    for ix_epoch in range(10):
        print(f"Epoch {ix_epoch}\n---------")
        train_model(train_loader, model, loss_function, optimizer, train_losses)
        test_model(test_loader, model, loss_function, test_losses)
        print()

    plt.plot(train_losses)
    plt.plot(test_losses)
    plt.show()

    torch.save({
        "params" : model.state_dict(),
        "standard_scaler" : ss,
        "minmax_scaler" : ss
    }, "lstm_parameters.pth")

    # train_eval_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)

    # ystar_col = "Model forecast"
    # df_train[ystar_col] = predict(train_eval_loader, model).numpy()
    # df_test[ystar_col] = predict(test_loader, model).numpy()

    # df_out = pd.concat((df_train, df_test))[[target, ystar_col]]

    # for c in df_out.columns:
    #     df_out[c] = df_out[c] * target_stdev + target_mean

    # print(df_o)



