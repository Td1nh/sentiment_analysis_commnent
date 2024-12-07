import streamlit as st

# ================================== STREAMLIT ===================================
st.set_page_config(
    page_title="Trang chủ",
    page_icon="🏠",
    layout = "wide"
)

st.write("# Bài toán Sentiment Analysis! 👋")
st.write("### Doanh nghiệp: Hasaki")

st.sidebar.write("""#### Thành viên thực hiện:\n
                 Trang Thư Đình
                 Nguyễn Quang Khải""")
st.sidebar.write("""#### Giảng viên hướng dẫn:\n
                Khuất Thùy Phương""")
st.sidebar.write("""#### Thời gian thực hiện: 7/12/2024""")
st.markdown(
    """
    ###### Giới thiệu doanh nghiệp: HASAKI.VN
    HASAKI.VN là hệ thống cửa hàng mỹ phẩm chính hãng và dịch vụ chăm sóc sắc đẹp với quy mô toàn quốc.
    Đối tác chiến lược của nhiều thương hiệu lớn tại thị trường Việt Nam.
    
    ###### Nhu cầu của khách hàng: Lựa chọn sản phẩm, xem đánh giá, nhận xét và đặt mua trực tuyến.
    
    ###### Vấn đề đặt ra: Các nhãn hàng cần hiểu rõ hơn cảm xúc, ý kiến của khách hàng về sản phẩm và dịch vụ.

    ###### Mục tiêu: Cải thiện chất lượng sản phẩm và nâng cao trải nghiệm dịch vụ.
    
    ###### Cần thực hiện:
    * Lựa chọn sản phẩm và có thể xem được cái thông tin liên quan đến sản phẩm: thống kê về đánh giá, thống kê về ngày bình luận,...
    * Nhập bình luận và hệ thống sẽ đánh giá, phân tích về nhãn của bình luận đó: tích cực - tiêu cực - trung bình.

    """
)





    