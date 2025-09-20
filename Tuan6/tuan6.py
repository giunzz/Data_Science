import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.svm import SVC

# %% Read Data
df = pd.read_csv("C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Tuan6\\clean_feature.csv")
df = df.dropna()
df = df.drop_duplicates()
df["datetime"] = pd.to_datetime(df["Day"]) + pd.to_timedelta(df["hour"], unit="h")
print(df["ServiceID"].unique().shape)  

# %% Query Function
def query_interval(df, t_datetime, T):
    start = t_datetime - pd.Timedelta(hours=T)
    return df[(df["datetime"] >= start) & (df["datetime"] <= t_datetime)]

# %% Query
t = pd.to_datetime("2023-07-27 18:00:00")
result = query_interval(df, t, 12)
result = result.sort_index()
print(result.shape)

# %% Groupby and aggregation
features = result.groupby(["datetime", "ServiceID"]).agg(
        total_calls=("count", "sum"),  # a> Total call count
        total_success=("passed", "sum"),  # b> Total successful calls
        mean_exec_time=("period", "mean"),  # c> Mean execution time
        mean_data_usage=("data", "mean")  # d> Mean data usage
    )
matrix = features.unstack(level="ServiceID", fill_value=0)
matrix = matrix.sort_index(axis=1, level=1)
matrix.to_csv("feature.csv", index=False)
matrix

# %% Adding label column
same_all = (matrix["total_calls"] == matrix["total_success"]).all(axis=1)  
matrix["label"] = same_all.astype(int)
print(matrix["label"].value_counts())
matrix

# %% Add 'hour' and 'day' columns
trans_matrix = matrix.copy()
trans_matrix["hour"] = trans_matrix.index.hour
trans_matrix["day"] = trans_matrix.index.day
trans_matrix.to_csv("feature.csv", index=False) 
trans_matrix

# %% HourToXY Transformer
class HourToXY(BaseEstimator, TransformerMixin):
    def __init__(self, period=24):
        self.period = period

    def fit(self, X, y=None):
        return self  # No fitting needed

    def transform(self, X):
        if 'hour' not in X.columns:
            raise ValueError("DataFrame must contain 'hour' column")
        h = X["hour"].values  # Assume X has an 'hour' column
        theta = 2 * np.pi * h / self.period
        x = np.cos(theta)
        y = np.sin(theta)
        return np.c_[x, y]
    
    def get_feature_names_out(self, input_features=None):   
        base = (input_features[0] if (input_features is not None and len(input_features)) else "hour")
        return np.array([f"{base}_x", f"{base}_y"])

HourToXY(period=24)

# %% OneHotEncoder Setup
try:
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
except TypeError:
    ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)

hour_col = trans_matrix["hour"].astype(int)
day_col = trans_matrix["day"].astype(int)

# %% Pipeline Setup
hour_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("xy",  HourToXY(period=24)),
])

day_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("ohe", ohe),
])

# %% ColumnTransformer Setup
pre = ColumnTransformer(
    transformers = [
        ("hour_xy", hour_pipe, hour_col),
        ("day_ohe", day_pipe, day_col),
    ],
    remainder="drop"  # Drop columns not in the list
)

# %% Split Data Function
def Split_data(df, n_splits: int = 5):
    X = df.drop(columns=["label"])  
    y = df["label"].astype(int)  
    
    tscv = TimeSeriesSplit(n_splits=n_splits)
    folds = list(tscv.split(X))

    train_idx = folds[-2][0]
    val_idx   = folds[-2][1]
    test_idx  = folds[-1][1]

    X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
    X_val,   y_val   = X.iloc[val_idx], y.iloc[val_idx]
    X_test,  y_test  = X.iloc[test_idx], y.iloc[test_idx]

    return X_train, y_train, X_val, y_val, X_test, y_test

X_train, y_train, X_val, y_val, X_test, y_test = Split_data(matrix)

# %% GridSearchCV
pipe = Pipeline([
    ("prep",  pre),                            
    ("scale", StandardScaler()),  # Scaling for correlation if data has too much noise
    ("svm",   SVC(probability=True, class_weight="balanced"))
])

param_grid = [
    {"svm__kernel": ["rbf"], "svm__C": [0.1, 1, 10], "svm__gamma": ["scale", 0.01, 0.1, 1]},
    {"svm__kernel": ["linear"], "svm__C": [0.1, 1, 10]},
]

grid = GridSearchCV(pipe, param_grid, cv=3, scoring="accuracy", n_jobs=-1, verbose=2)
grid.fit(X_train, y_train) 

# %% Model Evaluation
best_pipe = grid.best_estimator_
best_pipe.fit(X_train, y_train)
print("Test score:", best_pipe.score(X_test, y_test))
print("Thực tế:", y_test.iloc[:5].values)
print("Dự đoán:", best_pipe.predict(X_test[:5]))
