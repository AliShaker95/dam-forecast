import pandas as pd
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv("data/processed/dams_clean.csv", parse_dates=["date"])

# inputs (only today and the past)
rain_cols = [c for c in data.columns if c.startswith("rain_")]
data["rain_30d"] = data[rain_cols].mean(axis=1).rolling(30).sum()
data["use_30d"] = data["consumption"].rolling(30).mean()
data["change_30d"] = data["occ_total"].diff(30)
data["month"] = data["date"].dt.month

# the answer: level 30 days later
data["target"] = data["occ_total"].shift(-30)
data = data.dropna(subset=["rain_30d", "change_30d", "target"])

months = pd.get_dummies(data["month"], prefix="m", dtype=int)
X = pd.concat(
    [data[["occ_total", "change_30d", "rain_30d", "use_30d"]], months], axis=1
)
y = data["target"]

# split by date
train = data["date"] < "2022-12-02"
test = data["date"] >= "2023-01-01"

# learn, then predict
model = RandomForestRegressor(
    n_estimators=300, min_samples_leaf=5, random_state=0, n_jobs=-1
)
model.fit(X[train], y[train])
pred = model.predict(X[test])

error = pred - y[test]
print("test days:", test.sum())
print(
    "average miss:",
    round(error.abs().mean(), 2),
    "points   (baseline: 8.05, linear: 6.03)",
)
print(
    "too full:", (error > 0).sum(), "days, average", round(error[error > 0].mean(), 2)
)
print(
    "too empty:", (error < 0).sum(), "days, average", round(error[error < 0].mean(), 2)
)
