import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

data = pd.read_csv("data/processed/dams_clean.csv", parse_dates=["date"])

# same inputs as before
rain_cols = [c for c in data.columns if c.startswith("rain_")]
data["rain_30d"] = data[rain_cols].mean(axis=1).rolling(30).sum()
data["use_30d"] = data["consumption"].rolling(30).mean()
data["change_30d"] = data["occ_total"].diff(30)
data["month"] = data["date"].dt.month
data["target"] = data["occ_total"].shift(-30)
data = data.dropna(subset=["rain_30d", "change_30d", "target"])

months = pd.get_dummies(data["month"], prefix="m", dtype=int)
X = pd.concat(
    [data[["occ_total", "change_30d", "rain_30d", "use_30d"]], months], axis=1
)
y = data["target"]
train = data["date"] < "2022-12-02"
test = data["date"] >= "2023-01-01"

linear = LinearRegression().fit(X[train], y[train])
forest = RandomForestRegressor(
    n_estimators=300, min_samples_leaf=5, random_state=0, n_jobs=-1
).fit(X[train], y[train])

# one table: the day each prediction is ABOUT, the real level, and each guess
res = pd.DataFrame(
    {
        "date": data.loc[test, "date"] + pd.Timedelta(days=30),
        "real": y[test],
        "baseline": data.loc[test, "occ_total"],
        "linear": linear.predict(X[test]),
        "forest": forest.predict(X[test]),
    }
)

# chart
plt.figure(figsize=(12, 5))
plt.plot(res["date"], res["real"], color="black", linewidth=2, label="real")
for name in ["baseline", "linear", "forest"]:
    plt.plot(res["date"], res[name], label=name)
plt.title("Predicted vs real level, 30 days ahead")
plt.xlabel("Date")
plt.ylabel("Level (%)")
plt.legend()
plt.savefig("figures/predicted_vs_real.png")
plt.show()

# average miss per month (+ = too full, - = too empty)
for name in ["baseline", "linear", "forest"]:
    res[name + "_miss"] = res[name] - res["real"]
monthly = (
    res.groupby(res["date"].dt.to_period("M"))[
        ["baseline_miss", "linear_miss", "forest_miss"]
    ]
    .mean()
    .round(1)
)
print(monthly)
