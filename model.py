import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from numpy import mean
from numpy import std
from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline

data = pd.read_csv("C:/Users/danny/Downloads/feed.csv", low_memory = False)

# use matches that have a winner, ignore nc, draws
data = data.loc[(data["winner"] == 1) | (data["winner"] == 2)]
data["winner2"] = data["winner"].apply(lambda x: 1 if x == 1 else 0)

# impute missing fighter stances to Orthodox
def missing_stance(x):
  if x == "--":
    return "Orthodox"
  elif x == "Open Stance":
    return "Orthodox"
  elif x == "Sideways":
    return "Orthodox"
  else:
    return x

data["fighter1_stance"] = data["fighter1_stance"].apply(missing_stance)
data["fighter2_stance"] = data["fighter2_stance"].apply(missing_stance)

# impute missing fighter_birthyear
def missing_birthyear(x):
  if x == "--":
    return 1992
  else:
    return x

data["fighter1_birthyear"] = data["fighter1_birthyear"].apply(missing_birthyear)
data["fighter2_birthyear"] = data["fighter2_birthyear"].apply(missing_birthyear)

# calculate age field based on fighter birthyear
data["fighter1_age"] = 2022 - data["fighter1_birthyear"].astype(str).astype(int)
data["fighter2_age"] = 2022 - data["fighter2_birthyear"].astype(str).astype(int)

data = data.drop(columns = ["fighter1_birthyear","fighter2_birthyear"])

# calculate total fights for each fighter
data["fighter1_totalfights"] = data.iloc[:,10:14].sum(axis=1)
data["fighter2_totalfights"] = data.iloc[:,67:71].sum(axis=1)

# convert total fight time from seconds to minutes
data["fighter1_total_time_fought"] = data["fighter1_total_time_fought"]/60
data["fighter2_total_time_fought"] = data["fighter2_total_time_fought"]/60

# convert CTRL time from seconds to minutes
data["fighter1_CTRL"] = data["fighter1_CTRL"]/60
data["fighter2_CTRL"] = data["fighter2_CTRL"]/60

# convert CTRLED time from seconds to minutes
data["fighter1_CTRLED"] = data["fighter1_CTRLED"]/60
data["fighter2_CTRLED"] = data["fighter2_CTRLED"]/60

# FEATURE ENGINEERING

#@title treatment for KD, REV, REVED, DOWNED
# calculate wsub per SUBATT
data["fighter1_wsub_subatt"] = data["fighter1_wsub"]/data["fighter1_SUBATT"]
data["fighter2_wsub_subatt"] = data["fighter2_wsub"]/data["fighter1_SUBATT"]

# calculate rounds fought per total fights
data["fighter1_rounds_fought_totalfights"] = data["fighter1_rounds_fought"]/data["fighter1_totalfights"]
data["fighter2_rounds_fought_totalfights"] = data["fighter2_rounds_fought"]/data["fighter2_totalfights"]

# calculate KD per total fights
data["fighter1_KD"] = data["fighter1_KD"]/data["fighter1_totalfights"]
data["fighter2_KD"] = data["fighter2_KD"]/data["fighter2_totalfights"]

# calculate DOWNED per total fights
data["fighter1_DOWNED"] = data["fighter1_DOWNED"]/data["fighter1_totalfights"]
data["fighter2_DOWNED"] = data["fighter2_DOWNED"]/data["fighter2_totalfights"]

# subattempts per CTRL min
data["fighter1_SUBATT_CTRL"] = data["fighter1_SUBATT"]/data["fighter1_CTRL"]
data.drop(columns = "fighter1_SUBATT")

data["fighter2_SUBATT_CTRL"] = data["fighter2_SUBATT"]/data["fighter2_CTRL"]
data.drop(columns = "fighter2_SUBATT")

# REV per total fight mins
data["fighter1_REV_mins"] = data["fighter1_REV"]/data["fighter1_CTRL"]
data.drop(columns = "fighter1_REV")

data["fighter2_REV_mins"] = data["fighter2_REV"]/data["fighter2_CTRL"]
data.drop(columns = "fighter2_REV")

# REVED per total fight mins
data["fighter1_REVED_mins"] = data["fighter1_REVED"]/data["fighter1_CTRL"]
data.drop(columns = "fighter1_REV")

data["fighter2_REVED_mins"] = data["fighter2_REVED"]/data["fighter2_CTRL"]
data.drop(columns = "fighter2_REV")

#@title treatement for dynamic stats with attempts
# calculate "attempt" features with per total fight mins, per attempt, and attempt per total fight mins
data["fighter1_SS_mins"] = data["fighter1_SS"]/data["fighter1_total_time_fought"]
data["fighter1_SS_att"] = data["fighter1_SS"]/data["fighter1_SSA"]
data["fighter1_SSA_mins"] = data["fighter1_SSA"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_SS","fighter1_SSA"])

data["fighter2_SS_mins"] = data["fighter2_SS"]/data["fighter2_total_time_fought"]
data["fighter2_SS_att"] = data["fighter2_SS"]/data["fighter2_SSA"]
data["fighter2_SSA_mins"] = data["fighter2_SSA"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_SS","fighter2_SSA"])

# Takedowns
data["fighter1_TD_mins"] = data["fighter1_TD"]/data["fighter1_total_time_fought"]
data["fighter1_TD_att"] = data["fighter1_TD"]/data["fighter1_TDA"]
data["fighter1_TD_mins"] = data["fighter1_TD"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_TD","fighter1_TDA"])

data["fighter2_TD_mins"] = data["fighter2_TD"]/data["fighter2_total_time_fought"]
data["fighter2_TD_att"] = data["fighter2_TD"]/data["fighter2_TDA"]
data["fighter2_TD_mins"] = data["fighter2_TD"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_TD","fighter2_TDA"])

# HS
data["fighter1_HS_mins"] = data["fighter1_HS"]/data["fighter1_total_time_fought"]
data["fighter1_HS_att"] = data["fighter1_HS"]/data["fighter1_HSA"]
data["fighter1_HS_mins"] = data["fighter1_HS"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_HS","fighter1_HSA"])

data["fighter2_HS_mins"] = data["fighter2_HS"]/data["fighter2_total_time_fought"]
data["fighter2_HS_att"] = data["fighter2_HS"]/data["fighter2_HSA"]
data["fighter2_HS_mins"] = data["fighter2_HS"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_HS","fighter2_HSA"])

# BS
data["fighter1_BS_mins"] = data["fighter1_BS"]/data["fighter1_total_time_fought"]
data["fighter1_BS_att"] = data["fighter1_BS"]/data["fighter1_BSA"]
data["fighter1_BS_mins"] = data["fighter1_BS"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_BS","fighter1_BSA"])

data["fighter2_BS_mins"] = data["fighter2_BS"]/data["fighter2_total_time_fought"]
data["fighter2_BS_att"] = data["fighter2_BS"]/data["fighter2_BSA"]
data["fighter2_BS_mins"] = data["fighter2_BS"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_BS","fighter2_BSA"])

# LS
data["fighter1_LS_mins"] = data["fighter1_LS"]/data["fighter1_total_time_fought"]
data["fighter1_LS_att"] = data["fighter1_LS"]/data["fighter1_LSA"]
data["fighter1_LS_mins"] = data["fighter1_LS"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_LS","fighter1_LSA"])

data["fighter2_LS_mins"] = data["fighter2_LS"]/data["fighter2_total_time_fought"]
data["fighter2_LS_att"] = data["fighter2_LS"]/data["fighter2_LSA"]
data["fighter2_LS_mins"] = data["fighter2_LS"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_LS","fighter2_LSA"])

# DS
data["fighter1_DS_mins"] = data["fighter1_DS"]/data["fighter1_total_time_fought"]
data["fighter1_DS_att"] = data["fighter1_DS"]/data["fighter1_DSA"]
data["fighter1_DS_mins"] = data["fighter1_DS"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_DS","fighter1_DSA"])

data["fighter2_DS_mins"] = data["fighter2_DS"]/data["fighter2_total_time_fought"]
data["fighter2_DS_att"] = data["fighter2_DS"]/data["fighter2_DSA"]
data["fighter2_DS_mins"] = data["fighter2_DS"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_DS","fighter2_DSA"])

# CS
data["fighter1_CS_mins"] = data["fighter1_CS"]/data["fighter1_total_time_fought"]
data["fighter1_CS_att"] = data["fighter1_CS"]/data["fighter1_CSA"]
data["fighter1_CS_mins"] = data["fighter1_CS"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_CS","fighter1_CSA"])

data["fighter2_CS_mins"] = data["fighter2_CS"]/data["fighter2_total_time_fought"]
data["fighter2_CS_att"] = data["fighter2_CS"]/data["fighter2_CSA"]
data["fighter2_CS_mins"] = data["fighter2_CS"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_CS","fighter2_CSA"])

# GS
data["fighter1_GS_mins"] = data["fighter1_GS"]/data["fighter1_total_time_fought"]
data["fighter1_GS_att"] = data["fighter1_GS"]/data["fighter1_GSA"]
data["fighter1_GS_mins"] = data["fighter1_GS"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_GS","fighter1_GSA"])

data["fighter2_GS_mins"] = data["fighter2_GS"]/data["fighter2_total_time_fought"]
data["fighter2_GS_att"] = data["fighter2_GS"]/data["fighter2_GSA"]
data["fighter2_GS_mins"] = data["fighter2_GS"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_GS","fighter2_GSA"])

# SSD
data["fighter1_SSD_mins"] = data["fighter1_SSD"]/data["fighter1_total_time_fought"]
data["fighter1_SSD_SSR"] = data["fighter1_SSD"]/data["fighter1_SSR"]
data["fighter1_SSR_mins"] = data["fighter1_SSR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_SSD","fighter1_SSR"])

data["fighter2_SSD_mins"] = data["fighter2_SSD"]/data["fighter2_total_time_fought"]
data["fighter2_SSD_SSR"] = data["fighter2_SSD"]/data["fighter2_SSR"]
data["fighter2_SSR_mins"] = data["fighter2_SSR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_SSD","fighter2_SSR"])

# TDD
data["fighter1_TDD_mins"] = data["fighter1_TDD"]/data["fighter1_total_time_fought"]
data["fighter1_TDD_TDR"] = data["fighter1_TDD"]/data["fighter1_TDR"]
data["fighter1_TDR_mins"] = data["fighter1_TDR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_TDD","fighter1_TDR"])

data["fighter2_TDD_mins"] = data["fighter2_TDD"]/data["fighter2_total_time_fought"]
data["fighter2_TDD_TDR"] = data["fighter2_TDD"]/data["fighter2_TDR"]
data["fighter2_TDR_mins"] = data["fighter2_TDR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_TDD","fighter2_TDR"])

# HDD
data["fighter1_HSD_mins"] = data["fighter1_HSD"]/data["fighter1_total_time_fought"]
data["fighter1_HSD_HSR"] = data["fighter1_HSD"]/data["fighter1_HSR"]
data["fighter1_HSR_mins"] = data["fighter1_HSR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_HSD","fighter1_HSR"])

data["fighter2_HSD_mins"] = data["fighter2_HSD"]/data["fighter2_total_time_fought"]
data["fighter2_HSD_HSR"] = data["fighter2_HSD"]/data["fighter2_HSR"]
data["fighter2_HSR_mins"] = data["fighter2_HSR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_HSD","fighter2_HSR"])

# BSD
data["fighter1_BSD_mins"] = data["fighter1_BSD"]/data["fighter1_total_time_fought"]
data["fighter1_BSD_BSR"] = data["fighter1_BSD"]/data["fighter1_BSR"]
data["fighter1_BSR_mins"] = data["fighter1_BSR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_BSD","fighter1_BSR"])

data["fighter2_BSD_mins"] = data["fighter2_BSD"]/data["fighter2_total_time_fought"]
data["fighter2_BSD_BSR"] = data["fighter2_BSD"]/data["fighter2_BSR"]
data["fighter2_BSR_mins"] = data["fighter2_BSR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_BSD","fighter2_BSR"])

# LSD
data["fighter1_LSD_mins"] = data["fighter1_LSD"]/data["fighter1_total_time_fought"]
data["fighter1_LSD_LSR"] = data["fighter1_LSD"]/data["fighter1_LSR"]
data["fighter1_LSR_mins"] = data["fighter1_LSR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_LSD","fighter1_LSR"])

data["fighter2_LSD_mins"] = data["fighter2_LSD"]/data["fighter2_total_time_fought"]
data["fighter2_LSD_LSR"] = data["fighter2_LSD"]/data["fighter2_LSR"]
data["fighter2_LSR_mins"] = data["fighter2_LSR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_LSD","fighter2_LSR"])

# DSD
data["fighter1_DSD_mins"] = data["fighter1_DSD"]/data["fighter1_total_time_fought"]
data["fighter1_DSD_DSR"] = data["fighter1_DSD"]/data["fighter1_DSR"]
data["fighter1_DSR_mins"] = data["fighter1_DSR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_DSD","fighter1_DSR"])

data["fighter2_DSD_mins"] = data["fighter2_DSD"]/data["fighter2_total_time_fought"]
data["fighter2_DSD_DSR"] = data["fighter2_DSD"]/data["fighter2_DSR"]
data["fighter2_DSR_mins"] = data["fighter2_DSR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_DSD","fighter2_DSR"])

# CSD
data["fighter1_CSD_mins"] = data["fighter1_CSD"]/data["fighter1_total_time_fought"]
data["fighter1_CSD_CSR"] = data["fighter1_CSD"]/data["fighter1_CSR"]
data["fighter1_CSR_mins"] = data["fighter1_CSR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_CSD","fighter1_CSR"])

data["fighter2_CSD_mins"] = data["fighter2_CSD"]/data["fighter2_total_time_fought"]
data["fighter2_CSD_CSR"] = data["fighter2_CSD"]/data["fighter2_CSR"]
data["fighter2_CSR_mins"] = data["fighter2_CSR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_CSD","fighter2_CSR"])

#GSD
data["fighter1_GSD_mins"] = data["fighter1_GSD"]/data["fighter1_total_time_fought"]
data["fighter1_GSD_GSR"] = data["fighter1_GSD"]/data["fighter1_GSR"]
data["fighter1_GSR_mins"] = data["fighter1_GSR"]/data["fighter1_total_time_fought"]
data.drop(columns = ["fighter1_GSD","fighter1_GSR"])

data["fighter2_GSD_mins"] = data["fighter2_GSD"]/data["fighter2_total_time_fought"]
data["fighter2_GSD_GSR"] = data["fighter2_GSD"]/data["fighter2_GSR"]
data["fighter2_GSR_mins"] = data["fighter2_GSR"]/data["fighter2_total_time_fought"]
data.drop(columns = ["fighter2_GSD","fighter2_GSR"])

# calculate win percentage
data["fighter1_win_pct"] = data["fighter1_wins"]/data["fighter1_totalfights"]
data["fighter2_win_pct"] = data["fighter2_wins"]/data["fighter2_totalfights"]


# convert features to percentage of wins
data["fighter1_wko"] = data["fighter1_wko"]/data["fighter1_wins"]
data["fighter1_wsub"] = data["fighter1_wsub"]/data["fighter1_wins"]
data["fighter1_wdec"] = data["fighter1_wdec"]/data["fighter1_wins"]
data["fighter1_wdq"] = data["fighter1_wdq"]/data["fighter1_wins"]

data["fighter2_wko"] = data["fighter2_wko"]/data["fighter1_wins"]
data["fighter2_wsub"] = data["fighter2_wsub"]/data["fighter1_wins"]
data["fighter2_wdec"] = data["fighter2_wdec"]/data["fighter1_wins"]
data["fighter2_wdq"] = data["fighter2_wdq"]/data["fighter1_wins"]

# convert features to percentage of loss
data["fighter1_lko"] = data["fighter1_lko"]/data["fighter1_losses"]
data["fighter1_lsub"] = data["fighter1_lsub"]/data["fighter1_losses"]
data["fighter1_ldec"] = data["fighter1_ldec"]/data["fighter1_losses"]
data["fighter1_ldq"] = data["fighter1_ldq"]/data["fighter1_losses"]

data["fighter2_lko"] = data["fighter2_lko"]/data["fighter1_losses"]
data["fighter2_lsub"] = data["fighter2_lsub"]/data["fighter1_losses"]
data["fighter2_ldec"] = data["fighter2_ldec"]/data["fighter1_losses"]
data["fighter2_ldq"] = data["fighter2_ldq"]/data["fighter1_losses"]

data.drop(columns="fighter1_wins")
data.drop(columns="fighter2_wins")

print(len(data.filter(regex="^fighter1",axis=1).columns))
print(len(data.filter(regex="^fighter2",axis=1).columns))

data["winner2"].value_counts()

data = data.reindex(sorted(data.columns), axis=1)

# convert special characters to nan values for imputation

data = data.replace('--', np.nan)

data = data.replace(np.inf, np.nan)

# encode categorical features
cats = ["fighter1_stance","fighter2_stance"]


for cat in cats:
  data[cat] = pd.Categorical(data[cat])

data[cats] = data[cats].apply(lambda col: col.cat.codes)


# drop unusable columns
data = data.drop(columns= ["_id","year","fighter1_name","fighter2_name","fighter1_id","fighter2_id","method","end_round","fighter1_total_time_fought","fighter2_total_time_fought","winner","weight_class"])

# split the dataset
from sklearn.model_selection import train_test_split
X, y = data.drop("winner2", axis=1), data["winner2"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

conts = X.drop(cats, axis=1).columns.values.tolist()

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

print(y_train.mean(), y_test.mean())

# define pipeline for iterative imputation
imputer = IterativeImputer()
pipeline = Pipeline(steps=[('i', imputer)])

X_train = pd.DataFrame(pipeline.fit_transform(X_train), columns = X_train.columns)
X_test= pd.DataFrame(pipeline.transform(X_test), columns = X_test.columns)


class UfcDataset(Dataset):
    def __init__(self, df, cats, conts, targets):
        self.X_cats = df[cats].astype(np.int64).values
        self.X_conts = df[conts].astype(np.float32).values
        self.y = targets.astype(np.float32).values.reshape(-1, 1)

    def __len__(self):
        return self.y.shape[0]

    def __getitem__(self, i):
        return [self.X_cats[i], self.X_conts[i], self.y[i]]



train_dataset = UfcDataset(X_train, cats, conts, y_train)
test_dataset = UfcDataset(X_test, cats, conts, y_test)

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# Data loaders
bz=32
train_dl = torch.utils.data.DataLoader(train_dataset, batch_size=bz, shuffle=True)
test_dl = torch.utils.data.DataLoader(test_dataset, batch_size=bz, shuffle=False)


class UfcNet(nn.Module):
    def __init__(self, emb_dims, num_conts, fc_layer_sizes, emb_drop, ps):
        super(UfcNet, self).__init__()

        # embedding layers for categorical features
        self.emb_layers = nn.ModuleList([nn.Embedding(x, y) for x, y in emb_dims])
        self.num_embs = sum([y for _, y in emb_dims])
        self.num_conts = num_conts

        # fully connected layers
        fc_layer_sizes = [self.num_embs + self.num_conts] + fc_layer_sizes
        self.fc_layers = nn.ModuleList([nn.Linear(fc_layer_sizes[i], fc_layer_sizes[i + 1])
                                        for i in range(len(fc_layer_sizes) - 1)])

        # out layer
        self.out = nn.Linear(fc_layer_sizes[-1], 1)

        # batch norm layers
        self.first_bn = nn.BatchNorm1d(self.num_conts)
        self.bn_layers = nn.ModuleList([nn.BatchNorm1d(sz)
                                        for sz in fc_layer_sizes[1:]])
        # dropout layers
        self.emb_drop = nn.Dropout(emb_drop)
        self.dropout_layers = nn.ModuleList([nn.Dropout(p) for p in ps])

    def forward(self, x_cats, x_conts):
        x = [e(x_cats[:, i]) for i, e in enumerate(self.emb_layers)]
        x = torch.cat(x, 1)
        x = self.emb_drop(x)

        x_c = self.first_bn(x_conts)
        x = torch.cat([x, x_c], 1)

        for fc, bn, d in zip(self.fc_layers, self.bn_layers, self.dropout_layers):
            x = F.relu(fc(x))
            x = bn(x)
            x = d(x)

        x = self.out(x)
        return torch.sigmoid(x)

emb_dims = [(len(data[cat].unique()), min(50, len(data[cat].unique())//2)) for cat in cats]
emb_dims

num_conts = len(conts)
fc_layer_sizes = [256, 64, 16]
emb_drop = 0.5
ps = [0.5] * 3

ufc_model = UfcNet(emb_dims, num_conts, fc_layer_sizes, emb_drop, ps).to(device)


criterion = nn.BCELoss()
learning_rate = 1e-2
optimizer = torch.optim.Adam(ufc_model.parameters(), lr=learning_rate, weight_decay=1e-4)

num_epochs = 4
total_step = len(train_dl)
for epoch in range(num_epochs):
    for i, (x_cats, x_conts, y) in enumerate(train_dl):
        x_cats, x_conts, y = x_cats.to(device), x_conts.to(device), y.to(device)

        # forward
        outputs = ufc_model(x_cats, x_conts)
        loss = criterion(outputs, y)

        # backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i + 1) % 100 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                  .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

with torch.no_grad():
    correct = 0
    total = 0
    for x_cats, x_conts, y in test_dl:
        x_cats, x_conts, y = x_cats.to(device), x_conts.to(device), y.to(device)
        outputs = ufc_model(x_cats, x_conts)
        preds = (outputs>0.5).type(torch.FloatTensor)
        total += y.size(0)
        correct += (preds == y).sum().item()

print ("Accuracy: {:.2f}%".format(100*correct/total))