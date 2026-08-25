import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
from sklearn.model_selection import GroupKFold
import os
import optuna

script_dir = os.path.dirname(os.path.abspath(__file__))
data = os.path.join(script_dir, "k_2026.csv")
df = pd.read_csv(data)

training = [2021, 2022, 2023, 2024]
validation = 2025

train_df = df[df['Season'].isin(training)].copy()
val_df = df[df['Season'] == validation].copy()

features = ['TBF', 'Stuff+', 'Age']
target = 'K%'

X_train, y_train = train_df[features], train_df[target]
X_val, y_val = val_df[features], val_df[target]

w_train = train_df['TBF']
w_val = val_df['TBF']


def objective(trial):
    params = {
        'objective': 'reg:logistic',
        'n_estimators': trial.suggest_int('n_estimators', 100, 800),
        'max_depth': trial.suggest_int('max_depth', 2, 6),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0, log=True),
        'random_state': 42,
    }

    gkf = GroupKFold(n_splits=4)
    groups = train_df['Season']
    scores = []

    for tr_idx, te_idx in gkf.split(X_train, y_train, groups=groups):
        X_tr, X_te = X_train.iloc[tr_idx], X_train.iloc[te_idx]
        y_tr, y_te = y_train.iloc[tr_idx], y_train.iloc[te_idx]
        w_tr = w_train.iloc[tr_idx]

        model = XGBRegressor(**params)
        model.fit(X_tr, y_tr, sample_weight=w_tr)
        preds = model.predict(X_te)
        scores.append(mean_absolute_error(y_te, preds))

    return np.mean(scores)

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)

print("Best Parameters:", study.best_params)

best_params = study.best_params
best_params['objective'] = 'reg:logistic'
best_params['random_state'] = 42

final_model = XGBRegressor(**best_params)
final_model.fit(X_train, y_train, sample_weight=w_train)

val_preds = final_model.predict(X_val)

rmse = root_mean_squared_error(y_val, val_preds)
mae = mean_absolute_error(y_val, val_preds)

print(f"Validation RMSE: {rmse:.4f}")
print(f"Validation MAE: {mae:.4f}")