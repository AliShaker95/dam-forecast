import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data/processed/dams_clean.csv", parse_dates=["date"])

plt.figure(figsize=(12, 5))
plt.plot(data["date"], data["occ_total"])
plt.title("Overall dam level")
plt.xlabel("Date")
plt.ylabel("Level (%)")
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.grid(axis="x", which="major", alpha=0.3)
# plt.savefig("figures/occ_total.png")
plt.show()


data["month"] = data["date"].dt.month
monthly = data.groupby("month")["occ_total"].mean().round(1)
print(monthly)

plt.figure(figsize=(8, 4))
plt.bar(monthly.index, monthly.values)
plt.title("Average level by month")
plt.xlabel("Month")
plt.ylabel("Level (%)")
plt.xticks(range(1, 13))
# plt.savefig("figures/level_by_month.png")
plt.show()


rain_cols = [c for c in data.columns if c.startswith("rain_")]
data["rain_avg"] = data[rain_cols].mean(axis=1)          # average rain of the 10 dams, per day
data["rain_30d"] = data["rain_avg"].rolling(30).sum()    # total rain over the last 30 days
data["change_30d"] = data["occ_total"].diff(30)          # level today minus level 30 days ago

print(data[["rain_30d", "change_30d"]].corr().round(2))

plt.figure(figsize=(7, 5))
plt.scatter(data["rain_30d"], data["change_30d"], s=3, alpha=0.3)
plt.axhline(0, color="gray", linewidth=0.8)              # line at "no change"
plt.title("Rain vs level change (30 days)")
plt.xlabel("Rain in the last 30 days (mm)")
plt.ylabel("Level change over the same 30 days (points)")
# plt.savefig("figures/rain_vs_change.png")
plt.show()