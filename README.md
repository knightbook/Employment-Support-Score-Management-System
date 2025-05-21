# 就労支援A型 スコア管理システム

就労継続支援A型事業所向けに、利用者のスコアを管理・評価・可視化するためのWebアプリケーションです。  
スコアの入力、集計、グラフ表示、CSV出力、支援記録管理などに対応予定です。

---

## 📂 プロジェクト構成

```text
Employment-Support-Score-Management-System/
├── project/ # Flaskアプリ本体
│ ├── app.py # メインアプリ
│ ├── templates/ # HTMLテンプレート（Jinja2）
│ └── static/ # CSS・画像など
├── docs/ # 設計・資料
│ ├── wireframes/ # ワイヤーフレーム（drawio, png）
│ ├── diagrams/ # クラス図・画面遷移図など
│ └── gantt_schedule.xlsx # ガントチャート
└── README.md # このファイル
```
---

## 🛠 使用技術

- **Python 3.x**
- **Flask** – 軽量Webフレームワーク
- **Jinja2** – テンプレートエンジン
- **Bootstrap 5** – CSSスタイリング（CDN利用）
- **SQLite**（予定）– 軽量DB

---

## 🚀 セットアップ手順（ローカル実行）

```bash
git clone https://github.com/knightbook/Employment-Support-Score-Management-System.git
cd project
pip install -r requirements.txt  # ← 未作成の場合は flask だけでOK
python app.py
```
初期状態でアクセス：
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