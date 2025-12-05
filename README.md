# TRỢ LÝ PHÂN LOẠI CẢM XÚC TIẾNG VIỆT (VIETNAMESE SENTIMENT ANALYSIS)

---

## 📖 1. Giới thiệu Đồ án
Đây là ứng dụng web được xây dựng nhằm mục đích **phân loại cảm xúc (Sentiment Analysis)** của các câu văn bản tiếng Việt. Hệ thống tự động nhận diện và gán nhãn: **Tích cực (POSITIVE)**, **Tiêu cực (NEGATIVE)**, hoặc **Trung tính (NEUTRAL)**.

**Điểm nổi bật:**
* Sử dụng mô hình học sâu **Transformer (PhoBERT)** tiên tiến.
* Giao diện trực quan bằng **Streamlit**.
* Lưu trữ lịch sử tra cứu vào cơ sở dữ liệu **SQLite** cục bộ.

## 🛠️ 2. Công nghệ sử dụng
* **Ngôn ngữ lập trình:** Python 3.10+
* **Giao diện (Frontend):** Streamlit Framework
* **Mô hình AI (NLP):** Hugging Face Transformers
    * *Model checkpoint:* `wonrax/phobert-base-vietnamese-sentiment`
* **Cơ sở dữ liệu:** SQLite3 (Tích hợp sẵn trong Python)

## 📂 3. Cấu trúc thư mục
SentimentProject/
├── app.py              # Mã nguồn chính (Source code)
├── history.db          # Cơ sở dữ liệu (Tự động tạo khi chạy app)
├── requirements.txt    # Danh sách các thư viện cần thiết
└── README.md           # Tài liệu hướng dẫn sử dụng

## 🚀 4. Hướng dẫn Cài đặt & Vận hành (Quan trọng)

Để chạy được đồ án, vui lòng thực hiện tuần tự **5 bước** sau trong Terminal (Command Prompt) hoặc VS Code:

### Bước 1: Tải mã nguồn về máy
Bạn có thể tải file ZIP hoặc dùng lệnh Git để sao chép dự án về máy:
```bash
git clone [https://github.com/tuansgu/final-seminar.git](https://github.com/tuansgu/final-seminar.git)
cd final-seminar
```
### Bước 2: Cài đặt thư viện phụ thuộc
Chạy lệnh sau để cài đặt các thư viện theo đúng phiên bản đã kiểm thử:
```bash
pip install -r requirements.txt
```
(Lưu ý: Nếu cài thủ công, vui lòng dùng lệnh sau để tránh lỗi xung đột phiên bản: pip install streamlit transformers==4.30.0 torch==2.0.0 numpy==1.26.4 sentencepiece)

### Bước 3: Khắc phục lỗi WinError 1114 (Chỉ dành cho Windows)
Do xung đột thư viện PyTorch với driver hệ thống trên Windows, bạn BẮT BUỘC phải chạy lệnh sau trước khi mở ứng dụng:

DOS

set KMP_DUPLICATE_LIB_OK=TRUE
### Bước 4: Khởi chạy ứng dụng
Gõ lệnh sau để bật máy chủ Streamlit:
```bash
streamlit run app.py
```
Sau khi chạy, trình duyệt web sẽ tự động mở tại địa chỉ: http://localhost:8501. (Lưu ý: Lần chạy đầu tiên sẽ mất vài phút để tải mô hình AI về máy).

## ✨ 5. Các tính năng chính
Phân loại thông minh: Xử lý tốt tiếng Việt có dấu, không dấu, và viết tắt cơ bản.

Lưu trữ lịch sử: Tự động lưu câu hỏi và kết quả vào Database SQLite.

Bảo mật: Code sử dụng kỹ thuật Parameterized Queries để chống tấn công SQL Injection.

Hiệu năng cao:

Sử dụng @st.cache_resource để cache mô hình vào RAM.


Giới hạn hiển thị 50 dòng lịch sử mới nhất để tránh lag giao diện.

