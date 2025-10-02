Cho dữ liệu trong file ‘clean_feature.csv”


1>  0.5 điểm

Viết chương trình con thực hiện công việc sau: ứng với thời điểm t cho trước và một khoảng thời gian delta_t, hãy rút trích đặc trưng cho khoảng thời gian từ [t-delta , t].

Các đặc trưng bao gồm: [mean_cound, mean_pass, data, time] *12, DoW, HiD

 

0.5 điểm

Label cho mỗi thời gian t là trạng thái có lỗi/ ko có lỗi của 2 tiếng sau đó.

 

2> 1 điểm 

Hãy chuẩn bị dữ liệu cho bài toán này theo các bước như sau: Loại bỏ các dữ liệu bị trùng.

Gọi B và E là thời điểm bắt đầu và thời điểm kết thúc của dữ liệu.

Dữ liệu 3 tháng cuối được dùng làm dữ liệu test - Dữ liệu còn lại làm dữ liệu train.

Các dữ liệu train- val được chia ngẫu nhiên theo tỷ lệ 70-30

 

3> 2 điểm

Xử lý dữ liệu theo các bước như sau:

[mean_cound, mean_pass] *12 sẽ được xử lý theo cùng một cách

data *12 sẽ được xử lý theo cùng một cách

time *12  sẽ được xử lý theo cùng một cách

HiD sẽ xử lý dựa theo kỹ thuật embedding với số đặc trưng là 2.

DoW không cần xử lý

Lưu ý, các phép xử lý phải được tuỳ biến và đóng gói thành một khối duy nhất theo quy chuẩn của class columntransform và thư viện sklearn

 

4> 2 điểm

 

Sử dụng thuật toán giảm chiều dữ liệu để giảm chiều dữ liệu cho đặc trưng

 [mean_cound, mean_pass, data, time] *12 sao cho lượng thông tin giữ lại là 95%

Các đặc trưng DoW, HiD giữ nguyên

 

5> 2 điểm

Xây dựng pipeline theo cấu trúc [ Tiền xử lý, giảm chiều dữ liêu, bộ phân loại ]

Trong đó Tiền xử lý là khối được định nghĩa ở các bước 3-4

giảm chiều dữ liệu là mô hình PCA

Bộ phân loại là SVC

 

6> 2 điểm

Tiến hành lựa chọn mô hình tốt nhất bằng cách sử dụng grid search

 

PCA sẽ thay đổi số lượng các feature được giữ lại

SVC sẽ thay đổi các kernel và tham số điều khiển băng thông của kernel