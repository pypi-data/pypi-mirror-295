from sklearn.cluster import DBSCAN
import numpy as np


def dbscan(X, eps=0.5, min_samples=5, metric='euclidean'):
    """
    Выполняет кластеризацию DBSCAN на входных данных.
    
    Параметры:
    X : array-like, shape (n_samples, n_features)
        Входные данные для кластеризации.
    eps : float, optional (default=0.5)
        Максимальное расстояние между двумя образцами для их рассмотрения как соседей.
    min_samples : int, optional (default=5)
        Минимальное количество образцов в окрестности для основных точек.
    metric : string, or callable, optional (default='euclidean')
        Метрика для вычисления расстояния между экземплярами в наборе данных.
    
    Возвращает:
    labels : array, shape (n_samples,)
        Метки кластеров для каждой точки в наборе данных.
    n_clusters : int
        Количество кластеров, найденных алгоритмом.
    """
    # Создаем и применяем модель DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    labels = dbscan.fit_predict(X)
    
    # Определяем количество кластеров
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print("Кол-во кластеров:", n_clusters,"\n")
    
    return labels 
