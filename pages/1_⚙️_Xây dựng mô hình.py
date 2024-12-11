import pandas as pd
import streamlit as st
import plotly.express as px

# ================================== DATA ===================================
# Đọc data đánh giá
danh_gia = pd.read_csv('data/DATA - FINAL/Danh_gia_clean.csv', sep=';')

# ================================== STREAMLIT ===================================
st.set_page_config(
    page_title="Xây dựng mô hình",
    page_icon="⚙️",
    layout = "wide"
)

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center; /* Căn giữa */
        font-family: 'Arial', sans-serif; /* Đổi font chữ (hoặc thay bằng font khác) */
        font-size: 4em; /* Kích thước chữ */
        font-weight: bold; /* Đậm chữ */
    }
    </style>
    <h1 class="centered-title">👋 Sentiment Analysis! 👋</h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("👋 Sentiment Analysis 👋")

# Đường link của ảnh
image_url = 'https://tamancosmetics.vn/wp-content/uploads/2024/01/hasaki.png'
# Hiển thị ảnh từ đường link
# Căn giữa ảnh và thay đổi kích thước
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="{image_url}" width="900">
    </div>
    """, 
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
    .intro-title {
        font-weight: bold; /* Làm đậm chữ */
        font-size: 2em; /* Kích thước chữ */
        margin-bottom: 5px; /* Khoảng cách dưới tiêu đề */
        display: flex; /* Dùng flex để căn icon và tiêu đề cùng dòng */
        align-items: center; /* Căn icon theo trục dọc */
    }
    .intro-icon {
        margin-right: 8px; /* Khoảng cách giữa icon và chữ */
        font-size: 2em; /* Kích thước icon */
    }
    </style>
    <div class="intro-title">
        <span class="intro-icon">⚙️</span> <!-- Icon -->
        Xây dựng mô hình
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.write("""#### Thành viên thực hiện:\n
                 Trang Thư Đình &
                 Nguyễn Quang Khải""")
st.sidebar.write("""#### Giảng viên hướng dẫn:\n
                Khuất Thùy Phương""")
st.sidebar.write("""#### Thời gian thực hiện: 7/12/2024""")

st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 10px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.8em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>1. Dữ liệu:</strong>
        </p>
        """,
        unsafe_allow_html=True)
st.dataframe(danh_gia[['noi_dung_binh_luan', 'so_sao']].head(3))
st.dataframe(danh_gia[['noi_dung_binh_luan', 'so_sao']].tail(3)) 

st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 10px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.8em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>2. Thống kê số sao và các nhãn:</strong>
        </p>
        """,
        unsafe_allow_html=True)
# Chọn cột danh mục cần hiển thị
cat_cols = ['so_sao', 'label']

st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 15px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>🌟 Theo số sao:</strong>
        </p>
        """,
        unsafe_allow_html=True)
# Tạo biểu đồ cho cột `so_sao` với màu gradient từ đỏ đến xanh lá cây
so_sao_counts = danh_gia['so_sao'].value_counts().reset_index()
so_sao_counts.columns = ['so_sao', 'count']
fig_so_sao = px.bar(
    so_sao_counts,
    x='so_sao',
    y='count',
    text='count',
    labels={'so_sao': 'Số sao', 'count': 'Tần suất'},
    color='so_sao',  # Áp dụng màu theo giá trị
    color_continuous_scale=px.colors.diverging.RdYlGn  # Gradient từ đỏ (ít) đến xanh (nhiều)
)
st.plotly_chart(fig_so_sao, use_container_width=True)

st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 15px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>😊 Theo nhãn: tích cực - bình thường - tiêu cực:</strong>
        </p>
        """,
        unsafe_allow_html=True)
# Tạo biểu đồ cho cột `label` với màu xanh cho `positive`
label_counts = danh_gia['label'].value_counts().reset_index()
label_counts.columns = ['label', 'count']
fig_label = px.bar(
    label_counts,
    x='label',
    y='count',
    text='count',
    labels={'label': 'Nhãn', 'count': 'Tần suất'},
    color='label',  # Tùy chỉnh màu theo nhãn
    color_discrete_map={'positive': '#008000', 'negative': '#FF0000', 'neutral': '#808080'}  # Xanh, đỏ, xám
)
st.plotly_chart(fig_label, use_container_width=True)

st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 10px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.8em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>3. Đánh giá kết quả mô hình:</strong>
        </p>
        """,
        unsafe_allow_html=True)

st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 15px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>📋 Bảng đánh giá chung:</strong>
        </p>
        """,
        unsafe_allow_html=True)
file_path = 'saved_models/model_results.csv'
data = pd.read_csv(file_path, delimiter=",")
# Tìm các cột có giá trị cao nhất
def highlight_max_column(s):
    # Tìm giá trị lớn nhất trong cột
    is_max = s == s.max()
    # Tô màu cho giá trị lớn nhất trong cột
    return ['background-color: yellow' if v else '' for v in is_max]

# Áp dụng hàm highlight_max_column vào từng cột của DataFrame
styled_data = data.style.apply(highlight_max_column, axis=0)
# Hiển thị DataFrame với Streamlit
st.dataframe(styled_data)

st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 15px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>📝 Chi tiết mô hình:</strong>
        </p>
        """,
        unsafe_allow_html=True)
# Tạo menu lựa chọn tab với 3 mô hình
# Tạo 3 cột
col1, col2, col3 = st.columns(3)

# Nội dung cho mỗi mô hình trong từng cột
with col1:
    with st.expander("Gradient Boosting Classifier"):
        # Đọc dữ liệu từ file
        df = pd.read_csv('saved_models/Gradient_Boosting_Classifier_classification_report.csv')
        df_pivot = df.pivot(index='Label', columns='Sub-label', values='Value')
        desired_order = ['negative', 'neutral', 'positive', 'macro avg', 'weighted avg']
        df_pivot = df_pivot.loc[desired_order]
        df_pivot = df_pivot.dropna(axis=1)
        df_pivot = df_pivot[['precision', 'recall', 'f1-score', 'support']]
        st.dataframe(df_pivot)
        st.image('saved_models/Gradient_Boosting_Classifier_confusion_matrix.png', use_container_width=True)


        
with col2:
    with st.expander("Extra Trees Classifier"): 
        df = pd.read_csv('saved_models/Extra_Trees_Classifier_classification_report.csv')
        df_pivot = df.pivot(index='Label', columns='Sub-label', values='Value')
        desired_order = ['negative', 'neutral', 'positive', 'macro avg', 'weighted avg']
        df_pivot = df_pivot.loc[desired_order]
        df_pivot = df_pivot.dropna(axis=1)
        df_pivot = df_pivot[['precision', 'recall', 'f1-score', 'support']]
        st.dataframe(df_pivot)
        st.image('saved_models/Extra_Trees_Classifier_confusion_matrix.png', use_container_width=True)

        
with col3:
    with st.expander("Random Forest Classifier"): 
        df = pd.read_csv('saved_models/Random_Forest_Classifier_classification_report.csv')
        df_pivot = df.pivot(index='Label', columns='Sub-label', values='Value')
        desired_order = ['negative', 'neutral', 'positive', 'macro avg', 'weighted avg']
        df_pivot = df_pivot.loc[desired_order]
        df_pivot = df_pivot.dropna(axis=1)
        df_pivot = df_pivot[['precision', 'recall', 'f1-score', 'support']]
        st.dataframe(df_pivot) 
        st.image('saved_models/Random_Forest_Classifier_confusion_matrix.png', use_container_width=True)


st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 15px; /* Thụt lề đầu dòng */
            margin-left: 10px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.8em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>4. Kết luận:</strong> Chọn mô hình Random Forest
        </p>
        """,
        unsafe_allow_html=True)




    