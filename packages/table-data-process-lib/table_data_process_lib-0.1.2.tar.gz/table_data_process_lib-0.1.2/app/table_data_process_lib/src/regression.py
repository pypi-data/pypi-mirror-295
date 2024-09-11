from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from xgboost import XGBRegressor


def linear_regression(X_train, y_train):
    """
    Обучение модели линейной регрессии

    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def polynomial_regression(X_train, y_train, degree=2):
    """
    Обучение модели полиномиальной регрессии

    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    degree: степень полинома
    """
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X_train)
    model = LinearRegression()
    model.fit(X_poly, y_train)
    return model


def xgb_regressor(X_train, y_train, n_estimators=100, learning_rate=0.1, max_depth=3):
    """
    Обучение модели XGBRegressor

    X_train: датасет признаков для обучения
    y_train: данные целевого признака, используемые для обучения
    n_estimators: количество деревьев в ансамбле
    learning_rate: скорость обучения
    max_depth: максимальная глубина деревьев
    """
    model = XGBRegressor(
        objective ='reg:squarederror',
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth
    )
    model.fit(X_train, y_train)
    return model