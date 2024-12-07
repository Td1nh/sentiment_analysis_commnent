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

st.sidebar.write("""#### Thành viên thực hiện:\n
                 Trang Thư Đình
                 Nguyễn Quang Khải""")
st.sidebar.write("""#### Giảng viên hướng dẫn:\n
                Khuất Thùy Phương""")
st.sidebar.write("""#### Thời gian thực hiện: 7/12/2024""")

st.subheader("Xây dựng mô hình")
st.write("##### 1. Dữ liệu")
st.dataframe(danh_gia[['noi_dung_binh_luan_sai_chinh_ta', 'so_sao']].rename(columns={'noi_dung_binh_luan_sai_chinh_ta': 'noi_dung_binh_luan'}).head(3))
st.dataframe(danh_gia[['noi_dung_binh_luan_sai_chinh_ta', 'so_sao']].rename(columns={'noi_dung_binh_luan_sai_chinh_ta': 'noi_dung_binh_luan'}).tail(3)) 

st.write("##### 2. Thống kê số sao và các nhãn")
# Chọn cột danh mục cần hiển thị
cat_cols = ['so_sao', 'label']

# Giao diện với Streamlit
st.write("###### a.Theo số sao")
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

st.write("###### b.Theo nhãn: tích cực - bình thường - tiêu cực")
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

st.write("##### 3. Đánh giá kết quả mô hình")
st.write("###### a. Bảng đánh giá chung")
file_path = 'saved_models/model_results.csv'
data = pd.read_csv(file_path, delimiter=",")
# Tìm các cột có giá trị cao nhất
def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]
# Áp dụng hàm highlight_max vào DataFrame
styled_data = data.style.apply(highlight_max)
# Hiển thị DataFrame với Streamlit
st.dataframe(styled_data)

st.write("###### b. Chi tiết mô hình")
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



st.write("##### 4. Kết luận: Chọn mô hình Random Forest")





    