import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox
from fuzzywuzzy import process
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import os

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
    ma_sp = san_pham[san_pham['ten_san_pham']==selected_product]['ma_san_pham'].iloc[0]
    danh_gia_lien_quan = danh_gia[danh_gia['ma_san_pham']==ma_sp]

    # Kiểm tra nếu thư mục chưa tồn tại thì tạo mới
    folder = os.path.dirname(save_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # Lọc các bình luận theo từng cảm xúc và xử lý NaN
    pos = ' '.join(danh_gia_lien_quan[(danh_gia_lien_quan['label'] == 'positive') & (~danh_gia_lien_quan['noi_dung_binh_luan_processed'].isna())]['noi_dung_binh_luan_processed'])
    neu = ' '.join(danh_gia_lien_quan[(danh_gia_lien_quan['label'] == 'neutral') & (~danh_gia_lien_quan['noi_dung_binh_luan_processed'].isna())]['noi_dung_binh_luan_processed'])
    neg = ' '.join(danh_gia_lien_quan[(danh_gia_lien_quan['label'] == 'negative') & (~danh_gia_lien_quan['noi_dung_binh_luan_processed'].isna())]['noi_dung_binh_luan_processed'])
    # Vẽ wordcloud cho từng cảm xúc
    plt.figure(figsize=(18, 6))
    # Positive
    plt.subplot(1, 3, 1)
    generate_wordcloud(pos, 'Greens', "Positive Sentiments")
    # Neutral
    plt.subplot(1, 3, 2)
    generate_wordcloud(neu, 'Blues', "Neutral Sentiments")
    # Negative
    plt.subplot(1, 3, 3)
    generate_wordcloud(neg, 'Reds', "Negative Sentiments")
    # Tạo bố cục và lưu hình ảnh
    plt.tight_layout()
    plt.savefig(save_path, format='png')
    plt.close()
    return save_path, ma_sp, danh_gia_lien_quan

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

    years_order = sorted(danh_gia_lien_quan['nam'].unique())
    danh_gia_lien_quan['nam'] = pd.Categorical(danh_gia_lien_quan['nam'], categories=sorted(danh_gia_lien_quan['nam'].unique()), ordered=True)
    # Tạo biểu đồ cho số lượng bình luận theo Năm
    fig1 = px.histogram(danh_gia_lien_quan, x='nam', title='Số lượng bình luận theo Năm', color='nam', color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_layout(
        xaxis_title='Năm',
        yaxis_title='Số lượng bình luận',
        xaxis_tickangle=45,
        showlegend=False,
        xaxis=dict(type='category', categoryorder='array', categoryarray=years_order)   # Trục X là dạng category
    )
    fig1.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=12, color='black'))

    # Tạo biểu đồ cho số lượng bình luận theo Tháng với sắp xếp trục x theo đúng thứ tự tháng
    fig2 = px.histogram(danh_gia_lien_quan, x='thang', title='Số lượng bình luận theo Tháng', color='thang', color_discrete_sequence=px.colors.sequential.Blues)
    fig2.update_layout(
        xaxis_title='Tháng',
        yaxis_title='Số lượng bình luận',
        xaxis_tickangle=45,
        showlegend=False,
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=month_order  # Sắp xếp trục x theo tháng
        )
    )
    fig2.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=12, color='black'))

    # Tạo biểu đồ cho số lượng bình luận theo Thứ trong tuần
    fig3 = px.histogram(danh_gia_lien_quan, x='thu_trong_tuan', title='Số lượng bình luận theo Thứ trong tuần', color='thu_trong_tuan', color_discrete_sequence=px.colors.sequential.Magma)
    fig3.update_layout(
        xaxis_title='Thứ trong tuần',
        yaxis_title='Số lượng bình luận',
        xaxis_tickangle=45,
        showlegend=False,
        xaxis=dict(type='category',
                   categoryorder='array',
                    categoryarray=thu_tu_thu)  # Trục X là dạng category
    )
    fig3.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=12, color='black'))

    # Hiển thị các biểu đồ trong Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)


# ================================== DATA ===================================
# Đọc data đánh giá
danh_gia = pd.read_csv('data/DATA - FINAL/Danh_gia_clean.csv', sep=';')
danh_gia['noi_dung_binh_luan_processed'] = danh_gia['noi_dung_binh_luan_processed'].fillna("không_có_dữ_liệu")

# Đọc data thông tin sản phẩm
san_pham = pd.read_csv('data/DATA - FINAL/All_San_pham_clean.csv', sep=';')


# ================================== STREAMLIT ===================================
st.set_page_config(page_title="Thông tin sản phẩm", page_icon="📊", layout = "wide")

st.markdown("# Thống kê sản phẩm")
st.write(
    """Đây là trang thống kê thông tin về sản phẩm có trong hệ thống. Xin nhập tên sản phẩm."""
)

st.sidebar.write("""#### Thành viên thực hiện:\n
                 Trang Thư Đình
                 Nguyễn Quang Khải""")
st.sidebar.write("""#### Giảng viên hướng dẫn:\n
                Khuất Thùy Phương""")
st.sidebar.write("""#### Thời gian thực hiện: 7/12/2024""")

products = san_pham[san_pham['ma_san_pham'].isin(danh_gia['ma_san_pham'].unique())]['ten_san_pham'].unique().tolist()

# Hiển thị ô tìm kiếm với gợi ý
selected_product = st_searchbox(
    search_function=search_products,
    placeholder="Nhập tên sản phẩm...",
    label="Chọn sản phẩm"
)

if selected_product:
    savepath, ma_sp, danh_gia_lien_quan = find_product_code_and_wordcloud(selected_product, san_pham, danh_gia, 'image/wordcloud_image.png')

    # Thông tin sản phẩm
    st.write("## Bạn đã chọn")
    st.write(f"Sản phẩm: {selected_product}")
    st.write(f'Mã sản phẩm: {ma_sp}')

    # Word could
    st.write('## Word cloud của sản phẩm')
    st.image(savepath, use_container_width=True)

    # Thống kê
    st.write('## Thống kê cơ bản')

    st.write('### Số sao và độ dài theo nhãn')
    group_by_so_sao_do_dai(danh_gia_lien_quan)

    st.write('### Số lượng bình luận theo sao và từ tích cực - tiêu cực')
    so_luong(danh_gia_lien_quan)

    st.write('### Số lượng theo ngày bình luận')
    time_series(danh_gia_lien_quan)





    