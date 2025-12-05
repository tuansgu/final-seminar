import streamlit as st
import torch 
import sqlite3 
from datetime import datetime
from transformers import pipeline

# ==========================================
# PHẦN 1: CORE ENGINE (DATABASE & LƯU TRỮ)
# ==========================================

def init_db():
    """Khởi tạo database chuẩn theo cấu trúc bảng sentiments"""
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(text, sentiment):
    """Lưu kết quả phân loại vào SQLite."""
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)', 
              (text, sentiment, timestamp))
    conn.commit()
    conn.close()

def get_history():
    """Lấy dữ liệu hiển thị (Giới hạn 50 dòng)."""
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('SELECT timestamp, text, sentiment FROM sentiments ORDER BY timestamp DESC LIMIT 50')
    data = c.fetchall()
    conn.close()
    return data

# ==========================================
# PHẦN 2: AI PIPELINE (CÁC COMPONENT XỬ LÝ)
# ==========================================

@st.cache_resource
def load_model():
    print("Đang tải mô hình...")
    return pipeline("sentiment-analysis", model="wonrax/phobert-base-vietnamese-sentiment")

try:
    classifier = load_model()
except Exception as e:
    st.error(f"LỖI TẢI MÔ HÌNH: {e}")
    st.stop()

# --- Component 1: Tiền xử lý ---
def preprocess_text(text):
    if not text:
        return ""
    return text.strip()

# --- Component 2 & 3: Phân loại & Hợp nhất ---
def analyze_sentiment(raw_text):
    """
    Hàm xử lý chính:
    1. Kiểm tra hợp lệ (Validation).
    2. Gọi Model.
    3. Trả về Dictionary hoặc Lỗi.
    """
    # 1. Preprocessing
    clean_text = preprocess_text(raw_text)
    
    # === SỬA ĐỔI: Validation chuẩn theo ảnh yêu cầu ===
    # Yêu cầu: Nếu < 5 ký tự hoặc rỗng -> Báo lỗi "Câu không hợp lệ, thử lại"
    if len(clean_text) < 5:
        return {"error": "Câu không hợp lệ, thử lại"}

    # 2. Sentiment Analysis
    try:
        result = classifier(clean_text)
        label = result[0]['label']
        score = result[0]['score']

        sentiment_map = {
            "POS": "POSITIVE",
            "NEG": "NEGATIVE",
            "NEU": "NEUTRAL"
        }
        sentiment = sentiment_map.get(label, "UNKNOWN")
        
        # 3. Output Dictionary (Theo yêu cầu: {text, sentiment})
        return {
            "text": clean_text,
            "sentiment": sentiment,
            "score": score,
            "error": None
        }
    except Exception as e:
        # Trường hợp lỗi Pipeline cũng báo câu này theo yêu cầu
        return {"error": "Câu không hợp lệ, thử lại (Lỗi hệ thống)"}

# ==========================================
# PHẦN 3: GIAO DIỆN NGƯỜI DÙNG (UI)
# ==========================================

st.set_page_config(page_title="Trợ lý Cảm xúc", layout="wide")
st.title("🤖 Trợ lý Phân loại Cảm xúc (Transformer)")

init_db()

col1, col2 = st.columns([1, 1])

# --- Cột Trái: Nhập liệu ---
with col1:
    st.subheader("📝 Nhập liệu")
    user_input = st.text_input("Nhập câu tiếng Việt:", placeholder="Ví dụ: Hôm nay tôi rất vui")

    if st.button("Phân loại & Lưu", type="primary"): 
        if user_input:
            with st.spinner("Đang xử lý qua Pipeline..."):
                result_dict = analyze_sentiment(user_input)
                
                # === HIỂN THỊ LỖI (POP-UP) ===
                if result_dict.get("error"):
                    # st.error hiện khung đỏ, st.toast hiện pop-up nhỏ
                    st.error(f"⚠️ {result_dict['error']}") 
                    st.toast(result_dict['error'], icon="❌") # Thêm cái này cho chuẩn "pop-up"
                else:
                    # Hiển thị kết quả
                    sentiment = result_dict['sentiment']
                    score = result_dict['score']
                    
                    if sentiment == "POSITIVE":
                        st.success(f"Kết quả: {sentiment} (Tin cậy: {score:.2%})")
                    elif sentiment == "NEGATIVE":
                        st.error(f"Kết quả: {sentiment} (Tin cậy: {score:.2%})")
                    else:
                        st.info(f"Kết quả: {sentiment} (Tin cậy: {score:.2%})")

                    # Lưu vào DB và hiển thị
                    save_to_db(result_dict['text'], sentiment)
                    st.toast("Đã lưu vào hệ thống!", icon="✅")
        else:
            st.warning("Vui lòng nhập nội dung.")

# --- Cột Phải: Lịch sử ---
with col2:
    st.subheader("🗂️ Lịch sử Phân loại")
    if st.button("Tải lại danh sách"):
        st.rerun()
        
    history_data = get_history()
    
    if history_data:
        import pandas as pd
        df = pd.DataFrame(history_data, columns=["Thời gian", "Nội dung", "Cảm xúc"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu lịch sử.")