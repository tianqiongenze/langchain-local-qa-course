# LangChain RAG Demo

本リポジトリは、**RAG（Retrieval-Augmented Generation）** の仕組みを利用した簡易的な QA（質疑応答）システムとジョーク生成機能のデモです。  
主に **LangChain**、**OpenAI API**、**BM25 + FAISS** によるドキュメント検索技術を組み合わせて動作します。

---

## プロジェクト概要

- **目的**  
  社内文書や大量データを取り込んだ後、それらを効率的に検索しながら回答を生成する仕組み（RAG）を試作・学習するために作成したデモプロジェクトです。

- **機能**  
  1. **QA 機能**：特定のデータセットをもとに質問に答える。  
  2. **ジョーク生成**：指定したトピックに関するジョークを生成。  
  3. **FastAPI サーバ**：ブラウザまたは API 経由で簡単に機能をテストできます。

- **想定シナリオ**  
  - 企業内の大量 PDF・テキストから必要な情報を素早く検索し、要約して回答する。  
  - ユーザが与えたトピックをもとに、LLM を活用したコンテンツ生成のサンプルを確認する。

---

## 必要環境・前提

1. **Python バージョン**  
   - **Python 3.10** を利用する例で作成していますが、学習目的であれば 3.12 など新しいバージョンでも試すことを推奨しています。  
   - ただし、最新版では一部ライブラリが未対応の可能性があるため、適宜バージョンを調整してください。

2. **OpenAI API Key**  
   - `.env` ファイルなどに `OPENAI_API_KEY=sk-**********` を設定してください。

3. **httpx のバージョン注意**  
   - httpx はプロジェクトによってはバグや互換性の問題が起きる場合があります。  
   - 特定のバージョンが必要な場合は `pip install "httpx==<バージョン>"` のように指定します。

---

## セットアップ手順

### 1. Python インストール

- システムに Python 3.10 または 3.12 をインストールしてください。  
- Anaconda や公式インストーラなどお好みの方法で導入可能です。

### 2. 仮想環境を作成 & 有効化

- **Anaconda の例**  
  ```bash
  conda create -n rag-demo python=3.10
  conda activate rag-demo
  ```

- **venv の例**  
  ```bash
  python -m venv venv
  source venv/bin/activate  # Mac/Linux
  .\venv\Scripts\activate   # Windows
  ```

### 3. 依存ライブラリをインストール

#### A) 手動インストール（推奨）
```bash
pip install -U openai langchain langchain-core python-dotenv loguru tyro
pip install "langserve[all]"
pip install rank-bm25 faiss-cpu tiktoken
```
※ httpx の特定バージョンが必要な場合は `pip install "httpx==<バージョン>"` を利用してください。

#### B) requirements.txt を使う場合
- `pip install -r requirements.txt` で一括インストールができますが、衝突回避のために個別インストールが推奨されています。
- 必要に応じて `requirements.txt` 内のバージョンを調整してください。

### 4. .env ファイルの作成
プロジェクト直下（またはコードが指定する場所）に `.env` を作成し、以下のように記載:
```bash
OPENAI_API_KEY=sk-***************
OPENAI_API_BASE=https://api.openai.com/v1
```
> **注意**: `.env` は API キーを含むため、`.gitignore` に含めて **公開しない** ようにしてください。

## 実行方法

### メインスクリプトの起動
```bash
python src/main.py
```
ログに `Running on http://localhost:8005` のような出力があれば正常に起動しています。

### API / Playground の確認
- ブラウザで `http://localhost:8005/docs` にアクセスし、Swagger UI を使ってエンドポイントをテストできます。
- また、`/qa/playground` と `/joke/playground` にアクセスすると、GUI 形式のフォームで入力→出力を確認できます。

## サンプルスクリーンショット

### QA Playground
例：「RAGの本質は何ですか？」と入力すると、ドキュメント検索と回答生成が行われます。

### ジョーク生成
例：「猫」や「音楽」などのトピックを入力すると、指定トピックに沿ったジョークが生成されます。

## 注意事項
- 本プロジェクトはデモ用途のため、ライセンスやセキュリティ面の検証は最小限です。運用環境での利用時は十分な検証を行ってください。
- OpenAI API の使用には有効な API Key と場合によってはクレジットカード登録が必要です。Rate Limit や Quota に注意してください。
- httpx、langchain などはバージョン違いに伴うバグや警告が発生する可能性があるため、必要に応じて適宜調整してください。

## 今後の拡張
- **大規模データ対応**：PDF、Markdown、Webサイトからのデータ取り込みと検索精度向上。
- **LLM の切り替え**：Azure OpenAI やローカル LLM との連携など。
- **クラウドデプロイ / Docker 化**：本番環境への展開、チーム内での共有の効率化。

## 参考
- [LangChain](https://python.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [langserve](https://github.com/langchain-ai/langserve)
- [faiss](https://github.com/facebookresearch/faiss)


