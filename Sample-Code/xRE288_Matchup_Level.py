#imports
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import os

#load datasets
script_dir = os.path.dirname(os.path.abspath(__file__))
training = os.path.join(script_dir, "trainingData_withNoSmallSample.csv")
training_df = pd.read_csv(training)
validation = os.path.join(script_dir, "outOfSampleValidationData.csv")
validation_df = pd.read_csv(validation)
re288 = os.path.join(script_dir, "re288Data.csv")
re288_df = pd.read_csv(re288)

#map handedness to binary values for modeling
training_df["stand"] = training_df["stand"].map({"L": 0, "R": 1})
training_df["p_throws"] = training_df["p_throws"].map({"L": 0, "R": 1})

validation_df["stand"] = validation_df["stand"].map({"L": 0, "R": 1})
validation_df["p_throws"] = validation_df["p_throws"].map({"L": 0, "R": 1})

#platoon advantage: 1 opposite handedness, 0 same handedness
training_df["platoon_adv"] = (training_df["stand"] != training_df["p_throws"]).astype(int)
validation_df['platoon_adv'] = (validation_df['stand'] != validation_df['p_throws']).astype(int)

#handedness matchup: 0 is LHP LHH, 1 is LHP RHH, 2 is RHP LHH, 3 is RHP RHH
training_df["matchup"] = training_df["p_throws"] * 2 + training_df["stand"]
validation_df["matchup"] = validation_df["p_throws"] * 2 + validation_df["stand"]

state_cols = ['balls', 'strikes', 'outs_when_up', '1b', '2b', '3b']

#merge RE288 data to training and validation datasets to get runs after count for validation and comparison
training_df = training_df.merge(
    re288_df[state_cols + ['runs_after_count']],
    on=state_cols,
    how='left',
    validate='many_to_one'
)

validation_df = validation_df.merge(
    re288_df[state_cols + ['runs_after_count']],
    on=state_cols,
    how='left',
    validate='many_to_one'
)

#features
features = [
    "platoon_adv",
    "Rbat+",
    "ERA+",
    "team_Rbat+",
    "balls",
    "strikes",
    "outs_when_up",
    "1b", "2b", "3b"
]

monotone_constraints = {
    "platoon_adv": 1,
    "Rbat+": 1,
    "ERA+": -1,
    "team_Rbat+": 1,
    "balls": 1,
    "strikes": -1,
    "outs_when_up": -1,
    "1b": 1,
    "2b": 1,
    "3b": 1,
}

#target
target = "runs_after_pitch"

#prepare datasets for modeling, dropping any rows with missing values in features or target
model_df = training_df[features + [target]].dropna().copy()
validation_df = validation_df[features + [target, "runs_after_count"]].dropna().copy()
away_from_league_avg_df = validation_df[(validation_df['Rbat+'] <= 40) | (validation_df['Rbat+'] >= 160) | (validation_df['ERA+'] <= 40) | (validation_df['ERA+'] >= 160)].copy()

#Specific matchup test
gore_vs_alonso_df = re288_df.copy()
gore_vs_alonso_df["ERA+"] = 99
gore_vs_alonso_df["Rbat+"] = 142
gore_vs_alonso_df["HR%"] = 0.54
gore_vs_alonso_df["ISO"] = 0.252
gore_vs_alonso_df["team_Rbat+"] = 113
gore_vs_alonso_df["team_ISO"] = 0.178
gore_vs_alonso_df["team_HR%"] = 0.36
stand = 1
p_throws = 0
gore_vs_alonso_df["stand"] = stand
gore_vs_alonso_df["p_throws"] = p_throws
gore_vs_alonso_df["platoon_adv"] = int(stand != p_throws)
gore_vs_alonso_df["matchup"] = p_throws * 2 + stand
gore_vs_alonso_X = gore_vs_alonso_df[features]


#overall x and y
X = model_df[features]
y = model_df[target]

#validation x and y
X_val = validation_df[features]
y_val = validation_df[target]
away_avg_X_val = away_from_league_avg_df[features]
away_avg_y_val = away_from_league_avg_df[target]

#model parameters
model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=1000,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    min_child_weight=3,
    gamma=0.1,
    random_state=42,
    monotone_constraints=monotone_constraints
)

#train model
model.fit(X, y)
print(model.get_booster().get_score(importance_type="gain"))
val_preds = model.predict(X_val)
val_rmse = np.sqrt(mean_squared_error(y_val, val_preds))
away_avg_preds = model.predict(away_avg_X_val)
away_avg_rmse = np.sqrt(mean_squared_error(away_avg_y_val, away_avg_preds))

#calculate and print evaluation metrics
rmse_re288 = np.sqrt(mean_squared_error(validation_df['runs_after_pitch'], validation_df['runs_after_count']))
rmse_re288_away_avg = np.sqrt(mean_squared_error(away_from_league_avg_df['runs_after_pitch'], away_from_league_avg_df['runs_after_count']))

print("\nValidation Check:")
print("\nValidation RMSE:", val_rmse)
print("RMSE (RE288):", rmse_re288)
print("Validation vs RE288 RMSE Difference:", val_rmse - rmse_re288)
print("\nAway from League Average Validation Check:")
print("\nAway from League Average Validation RMSE:", away_avg_rmse)
print("Away from League Average Validation vs RE288 RMSE Difference:", away_avg_rmse - rmse_re288)

matchup_preds = model.predict(gore_vs_alonso_X)

gore_vs_alonso_df["model_pred"] = matchup_preds
gore_vs_alonso_df["re288"] = gore_vs_alonso_df["runs_after_count"]
gore_vs_alonso_df["difference"] = (
    gore_vs_alonso_df["model_pred"] - gore_vs_alonso_df["re288"]
)

gore_vs_alonso_df.to_csv(os.path.join(script_dir, "gore_vs_alonso_all_states.csv"), index=False)
