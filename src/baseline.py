import pandas as pd

data = pd.read_csv("data/processed/dams_clean.csv", parse_dates=["date"])

# the answer: the level 30 days later
data["target"] = data["occ_total"].shift(-30)
data = data.dropna(subset=["target"])          # the last 30 days have no answer

# split by date
test = data[data["date"] >= "2023-01-01"]

# the guess: same as today
guess = test["occ_total"]
error = guess - test["target"]                 # positive = guessed too full

# the score
print("test days:", len(test))
print("average miss:", error.abs().mean().round(2), "points")
print("too full:", (error > 0).sum(), "days, average", error[error > 0].mean().round(2))
print("too empty:", (error < 0).sum(), "days, average", error[error < 0].mean().round(2))