"""
就労支援A型スコア管理システム  Flask アプリ
---------------------------------------------
- ログイン / 新規登録
- スコア入力・保存（様式 2-1, 2-2 対応）
- スコア一覧表示
SQLite + SQLAlchemy で永続化
"""

from datetime import datetime
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# アプリ基本設定
# ============================================================
app = Flask(__name__)
app.secret_key = 'your_secret_key'          # TODO: 本番は環境変数に
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///essms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ============================================================
# DB モデル定義
# ============================================================
class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email    = db.Column(db.String(120))

class Score(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    # --- 様式 2-1 ------------------------------------------------
    working_hours   = db.Column(db.Integer, default=0)
    production_res  = db.Column(db.Integer, default=0)
    diversity       = db.Column(db.Text)           # CSV 文字列
    support_skill   = db.Column(db.Text)           # CSV 文字列
    regional_score  = db.Column(db.Integer, default=0)
    improve_plan    = db.Column(db.Integer, default=0)
    skill_up        = db.Column(db.Integer, default=0)

    # --- 様式 2-2 ------------------------------------------------
    num_users       = db.Column(db.Integer)
    average_wage    = db.Column(db.Integer)
    employment_rate = db.Column(db.Integer)
    production_json = db.Column(db.Text)           # 年度別収支を JSON で保存

    memo            = db.Column(db.Text)
    total           = db.Column(db.Integer, default=0)

# 初回のみ下記 2 行を Python シェル等で実行
# >>> from app import db
# >>> db.create_all()

# ============================================================
# 認証系ルート
# ============================================================
@app.route('/', methods=['GET', 'POST'])
def login():
    """ログイン画面 & 認証処理"""
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['userId']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        flash('ユーザーIDまたはパスワードが違います。')
    return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """新規ユーザー登録"""
    if request.method == 'POST':
        uid      = request.form['userId']
        pwd      = request.form['password']
        pwd2     = request.form['passwordConfirm']
        email    = request.form['email']

        if not uid or not pwd or not email:
            flash('必須項目を入力してください。')
        elif pwd != pwd2:
            flash('パスワードが一致しません。')
        elif User.query.filter_by(username=uid).first():
            flash('このユーザーIDは既に存在します。')
        else:
            user = User(username=uid,
                        password=generate_password_hash(pwd),
                        email=email)
            db.session.add(user); db.session.commit()
            flash('登録が完了しました。ログインしてください。')
            return redirect(url_for('login'))
    return render_template('sign_up.html')

@app.route('/logout')
def logout():
    """ログアウト"""
    session.clear()
    flash('ログアウトしました。')
    return redirect(url_for('login'))

# ============================================================
# メインメニュー
# ============================================================
@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))
    return render_template('home.html')

# ============================================================
# スコア入力
# ============================================================
@app.route('/score_input', methods=['GET', 'POST'])
def score_input():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # ---- フォーム値取得 ------------------------------------
        sc = Score(
            user_id         = session['user_id'],
            working_hours   = int(request.form.get('working_hours', 0)),
            production_res  = int(request.form.get('production_result', 0)),
            diversity       = ','.join(request.form.getlist('diversity[]')),
            support_skill   = ','.join(request.form.getlist('support_skill[]')),
            regional_score  = int(request.form.get('regional_activity_checked') or 0),
            improve_plan    = int(request.form.get('improve_plan', 0)),
            skill_up        = int(request.form.get('user_skill_up', 0)),
            num_users       = int(request.form.get('num_users', 0)),
            average_wage    = int(request.form.get('average_wage', 0)),
            employment_rate = int(request.form.get('employment_rate', 0)),
            memo            = request.form.get('memo', '')
        )
        # TODO: 年度別収支テーブル→JSON 保存
        # --------------------------------------------------------

        # ---- 合計点計算（簡易） ---------------------------------
        sc.total = (
            sc.working_hours + sc.production_res +
            len(sc.diversity.split(','))*5 +
            len(sc.support_skill.split(','))*5 +
            sc.regional_score + sc.improve_plan + sc.skill_up
        )
        # ---------------------------------------------------------
        db.session.add(sc); db.session.commit()
        flash(f"スコアを登録しました。（合計 {sc.total} 点）")
        return redirect(url_for('score_list'))

    return render_template('score_input.html')

# ============================================================
# スコア一覧
# ============================================================
@app.route('/score_list')
def score_list():
    if 'user_id' not in session: return redirect(url_for('login'))
    user_scores = Score.query.filter_by(user_id=session['user_id']).order_by(Score.created_at.desc()).all()
    return render_template('score_list.html', scores=user_scores)

# ============================================================
# プレースホルダ ルート（今後実装）
# ============================================================
@app.route('/user_list')
def user_list():
    return "<h3>ユーザー一覧（開発中）</h3>"

@app.route('/aggregate')
def aggregate():
    return "<h3>集計・グラフ表示（開発中）</h3>"

@app.route('/data_management')
def data_management():
    return "<h3>データ管理（開発中）</h3>"

@app.route('/help')
def help():
    return "<h3>ヘルプページ（開発中）</h3>"

# ============================================================
# アプリ起動
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)
