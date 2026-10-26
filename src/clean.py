import pandas as pd

dams = pd.read_excel("data/raw/istanbul-dams-daily-occupancy-rates.xlsx")
rain = pd.read_excel("data/raw/istanbul-barajlarnda-ya-ve-gunluk-tuketim-verileri.xlsx")

dams_capacity = {
    "omerli": 244540000,
    "darlik": 102463000,
    "elmali": 9600000,
    "terkos": 195974000,
    "alibey": 34143000,
    "buyukcekmece": 129892000,
    "sazlidere": 88730000,
    "kazandere": 21096000,
    "pabucdere": 35222000,
    "istrancalar": 6231000,
}

rain = rain.drop(columns=["Unnamed: 11"])

dams = dams.rename(
    columns={
        "Tarih": "date",
        "Ömerli": "occ_omerli",
        "Darlık": "occ_darlik",
        "Elmalı": "occ_elmali",
        "Terkos": "occ_terkos",
        "Alibey": "occ_alibey",
        "Büyükçekmece": "occ_buyukcekmece",
        "Sazlıdere": "occ_sazlidere",
        "Kazandere": "occ_kazandere",
        "Pabuçdere": "occ_pabucdere",
        "Istrancalar": "occ_istrancalar",
    }
)

rain = rain.rename(
    columns={
        "Tarih": "date",
        "Ömerli": "rain_omerli",
        "Darlik": "rain_darlik",
        "Elmali": "rain_elmali",
        "Terkos": "rain_terkos",
        "B.çekmece": "rain_buyukcekmece",
        "Sazlidere": "rain_sazlidere",
        "Alibey": "rain_alibey",
        "Kazandere": "rain_kazandere",
        "Pabuçdere": "rain_pabucdere",
        "ıstırancalar": "rain_istrancalar",
        "İstanbul günlük tüketim(m³/gün)": "consumption",
    }
)

is_text = dams["date"].map(type) == str
dams.loc[is_text, "date"] = pd.to_datetime(dams.loc[is_text, "date"], format="%d.%m.%Y")

dams["date"] = pd.to_datetime(dams["date"])

occ_cols = dams.columns.drop("date")
not_percent = dams["occ_omerli"] <= 1
dams.loc[not_percent, occ_cols] = dams.loc[not_percent, occ_cols] * 100

capacity = pd.Series(dams_capacity)
capacity.index = "occ_" + capacity.index
water = dams[capacity.index] * capacity / 100
dams["occ_total"] = water.sum(axis=1) / capacity.sum() * 100

data = pd.merge(dams, rain, on="date", how="inner")

data.to_csv("data/processed/dams_clean.csv", index=False)