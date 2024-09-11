import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from app.table_data_process_lib import train_and_evaluate_mlp

df = pd.read_csv('ECG_array_arrow_data.csv', delimiter=';')
X = df.drop(['Healthy Status', 'subject_id', 'study_id', 'cart_id', 'eeg_time ', 'eeg_date '], axis=1)
y = df['Healthy Status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


mlp_model, mlp_accuracy, mlp_report = train_and_evaluate_mlp(
    X_train_scaled, X_test_scaled, y_train, y_test,
    hidden_layer_sizes=(100, 50),  # Пример: два скрытых слоя с 100 и 50 нейронов
    activation='relu',
    alpha=0.001,
    learning_rate_init=0.01,
    max_iter=500
)

print(f"MLP Accuracy: {mlp_accuracy}")
print("MLP Classification Report:")
print(mlp_report)