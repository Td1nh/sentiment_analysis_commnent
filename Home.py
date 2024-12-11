import streamlit as st

# ================================== STREAMLIT ===================================
st.set_page_config(
    page_title="Trang chủ",
    page_icon="🏠",
    layout = "wide"
)


st.markdown("""
    <style>
    /* Overall page background */
    body {
        background-color: #F2F1F6; /* Màu nền mới */
        color: #000000; /* Màu chữ mặc định */
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        border-right: 2px solid #2f6e51;
    }

    /* Header and title styles */
    .header-title {
        color: #2f6e51;
        font-family: 'Arial', sans-serif;
        text-align: center;
        padding: 20px;
        background-color: #d0e5d3;
        border-radius: 10px;
        margin-bottom: 20px;
    }
            
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:2.1rem;
        color: #2f6e51;
    }

    .sttext { 
        text-indent: 25px; /* Thụt lề đầu dòng */
        font-size:1.5em;
    }
            
    </style>
""", unsafe_allow_html=True)


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

st.sidebar.write("""#### Thành viên thực hiện:\n
                 Trang Thư Đình &
                 Nguyễn Quang Khải""")
st.sidebar.write("""#### Giảng viên hướng dẫn:\n
                Khuất Thùy Phương""")
st.sidebar.write("""#### Thời gian thực hiện: 7/12/2024""")


tab1, tab2 = st.tabs(["💄 Giới thiệu Hasaki", "🔑 Mục tiêu"])

with tab1:
    st.write('<p class="sttext"> <strong>Hasaki.vn</strong> là hệ thống cửa hàng mỹ phẩm chính hãng và dịch vụ chăm sóc sắc đẹp với quy mô toàn quốc. Là đối tác chiến lược của nhiều thương hiệu lớn tại thị trường Việt Nam.</p>', unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; line-height: 1.5;">
            <img src="https://cdn.hpdecor.vn/wp-content/uploads/2022/05/hasaki-1.jpg" width="600">
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.write("""<p class="sttext"> 
        <br>
        Hasaki.vn được thành lập tại Việt Nam vào tháng 4/2016 với mục tiêu chăm sóc sắc đẹp và sức khỏe toàn diện cho người Việt Nam. Hasaki.vn đã tạo ra những trải nghiệm mua sắm trực tuyến tuyệt vời cùng dịch vụ chăm sóc Spa chuyên nghiệp với các thiết bị hiện đại hàng đầu thế giới hiện nay. <br>
        Đến với Hasaki.vn khách hàng sẽ trải nghiệm việc mua sắm trực tuyến với các bước thanh toán an toàn, đơn giản, nhanh chóng, đáp ứng tiêu chuẩn Quốc tế. Với phương châm <strong>“Chất lượng thật - Giá trị thật”</strong>, Hasaki.vn luôn nỗ lực không ngừng nhằm nâng cao chất lượng dịch vụ để khách hàng được hưởng các dịch vụ chăm sóc tốt nhất.</p>""", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .intro-container {
            display: flex; /* Sử dụng Flexbox */
            justify-content: center; /* Canh giữa nội dung */
            align-items: center; /* Canh giữa theo chiều dọc */
            height: 100%; /* Chiều cao để đảm bảo toàn bộ khung */
        }
        .intro-paragraph {
            text-align: center; /* Canh giữa đoạn văn */
            font-size: 2em; /* Kích thước chữ */
            line-height: 1.5; /* Khoảng cách dòng */
            font-style: italic; /* In nghiêng đoạn văn */
            color: #2f6e51; 
        }
        .intro-link {
            color: #2f6e51; 
            text-decoration: none; /* Bỏ gạch chân */
            font-size: 2.5em;
        }
        .intro-link:hover {
            text-decoration: underline; /* Gạch chân khi hover */
        }
        </style>
        <div class="intro-container">
            <p class="intro-paragraph">
                <a class="intro-link" href="https://hasaki.vn/" target="_blank">
                    https://hasaki.vn/
                </a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab2:
    st.markdown(
        """
        <style>
        .intro-paragraph1 {
            text-indent: 0px; /* Thụt lề đầu dòng */
            margin-left: 10px; /* Thụt toàn bộ đoạn văn vào */
            font-size: 1.5em; /* Kích thước chữ */
            line-height: 2; /* Khoảng cách dòng */
            text-align: justify; /* Canh đều đoạn văn */
            color: #000000
            font-style: normal; /* Đảm bảo không in nghiêng */
        }
        </style>
        <p class="intro-paragraph1">
        <strong>👨‍👨‍👦‍👦 Nhu cầu của khách hàng:</strong> Lựa chọn sản phẩm, xem đánh giá, nhận xét và đặt mua trực tuyến.<br>
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div style="display: flex; justify-content: justify; line-height: 1.5; margin-left: 200px;">
            <img src="https://simpleshop.vn/blog/wp-content/uploads/2021/09/web-ban-hang-online-thoi-nay.jpg" width="400">
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p class="intro-paragraph1">
        <strong>👨🏻‍💼Nhu cầu của nhãn hàng:</strong> Hiểu rõ hơn cảm xúc, ý kiến của khách hàng về sản phẩm và dịch vụ.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div style="display: flex; justify-content: justify; line-height: 1.5; margin-left: 150px;">
            <img src="https://www.mathworks.com/discovery/sentiment-analysis/_jcr_content/mainParsys/image_695965980_copy.adapt.full.medium.jpg/1719309393930.jpg" width="500">
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p class="intro-paragraph1">
        <strong>🎯 Bài toán đặt ra:</strong><br>
        - Làm sao để các nhãn hàng hiểu rõ hơn về cảm nhận và ý kiến của khách hàng qua đánh giá sản phẩm.<br>
        - Từ đó cải thiện chất lượng sản phẩm và nâng cao trải nghiệm dịch vụ. <br>
        <strong>🚀 Thực hiện:</strong> <br>
        - Lựa chọn sản phẩm và có thể xem được cái thông tin liên quan đến sản phẩm: thống kê về đánh giá, thống kê về ngày bình luận,... <br>
        - Nhập bình luận và hệ thống sẽ đánh giá, phân tích về nhãn của bình luận đó: tích cực - tiêu cực - trung bình.
        </p>
        """,
        unsafe_allow_html=True
    )
