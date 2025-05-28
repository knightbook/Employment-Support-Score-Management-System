"""
就労支援A型スコア管理システム  Flask アプリ
---------------------------------------------
- ログイン / 新規登録
- スタッフ（User）単位のログイン管理
- スコア入力・保存（利用者ごとに記録／様式 2-1, 2-2 対応）
- スコア一覧表示（自分が入力した分 or 全体 or 利用者ごと切り替え可）
- スコア集計・グラフ表示（棒／折れ線／レーダー、全体・個別切り替え）
- CSV出力対応
SQLite + SQLAlchemy で永続化
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, Response
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Client, Score
from datetime import datetime
import json
import os
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "your_secret_key"  # TODO: 本番は環境変数で管理する

# フィルター等（例）
from utils.filters import display_labels, DIVERSITY_LABELS, SUPPORT_SKILL_LABELS

@app.template_filter('display_diversity')
def display_diversity_filter(value):
    return display_labels(value, DIVERSITY_LABELS)

@app.template_filter('display_support_skill')
def display_support_skill_filter(value):
    return display_labels(value, SUPPORT_SKILL_LABELS)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "instance", "essms.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
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
            session["username"] = user.username
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
    clients = Client.query.order_by(Client.name.asc()).all()  # 利用者リスト

    def safe_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    if request.method == "POST":
        client_id = int(request.form.get("client_id", 0))
        if not client_id:
            flash("利用者を選択してください。")
            return render_template("score_input.html", clients=clients, current_user=user)

        production_json = {}
        for i in (1, 2, 3):
            production_json[f"year_{i}"] = request.form.get(f"year_{i}", "")
            production_json[f"income_{i}"] = safe_int(request.form.get(f"income_{i}"))
            production_json[f"wage_{i}"] = safe_int(request.form.get(f"wage_{i}"))
            production_json[f"note_income_{i}"] = request.form.get(f"note_income_{i}", "")

        sc = Score(
            client_id      = client_id,
            staff_user_id  = session["user_id"],
            created_at     = datetime.now(),
            working_hours   = safe_int(request.form.get("working_hours")),
            production_res  = safe_int(request.form.get("production_result")),
            diversity       = ",".join(request.form.getlist("diversity[]")),
            support_skill   = ",".join(request.form.getlist("support_skill[]")),
            regional_score  = safe_int(request.form.get("regional_activity_checked")),
            improve_plan    = safe_int(request.form.get("improve_plan")),
            skill_up        = safe_int(request.form.get("user_skill_up")),
            num_users       = safe_int(request.form.get("num_users")),
            average_wage    = safe_int(request.form.get("average_wage")),
            employment_rate = safe_int(request.form.get("employment_rate")),
            production_json = json.dumps(production_json, ensure_ascii=False),
            memo            = request.form.get("memo", "")
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

    return render_template("score_input.html", 
                           clients=clients, 
                           current_user=user,
                           menu_nav=True)

# ------------------------------------------------------------------
# スコア一覧
# ------------------------------------------------------------------
@app.route("/score_list")
def score_list():
    if "user_id" not in session:
        return redirect(url_for("login"))

    client_id = request.args.get("client_id", "")
    clients = Client.query.order_by(Client.name.asc()).all()

    query = Score.query.order_by(Score.created_at.desc())
    if client_id:
        query = query.filter(Score.client_id == int(client_id))
    scores = query.all()
    return render_template("score_list.html",
                            scores=scores,
                            clients=clients, 
                            client_id=client_id,
                            menu_nav=True)


# ------------------------------------------------------------------
# スコア集計・グラフ表示（全体・個別切り替え）
# ------------------------------------------------------------------
@app.route("/aggregate", methods=["GET"])
def aggregate():
    if "user_id" not in session:
        flash("ログインしてください。")
        return redirect(url_for("login"))

    start_date_str = request.args.get("start_date", datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d"))
    end_date_str = request.args.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    graph_type = request.args.get("graph_type", "line")
    client_id = request.args.get("client_id", "")  # 利用者ID（全体の場合は空）

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        flash("日付の形式が正しくありません。")
        return redirect(url_for("aggregate"))

    clients = Client.query.order_by(Client.name.asc()).all()

    # データセットを組み立て
    datasets = []
    dates = []
    if client_id:  # 利用者指定あり
        client = Client.query.get(int(client_id))
        scores = (
            Score.query
            .filter(
                Score.client_id == int(client_id),
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
        sorted_dates = sorted(aggregate_data.keys())
        dates = sorted_dates
        data = [aggregate_data[d] for d in sorted_dates]
        datasets.append({"label": client.name if client else f"ID:{client_id}", "data": data})
        total_score = sum(data)
        avg_score = total_score / len(data) if data else 0
    else:  # 全体
        # 全利用者で日付ごとに合算
        all_scores = (
            Score.query
            .filter(
                Score.created_at >= start_date,
                Score.created_at <= end_date
            )
            .order_by(Score.created_at.asc())
            .all()
        )
        # 日付ごとに利用者ごと合計
        aggregate_by_client = {}
        for sc in all_scores:
            date_key = sc.created_at.strftime("%Y-%m-%d")
            if sc.client_id not in aggregate_by_client:
                aggregate_by_client[sc.client_id] = {}
            aggregate_by_client[sc.client_id][date_key] = aggregate_by_client[sc.client_id].get(date_key, 0) + sc.total

        # すべての日付を抽出
        all_dates = set()
        for dmap in aggregate_by_client.values():
            all_dates |= set(dmap.keys())
        dates = sorted(all_dates)

        # 各利用者のデータ系列
        for cid, dmap in aggregate_by_client.items():
            client = Client.query.get(cid)
            data = [dmap.get(date, 0) for date in dates]
            # ここで「clientがNone」の場合にも備える！
            datasets.append({"label": client.name if client else f"ID:{cid}", "data": data})
        total_score = sum([sum(ds["data"]) for ds in datasets])
        total_count = sum([len(ds["data"]) for ds in datasets])
        avg_score = total_score / total_count if total_count else 0

    return render_template("aggregate.html",
                           dates=dates,
                           datasets=datasets,
                           total_score=total_score,
                           avg_score=avg_score,
                           start_date=start_date_str,
                           end_date=end_date_str,
                           graph_type=graph_type,
                           clients=clients,
                           client_id=client_id,
                           menu_nav=True)


# ------------------------------------------------------------------
# CSV出力
# ------------------------------------------------------------------
@app.route("/aggregate/csv_full")
def download_csv_full():
    if "user_id" not in session:
        flash("ログインしてください。")
        return redirect(url_for("login"))

    start_date_str = request.args.get("start_date", datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d"))
    end_date_str = request.args.get("end_date", datetime.now().strftime("%Y-%m-%d"))
    client_id = request.args.get("client_id", "")

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        flash("日付の形式が正しくありません。")
        return redirect(url_for("aggregate"))

    if client_id:
        scores = (
            Score.query
            .filter(
                Score.client_id == int(client_id),
                Score.created_at >= start_date,
                Score.created_at <= end_date
            )
            .order_by(Score.created_at.asc())
            .all()
        )
    else:
        scores = (
            Score.query
            .filter(
                Score.created_at >= start_date,
                Score.created_at <= end_date
            )
            .order_by(Score.created_at.asc())
            .all()
        )

    si = StringIO()
    writer = csv.writer(si)

    # ヘッダー
    writer.writerow([
        "登録日", "利用者", "入力者", "稼働時間", "生産結果", "多様な働き方", "支援力向上",
        "地域連携", "経営改善", "知識向上", "利用者数", "平均賃金", "雇用率", "備考", "合計スコア"
    ])

    for sc in scores:
        writer.writerow([
            sc.created_at.strftime("%Y-%m-%d"),
            sc.client.name if sc.client else "",
            sc.staff_user.username if sc.staff_user else "",
            sc.working_hours,
            sc.production_res,
            sc.diversity,
            sc.support_skill,
            sc.regional_score,
            sc.improve_plan,
            sc.skill_up,
            sc.num_users,
            sc.average_wage,
            sc.employment_rate or "",
            sc.memo or "",
            sc.total
        ])

    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=score_details.csv"}
    )

# ------------------------------------------------------------------
# アプリ起動
# ------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
