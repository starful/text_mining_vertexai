import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from fugashi import Tagger
from fugashi import GenericTagger

# ✅ ipadic 경로 명시
tagger = GenericTagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/ipadic")

# ✅ 형태소 분석 함수
def tokenize_ja(text):
    tokens = []
    for word in tagger(text):
        features = word.feature  # tuple로 반환됨
        if len(features) > 0 and features[0] in ["名詞", "動詞", "形容詞"]:
            tokens.append(word.surface)
    return tokens

# ✅ 키워드 스코어 계산
def get_keywords(text):
    tfidf = TfidfVectorizer(tokenizer=tokenize_ja)
    tfidf_matrix = tfidf.fit_transform([text])
    feature_names = tfidf.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    return dict(zip(feature_names, scores))

# ✅ 워드클라우드 생성
def generate_wordcloud(keyword_score: dict):
    wc = WordCloud(
        font_path="/usr/share/fonts/truetype/ipafont-gothic/ipagp.ttf",  # 일본어 글꼴
        background_color="white",
        width=800,
        height=400,
        colormap="tab20"
    ).generate_from_frequencies(keyword_score)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig

# ✅ Streamlit 화면 구성
st.set_page_config(page_title="日本語ワードクラウド", layout="wide")
st.title("🧠 日本語キーワードクラウド (TF-IDF)")

text = st.text_area("✏️ 日本語のテキストを入力してください", height=300)

if st.button("ワードクラウド生成") and text.strip():
    st.info("⏳ キーワード抽出中...")
    keywords = get_keywords(text)
    fig = generate_wordcloud(keywords)
    st.success("✅ 以下にワードクラウドを表示します")
    st.pyplot(fig)
