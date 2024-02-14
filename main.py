# Импорт необходимых библиотек
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from matplotlib import colors


def load_and_prepare_data(dataset_path):
    """Загрузка и подготовка данных."""
    # Загрузка данных
    sf = pd.read_csv(dataset_path)

    # Настройка отображения данных в pandas
    pd.set_option('display.max_rows', 5)

    # Добавление столбцов с месяцем и днем из даты
    sf['Month'] = sf['Date'].apply(lambda row: int(row[0:2]))
    sf['Day'] = sf['Date'].apply(lambda row: int(row[3:5]))

    # Удаление ненужных столбцов
    sf.drop(['IncidntNum', 'Location'], axis=1, inplace=True)

    return sf


def analyze_data(sf):
    """Анализ данных."""
    # Вывод количества инцидентов по категориям
    print("\nКоличество инцидентов по категориям, убывающий порядок:")
    print(sf['Category'].value_counts())
    print("\nКоличество инцидентов по категориям, возрастающий порядок:")
    print(sf['Category'].value_counts(ascending=True))

    # Вывод количества инцидентов по районам
    print("\nКоличество инцидентов по районам, возрастающий порядок:")
    print(sf['PdDistrict'].value_counts(ascending=True))

    # Фильтрация данных за август и по категории 'BURGLARY'
    print("\nИнциденты за август:")
    august_crimes = sf[sf['Month'] == 8]
    print(august_crimes.head())

    print("\nКоличество инцидентов 'BURGLARY':")
    august_crimes_b = sf[sf['Category'] == 'BURGLARY']
    print(len(august_crimes_b))

    print("\nИнциденты 4 июля:")
    crime_0704 = sf.query('Month == 7 and Day == 4')
    print(crime_0704.head())


def plot_and_save_data(sf):
    """Представление данных и сохранение графиков."""
    # Точечный график координат инцидентов
    plt.figure()
    plt.plot(sf['X'], sf['Y'], 'ro')
    plt.savefig('plot.png')

    # Распределение инцидентов по районам с кодированием цветом
    pd_districts = np.unique(sf['PdDistrict'])
    pd_districts_levels = dict(zip(pd_districts, range(len(pd_districts))))
    sf['PdDistrictCode'] = sf['PdDistrict'].apply(lambda row: pd_districts_levels[row])

    plt.figure()
    plt.scatter(sf['X'], sf['Y'], c=sf['PdDistrictCode'])
    plt.savefig('scatter_plot.png')

    # Создание карты с метками инцидентов
    color_dict = dict(zip(pd_districts, list(colors.cnames.values())[0:len(pd_districts)]))
    map_osm = folium.Map(location=[sf['Y'].mean(), sf['X'].mean()], zoom_start=12)
    plot_every = 50
    for el in list(zip(sf['Y'], sf['X'], sf['PdDistrict']))[0::plot_every]:
        folium.CircleMarker(el[0:2], color=color_dict[el[2]], fill_color=color_dict[el[2]], radius=10).add_to(map_osm)

    # Сохранение карты в HTML
    map_osm.save('sf_crime_map.html')


# Основной блок
if __name__ == "__main__":
    dataset_path = 'Map-Crime_Incidents-Previous_Three_Months.csv'
    sf = load_and_prepare_data(dataset_path)

    # Вывод названий колонок и общего количества записей
    print("Названия столбцов:")
    print(sf.columns)
    print("\nОбщее количество записей:")
    print(len(sf))

    analyze_data(sf)
    plot_and_save_data(sf)
