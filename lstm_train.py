""" Training from scratch of the lstm network for energy production forecasting.
    Run the main only if you want to reatrain all the network.
    The training dataset is TurbineDataset.csv
"""

from lstm_model import energyLSTM, SequenceDataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
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
    ct = ColumnTransformer([
        ('input_normalization', StandardScaler(), [c for c in df.columns if c != 'index' and c != 'System power generated | (kW)']),
        ('target_normalization', MinMaxScaler(), ['System power generated | (kW)'])
    ])

    df = pd.DataFrame(ct.fit_transform(df), columns=[c for c in df.columns if c != 'index'])

    return df, ct.transformers_[0][1], ct.transformers_[1][1]


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
            print("o: ", output)
            total_loss += loss_function(output, y).item()

    avg_loss = total_loss / num_batches
    losses.append(avg_loss)
    print(f"Test loss: {avg_loss}")


if __name__ == '__main__':
    dataframe = pd.read_csv("TurbineDataset.csv")

    num_features = 7
    sequence_length = 8
    batch_size = 2
    target = 'System power generated | (kW)'
    learning_rate = 0.001
    num_hidden_units = 3

    dataframe = dataframe.iloc[:-sequence_length]

    # Modify the TurbineDataset.csv
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

    model = energyLSTM(num_features=num_features, hidden_units=num_hidden_units)
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

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
        "minmax_scaler" : mms
    }, "lstm_parameters.pth")

    # Ritrainare tutta la rete con tutto il dataset, senza dividere in test/train (così ho un dataset più grande)