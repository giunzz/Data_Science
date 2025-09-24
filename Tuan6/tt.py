import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score

# --- Load & xử lý dữ liệu ---

df = pd.read_csv("C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Tuan6\\clean_feature.csv")

df["datetime"] = pd.to_datetime(df["Day"]) + pd.to_timedelta(df["hour"], unit="h")

t = pd.to_datetime("2023-06-08 03:00:00")
result = df[(df["datetime"] >= t - pd.Timedelta(hours=18)) & (df["datetime"] <= t)]

features = result.groupby(["datetime", "ServiceID"]).agg(
    total_calls=("count", "sum"),
    total_success=("passed", "sum"),
    mean_exec_time=("period", "mean"),
    mean_data_usage=("data", "mean")
)

matrix = features.unstack(level="ServiceID", fill_value=0)
matrix.columns = [
    "_".join([str(c) for c in col if c != ""]) if isinstance(col, tuple) else str(col)
    for col in matrix.columns
]
matrix["label"] = (matrix.filter(like="total_calls").values == matrix.filter(like="total_success").values).all(axis=1).astype(int)

matrix["hour"] = matrix.index.hour
matrix["day"] = matrix.index.dayofweek

# --- Train / Test split ---
split_point = int(len(matrix) * 0.7)
trainval = matrix.iloc[:split_point]
test = matrix.iloc[split_point:]

X = trainval.drop(columns=["label"])
y = trainval["label"]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

X_test = test.drop(columns=["label"])
y_test = test["label"]

# --- Custom transformer HourToXY ---
class HourToXY(BaseEstimator, TransformerMixin):
    def __init__(self, period=24):
        self.period = period
    def fit(self, X, y=None): return self
    def transform(self, X):
        X = np.asarray(X)
        h = X if X.ndim == 1 else X[:, 0]
        theta = 2*np.pi*h/self.period
        return np.c_[np.cos(theta), np.sin(theta)]
    def get_feature_names_out(self, input_features=None):
        base = input_features[0] if input_features else "hour"
        return np.array([f"{base}_x", f"{base}_y"])

hour_to_xy = HourToXY(period=24)

ct = ColumnTransformer(
    transformers=[
        ("hour_to_xy", hour_to_xy, ["hour"]),
        ("onehot_day", OneHotEncoder(handle_unknown="ignore"), ["day"]),
    ],
    remainder="passthrough"
)

# --- Pipeline ---
pipe = Pipeline([
    ("transform", ct),
    ("scale", RobustScaler(with_centering=False)),  # ✅ quan trọng
    ("svm", SVC(probability=True, class_weight="balanced"))
])

# --- GridSearchCV ---
param_grid = {
    'svm__C': [0.1, 1, 10],
    'svm__gamma': ['scale', 0.01, 0.1],
    'svm__kernel': ['rbf']
}

cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

grid = GridSearchCV(pipe, param_grid, cv=cv, scoring="accuracy", 
                    n_jobs=-1, verbose=2)
grid.fit(X_train, y_train)

print("Best params:", grid.best_params_)
print("Best cross-val acc:", grid.best_score_)
