import pandas as pd
import streamlit as st
from underthesea import sent_tokenize
import regex
import re
import joblib
from scipy.sparse import hstack
from pyvi import ViPosTagger, ViTokenizer
import string


# ================================= DATA SỬ DỤNG CHO HÀM ===================================
#LOAD EMOJICON
file = open('files/emojicon.txt', 'r', encoding="utf8")
emoji_lst = file.read().split('\n')
emoji_dict = {}
for line in emoji_lst:
    key, value = line.split('\t')
    emoji_dict[key] = str(value)
file.close()

#################
#LOAD TEENCODE & ABBREVIATION
file = open('files/teencode.txt', 'r', encoding="utf8")
teen_lst = file.read().split('\n')
teen_dict = {}
for line in teen_lst:
    key, value = line.split('\t')
    teen_dict[key] = str(value)
file.close()

#################
#LOAD STOPWORDS
file = open('files/vietnamese-stopwords.txt', 'r', encoding="utf8")
stopwords_lst = file.read().split('\n')
file.close()

#LOAD CORRECTION
file = open('files/corrected_word.txt', 'r', encoding="utf8")
corrected_word_lst = file.read().split('\n')
corrected_word_dict = {}
for line in corrected_word_lst:
    key, value = line.split('\t')
    corrected_word_dict[key] = str(value)
file.close()

#################
#LOAD KEEPWORDS
file = open('files/keep_word.txt', 'r', encoding="utf8")
keep_lst = file.read().split('\n')
file.close()

#LOAD positive words
file = open('files/positive_VN.txt', 'r', encoding="utf8")
positive_words = file.read().split('\n')
file.close()

#LOAD negative words
file = open('files/negative_VN.txt', 'r', encoding="utf8")
negative_words = file.read().split('\n')
file.close()

#LOAD positive emojis
file = open('files/positive_emoji.txt', 'r', encoding="utf8")
positive_emojis = file.read().split('\n')
file.close()

#LOAD positive emojis
file = open('files/negative_emoji.txt', 'r', encoding="utf8")
negative_emojis = file.read().split('\n')
file.close()

# ================================== FUNCTION LIÊN QUAN ===================================
# THÊM DẤU CÁCH TRƯỚC EMOJI
def add_emoji_spaces(text, emoji_dict):
    # Find and add spaces around emojis
    for emoji in emoji_dict.keys():
        # Add space before and after emoji
        text = text.replace(emoji, f' {emoji} ')
    # Remove punctuation
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading and trailing spaces
    text = text.strip()
    return text



# SỬA EMOJI, TEENCODE, SAI CHÍNH TẢ, BỎ KÝ TỰ ĐẶC BIỆT
def process_text(text, emoji_dict, teen_dict):
    # Apply emoji space handling first
    document = add_emoji_spaces(text.lower(), emoji_dict)
    document = document.replace("'",'')
    document = regex.sub(r'\.+', ".", document)
    new_sentence = ''
    for sentence in sent_tokenize(document):
        # CONVERT EMOJICON
        sentence = ''.join(emoji_dict[word]+' ' if word in emoji_dict else word for word in list(sentence))

        # CONVERT TEENCODE & ABBREVIATION
        sentence = ' '.join(teen_dict[word] if word in teen_dict else word for word in sentence.split())

        # # DEL Punctuation & Numbers
        # pattern = r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b'
        # sentence = ' '.join(regex.findall(pattern,sentence))

        new_sentence = new_sentence + sentence
    document = new_sentence
    # DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    return document



# CHUẨN HÓA UNICODE TIẾNG VIỆT
def loaddicchar():
    uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
    unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

def covert_unicode(txt):
    dicchar = loaddicchar()
    return regex.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)



# NỐI CÁC TỪ CẦN XỬ LÝ ĐẶC BIỆT
def process_special_word(text):
    if not text:
        return ""
    
    # Danh sách các từ đặc biệt cần xử lý
    special_words = {'không', 'chả', 'kém', 'chẳng', 'đừng', 'chớ', 'chưa', 'không_có', 'không_quá', 'nên', 'khó', 'không_nên', 'không_làm', 'nên', 'chất_lượng', 'bị', 'không_bị'}
    
    words = text.split()
    result = []
    i = 0
    
    while i < len(words):
        current_word = words[i]

        if current_word in special_words and i + 1 < len(words) and words[i + 1] not in special_words:
            # Nối từ đặc biệt với từ tiếp theo nếu từ tiếp theo không phải là từ đặc biệt
            combined_word = f"{current_word}_{words[i + 1]}"
            result.append(combined_word)
            i += 2  # Bỏ qua từ tiếp theo vì đã xử lý
        else:
            result.append(current_word)
            i += 1
    
    return ' '.join(result)

# CHUẨN HÓA TỪ CÓ KÝ TỰ LẶP
def normalize_repeated_characters(text):
    return re.sub(r'(.)\1+', r'\1', text)



# GHÉP TỪ
def process_postag_pyvi(text, keep_lst):
    # Tách câu
    sentences = text.split('.')  # Chia các câu dựa trên dấu chấm.

    # Danh sách các từ loại POS cần giữ lại và các từ đặc biệt
    lst_word_type = ['A', 'V', 'R', 'Np']
    special_words =  keep_lst # Các từ đặc biệt mà bạn muốn giữ lại
    processed_sentences = []
    for sentence in sentences:
        # Bỏ khoảng trắng thừa
        sentence = sentence.strip()
        if not sentence:
            continue

        # Tokenize và POS tagging
        tokens = ViTokenizer.tokenize(sentence)
        words, pos_tags = ViPosTagger.postagging(tokens)

        # Giữ lại các từ thuộc POS mong muốn và các từ đặc biệt
        filtered_words = [word for word, pos in zip(words, pos_tags) if pos in lst_word_type or word in special_words]

        # Ghép các từ lại thành câu
        processed_sentences.append(' '.join(filtered_words))

    # Ghép lại các câu thành văn bản hoàn chỉnh
    result = ' '.join(processed_sentences).strip()

    return result




# LOẠI BỎ STOPWORD
def remove_stopword(text, stopwords):
    ###### REMOVE stop words
    document = ' '.join('' if word in stopwords else word for word in text.split())

    ###### DEL excess blank space
    document = regex.sub(r'\s+', ' ', document).strip()
    return document


# CHỈNH SỬA CHÍNH TẢ
def correct_spelling(text, corrected_word_dict):
    # Tạo regex pattern để tìm các từ cần thay thế
    pattern = regex.compile(r'\b(' + '|'.join(regex.escape(key) for key in corrected_word_dict.keys()) + r')\b')
    # Hàm thay thế từ sai thành từ đúng
    def replace_word(match):
        word = match.group(0)
        return corrected_word_dict.get(word, word)
    # Thực hiện thay thế
    corrected_text = pattern.sub(replace_word, text)
    return corrected_text


# PIPELINE
class VietnameseTextProcessor:
    def __init__(self, emoji_dict, teen_dict, stopwords_lst, keep_lst):
        self.emoji_dict = emoji_dict
        self.teen_dict = teen_dict
        self.stopwords_lst = stopwords_lst
        self.keep_lst = keep_lst

    def process_pipeline(self, text):
        # Chuyển text về string nếu không phải
        text = str(text)

        text = add_emoji_spaces(text, emoji_dict)
        
        text = normalize_repeated_characters(text)

        text = process_text(text, emoji_dict, teen_dict)

        text = correct_spelling(text, corrected_word_dict)

        text = covert_unicode(text)

        text = process_postag_pyvi(text, keep_lst)

        text = process_special_word(text)

        text = remove_stopword(text, stopwords_lst)
        return text

# Khởi tạo processor
processor = VietnameseTextProcessor(
    emoji_dict=emoji_dict,
    teen_dict=teen_dict,
    stopwords_lst=stopwords_lst,
    keep_lst = keep_lst
)


def find_words(text, word_list):
    text_lower = text.lower()
    word_count = 0
    found_words = []
    # Tách các từ trong văn bản bằng dấu cách
    words_in_text = text_lower.split()
    for text_word in words_in_text:
        if text_word in word_list:
          found_words.append(text_word)
          word_count += 1
    return word_count, found_words


def sentiment_pipeline(document, positive_words, negative_words, positive_emojis, negative_emojis):
    # Calculate word sentiment
    positive_count, positive_word_list = find_words(document, positive_words)
    negative_count, negative_word_list = find_words(document, negative_words)

    # Calculate emoji sentiment
    positive_icon, positive_icon_list = find_words(document, positive_emojis)
    negative_icon, negative_icon_list = find_words(document, negative_emojis)

    # Total sentiment calculation
    total_positive = positive_count + positive_icon
    total_negative = negative_count + negative_icon
    return total_positive, positive_word_list + positive_icon_list, total_negative, negative_word_list + negative_icon_list


def preprocess_sentiment_text(text, processor, positive_words, negative_words, positive_emojis, negative_emojis):
    # Tách văn bản thành các dòng, mỗi dòng cách nhau bởi \n
    lines = text.split('\n')
    
    # Danh sách để chứa kết quả
    processed_texts = []
    positive_counts = []
    negative_counts = []
    lengths = []

    # Lặp qua từng dòng
    for line in lines:
        # Tiền xử lý văn bản
        processed_text = processor.process_pipeline(line)
        count_text = process_special_word(process_postag_pyvi(normalize_repeated_characters(add_emoji_spaces(line, emoji_dict)), keep_lst))
        
        # Dự đoán cảm xúc
        result = sentiment_pipeline(count_text, positive_words, negative_words, positive_emojis, negative_emojis)
        
        # Thêm kết quả vào các danh sách
        processed_texts.append(processed_text)
        positive_counts.append(result[0])
        negative_counts.append(result[2])
        lengths.append(len(str(line).split()))
    
    # Tạo DataFrame chứa kết quả
    data = {
        "noi_dung_binh_luan": lines,
        "noi_dung_binh_luan_processed": processed_texts,
        "positive_count": positive_counts,
        "negative_count": negative_counts,
        "do_dai": lengths
    }
    
    du_doan = pd.DataFrame(data)
    return du_doan


def x_with_engineering_model(du_doan, vectorizer_path='saved_models/count_vectorizer_model.pkl', scaler_path='saved_models/scaler_minmax.pkl'):
    # Tải mô hình và vectorizer từ file
    train, count_vectorizer = joblib.load(vectorizer_path)
    # Chuyển văn bản đã xử lý thành vector 
    du_doan_vec = count_vectorizer.transform(du_doan['noi_dung_binh_luan_processed'])
    # Kết hợp các đặc trưng số
    du_doan_num = du_doan[['do_dai', 'positive_count', 'negative_count']].copy()

    scaler_loaded = joblib.load(scaler_path)
    du_doan_num[['do_dai']] = scaler_loaded.transform(du_doan_num[['do_dai']])

    du_doan_num = du_doan_num[['do_dai', 'positive_count', 'negative_count']].values 
    du_doan_combined = hstack([du_doan_vec, du_doan_num])
    return du_doan_combined

# ================================== DATA ===================================
# Đọc data đánh giá
danh_gia = pd.read_csv('data/DATA - FINAL/Danh_gia_clean.csv', sep=';')

# ================================== STREAMLIT ===================================
st.set_page_config(
    page_title="Dự đoán nhãn",
    page_icon="📉",
    layout = "wide"
)

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
        <strong>📉 Dự đoán nhãn</strong>
        </p>
        """,
        unsafe_allow_html=True)

st.sidebar.write("""#### Thành viên thực hiện:\n
                 Trang Thư Đình &
                 Nguyễn Quang Khải""")
st.sidebar.write("""#### Giảng viên hướng dẫn:\n
                Khuất Thùy Phương""")
st.sidebar.write("""#### Thời gian thực hiện: 7/12/2024""")

# Khởi tạo processor
processor = VietnameseTextProcessor(
    emoji_dict=emoji_dict,
    teen_dict=teen_dict,
    stopwords_lst=stopwords_lst,
    keep_lst = keep_lst
)
flag = False
lines = None

# Hiển thị widget radio
type = st.radio("Tải bình luận lên hay Nhập liệu?", options=("Tải lên", "Nhập bình luận"))
if type=="Tải lên":
    # Upload file
    uploaded_file_1 = st.file_uploader("Chọn file", type=['txt', 'csv', 'xlsx'])
    if uploaded_file_1 is not None:
        # Kiểm tra loại file và đọc tương ứng
        if uploaded_file_1.name.endswith('.csv') or uploaded_file_1.name.endswith('.txt'):
            # Đọc file CSV hoặc TXT, bỏ qua các dòng có lỗi
            lines = pd.read_csv(uploaded_file_1, header=None, sep=';')
        elif uploaded_file_1.name.endswith('.xlsx'):
            # Đọc file Excel
            lines = pd.read_excel(uploaded_file_1, header=None)
        # Chỉ lấy cột đầu tiên
        lines = lines[0]  
        # Tạo DataFrame mới và đổi tên cột thành 'noi_dung_binh_luan'
        du_doan = pd.DataFrame(lines)
        du_doan.columns = ['noi_dung_binh_luan']
        # Hiển thị DataFrame mới
        st.markdown(
                f"""
                <style>
                .intro-paragraph {{
                    text-indent: 0px; /* Thụt lề đầu dòng */
                    margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
                    font-size: 1.5em; /* Kích thước chữ */
                    line-height: 1.5; /* Khoảng cách dòng */
                    text-align: justify; /* Canh đều đoạn văn */
                    font-style: italic; /* In nghiêng đoạn văn */
                }}
                </style>
                <p class="intro-paragraph">
                <strong>💬 Nội dung bình luận:</strong>
                </p>
                """,
                unsafe_allow_html=True)
        st.dataframe(du_doan)

        with st.spinner('Đang tải...'):
            # Lưu ý: Cần cung cấp các tham số như processor, positive_words, negative_words, positive_emojis, negative_emojis.
            df_processed = du_doan['noi_dung_binh_luan'].apply(
                lambda x: preprocess_sentiment_text(x, processor, positive_words, negative_words, positive_emojis, negative_emojis)
            )
            # Merging kết quả vào một DataFrame duy nhất
            du_doan = pd.concat(df_processed.tolist(), ignore_index=True)

            du_doan_combined = x_with_engineering_model(du_doan, vectorizer_path='saved_models/count_vectorizer_model.pkl', scaler_path='saved_models/scaler_minmax.pkl')

            loaded_model = joblib.load('saved_models/Random_Forest_Classifier.pkl', mmap_mode=None)

            # Dự đoán nhãn
            predictions = loaded_model.predict(du_doan_combined)
            # Dự đoán xác suất
            probabilities = loaded_model.predict_proba(du_doan_combined)

        st.success("Xong!")

        # In xác suất theo từng mẫu
        st.markdown(
                f"""
                <style>
                .intro-paragraph {{
                    text-indent: 0px; /* Thụt lề đầu dòng */
                    margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
                    font-size: 1.5em; /* Kích thước chữ */
                    line-height: 1.5; /* Khoảng cách dòng */
                    text-align: justify; /* Canh đều đoạn văn */
                    font-style: italic; /* In nghiêng đoạn văn */
                }}
                </style>
                <p class="intro-paragraph">
                <strong>🧮 Dự đoán nhãn:</strong>
                </p>
                """,
                unsafe_allow_html=True)
        class_labels = loaded_model.classes_
        prob_df = pd.DataFrame(probabilities, columns=class_labels)
        prob_df["Predicted Label"] = predictions
        result = pd.merge(du_doan['noi_dung_binh_luan'], prob_df, left_index=True, right_index=True)
        
        for index, row in result.iterrows():
            if row['Predicted Label'] == 'positive':  # Kiểm tra nếu nhãn là "positive"
                st.markdown(
                    f"""
                    <style>
                    .intro-paragraph3 {{
                        margin-left: 10px; /* Thụt toàn bộ đoạn văn vào */
                        font-size: 1.2em; /* Kích thước chữ */
                        line-height: 1.5; /* Khoảng cách dòng */
                    }}
                    .positive-label {{
                        color: green; /* Màu xanh lá cho nhãn positive */
                        font-weight: bold; /* Làm đậm nhãn */
                    }}
                    </style>
                    <p class="intro-paragraph3">
                    <strong>{"- "*50} Nội dung {index+1} {"- "*50}<br></strong>
                    {row['noi_dung_binh_luan']}<br>
                    <span class="positive-label">🤩 {row['Predicted Label']}</span><br>
                    
                    </p>
                    """,
                    unsafe_allow_html=True)
            elif row['Predicted Label'] == 'negative':  # Kiểm tra nếu nhãn là "positive"
                st.markdown(
                    f"""
                    <style>
                    .negative-label {{
                        color: red; /* Màu xanh lá cho nhãn positive */
                        font-weight: bold; /* Làm đậm nhãn */
                    }}
                    </style>
                    <p class="intro-paragraph3">
                    <strong>{"- "*50} Nội dung {index+1} {"- "*50}<br></strong>
                    {row['noi_dung_binh_luan']}<br>
                    <span class="negative-label">😡 {row['Predicted Label']}</span><br>
                    
                    </p>
                    """,
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""
                    <style>
                    </style>
                    <p class="intro-paragraph3">
                    <strong>{"- "*50} Nội dung {index+1} {"- "*50}<br></strong>
                    {row['noi_dung_binh_luan']}<br>
                    <strong>😐 {row['Predicted Label']}<strong><br>
                    </p>
                    """,
                    unsafe_allow_html=True)
        st.markdown(
                f"""
                <style>
                .intro-paragraph {{
                    text-indent: 0px; /* Thụt lề đầu dòng */
                    margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
                    font-size: 1.5em; /* Kích thước chữ */
                    line-height: 1.5; /* Khoảng cách dòng */
                    text-align: justify; /* Canh đều đoạn văn */
                    font-style: italic; /* In nghiêng đoạn văn */
                }}
                </style>
                <p class="intro-paragraph">
                <strong>🧮 Xác suất nhãn:</strong>
                </p>
                """,
                unsafe_allow_html=True)
        def highlight_max_in_row(row):
            styles = ['background-color: yellow' if v == row[1:-1].max() else '' for v in row[1:-1]]  # Không highlight cột đầu và cột cuối
            styles.insert(0, '')
            styles.append('font-weight: bold; color: blue')  # Nhấn mạnh cột "Predicted Label" (cột cuối)
            return styles
        st.dataframe(result.style.apply(highlight_max_in_row, axis=1))


if type=="Nhập bình luận":    
    # Add custom CSS to adjust the font size
    # Text area input
    text = st.text_area(label="Nhập bình luận (mỗi bình luận xuống hàng):")

    if text!="":
        flag = True
        
        with st.spinner('Đang tải...'):
            du_doan = preprocess_sentiment_text(text, processor, positive_words, negative_words, positive_emojis, negative_emojis)

            du_doan_combined = x_with_engineering_model(du_doan, vectorizer_path='saved_models/count_vectorizer_model.pkl', scaler_path='saved_models/scaler_minmax.pkl')
            loaded_model = joblib.load('saved_models/Random_Forest_Classifier.pkl', mmap_mode='r')
    
            # Dự đoán nhãn
            predictions = loaded_model.predict(du_doan_combined)
            # Dự đoán xác suất
            probabilities = loaded_model.predict_proba(du_doan_combined)
        st.success("Xong!")

        # In xác suất theo từng mẫu
        st.markdown(
                f"""
                <style>
                .intro-paragraph {{
                    text-indent: 0px; /* Thụt lề đầu dòng */
                    margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
                    font-size: 1.5em; /* Kích thước chữ */
                    line-height: 1.5; /* Khoảng cách dòng */
                    text-align: justify; /* Canh đều đoạn văn */
                    font-style: italic; /* In nghiêng đoạn văn */
                }}
                </style>
                <p class="intro-paragraph">
                <strong>🧮 Dự đoán nhãn:</strong>
                </p>
                """,
                unsafe_allow_html=True)
        class_labels = loaded_model.classes_
        prob_df = pd.DataFrame(probabilities, columns=class_labels)
        prob_df["Predicted Label"] = predictions
        result = pd.merge(du_doan['noi_dung_binh_luan'], prob_df, left_index=True, right_index=True)
        
        for index, row in result.iterrows():
            if row['Predicted Label'] == 'positive':  # Kiểm tra nếu nhãn là "positive"
                st.markdown(
                    f"""
                    <style>
                    .intro-paragraph3 {{
                        margin-left: 10px; /* Thụt toàn bộ đoạn văn vào */
                        font-size: 1.2em; /* Kích thước chữ */
                        line-height: 1.5; /* Khoảng cách dòng */
                    }}
                    .positive-label {{
                        color: green; /* Màu xanh lá cho nhãn positive */
                        font-weight: bold; /* Làm đậm nhãn */
                    }}
                    </style>
                    <p class="intro-paragraph3">
                    <strong>{"- "*50} Nội dung {index+1} {"- "*50}<br></strong>
                    {row['noi_dung_binh_luan']}<br>
                    <span class="positive-label">🤩 {row['Predicted Label']}</span><br>
                    
                    </p>
                    """,
                    unsafe_allow_html=True)
            elif row['Predicted Label'] == 'negative':  # Kiểm tra nếu nhãn là "positive"
                st.markdown(
                    f"""
                    <style>
                    .negative-label {{
                        color: red; /* Màu xanh lá cho nhãn positive */
                        font-weight: bold; /* Làm đậm nhãn */
                    }}
                    </style>
                    <p class="intro-paragraph3">
                    <strong>{"- "*50} Nội dung {index+1} {"- "*50}<br></strong>
                    {row['noi_dung_binh_luan']}<br>
                    <span class="negative-label">😡 {row['Predicted Label']}</span><br>
                    
                    </p>
                    """,
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""
                    <style>
                    </style>
                    <p class="intro-paragraph3">
                    <strong>{"- "*50} Nội dung {index+1} {"- "*50}<br></strong>
                    {row['noi_dung_binh_luan']}<br>
                    <strong>😐 {row['Predicted Label']}<strong><br>
                    </p>
                    """,
                    unsafe_allow_html=True)
        st.markdown(
                f"""
                <style>
                .intro-paragraph {{
                    text-indent: 0px; /* Thụt lề đầu dòng */
                    margin-left: 0px; /* Thụt toàn bộ đoạn văn vào */
                    font-size: 1.5em; /* Kích thước chữ */
                    line-height: 1.5; /* Khoảng cách dòng */
                    text-align: justify; /* Canh đều đoạn văn */
                    font-style: italic; /* In nghiêng đoạn văn */
                }}
                </style>
                <p class="intro-paragraph">
                <strong>🧮 Xác suất nhãn:</strong>
                </p>
                """,
                unsafe_allow_html=True)
        def highlight_max_in_row(row):
            styles = ['background-color: yellow' if v == row[1:-1].max() else '' for v in row[1:-1]]  # Không highlight cột đầu và cột cuối
            styles.insert(0, '')
            styles.append('font-weight: bold; color: blue')  # Nhấn mạnh cột "Predicted Label" (cột cuối)
            return styles
        st.dataframe(result.style.apply(highlight_max_in_row, axis=1))

    