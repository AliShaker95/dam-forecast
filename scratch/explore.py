import pandas as pd

dams = pd.read_excel("data/raw/istanbul-dams-daily-occupancy-rates.xlsx")
rain = pd.read_excel("data/raw/istanbul-barajlarnda-ya-ve-gunluk-tuketim-verileri.xlsx")


print(dams.head())
print(dams.shape)

print(rain.head())
print(rain.shape)

print(dams.dtypes)
print(rain.dtypes)

print(rain.columns)
print(rain["Unnamed: 11"].isna().sum())
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

print(dams.columns)
print(rain.columns)
