import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox
from fuzzywuzzy import process
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import os
import numpy as np

# ================================== FUNCTION LIÊN QUAN ===================================
# Tìm từ liên quan
def search_products(searchterm: str):
    if not searchterm:
        return []
    # Tìm các sản phẩm có liên quan
    related_products = process.extractBests(searchterm, products, limit=10, score_cutoff=60)
    return [product for product, score in related_products]

# tìm wordcloud
def generate_wordcloud(text, colormap, title):
    if text:  # Check if text has a value
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=80, colormap=colormap).generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title, fontsize=16)
        plt.axis('off')
        plt.show()
    else:
        # If no text, generate a wordcloud with a default message
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=80, colormap=colormap).generate("không_có_dữ_liệu")
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(title, fontsize=16)
        plt.axis('off')
        plt.show()

# Tìm mã sản phẩm
def find_product_code_and_wordcloud(selected_product, san_pham, danh_gia, save_path):
    ma_sp = san_pham[san_pham['ten_san_pham'] == selected_product]['ma_san_pham'].iloc[0]
    danh_gia_lien_quan = danh_gia[danh_gia['ma_san_pham'] == ma_sp]
    diem_trung_binh = danh_gia[danh_gia['ma_san_pham'] == ma_sp]['so_sao'].mean()
    # Kiểm tra nếu thư mục chưa tồn tại thì tạo mới
    folder = os.path.dirname(save_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # Lọc các bình luận theo từng cảm xúc và xử lý NaN
    pos = ' '.join(danh_gia_lien_quan[
        (danh_gia_lien_quan['label'] == 'positive') & 
        (~danh_gia_lien_quan['noi_dung_binh_luan_processed'].isna())
    ]['noi_dung_binh_luan_processed'])
    neu = ' '.join(danh_gia_lien_quan[
        (danh_gia_lien_quan['label'] == 'neutral') & 
        (~danh_gia_lien_quan['noi_dung_binh_luan_processed'].isna())
    ]['noi_dung_binh_luan_processed'])
    neg = ' '.join(danh_gia_lien_quan[
        (danh_gia_lien_quan['label'] == 'negative') & 
        (~danh_gia_lien_quan['noi_dung_binh_luan_processed'].isna())
    ]['noi_dung_binh_luan_processed'])
    
    # Vẽ wordcloud cho từng cảm xúc nếu dữ liệu không rỗng
    plt.figure(figsize=(18, 6))
    num_subplots = 0

    if pos:
        plt.subplot(1, 3, num_subplots + 1)
        generate_wordcloud(pos, 'Greens', "Positive Sentiments")
        num_subplots += 1

    if neu:
        plt.subplot(1, 3, num_subplots + 1)
        generate_wordcloud(neu, 'Blues', "Neutral Sentiments")
        num_subplots += 1

    if neg:
        plt.subplot(1, 3, num_subplots + 1)
        generate_wordcloud(neg, 'Reds', "Negative Sentiments")
        num_subplots += 1

    # Nếu có ít nhất một cảm xúc được vẽ, tạo bố cục và lưu hình ảnh
    if num_subplots > 0:
        plt.tight_layout()
        plt.savefig(save_path, format='png')
        plt.close()
    else:
        plt.close()  # Đảm bảo giải phóng tài nguyên khi không có gì để vẽ
    return save_path, ma_sp, danh_gia_lien_quan, diem_trung_binh


# Thống kê cơ bản
def group_by_so_sao_do_dai(danh_gia_lien_quan):
    # Tính toán trung bình cho 'do_dai' và 'so_sao'
    data = danh_gia_lien_quan.groupby('label')[['do_dai', 'so_sao']].mean(numeric_only=True).reset_index()

    # Tạo color map cho từng nhãn
    color_map = {'positive': 'green', 'neutral': 'gray', 'negative': '#8B0000'}

    # Vẽ biểu đồ cột cho 'do_dai' với màu sắc tùy chỉnh
    fig1 = px.bar(
        data_frame=data, 
        x='label', 
        y='do_dai', 
        color='label', 
        title='Trung bình độ dài theo phân loại', 
        labels={'do_dai': 'Độ dài', 'label': 'Phân loại'},
        color_discrete_map=color_map  # Áp dụng màu sắc tùy chỉnh
    )
    fig1.update_traces(texttemplate='%{y:.2f}', textposition='outside', hoverinfo='x+y')

    # Vẽ biểu đồ cột cho 'so_sao' với màu sắc tùy chỉnh
    fig2 = px.bar(
        data_frame=data, 
        x='label', 
        y='so_sao', 
        color='label', 
        title='Trung bình số sao theo phân loại', 
        labels={'so_sao': 'Số sao', 'label': 'Phân loại'},
        color_discrete_map=color_map  # Áp dụng màu sắc tùy chỉnh
    )
    fig2.update_traces(texttemplate='%{y:.2f}', textposition='outside', hoverinfo='x+y')

    # Hiển thị đồ thị trong Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

def so_luong(danh_gia_lien_quan):
    # Dữ liệu tổng hợp
    data = {
        'Category': ['Số từ tích cực', 'Số từ tiêu cực'],
        'Count': [danh_gia_lien_quan['positive_count'].sum(), danh_gia_lien_quan['negative_count'].sum()]
    }
    count_df = pd.DataFrame(data)
    
    # Tạo biểu đồ barplot cho số từ tích cực và tiêu cực
    fig1 = px.bar(
        count_df, 
        x='Category', 
        y='Count', 
        color='Category',
        title='Số từ tích cực và tiêu cực', 
        labels={'Count': 'Số lượng', 'Category': 'Loại từ'},
        color_discrete_map={'Số từ tích cực': 'green', 'Số từ tiêu cực': 'red'}
    )
    fig1.update_traces(texttemplate='%{y}', textposition='outside', hoverinfo='x+y')

    danh_gia_lien_quan['so_sao'] = pd.Categorical(danh_gia_lien_quan['so_sao'], 
                                                   categories=sorted(danh_gia_lien_quan['so_sao'].unique()), 
                                                   ordered=True)
    # Tạo biểu đồ countplot cho số sao
    fig2 = px.histogram(
        danh_gia_lien_quan, 
        x='so_sao', 
        color='so_sao', 
        title='Số lượng sao đánh giá', 
        labels={'so_sao': 'Số sao'}, 
    )
    
    fig2.update_layout(
        xaxis_title='Số sao',
        yaxis_title='Số lượng bình luận',
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=sorted(danh_gia_lien_quan['so_sao'].unique())  # Sắp xếp trục X theo số sao từ nhỏ đến lớn
        )
    )
    fig2.update_traces(texttemplate='%{y}', textposition='outside', hoverinfo='x+y')

    # Hiển thị đồ thị trong Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)


def time_series(danh_gia_lien_quan):
    # Xử lý cột 'nam' để đảm bảo định dạng là chuỗi và lấy phần trước dấu chấm
    danh_gia_lien_quan['nam'] = danh_gia_lien_quan['nam'].astype('str').str.split('.').str[0]

    # Đảm bảo thứ trong tuần sắp xếp đúng thứ tự
    thu_tu_thu = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'nan']
    danh_gia_lien_quan['thu_trong_tuan'] = pd.Categorical(danh_gia_lien_quan['thu_trong_tuan'], categories=thu_tu_thu, ordered=True)

    # Đảm bảo tháng được sắp xếp theo đúng thứ tự tháng
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'nan']
    danh_gia_lien_quan['thang'] = pd.Categorical(danh_gia_lien_quan['thang'], categories=month_order, ordered=True)

    # Chuyển đổi giá trị 'ngay_trong_thang' thành số
    danh_gia_lien_quan['ngay_trong_thang'] = pd.to_numeric(danh_gia_lien_quan['ngay_trong_thang'], errors='coerce')

    # Đảm bảo thứ tự ngày trong tháng
    ngay_order = list(range(1, 32)) + ['nan']
    danh_gia_lien_quan['ngay_trong_thang'] = pd.Categorical(danh_gia_lien_quan['ngay_trong_thang'], categories=ngay_order, ordered=True)

    # Tạo thứ tự năm
    years_order = sorted(danh_gia_lien_quan['nam'].unique())
    danh_gia_lien_quan['nam'] = pd.Categorical(danh_gia_lien_quan['nam'], categories=years_order, ordered=True)

    # Biểu đồ số lượng bình luận theo Năm
    fig1 = px.histogram(danh_gia_lien_quan, x='nam', title='Số lượng bình luận theo Năm', color='nam', color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_layout(
        xaxis_title='Năm',
        yaxis_title='Số lượng bình luận',
        xaxis_tickangle=45,
        showlegend=False,
        xaxis=dict(type='category', categoryorder='array', categoryarray=years_order)
    )
    fig1.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=12, color='black'))

    # Biểu đồ số lượng bình luận theo Tháng
    fig2 = px.histogram(danh_gia_lien_quan, x='thang', title='Số lượng bình luận theo Tháng', color='thang', color_discrete_sequence=px.colors.sequential.Blues)
    fig2.update_layout(
        xaxis_title='Tháng',
        yaxis_title='Số lượng bình luận',
        xaxis_tickangle=45,
        showlegend=False,
        xaxis=dict(type='category', categoryorder='array', categoryarray=month_order)
    )
    fig2.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=12, color='black'))

    # Biểu đồ số lượng bình luận theo Thứ trong tuần
    fig3 = px.histogram(danh_gia_lien_quan, x='thu_trong_tuan', title='Số lượng bình luận theo Thứ trong tuần', color='thu_trong_tuan', color_discrete_sequence=px.colors.sequential.Magma)
    fig3.update_layout(
        xaxis_title='Thứ trong tuần',
        yaxis_title='Số lượng bình luận',
        xaxis_tickangle=45,
        showlegend=False,
        xaxis=dict(type='category', categoryorder='array', categoryarray=thu_tu_thu)
    )
    fig3.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=12, color='black'))

    # Biểu đồ số lượng bình luận theo Ngày trong tháng
    fig4 = px.histogram(danh_gia_lien_quan, x='ngay_trong_thang', title='Số lượng bình luận theo Ngày trong tháng', color='ngay_trong_thang', color_discrete_sequence=px.colors.sequential.Plasma)
    fig4.update_layout(
        xaxis_title='Ngày trong tháng',
        yaxis_title='Số lượng bình luận',
        xaxis_tickangle=45,
        showlegend=False,
        xaxis=dict(type='category', categoryorder='array', categoryarray=ngay_order)
    )
    fig4.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=12, color='black'))

    # Hiển thị các biểu đồ trong Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)


# ================================== DATA ===================================
# Đọc data đánh giá
danh_gia = pd.read_csv('data/DATA - FINAL/Danh_gia_clean.csv', sep=';')
danh_gia['noi_dung_binh_luan_processed'] = np.where(danh_gia['noi_dung_binh_luan_processed']=="không_có_dữ_liệu", None, danh_gia['noi_dung_binh_luan_processed'])

# Đọc data thông tin sản phẩm
san_pham = pd.read_csv('data/DATA - FINAL/All_San_pham_clean.csv', sep=';')


# ================================== STREAMLIT ===================================
st.set_page_config(page_title="Phân tích sản phẩm", page_icon="📊", layout = "wide")

st.sidebar.title("👋 Sentiment Analysis 👋")
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center; /* Căn giữa */
        font-family: 'Arial', sans-serif; /* Đổi font chữ (hoặc thay bằng font khác) */
        font-size: 4em; /* Kích thước chữ */
        font-weight: bold; /* Đậm chữ */
        color: #2f6e51;
    }
    </style>
    <h1 class="centered-title">👋 Sentiment Analysis! 👋</h1>
    """,
    unsafe_allow_html=True
)

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
        margin-bottom: 10px; /* Khoảng cách dưới tiêu đề */
        display: flex; /* Dùng flex để căn icon và tiêu đề cùng dòng */
        align-items: center; /* Căn icon theo trục dọc */
    }
    .intro-icon {
        margin-right: 10px; /* Khoảng cách giữa icon và chữ */
        font-size: 2em; /* Kích thước icon */
    }
    </style>
    <div class="intro-title">
        <span class="intro-icon">📊</span> <!-- Icon -->
        Thống kê sản phẩm
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .intro-paragraph {
        text-indent: 0px; /* Thụt lề đầu dòng */
        margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
        font-size: 1.8em; /* Kích thước chữ */
        line-height: 1.5; /* Khoảng cách dòng */
        text-align: justify; /* Canh đều đoạn văn */
        font-style: italic; /* In nghiêng đoạn văn */
    }
    </style>
    <p class="intro-paragraph">
    <strong>Chọn sản phẩm:</strong>
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .intro-paragraph {
        text-indent: 0px; /* Thụt lề đầu dòng */
        margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
        font-size: 1.8em; /* Kích thước chữ */
        line-height: 1.5; /* Khoảng cách dòng */
        text-align: center; /* Canh đều đoạn văn */
        font-style: italic; /* In nghiêng đoạn văn */
    }
    </style>
    <p class="intro-paragraph">
    ⌨️⌨️⌨️   Mời bạn nhập tên sản phẩm cần tìm    ⌨️⌨️⌨️
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.write("""#### Thành viên thực hiện:\n
                 Trang Thư Đình &
                 Nguyễn Quang Khải""")
st.sidebar.write("""#### Giảng viên hướng dẫn:\n
                Khuất Thùy Phương""")
st.sidebar.write("""#### Thời gian thực hiện: 7/12/2024""")

products = san_pham[san_pham['ma_san_pham'].isin(danh_gia['ma_san_pham'].unique())]['ten_san_pham'].unique()
selected_product = st.selectbox('Sản phẩm:',products)

if selected_product:
    savepath, ma_sp, danh_gia_lien_quan, diem_trung_binh = find_product_code_and_wordcloud(selected_product, san_pham, danh_gia, 'image/wordcloud_image.png')

    st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 0px; /* Thụt lề đầu dòng */
            margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.8em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>Bạn đã chọn:</strong>
        </p>
        """,
        unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <style>
        .intro-paragraph {{
            text-indent: 0px; /* Không thụt lề đầu dòng */
            margin-left: 0px; /* Không dịch chuyển cả đoạn văn */
            font-size: 1.3em; /* Tăng kích thước chữ */
            line-height: 1.5; /* Giãn dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* Làm nghiêng chữ */
        }}
        </style>
        <p class="intro-paragraph">
        - <strong>Sản phẩm:</strong> {selected_product} <br>
        - <strong>Mã sản phẩm:</strong> {ma_sp} <br>
        - <strong>Đánh giá trung bình:</strong> {round(diem_trung_binh,2)} <br>
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 0px; /* Thụt lề đầu dòng */
            margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.8em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>Word could:</strong>
        </p>
        """,
        unsafe_allow_html=True)
    
    st.image(savepath, use_container_width=True)

    # Thống kê
    st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 0px; /* Thụt lề đầu dòng */
            margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.8em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        <strong>Thống kê cơ bản:</strong>
        </p>
        """,
        unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 0px; /* Thụt lề đầu dòng */
            margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        🌟 Số sao và độ dài theo nhãn
        </p>
        """,
        unsafe_allow_html=True
    )
    group_by_so_sao_do_dai(danh_gia_lien_quan)

    st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 0px; /* Thụt lề đầu dòng */
            margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: italic; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        📧 Số lượng bình luận theo sao và từ tích cực - tiêu cực
        </p>
        """,
        unsafe_allow_html=True
    )
    so_luong(danh_gia_lien_quan)

    st.markdown(
        """
        <style>
        .intro-paragraph {
            text-indent: 0px; /* Thụt lề đầu dòng */
            margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            font-style: ; /* In nghiêng đoạn văn */
        }
        </style>
        <p class="intro-paragraph">
        📆 Số lượng theo ngày bình luận
        </p>
        """,
        unsafe_allow_html=True
    )
    time_series(danh_gia_lien_quan)





    