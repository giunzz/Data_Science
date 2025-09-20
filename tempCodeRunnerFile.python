# %%
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# %% [markdown]
# ## Format mẫu
# - Câu 1: Ứng với một thời gian cho trước, hãy rút trích đặc trưng cho mẫu….
# Tổ chức thành chương trình con 
# - Câu 2: Viết chương trình chuẩn bị bộ dữ liệu M hàng và N cột, trong đó Các cột là các đặc trưng như sau:
# - Câu 3: Chia dữ liệu thành tập train/val/ test theo quy tắc …..
# - Câu 4: Các đặc trưng sẽ được xử lý theo quy tắc …. . Hãy xây dựng chương trình định nghĩa đối tượng CoumnTransfor để thực hiện viẹc tiền xử lý dữ liệu
# - Câu 5: Thực hiện phân loại với Pipeline định nghĩa như sau. Hãy xác định những tham số điều khiển nào cần tinh chỉnh
# - Câu 6: Huấn luyện và lựa chọn mô hình tốt nhất bằng Grid search từ dữ liệu train / val
# - Câu 7: Đánh giá mô hình dựa vào dữ liệu test
# ## Đề mẫu
# - Câu 1: Cho thời điểm t (tính theo đơn vị giờ), hãy truy vấn các dữ liệu trong khoảng thời gian từ t - T đến t, trong đó T là giá trị đã biết, tính bằng giờ.
# - Câu 2: Giả sử M là số thời điểm (t) có thể lấy được trong bộ dữ liệu và N là số dịch vụ, hãy tạo một ma trận có kích thước M * (4 * N) chứa các đặc trưng đã rút trích ở câu 5 cho mỗi dịch vụ: 
#     5. Rút Trích Các Đặc Trưng Từ Mỗi Nhóm
#     Với mỗi nhóm dịch vụ, rút trích các đặc trưng sau:
#     
#     a. Tổng số lần gọi (Total Calls)
#     
#     b. Tổng số lần gọi thành công (Successful Calls)
#     
#     c. Trị trung bình thời gian thực thi (Average Execution Time)
#     
#     d. Trị trung bình dữ liệu sử dụng (Average Data Usage)
#     
#     datetime chia hour và day
# 
# - Câu 3: Chia dữ liệu thành tập train/val/ test theo quy tắc (nếu dự đoán phải dùng time series split, ngược lại train test split). Từ việc xây dựng chương trình định nghĩa đối tượng CoumnTransfor để thực hiện viẹc tiền xử lý dữ liệu với việc embeding hour theo (x,y, hình tròn để tìm khoảng cách) còn day sẽ dùng one hot encoder 
# 
# - Câu 5: Thực hiện phân loại với Pipeline định nghĩa như sau. Hãy xác định những tham số điều khiển nào cần tinh chỉnh (học giám sát)
# - Câu 6: Huấn luyện và lựa chọn mô hình tốt nhất bằng Grid search từ dữ liệu train / val
# - Câu 7: Đánh giá mô hình dựa vào dữ liệu test
# 

# %%
df = pd.read_csv("clean_feature.csv")
df = df.dropna()
df = df.drop_duplicates()
df["datetime"] = pd.to_datetime(df["Day"]) + pd.to_timedelta(df["hour"], unit="h")
print(df["ServiceID"].unique().shape)  


# %%
def query_interval(df, t_datetime, T):
    start = t_datetime - pd.Timedelta(hours=T)
    return df[(df["datetime"] >= start) & (df["datetime"] <= t_datetime)]


# %%
#query
t = pd.to_datetime("2023-07-27 18:00:00")
result = query_interval(df, t, 12)
result = result.sort_index()
print(result.shape)

# %%
#groupby
features = result.groupby(["datetime", "ServiceID"]).agg(
        total_calls=("count", "sum"), # a> Tổng số lần gọi
        total_success=("passed", "sum"), # b> Tổng số lần gọi thành công
        mean_exec_time=("period", "mean"), # c> Trị trung bình thời gian thực thi
        mean_data_usage=("data", "mean") # d> Trị trung bình dữ liệu sử dụng
        
    )
matrix = features.unstack(level="ServiceID", fill_value=0)
matrix = matrix.sort_index(axis=1, level=1)
matrix.to_csv("feature.csv", index=False)
matrix

# %%
same_all = (matrix["total_calls"] == matrix["total_success"]).all(axis=1)  
matrix["label"] = same_all.astype(int)
print(matrix["label"].value_counts())
matrix

# %%
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# %%
trans_matrix = matrix.copy()
trans_matrix["hour"] = trans_matrix.index.hour
trans_matrix["day"] = trans_matrix.index.day
trans_matrix.to_csv("feature.csv", index=False) 
trans_matrix

# %%
class HourToXY(BaseEstimator, TransformerMixin):
    def __init__(self, period=24):
        self.period = period

    def fit(self, X, y=None):
        return self  # không cần học gì cả

    def transform(self, X):
        h = X.iloc[:, 0]  # giả sử X chỉ có một cột giờ
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
    

# %%
try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
hour_col = trans_matrix["hour"].values.astype(int)  

day_col = trans_matrix["day"].values.astype(int)  
print(type(hour_col), getattr(hour_col, "shape", None))
print(type(day_col), getattr(day_col, "shape", None))
hour_col

# %%


hour_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("xy",  HourToXY(period=24)),
])
hour_pipe    

# %%
day_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("ohe", ohe),
])
day_pipe


# %%

pre = ColumnTransformer(
        transformers = [
        ("hour_xy", hour_pipe, [hour_col]),
        ("day_ohe", day_pipe,  [day_col]),
    ],
    remainder="drop"  # không mang theo cột ngoài danh sách
)
pre

# %%
from sklearn.model_selection import TimeSeriesSplit
def Split_data(df,n_splits: int = 5):
    X = df.drop(columns=["label"])  
    y = df["label"].values.astype(int)  
    print(y)
    
    print("Features shape:", X.shape)
    print("Labels shape:", y.shape)

    tscv = TimeSeriesSplit(n_splits=n_splits)
    folds = list(tscv.split(X))

    train_idx = folds[-2][0]
    val_idx   = folds[-2][1]
    test_idx  = folds[-1][1]

    X_train, y_train = X.iloc[train_idx], y[train_idx]
    X_val,   y_val   = X.iloc[val_idx], y[val_idx]
    X_test,  y_test  = X.iloc[test_idx],  y[test_idx]

    print(f"Split (n_splits={n_splits}) -> "
        f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

    return X_train, y_train, X_val, y_val, X_test, y_test
X_train, y_train, X_val, y_val, X_test, y_test = Split_data(matrix)


# %%
print(X_train.shape)
print(y_train.shape)
print("Matrix shape:", matrix.shape)
print(type(X_train), getattr(X_train, "shape", None))
print(type(y_train), getattr(y_train, "shape", None))


# %%
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipe = Pipeline([
    ("prep",  pre),                            
    ("scale", StandardScaler()), # vẽ chart xem độ tương quan (nếu dữ liệu quá nhiều noise) | robust scaler: xem dữ liệu
    ("svm",   SVC(probability=True, class_weight="balanced"))
])

pipe


# %%
param_grid = [
    {"svm__kernel": ["rbf"],    "svm__C": [0.1, 1, 10], "svm__gamma": ["scale", 0.01, 0.1, 1]},
    {"svm__kernel": ["linear"], "svm__C": [0.1, 1, 10]},
]
grid = GridSearchCV(pipe, param_grid, cv=3, scoring="accuracy", n_jobs=-1, verbose=2)
grid.fit(X_train, y_train) 

#Xgboost 
print("Best params:", grid.best_params_)
print("Best cross-val acc:", grid.best_score_)


# %%
best_pipe = grid.best_estimator_
best_pipe.fit(X_train, y_train)
print("Test score:", best_pipe.score(X_test, y_test))
print("Thực tế:", y_test.iloc[:5].values)
print("Dự đoán:", best_pipe.predict(X_test[:5]))
# chú trọng accuracy (giải thích lý do)


