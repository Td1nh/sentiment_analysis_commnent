import streamlit as st

# ================================== STREAMLIT ===================================
st.set_page_config(
    page_title="Trang chủ",
    page_icon="🏠",
    layout = "wide"
)

st.sidebar.title("👋 Sentiment Analysis 📄")
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
st.markdown(
    """
    <style>
    .intro-title {
        font-weight: bold; /* Làm đậm chữ */
        font-size: 1.5em; /* Kích thước chữ */
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
        <span class="intro-icon">💄</span> <!-- Icon -->
        Giới thiệu doanh nghiệp: HASAKI.VN
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .intro-paragraph {
        text-indent: 0px; /* Thụt lề đầu dòng */
        margin-left: 20px; /* Thụt toàn bộ đoạn văn vào */
        font-size: 1.5em; /* Kích thước chữ */
        line-height: 1.5; /* Khoảng cách dòng */
        text-align: justify; /* Canh đều đoạn văn */
        font-style: italic; /* In nghiêng đoạn văn */
    }
    </style>
    <p class="intro-paragraph">
    - <strong>HASAKI.VN</strong> là hệ thống cửa hàng mỹ phẩm chính hãng và dịch vụ chăm sóc sắc đẹp với quy mô toàn quốc. Là đối tác chiến lược của nhiều thương hiệu lớn tại thị trường Việt Nam.
    </p>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
    .intro-title {
        font-weight: bold; /* Làm đậm chữ */
        font-size: 1.5em; /* Kích thước chữ */
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
        <span class="intro-icon">🗒️</span> <!-- Icon -->
        Vấn đề đặt ra
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .intro-paragraph {
        text-indent: 0px; /* Thụt lề đầu dòng */
        margin-left: 20px; /* Thụt toàn bộ đoạn văn vào */
        font-size: 1.5em; /* Kích thước chữ */
        line-height: 1.5; /* Khoảng cách dòng */
        text-align: justify; /* Canh đều đoạn văn */
        font-style: italic; /* In nghiêng đoạn văn */
    }
    </style>
    <p class="intro-paragraph">
    - <strong>Nhu cầu của khách hàng:</strong> Lựa chọn sản phẩm, xem đánh giá, nhận xét và đặt mua trực tuyến.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .intro-paragraph {
        text-indent: 0px; /* Thụt lề đầu dòng */
        margin-left: 20px; /* Thụt toàn bộ đoạn văn vào */
        font-size: 1.5em; /* Kích thước chữ */
        line-height: 1.5; /* Khoảng cách dòng */
        text-align: justify; /* Canh đều đoạn văn */
        font-style: italic; /* In nghiêng đoạn văn */
    }
    </style>
    <p class="intro-paragraph">
    - <strong>Nhu cầu của nhãn hàng:</strong> Hiểu rõ hơn cảm xúc, ý kiến của khách hàng về sản phẩm và dịch vụ.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .intro-title {
        font-weight: bold; /* Làm đậm chữ */
        font-size: 1.5em; /* Kích thước chữ */
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
        <span class="intro-icon">🔑</span> <!-- Icon -->
        Mục tiêu
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .intro-paragraph {
        text-indent: 0px; /* Thụt lề đầu dòng */
        margin-left: 20px; /* Thụt toàn bộ đoạn văn vào */
        font-size: 1.5em; /* Kích thước chữ */
        line-height: 1.5; /* Khoảng cách dòng */
        text-align: justify; /* Canh đều đoạn văn */
        font-style: italic; /* In nghiêng đoạn văn */
    }
    </style>
    <p class="intro-paragraph">
    => Cải thiện chất lượng sản phẩm và nâng cao trải nghiệm dịch vụ. <br>
    - <strong>Thực hiện:</strong> <br>
        + Lựa chọn sản phẩm và có thể xem được cái thông tin liên quan đến sản phẩm: thống kê về đánh giá, thống kê về ngày bình luận,... <br>
        + Nhập bình luận và hệ thống sẽ đánh giá, phân tích về nhãn của bình luận đó: tích cực - tiêu cực - trung bình.
    </p>
    """,
    unsafe_allow_html=True
)