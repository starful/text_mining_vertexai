# Text Mining with Vertex AI 🎯

日本語テキストを入力し、TF-IDFベースのキーワード抽出とワードクラウドを生成する Streamlit アプリです。  
Google Cloud Vertex AI と fugashi(MeCab) を活用しています。

## 🔧 Features

- 日本語形態素解析（fugashi + MeCab）
- TF-IDF によるキーワードスコアリング
- WordCloud による視覚化
- Streamlit + GCP Cloud Run によるデプロイ対応

## 🚀 How to Deploy (Cloud Run)

```bash
gcloud builds submit --no-cache --tag gcr.io/dev-sungwhan-han/text-mining-summary-gemini

gcloud run deploy text-mining-summary-gemini \
  --image gcr.io/dev-sungwhan-han/text-mining-summary-gemini \
  --platform managed \
  --region us-central1 \
  --memory=2Gi \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=dev-sungwhan-han,REGION=us-central1
