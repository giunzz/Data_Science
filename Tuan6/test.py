import numpy as np
import pandas as pd

def query_interval(df, t_datetime, T):
    start = t_datetime - pd.Timedelta(hours=T)
    return df[(df["datetime"] >= start) & (df["datetime"] <= t_datetime)]



if __name__ == "__main__":
    df = pd.read_csv("C://Users//ASUS//Documents//GitHub//Data_sceince_ute//Data_Science//Tuan6//clean_feature.csv")
    print(df.iloc[:, 6].unique())  # In ra tất cả các giá trị duy nhất trong cột thứ 6
    df = df.dropna()
    df = df.drop_duplicates() 
    df["datetime"] = pd.to_datetime(df["Day"]) + pd.to_timedelta(df["hour"], unit="h")
    #query
    t = pd.to_datetime("2023-07-24 18:00:00")
    result = query_interval(df, t, 12)
    result = result.sort_index()
    result.to_csv ("feature.csv")  
    # Label dữ liệu
    # same_all = (result["count"] == result["passed"]).all(axis=1)
    # result["label"] = same_all.astype(int)
    # print(result["label"].value_counts())
    # result.to_csv ("feature.csv",index=False))  
    
    
