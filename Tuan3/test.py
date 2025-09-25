import pandas as pd
from datetime import timedelta

def load_data(path="clean_feature.csv"):
    df = pd.read_csv(path)
    # Chuẩn hoá thời gian: Day (date) + hour (giờ) -> timestamp
    df["Day"] = pd.to_datetime(df["Day"], errors="coerce")
    df = df.dropna(subset=["Day"])        # loại bỏ bản ghi lỗi ngày tháng nếu có
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    df = df.dropna(subset=["hour"])
    df["hour"] = df["hour"].astype(int)
    df["timestamp"] = df["Day"] + pd.to_timedelta(df["hour"], unit="h")
    return df

def query_events_T_minus_2_to_T(df, T_str):
    """
    Lọc tất cả sự kiện xảy ra trong khoảng (T-2h, T] theo timestamp đã ghép từ Day + hour.
    T_str ví dụ: '2022-01-01 10:00' hoặc '2022-01-01T10'
    """
    T = pd.to_datetime(T_str)
    start = T - timedelta(hours=2)

    # Lọc khoảng thời gian (start, T] — nếu muốn bao gồm cả start thì đổi thành >=
    mask = (df["timestamp"] > start) & (df["timestamp"] <= T)
    result = df.loc[mask].copy()

    # Sắp xếp cho dễ xem
    result = result.sort_values(["timestamp", "ServiceID"]).reset_index(drop=True)
    return result

if __name__ == "__main__":
    # 1) Đọc dữ liệu
    df = load_data("clean_feature.csv")

    # 2) (Tuỳ chọn) làm sạch cơ bản trước khi truy vấn
    df = df.drop_duplicates()  # loại bản ghi trùng nếu có

    # 3) Truy vấn ví dụ với T
    T = "2022-01-01 10:00"  # đổi thành thời điểm bạn muốn
    events = query_events_T_minus_2_to_T(df, T)

    print(f"Số sự kiện trong khoảng (T-2h, T] với T = {T}: {len(events)}")
    print(events.head(20))

    # (Tuỳ chọn) Lưu kết quả
    # events.to_csv("events_T_minus_2_to_T.csv", index=False)
