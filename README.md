# RSA Learning Lab

Ứng dụng Streamlit mô phỏng và minh họa thuật toán mã hóa công khai RSA,
được xây dựng theo bản thảo phân công module của học phần Mật mã học cơ sở.

## Chức năng

- Phần **Lý thuyết RSA** gồm khái niệm, nền tảng toán học, quy trình tạo
  khóa, mã hóa, giải mã, Square-and-Multiply và lưu ý an toàn.
- Phần **Mô phỏng từng bước** đi qua 10 bước từ kiểm tra `p`, `q` đến
  đối chiếu thông điệp sau giải mã.
- Phần **Mã Hóa, Giải Mã** cho phép chọn thao tác mã hóa hoặc giải mã, nhập
  văn bản/bản mã, xem kết quả đầu ra và các byte trung gian.
- Hỗ trợ hai chế độ: nhập thông điệp số và nhập văn bản UTF-8.
- Hiển thị bảng Euclid mở rộng `r = s·phi(n) + t·e`.
- Hiển thị đầy đủ trạng thái từng vòng của thuật toán Square-and-Multiply.
- Có ví dụ dễ học, ví dụ trung bình và bài tập tự luyện.

## Chạy bằng Docker

Yêu cầu máy đã cài Docker Desktop hoặc Docker Engine có Docker Compose.

```powershell
cd D:\RSA_Simulator_Web
docker compose up --build -d
```

Mở ứng dụng tại:

```text
http://localhost:8501
```

Kiểm tra trạng thái:

```powershell
docker compose ps
docker compose logs -f rsa-app
```

Dừng ứng dụng:

```powershell
docker compose down
```

Build và chạy không dùng Compose:

```powershell
docker build -t rsa-learning-lab .
docker run --name rsa-learning-lab -p 8501:8501 rsa-learning-lab
```

## Chạy trực tiếp bằng Python

```powershell
cd D:\RSA_Simulator_Web
.\run_app.ps1
```

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Lưu ý an toàn

Ứng dụng dùng số nguyên tố nhỏ và mã hóa trực tiếp từng byte để phục vụ học tập.
RSA trong thực tế cần khóa lớn, thư viện mật mã đã được kiểm chứng và cơ chế đệm
an toàn như OAEP.
