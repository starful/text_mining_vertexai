FROM python:3.10-slim

WORKDIR /app

# 🔧 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    mecab \
    libmecab-dev \
    fonts-ipafont-gothic \
    curl \
    build-essential \
    file \
    xz-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ✅ MeCab IPADIC 설치 (표준 경로에 설치되도록 명시)
RUN cd /tmp && \
    curl -L -o mecab-ipadic.tar.gz "https://downloads.sourceforge.net/project/mecab/mecab-ipadic/2.7.0-20070801/mecab-ipadic-2.7.0-20070801.tar.gz" && \
    tar -zxvf mecab-ipadic.tar.gz && \
    cd mecab-ipadic-2.7.0-20070801 && \
    ./configure --with-charset=utf8 --prefix=/usr && \
    make && \
    make install && \
    cd / && rm -rf /tmp/*

# ✅ mecabrc 설정 (fugashi가 참조 가능하도록 보장)
RUN if [ -f /etc/mecabrc ]; then cp /etc/mecabrc /usr/local/etc/mecabrc; fi

# ✅ Python 패키지 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 앱 복사
COPY . .

RUN find /usr -name dicrc

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
