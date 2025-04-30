import pyreadstat
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, recall_score, precision_score


def load_data(file_path):
    df, meta = pyreadstat.read_sas7bdat(file_path)
    return df

def change_binary(df, features):
    binary_map = {
        1: 0,
        2: 1,
    }
    for feature in features:
        df[feature] = df[feature].map(binary_map)
    return df

# Delete Proxy Skipped data
def drop_proxy_skipped(df):
    df = df.drop(df[df.AJ31 == -2].index)
    return df

def drop_dont_know(df, target_columns):
    df = df.copy()
    for col in target_columns:
        df = df[df[col] != 3]
        df[col] = df[col].replace({1: 0, 2: 1})
    return df

def preprocess_features(df):
    df = df.copy()

    ### --- SOCIAL2: life uncomfortable --- ###
    social2_map = {
        -1: 0,
        0: 0,
        1: 1,
        2: 2,
    }
    df['SOCIAL2'] = df['SOCIAL2'].map(social2_map)

    ### --- NUMCIG: the number of smoking--- ###
    numcig_map = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5
    }
    df['NUMCIG'] = df['NUMCIG'].map(numcig_map)

    # AC208: drinking time
    ac208_map = {
        0: 3,  # Never
        1: 0,
        2: 1,
        3: 2
    }
    df['AC208'] = df['AC208'].map(ac208_map)

    # AE15A: the frequency of smoking
    ae15a_map = {
        1: 2,
        2: 1,
        3: 0,
        -1: 0
    }
    df['AE15A'] = df['AE15A'].map(ae15a_map)

    # MARIT: marriage
    df['MARIT'] = df['MARIT'].replace({1: 0, 2: 1, 3: 2})

    # AJ29 the frequence of dress
    aj29_map = {
        1: 5,
        2: 4,
        3: 3,
        4: 2,
        5: 1
    }
    df['AJ29'] = df['AJ29'].map(aj29_map)


    ac117v2_days_map = {
        -1: 0,
        1: 0,
        2: 1.5,
        3: 4,
        4: 7.5,
        5: 15,
        6: 25,
        7: 30
    }
    df['AC117V2'] = df['AC117V2'].map(ac117v2_days_map)


    srage_map = {
        18: 21.5,
        26: 27.5,
        30: 32,
        35: 37,
        40: 42,
        45: 47,
        50: 52,
        55: 57,
        60: 62,
        65: 67,
        70: 72,
        75: 77,
        80: 82,
        85: 87
    }
    df['SRAGE_P1'] = df['SRAGE_P1'].map(srage_map)


    rbmi_map = {
        1: 0,  # UNDERWEIGHT
        2: 1,  # NORMAL
        3: 2,  # OVERWEIGHT
        4: 3  # OBESE
    }
    df['RBMI'] = df['RBMI'].map(rbmi_map)

    occ_map = {
        1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        6:6,
        7:7,
        8:8,
        9:9,
        10:10,
        11:11,
        12:12,
        13:13,
        14:14,
        99:15
    }
    df["OCCMAIN2"] = df["OCCMAIN2"].map(occ_map)

    return df

class CHISDataset(torch.utils.data.Dataset):

    def __init__(self, X, y):
        self.X = torch.from_numpy(X)  # shape: (N, d)
        self.y = torch.from_numpy(y)  # shape: (N,)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class LogisticRegressionModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1) 

    def forward(self, x):
        logits = self.linear(x)  
        return logits

class MLP_BN(nn.Module):
    def __init__(self, input_dim, hidden_dim=32):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim)
        self.relu2 = nn.ReLU()
        self.out = nn.Linear(hidden_dim, 1)
    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.out(x)
        return x

def dro_train_loop(
    model,
    train_loader,
    optimizer,
    bce_loss_fn,
    eta,
    epochs
):

    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        num_batches = 0

        for X_batch, y_batch in train_loader:
          
            logits = model(X_batch)
   
            losses = bce_loss_fn(logits.view(-1), y_batch) 

          
            with torch.no_grad():
                weights = torch.exp(eta * losses)        
                p_star = weights / torch.sum(weights)    
            dro_loss = torch.sum(p_star * losses)       

       
            optimizer.zero_grad()
            dro_loss.backward()
            optimizer.step()

            epoch_loss += dro_loss.item()
            num_batches += 1

        
        avg_epoch_loss = epoch_loss / num_batches
        if (epoch+1) % 5 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] - DRO Loss: {avg_epoch_loss:.4f}")

def evaluate_model(model, data_loader):
    model.eval()
    preds_list = []
    probs_list = []
    true_list = []
    with torch.no_grad():
        for X_batch, y_batch in data_loader:
            logits = model(X_batch).view(-1)     
            probs = torch.sigmoid(logits)       
            preds = (probs >= 0.5).float()       
            preds_list.append(preds.cpu().numpy())
            probs_list.append(probs.cpu().numpy())
            true_list.append(y_batch.cpu().numpy())

    y_pred = np.concatenate(preds_list)
    y_prob = np.concatenate(probs_list)
    y_true = np.concatenate(true_list)


    acc = accuracy_score(y_true, y_pred)
    f1  = f1_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_prob)
    recall = recall_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)

    return acc, f1, auc, recall, precision



if __name__ == '__main__':
    PATH1 = 'ADULT2022/adult.sas7bdat'
    PATH2 = 'ADULT2023/adult.sas7bdat'

    # List of feature columns
    SELECTED_FEATURES = [
        "AC117V2", "AC207", "AC208", "AC81C",
        "AE15A", "AF81",
        "AJ29", "AJ30", "AJ31", "AJ32", "AJ33", "AJ34",
        "DSTRS12", "DSTRSYR", "BINGE30",
        "ESMKCUR", "HOUSETYPE", "AQ1", "AQ12",
        "MARCUR", "MAREXPOSE", "MARIT",
        "NUMCIG", "OCCMAIN2", "OMBSRR_P1",
        "RBMI", "SMKEXPOSE",
        "SMOKING", "SOCIAL2", "SRAGE_P1", "SRSEX",
        "UR_CLRT4", "WGHTK_P"
    ]

    DISEASE_COLUMNS = ["AB17", "AB22V2", "AB29V2", "AB34"]

    CAT_COLS = ["OCCMAIN2", "OMBSRR_P1", "HOUSETYPE"]

    binary = ["AC207", "AC81C", "AF81", "DSTRS12", "BINGE30", "ESMKCUR", "AQ1", "AQ12", "MARCUR",
              "MAREXPOSE", "SMKEXPOSE"]

    LABEL_NAME = "AB22V2"


    df1 = load_data(PATH1)
    df1 = df1[SELECTED_FEATURES + [LABEL_NAME]]
    df2 = load_data(PATH2)
    df2 = df2[SELECTED_FEATURES + [LABEL_NAME]]
    data = pd.concat([df1, df2], ignore_index=True)
    data = data.astype("float32")
    # data = change_binary(data, binary)
    data = drop_proxy_skipped(data)
    data = drop_dont_know(data, [LABEL_NAME])
    data = preprocess_features(data)
    data = data.dropna()

  
    X = data[SELECTED_FEATURES].values.astype(np.float32)  # shape: (N, d)
    y = data[LABEL_NAME].values.astype(np.float32)  # shape: (N, )
    print(X.shape, y.shape)

    BATCH_SIZE = 32
    LR = 1e-4
    EPOCHS = 20
    ETA = 1  
    RANDOM_SEED = 42
    NUM_FOLDS = 5

    skf = StratifiedKFold(n_splits=NUM_FOLDS, shuffle=True, random_state=RANDOM_SEED)

    all_fold_results = []

    fold_id = 1
    for train_index, val_index in skf.split(X, y):
        print(f"\n=== Fold {fold_id} ===")

        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

     
        train_dataset = CHISDataset(X_train, y_train)
        val_dataset = CHISDataset(X_val, y_val)

        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=BATCH_SIZE, shuffle=True
        )
        val_loader = torch.utils.data.DataLoader(
            val_dataset, batch_size=len(val_dataset), shuffle=False
        )


        model = MLP_BN(input_dim=X_train.shape[1])
        optimizer = optim.SGD(model.parameters(), lr=LR, weight_decay=1e-4)
        bce_loss_fn = nn.BCEWithLogitsLoss(reduction='none') 


        dro_train_loop(
            model=model,
            train_loader=train_loader,
            optimizer=optimizer,
            bce_loss_fn=bce_loss_fn,
            eta=ETA,
            epochs=EPOCHS
        )

   
        acc, f1, auc, recall, precision = evaluate_model(model, val_loader)
        torch.save(model.state_dict(), LABEL_NAME+".pth")
        print(f"Fold {fold_id} | Val Acc={acc:.4f}, Recall={recall:.4f}, Precision={precision:.4f}, F1={f1:.4f}, AUC={auc:.4f}")
        all_fold_results.append((acc, recall, precision, f1, auc))

        fold_id += 1


    all_fold_results = np.array(all_fold_results)  
    mean_acc = all_fold_results[:, 0].mean()
    mean_recall = all_fold_results[:, 1].mean()
    mean_precision = all_fold_results[:, 2].mean()
    mean_f1 = all_fold_results[:, 3].mean()
    mean_auc = all_fold_results[:, 4].mean()
    print("\n=== K-Fold CV Average Metrics ===")
    print(f"Accuracy = {mean_acc:.4f}")
    print(f"Recall = {mean_recall:.4f}")
    print(f"Precision = {mean_precision:.4f}")
    print(f"F1       = {mean_f1:.4f}")
    print(f"AUC      = {mean_auc:.4f}")
