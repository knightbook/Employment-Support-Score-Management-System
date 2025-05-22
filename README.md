# 就労支援A型 スコア管理システム

就労継続支援A型事業所向けに、利用者のスコアを管理・評価・可視化するためのWebアプリケーションです。  
スコアの入力、集計、グラフ表示、CSV出力、支援記録管理などに対応予定です。

---

## 📂 プロジェクト構成

```text
Employment-Support-Score-Management-System/
│
├── project/                  # Flaskアプリ本体
│   ├── app.py               # メインアプリ
│   ├── templates/           # HTMLテンプレート（Jinja2）
│   ├── static/              # CSS・画像など
│   └── blueprints/          # Flask Blueprint構成（ログイン、スコア管理など）
│
├── docs/                    # 設計・資料
│   ├── wireframes/          # ワイヤーフレーム（drawio, png）
│   ├── diagrams/            # クラス図・画面遷移図など
│   └── gantt_schedule.xlsx  # ガントチャート
│
├── requirements.txt         # 必要パッケージ一覧
└── README.md                # このファイル
```
---

## 🛠 使用技術

### 🔙 バックエンド
- **Python 3.x**
- **Flask** – 軽量Webフレームワーク
- **Jinja2** – テンプレートエンジン（Flask組み込み）
- **SQLite** – 軽量データベース（ファイルベース）
- **SQLAlchemy** – ORM（オブジェクト関係マッピング）

### 🎨 フロントエンド
- **HTML5 / CSS3**
- **Bootstrap 5** – モバイルファーストなCSSフレームワーク（CDN利用）
- **JavaScript** – フォームバリデーションなどに利用予定

### ⚙ その他・開発ツール
- **Git / GitHub** – バージョン管理
- **draw.io** – ワイヤーフレーム・図作成
- **Excel / Googleスプレッドシート** – ガントチャート、仕様管理
- **venv** – 仮想環境構築

---

## 🚀 セットアップ手順（ローカル実行）

1. このリポジトリをクローン
```bash
git clone https://github.com/knightbook/Employment-Support-Score-Management-System.git
cd Employment-Support-Score-Management-System
```
2.Python仮想環境を作成して有効化（推奨）
```bash
python -m venv venv #←先ずはこちらをコマンド入力実行

# macOS/Linux環境の方は下記のコマンドを入力実行
source venv/bin/activate
# Windows環境の方は下記のコマンドをコピペ
venv\Scripts\Activate.ps1
```
3.依存パッケージをインストール
```bash
pip install -r requirements.txt
```
4.Flaskアプリのあるディレクトリに移動し起動
```bash
cd project
python app.py
```
5.ブラウザでアクセス
http://127.0.0.1:5000/

---

## 📊 ドキュメント

- [画面遷移図を見る](docs/spec/screen_transition.png)

- [クラス図を見る](docs/spec/class_diagram.md)

- [ER図を見る](docs/spec/er_diagram.md)

- [ガントチャートを見るExcel](docs/gantt_schedule.xlsx)
- [ガントチャートを見るスプレッドシート](https://docs.google.com/spreadsheets/d/1azG9TA4BbKPsPT6v6eGvHxt8wK9uoPRG2MnWV8D-lPI/edit?usp=sharing)

---

## 📌 ライセンス / 著作権
このリポジトリは開発学習目的で使用されています。
商用利用または業務導入の際は別途ライセンスに従ってください。

---

## 👤 開発者
GitHub: @knightbook

開発補助: ChatGPT（OpenAI）