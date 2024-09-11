from app.table_data_process_lib import (
    read_data, print_info, fill_nan, category_to_num, get_test_train, add_time_to_date, drop_columns, xgbclassifier,
    model_evaluation, smote_resampling, save_predictions
)


# Чтение данных
filepath = 'ECG_array_arrow_data.csv'
data = read_data(filepath, delimiter=';')

# Вывод сводки по датасету
print_info(data)

# Создание столбца с временем
datetime_column = add_time_to_date(data, 'eeg_date ', 'eeg_time ', new_column_name='ecg_time')

# Удаление неинформативных столбцов
report_columns = [col for col in data.columns if 'report_' in col]
data = drop_columns(data, report_columns)

# Заполнение пропусков
data = fill_nan(data)

# Преобразование категориальных прихзнаков в числовые
data = category_to_num(data)

# Разделение данных на обучающую и тестовую выборки
target_column = 'Healthy Status'
columns_to_drop = ['subject_id', 'study_id', 'cart_id', datetime_column, 'Count_subj']
X_train, X_test, y_train, y_test = get_test_train(data, target_column, columns_to_drop)

# SMOTE resampling
X_train_res, y_train_res = smote_resampling(X_train, y_train)

# Обучение модели XGB Classifier
model = xgbclassifier(X_train_res, y_train_res, n_estimators=100, learning_rate=0.1, max_depth=3)

# Оценка модели
report = model_evaluation(model, X_test, y_test, regression_task=False)
print('Classification Report:')
print(report)

# Получение предсказаний
predictions = model.predict(X_test)

# Сохранение предсказаний
save_predictions(X_test, predictions, 'ECG_predictions.csv')
