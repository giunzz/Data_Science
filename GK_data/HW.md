### Cho dữ liệu trong file ‘clean_feature.csv”

-> khai báo bảng (dùng pandas)
+) đọc cheatshaeet xem thuộc tính có sẵn (kích thích, sắp idex )

->  lấy file data -> xem sheat -> in ra các thông tin thuộc mong muốn

-> Tìm hiểu dataframe , series, numpy

| Thuộc tính       | Series                   | DataFrame                       |
| ---------------numpy - | ------------------------ | ------------------------------- |
| Chiều            | 1 chiều                  | 2 chiều                         |
| Dạng dữ liệu     | Một cột                  | Nhiều cột                       |
| Index            | Có                       | Có cho cả dòng (row) và cột     |
| Truy cập dữ liệu | `s["a"]`                 | `df["Age"][0]` hoặc `df.loc[0]` |
| Biểu diễn        | `[10, 20, 30]` với index | Bảng có dòng & cột              |



1>  0.5 điểm

Viết chương trình con thực hiện công việc sau: ứng với thời điểm t cho trước và một khoảng thời gian delta_t, hãy rút trích đặc trưng cho khoảng thời gian từ [t-delta , t]. 
-> hỏi delta: **tính theo tháng, ngày**, mình delta theo giờ 

Các đặc trưng bao gồm: [mean_cound, mean_pass, data, time]*12, DoW, HiD (hour in Day)
-> thay đổi mean, sum, ...
 
input: dataframe (từ 1 file csv): bảng có m hàng n cột , t: mốc thời gian mình chọn
process: truy vấn theo khoảng thời gian [t - delta, t] với t là thời điểm truy vấn và delta : giờ 
output: dataframe truy vấn (m hàng n cột)


0.5 điểm
Label (gán nhãn) cho mỗi thời gian t là trạng thái có lỗi/ ko có lỗi của 2 tiếng sau đó. 
input: thời điểm t cho trước cí ví dụ cho t = 2023-06-08 3:00:00 -> 2023-06-08 4:00:00, 2023-06-08 5:00:00

process: Tìm vị trí datetime cần gán -> gán nhán trạng thái lỗi (dựa count với passed)

output: 2 hàng 2 cột 
datetime             label 
2023-06-08 4:00:00   0/1
2023-06-08 5:00:00   0/1


 2> 1 điểm 

Hãy chuẩn bị dữ liệu cho bài toán này theo các bước như sau: Loại bỏ các dữ liệu bị trùng: . toàn bộ dữ liệu -> lấy dữ liệu theo tháng query từ câu 1

Gọi B và E là thời điểm bắt đầu và thời điểm kết thúc của dữ liệu.

Dữ liệu 3 tháng cuối được dùng làm dữ liệu test - Dữ liệu còn lại làm dữ liệu train.  -> cắt theo row 

Các dữ liệu train- val được chia ngẫu nhiên theo tỷ lệ 70-30 (modify)
-> train_test_split

 (Train , Val, Test: khasc nhau nhuư thế nào)

3> 2 điểm
column transform 
transformer = [("tên", đối tượng(class) transformer, feature(cột trong df))]
Tìm hiểu một số cách xử lý (đối tượng transformer: hàm tự code như HourToXy)

Xử lý dữ liệu theo các bước như sau:

[mean_count, mean_pass] *12 sẽ được xử lý theo cùng một cách

data *12 sẽ được xử lý theo cùng một cách

time *12  sẽ được xử lý theo cùng một cách 

### period trong df -> mean = time 

HiD sẽ xử lý dựa theo kỹ thuật embedding với số đặc trưng là 2. (Oxy)
DoW không cần xử lý

Lưu ý, các phép xử lý phải được tuỳ biến và đóng gói thành một khối duy nhất theo quy chuẩn của class columntransform và thư viện sklearn

 

4> 2 điểm

 
PCA (giảm chiều nhưng giữ một số feature )
Sử dụng thuật toán **giảm chiều dữ liệu** để giảm chiều dữ liệu cho đặc trưng

 [mean_cound, mean_pass, data, time] *12 sao cho lượng thông tin giữ lại là 95%

Các đặc trưng DoW, HiD giữ nguyên

 
 Input 
 nx (4*12 + 2): bảng gồm n hàng 50 cột trong đó 48 cột giữ lại 95%

 processs : vẽ biểu đồ phương sai với từng components 
 Chọn PCA(n_components=6, random_state=42)

 output: bảng gồn n hàng n_components + 2 ột

5> 2 điểm
pieline 
Xây dựng pipeline theo cấu trúc [ Tiền xử lý, giảm chiều dữ liêu, bộ phân loại ]

pipe = Pipeline([
    ("transform", ct), #tiền xử lý
    ("pca", PCA(n_components=6, random_state=42)), #giảm chiều dữ liệu
    ("svm", SVC(probability=True, class_weight="balanced")) #bộ phân loại
])

=) Tìm hiểu về các bộ phân loại và parameter của nó

Trong đó Tiền xử lý là khối được định nghĩa ở các bước 3-4
giảm chiều dữ liệu là mô hình PCA
Bộ phân loại là SVC (hoặc chỉnh sửa tham số hoặc đổi bộ phân loại)

 

6> 2 điểm

Tiến hành lựa chọn mô hình tốt nhất bằng cách sử dụng grid search

+) Tìm hiểu thông số (có thể nhiều hoen)

param_grid = {
    'pca__n_components': [5, 10, 20, 0.95], #PCA sẽ thay đổi số lượng các feature được giữ lại
    'svm__C': [0.1, 1, 10],
    'svm__gamma': ['scale', 0.01, 0.1],
    'svm__kernel': ['rbf'] #SVC sẽ thay đổi các kernel và tham số điều khiển băng thông của kernel
}

+) GridSearchCV: tìm hiểu parameter
 ---------------------------------------------------------
 Thứ 7 tmr: họp online 9h tối nhúng (gộp code)
 Chủ nhật: họp nhúng ở nhà t (pcung, gộp code)
 --------------------------------
 deadline tối 10h30 thứ 2 : Tìm hiểu + demo code (từng đứa) data sic 
 Thuyết trình : Dương (lý thuyết), Bình , Dung (demo code)

 esp -> Mqtt : Dương (pulisher, subrisber)

trưa thứ 2 29/9 1h chiều: họp IoT 
 2/10: báo cáo slide 

