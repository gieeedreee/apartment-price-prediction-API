import pandas as pd
import re as re


def load_data(filename: str):
    return pd.read_csv(filename)


def drop_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna(subset=['Year'])
    return data


def split_columns(data: pd.DataFrame) -> pd.DataFrame:
    data['Flat_floor'] = (data["Floor"].str.split("/", n=1, expand=True)[0])
    data['Total_floor'] = (data["Floor"].str.split("/", n=1, expand=True)[1])
    data['Price_eur'] = (data["Price"].str.split("€", n=1, expand=True)[0])
    data['Price_m2'] = (data["Price"].str.split("€", n=1, expand=True)[1])
    data = data.dropna(subset=['Total_floor'])
    return data


def find_number(text):
    num = re.findall(r'[0-9]+', text)
    return "".join(num)


def change_to_number(data: pd.DataFrame) -> pd.DataFrame:
    data['Price_eur'] = data['Price_eur'].apply(lambda x: find_number(x))
    data['Price_m2'] = data['Price_m2'].apply(lambda x: find_number(x))
    return data


def extract_city_merge(data: pd.DataFrame):
    data_copy = data.copy()
    title_city = data_copy.Title.str.extract('(?P<Title>.{17})(?P<City>.{1,})')
    final = pd.merge(data, title_city, left_index=True, right_index=True)
    return final


def transform_to_numeric_values(final: pd.DataFrame):
    final['Year'] = final['Year'].astype(int)
    final['Flat_floor'] = final['Flat_floor'].astype(int)
    final['Total_floor'] = final['Total_floor'].astype(int)
    final['Price_eur'] = final['Price_eur'].astype(int)
    final['Price_m2'] = final['Price_m2'].astype(int)
    return final


def drop_columns(final: pd.DataFrame):
    indexNames = final[(final['Price_eur'] < 2000)].index
    indexFloor = final[(final['Flat_floor'] > 40)].index
    indexArea = final[(final['Area'] > 1000)].index
    indexFloor2 = final[(final['Flat_floor'] < 0)].index
    final.drop(indexNames, inplace=True)
    final.drop(indexFloor, inplace=True)
    final.drop(indexArea, inplace=True)
    final.drop(indexFloor2, inplace=True)
    final.drop(['Floor', 'Price', 'Title_x', 'Title_y'], axis=1, inplace=True)
    return final


def replace_text_all(final: pd.DataFrame):
    final['City'] = final['City'].map({'Alytuje': 'Regionas',
                                       'Neringoje': 'Regionas',
                                       'Neringa': 'Regionas',
                                       'Neringa': 'Regionas',
                                       'Marijampolės sav.': 'Regionas',
                                       'Vilniaus rajono sav.': 'Regionas',
                                       'Vilniaus r. sav.': 'Regionas',
                                       'Kauno rajono sav.': 'Regionas',
                                       'Klaipėdos rajono sav.': 'Regionas',
                                       'Klaipėdos rajono sav. ': 'Regionas',
                                       'Klaipėdos r. sav.': 'Regionas',
                                       'Šiaulių rajono sav.': 'Regionas',
                                       'Panevėžio rajono sav.': 'Regionas',
                                       'Panevėžio r. sav.': 'Regionas',
                                       'Šventojoje': 'Regionas',
                                       'Neringa ': 'Regionas',
                                       'Kretingos rajono sav.': 'Regionas',
                                       'Kretingos r. sav.': 'Regionas',
                                       'Trakų r. sav.': 'Regionas',
                                       'Trakų rajono sav.': 'Regionas',
                                       'Elektrėnų sav.': 'Regionas',
                                       'Švenčionių rajono sav.': 'Regionas',
                                       'Radviliškio rajono sav.': 'Regionas',
                                       'Jonavos rajono sav.': 'Regionas',
                                       'Joniškio rajono sav.': 'Regionas',
                                       'Mažeikių rajono sav.': 'Regionas',
                                       'Akmenės rajono sav.': 'Regionas',
                                       'Ignalinos rajono sav.': 'Regionas',
                                       'Širvintų rajono sav.': 'Regionas',
                                       'Ukmergės rajono sav.': 'Regionas',
                                       'Raseinių rajono sav.': 'Regionas',
                                       'Kupiškio rajono sav.': 'Regionas',
                                       'Utenos rajono sav.': 'Regionas',
                                       'Tauragės rajono sav.': 'Regionas',
                                       'Kelmės rajono sav.': 'Regionas',
                                       'Šilutės rajono sav.': 'Regionas',
                                       'Anykščių rajono sav.': 'Regionas',
                                       'Pagėgių sav.': 'Regionas',
                                       'Šalčininkų rajono sav.': 'Regionas',
                                       'Kėdainių rajono sav.': 'Regionas',
                                       ' Pasvalio rajono sav.': 'Regionas',
                                       'Varėnos rajono sav.': 'Regionas',
                                       'Kaišiadorių rajono sav.': 'Regionas',
                                       'Birštono sav.': 'Regionas',
                                       'Rokiškio rajono sav.': 'Regionas',
                                       'Pakruojo rajono sav.': 'Regionas',
                                       'Biržų rajono sav.': 'Regionas',
                                       'Plungės rajono sav.': 'Regionas',
                                       'Rietavo sav.': 'Regionas',
                                       'Kelmės r. sav.': 'Regionas',
                                       'Širvintų r. sav.': 'Regionas',
                                       'Biržų r. sav.': 'Regionas',
                                       'Joniškio r. sav.': 'Regionas',
                                       'Šalčininkų r. sav.': 'Regionas',
                                       'Akmenės r. sav.': 'Regionas',
                                       'Tauragės r. sav.': 'Regionas',
                                       'Pasvalio rajono sav.': 'Regionas',
                                       'Vilniuje ': 'Vilnius',
                                       'Vilniuje': 'Vilnius',
                                       'Vilnius ': 'Vilnius',
                                       'Vilnius': 'Vilnius',
                                       'Šiauliuose': 'Siauliai',
                                       'Šiauliai': 'Siauliai',
                                       'Panevėžys': 'Panevezys',
                                       'Kaune': 'Kaunas',
                                       'Alytaus miesto sav.': 'Regionas',
                                       'Klaipėdoje': 'Klaipeda',
                                       'Panevėžyje': 'Panevezys',
                                       'Palangoje': 'Palanga',
                                       'Palangoje ': 'Palanga',
                                       'Vanagupėje': 'Palanga',
                                       'Klaipėda': 'Klaipeda',
                                       'Druskininkų sav.': 'Druskininkai'},
                                      na_action=None)
    return final


def make_intermediate(
        load_data_filename: str = "data/scraped_information.csv",
        output: str = "data/cleaned_data.csv",
) -> pd.DataFrame:
    data = load_data(load_data_filename)
    data = drop_missing_values(data)
    data = split_columns(data)
    data = change_to_number(data)
    final = extract_city_merge(data)
    final = transform_to_numeric_values(final)
    final = drop_columns(final)
    final = replace_text_all(final)
    final.to_csv(output)
    return final


if __name__ == "__main__":
    df = make_intermediate()
    df.to_csv("data/cleaned_data.csv")
