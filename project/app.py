"""
就労支援A型スコア管理システム  Flask アプリ
---------------------------------------------
- ログイン / 新規登録
- スコア入力・保存（様式 2-1, 2-2 対応）
- スコア一覧表示
- スコア集計・グラフ表示（棒／折れ線／レーダー）
SQLite + SQLAlchemy で永続化
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Score
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # TODO: 本番は環境変数で管理する
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///essms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ------------------------------------------------------------------
# 認証系ルート
# ------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["userId"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            return redirect(url_for("home"))
        flash("ユーザーIDまたはパスワードが違います。")
    return render_template("login.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user_name = request.form.get("userName", "").strip()
        password  = request.form.get("password", "").strip()
        if not user_name or not password:
            flash("氏名とパスワードを入力してください。")
            return redirect(url_for("sign_up"))

        if User.query.filter_by(username=user_name).first():
            flash("その氏名はすでに登録されています。")
            return redirect(url_for("sign_up"))

        hashed_password = generate_password_hash(password)
        db.session.add(User(username=user_name, password=hashed_password))
        db.session.commit()
        flash("登録完了しました。ログインしてください。")
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("ログアウトしました。")
    return redirect(url_for("login"))

# ------------------------------------------------------------------
# メインメニュー
# ------------------------------------------------------------------
@app.route("/home")
def home():
    if "user_id" not in session:
        flash("ログインしてください。")
        return redirect(url_for("login"))
    return render_template("home.html")

# ------------------------------------------------------------------
# スコア入力
# ------------------------------------------------------------------
@app.route("/score_input", methods=["GET", "POST"])
def score_input():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        # 年度別収支を JSON にまとめる
        production_json = {}
        for i in (1, 2, 3):
            production_json[f"year_{i}"] = request.form.get(f"year_{i}", "")
            production_json[f"income_{i}"] = int(request.form.get(f"income_{i}", 0))
            production_json[f"wage_{i}"] = int(request.form.get(f"wage_{i}", 0))
            production_json[f"note_income_{i}"] = request.form.get(f"note_income_{i}", "")

        sc = Score(
            user_id        = session["user_id"],
            working_hours  = int(request.form.get("working_hours", 0)),
            production_res = int(request.form.get("production_result", 0)),
            diversity      = ",".join(request.form.getlist("diversity[]")),
            support_skill  = ",".join(request.form.getlist("support_skill[]")),
            regional_score = int(request.form.get("regional_activity_checked") or 0),
            improve_plan   = int(request.form.get("improve_plan", 0)),
            skill_up       = int(request.form.get("user_skill_up", 0)),
            num_users      = int(request.form.get("num_users", 0)),
            average_wage   = int(request.form.get("average_wage", 0)),
            employment_rate= int(request.form.get("employment_rate", 0)),
            production_json= json.dumps(production_json, ensure_ascii=False),
            memo           = request.form.get("memo", ""),
            inputter_name  = request.form.get("inputter_name", "")
        )

        sc.total = (
            sc.working_hours + sc.production_res +
            len(sc.diversity.split(",")) * 5 +
            len(sc.support_skill.split(",")) * 5 +
            sc.regional_score + sc.improve_plan + sc.skill_up
        )
        db.session.add(sc)
        db.session.commit()
        flash(f"スコアを登録しました。（合計 {sc.total} 点）")
        return redirect(url_for("score_list"))

    return render_template("score_input.html", current_user=user)


# ------------------------------------------------------------------
# スコア一覧
# ------------------------------------------------------------------
@app.route("/score_list")
def score_list():
    if "user_id" not in session:
        return redirect(url_for("login"))
    scores = (
        Score.query
        .filter_by(user_id=session["user_id"])
        .order_by(Score.created_at.desc())
        .all()
    )
    return render_template("score_list.html", scores=scores)

# ------------------------------------------------------------------
# スコア集計・グラフ表示
# ------------------------------------------------------------------
@app.route("/aggregate", methods=["GET"])
def aggregate():
    if "user_id" not in session:
        flash("ログインしてください。")
        return redirect(url_for("login"))

    # パラメータ受け取り
    start_date_str = request.args.get(
        "start_date",
        datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d")
    )
    end_date_str = request.args.get(
        "end_date",
        datetime.now().strftime("%Y-%m-%d")
    )
    graph_type = request.args.get("graph_type", "line")  # line / bar / radar

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        flash("日付の形式が正しくありません。")
        return redirect(url_for("aggregate"))

    # データ抽出 & 集計
    scores = (
        Score.query
        .filter(
            Score.user_id == session["user_id"],
            Score.created_at >= start_date,
            Score.created_at <= end_date
        )
        .order_by(Score.created_at.asc())
        .all()
    )

    aggregate_data = {}
    for sc in scores:
        date_key = sc.created_at.strftime("%Y-%m-%d")
        aggregate_data[date_key] = aggregate_data.get(date_key, 0) + sc.total

    total_score = sum(aggregate_data.values())
    avg_score   = total_score / len(aggregate_data) if aggregate_data else 0

    sorted_dates = sorted(aggregate_data.keys())
    totals       = [aggregate_data[d] for d in sorted_dates]

    return render_template(
        "aggregate.html",
        dates=sorted_dates,
        totals=totals,
        total_score=total_score,
        avg_score=avg_score,
        start_date=start_date_str,
        end_date=end_date_str,
        graph_type=graph_type
    )

# ------------------------------------------------------------------
# プレースホルダ（将来機能追加用）
# ------------------------------------------------------------------
@app.route("/user_list")
def user_list():
    return "<h3>ユーザー一覧（開発中）</h3>"

@app.route("/data_management")
def data_management():
    return "<h3>データ管理（開発中）</h3>"

@app.route("/help")
def help():
    return "<h3>ヘルプページ（開発中）</h3>"

# ------------------------------------------------------------------
# アプリ起動
# ------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
