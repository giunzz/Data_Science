import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

import numpy as np

df = pd.DataFrame({
    "hour": [0, 6, 12, 18, 23],
    "total_calls": [100, 200, 300, 400, 500],
    "category": ["A", "B", "A", "B", "C"]
})


class HourToXY(BaseEstimator, TransformerMixin):
    def __init__(self, period=24):
        self.period = period

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.asarray(X)
        h = X if X.ndim == 1 else X[:, 0]
        h = h.astype(float)
        theta = 2*np.pi*h/self.period
        x = np.cos(theta)
        y = np.sin(theta)
        print(x, y)
        return np.c_[x, y] 

    def get_feature_names_out(self, input_features=None):
        base = (input_features[0] if (input_features is not None and len(input_features))
                else "hour")
        print(base)
        return np.array([f"{base}_x", f"{base}_y"])
HourToXY(period=24)

# Custom transformer của bạn
hour_to_xy = HourToXY(period=24)

# Xác định ColumnTransformer
ct = ColumnTransformer(
    transformers=[
        ("hour_cyclical", hour_to_xy, ["hour"]),            # xử lý cột hour bằng HourToXY
        ("scale_numeric", StandardScaler(), ["total_calls"]),  # scale cột số
        ("encode_cat", OneHotEncoder(), ["category"])       # one-hot cho cột phân loại
    ],
    remainder="drop"  # bỏ cột khác nếu chưa định nghĩa
)

# Cho vào pipeline (nếu muốn thêm bước model sau này)
pipeline = Pipeline([
    ("transform", ct)
])

# Fit + transform
X_transformed = pipeline.fit_transform(df)
print(X_transformed.toarray() if hasattr(X_transformed, "toarray") else X_transformed)
