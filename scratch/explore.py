import pandas as pd

dams = pd.read_excel("data/raw/istanbul-dams-daily-occupancy-rates.xlsx")
rain = pd.read_excel("data/raw/istanbul-barajlarnda-ya-ve-gunluk-tuketim-verileri.xlsx")


# print(dams.head())
# print(dams.shape)
# print(dams.dtypes)

# print(rain.head())
# print(rain.shape)
# print(rain.dtypes)

# print(rain.columns)
# print(rain["Unnamed: 11"].isna().sum())
rain = rain.drop(columns=['Unnamed: 11'])
print(rain.head())