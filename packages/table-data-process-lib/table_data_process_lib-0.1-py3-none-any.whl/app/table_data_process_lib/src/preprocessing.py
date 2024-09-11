import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def read_data(filepath, delimiter=None, dtype_dict=None):
    """
    Загрузка данных с указанием типов данных

    filepath: путь к файлу с данными
    delimiter: разделитель признаков
    dtype_dict: словарь типов столбцов
    """

    df = pd.read_csv(filepath, delimiter=delimiter, dtype=dtype_dict, on_bad_lines='skip', low_memory=False)

    return df


def print_info(data):
    """
    Вывод информации о датасете

    data: датасет
    """
    print("Описание данных с помощью метода info: \n", data.info())
    print("Описание данных с помощью метода describe: \n", data.describe(percentiles=[0.25, 0.5, 0.75]))
    print("Data head: \n", data.head(10))


def add_time_to_date(data, date_column, time_column, new_column_name=None):
    """
    Объединение столбцов даты и времени

    data: датасет
    date_column: столбец с датой
    time_column: столбец со временем
    """
    if new_column_name is not None:
        new_column = new_column_name
    else:
        new_column = date_column + 'time'

    # Преобразование даты и времени в единый временной формат
    data[new_column] = pd.to_datetime(data[date_column] + ' ' + data[time_column], dayfirst=True)

    # Удаление исходных столбцов времени и даты
    data.drop([time_column, date_column], axis=1, inplace=True)

    return new_column

def drop_columns(data, columns_to_drop):
    """
    Удаление столбцов из датасета

    data: Список столбцов для удаления
    """
    columns_to_drop = [col for col in columns_to_drop if col in data.columns]
    new_data = data.drop(columns_to_drop, axis=1)

    return new_data

def fill_nan(data, columns=None):
    """
    Заполнение пропущенных значений в признаках пустыми строками

    data: датасет
    columns: столбцы, в которых нужно заполнить пропущенные значения
    """
    if columns is not None:
        data[columns] = data[columns].fillna('')
    else:
        data = data.fillna('')

    return data

def category_to_num(data):
    """
    Преобразование категориальных признаков в числовые

    data: датасет
    """
    label_encoder = LabelEncoder()

    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()

    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col])

    return data

def get_test_train(data, target_column, columns_to_drop):
    """
    Разделение данных на обучающую и тестовую выборки

    data: датасет
    target_column: целеаой признак
    columns_to_drop: список признаков, которые не нужно использовать при обучении
    """
    # Определение целевой переменной и признаков
    columns_to_drop.append(target_column)

    X = data.drop(columns_to_drop, axis=1)
    y = data[target_column]

    # Разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test