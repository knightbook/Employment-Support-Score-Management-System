from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'   # FIXME: 本番環境では環境変数などで設定

# ===== 仮ユーザー辞書（本来はDB） =====
users = {"testuser": "1234"}

# ✨ 仮スコア保存（後でDBに置き換え） --------------------------
scores = []        # 1件 = dict で保存する簡易リスト

# ---------- ログイン ----------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        password = request.form.get('password')

        if user_id in users and users[user_id] == password:
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            flash('ユーザーIDまたはパスワードが違います。')
            return redirect(url_for('login'))

    return render_template('login.html')

# ---------- 新規ユーザー登録 ----------
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        password = request.form.get('password')
        password_confirm = request.form.get('passwordConfirm')
        email = request.form.get('email')

        if not user_id or not password or not email:
            flash('必須項目を入力してください。')
        elif password != password_confirm:
            flash('パスワードが一致しません。')
        elif user_id in users:
            flash('このユーザーIDはすでに使われています。')
        else:
            users[user_id] = password
            flash('登録が完了しました。ログインしてください。')
            return redirect(url_for('login'))

    return render_template('sign_up.html')

# ---------- ホーム ----------
@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))
    return render_template('home.html')

# ---------- スコア入力 ✨ ----------
@app.route('/score_input', methods=['GET', 'POST'])
def score_input():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # フォーム値を取得
        score_data = {
            'user_id': session['user_id'],
            'working_hours': int(request.form.get('working_hours', 0)),
            'production_result': int(request.form.get('production_result', 0)),
            'diversity': request.form.getlist('diversity[]'),
            'support_skill': request.form.getlist('support_skill[]'),
            'memo': request.form.get('memo', '')
        }

        # 合計点（多様な働き方や支援力向上は項目ごとに 5 点を仮で加算）
        total = score_data['working_hours'] + score_data['production_result']
        total += len(score_data['diversity']) * 5
        total += len(score_data['support_skill']) * 5
        score_data['total'] = total

        # 保存（後でDBへ変更予定）
        scores.append(score_data)

        flash(f"スコアを登録しました。（合計 {total} 点）")
        return redirect(url_for('score_list'))

    # GET → フォーム表示
    return render_template('score_input.html')

# ---------- スコア一覧 ✨ ----------
@app.route('/score_list')
def score_list():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))

    # 自分のスコアのみ表示
    user_scores = [s for s in scores if s['user_id'] == session['user_id']]
    return render_template('score_list.html', scores=user_scores)

# ---------- ユーザー一覧 ----------
@app.route('/user_list')
def user_list():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))
    return "<h3>ユーザー一覧画面（開発中）</h3>"

# ---------- 集計 / グラフ表示（プレースホルダ） ----------
@app.route('/aggregate')
def aggregate():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))
    return "<h3>集計・グラフ表示画面（開発中）</h3>"

# ---------- データ管理（プレースホルダ） ----------
@app.route('/data_management')
def data_management():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))
    return "<h3>データ管理画面（開発中）</h3>"

# ---------- ヘルプ ----------
@app.route('/help')
def help():
    if 'user_id' not in session:
        flash('ログインしてください。')
        return redirect(url_for('login'))
    return "<h3>ヘルプページ（開発中）</h3>"

# ---------- ログアウト ----------
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました。')
    return redirect(url_for('login'))

# ---------- エントリーポイント ----------
if __name__ == '__main__':
    app.run(debug=True)
