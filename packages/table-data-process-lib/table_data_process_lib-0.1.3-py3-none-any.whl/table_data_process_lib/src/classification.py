from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from imblearn.over_sampling import SMOTE
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report


def smote_resampling(X_train, y_train):
    """
    SMOTE resampling

    X_train: обучающие признаки
    y_train: целевой признак
    """
    smote = SMOTE()
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    return X_train_res, y_train_res


def xgbclassifier(X_train, y_train, n_estimators=100, learning_rate=0.1, max_depth=3):
    """
    Обучение модели XGBoost classifier

    X_train: датасет признаков для обучения
    y_train: данные цедевого признака, используемые для обучения
    use_label_encoder: Указывает, следует ли использовать встроенный label encoder
    n_estimators: Количество градиентно бустинговых деревьев, используемых в модели
    learning_rate: Шаг обучения, используемый для уменьшения вклада каждого дерева
    max_depth: Максимальная глубина каждого дерева

    """
    model = XGBClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth)
    model.fit(X_train, y_train)
    pickle.dump(model, open('model.pkl', "wb"))

    return model


def logistic_regression_classifier(X_train, y_train, C=1.0, max_iter=100, solver='lbfgs'):
    """
    Обучение модели Logistic Regression.

    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    C: обратная сила регуляризации (меньше значения, сильнее регуляризация)
    max_iter: максимальное количество итераций алгоритма
    solver: алгоритм, используемый в оптимизационных проблемах

    """
    model = LogisticRegression(C=C, max_iter=max_iter, solver=solver)
    model.fit(X_train, y_train)
    return model


def train_and_evaluate_mlp(X_train, X_test, y_train, y_test, hidden_layer_sizes=(100,), activation='relu', alpha=0.0001, learning_rate_init=0.001, max_iter=200):
    """
    Обучает MLPClassifier и оценивает его производительность

    Parameters:
    X_train: Training features
    X_test: Testing features
    y_train: Training labels
    y_test: Testing labels
    hidden_layer_sizes: Кортеж, представляющий количество нейронов в каждом скрытом слое
    activation: Функция активации ('relu', 'tanh', 'logistic')
    alpha: Параметр регуляризации L2
    learning_rate_init: Начальная скорость обучения
    max_iter: Максимальное количество итераций

    Returns:
    model: Обученный MLPClassifier
    accuracy: Accuracy score на тестовом датасете
    classification_report:  classification report
    """

    # Initialize and train the model
    model = MLPClassifier(
        hidden_layer_sizes=hidden_layer_sizes,
        activation=activation,
        alpha=alpha,
        learning_rate_init=learning_rate_init,
        max_iter=max_iter,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return model, accuracy, report


def model_evaluation(model, X_test, y_test, regression_task=True):
    """
    Оценка модели

    model: модель XGBoost
    X_test: датасет признаков для валидации
    y_test: данные цедевого признака, используемые для валидации
    regression_task: решается ли задача регрессии или классификации
    """
    y_pred = model.predict(X_test)
    if regression_task:
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        report = {'MSE': mse, 'MAE': mae, 'R2': r2}
    else:
        report = classification_report(y_test, y_pred)
    return report


def save_predictions(data, predictions, filename):
    """
    Добавление предсказаний к данным и сохранение

    data: датасет для предсказаний
    predictions: результат предсказаний
    filename: название файла для сохранения результата
    """
    data['predictions'] = predictions
    data.to_csv(filename, index=False)
