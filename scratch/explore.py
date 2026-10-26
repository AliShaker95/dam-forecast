import pandas as pd

dams = pd.read_excel("data/raw/istanbul-dams-daily-occupancy-rates.xlsx")
rain = pd.read_excel("data/raw/istanbul-barajlarnda-ya-ve-gunluk-tuketim-verileri.xlsx")


# print(dams.head())    # shows the head (first 5 rows) of dams.
# print(dams.shape)     # shows the shape (no of rows and columns) in dams.

# print(rain.head())    # shows the head (first 5 rows) of rain.
# print(rain.shape)     # shows the shape (no of rows and columns) in rain.

# print(dams.dtypes)    # shows the data type of each column in dams.
# print(rain.dtypes)    # shows the data type of each column in rain.

# print(rain.columns)
# print(rain["Unnamed: 11"].isna().sum())   # the total no of the empty cells in the column "Unnamed: 11".
rain = rain.drop(columns=["Unnamed: 11"])   # remove the empty column

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

# print(dams.columns)
# print(rain.columns)

# print(dams["date"].map(type).value_counts())        # counts different types of data in the column "date"
# text_dates = dams[dams["date"].map(type) == str]    # save the data that has the type "str" for column "date"
# print(text_dates.head(20))
# print(text_dates.tail(20))

is_text = dams["date"].map(type) == str     # true: the data in the column "date" is str, false: is not
# if the data type in column "date" is str, it changes it to the wanted format
dams.loc[is_text, "date"] = pd.to_datetime(dams.loc[is_text, "date"], format="%d.%m.%Y")

dams["date"] = pd.to_datetime(dams["date"])     # changes the entire column preset to the wanted format

# print(dams.dtypes)

gaps = dams["date"].diff()      # the difference from the row before in the column "date"
print(gaps.value_counts())

print(rain.dtypes)
print(rain["date"].diff().value_counts())