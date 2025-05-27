from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # 利用者 → スコア
    scores = db.relationship('Score', back_populates='client', cascade="all, delete-orphan")
    score_records = db.relationship('ScoreRecord', back_populates='client', cascade="all, delete-orphan")

class User(db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email    = db.Column(db.String(120))
    # スタッフ → スコア
    scores = db.relationship('Score', back_populates='staff_user')
    score_records = db.relationship('ScoreRecord', back_populates='staff_user')

class Score(db.Model):
    __tablename__ = 'scores'
    id            = db.Column(db.Integer, primary_key=True)
    client_id     = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)      # 利用者
    staff_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)        # 入力者（スタッフ）
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    # 入力者名（オプション: 履歴用に残す場合のみ、通常はリレーションでOK）
    inputter_name = db.Column(db.String(100))   

    # 様式 2-1
    working_hours   = db.Column(db.Integer, default=0)
    production_res  = db.Column(db.Integer, default=0)
    diversity       = db.Column(db.Text)     # CSV形式
    support_skill   = db.Column(db.Text)     # CSV形式
    regional_score  = db.Column(db.Integer, default=0)
    improve_plan    = db.Column(db.Integer, default=0)
    skill_up        = db.Column(db.Integer, default=0)

    # 様式 2-2
    num_users       = db.Column(db.Integer)
    average_wage    = db.Column(db.Integer)
    employment_rate = db.Column(db.Integer)
    production_json = db.Column(db.Text)     # 年度別収支（JSON）

    memo            = db.Column(db.Text)
    total           = db.Column(db.Integer, default=0)

    # リレーション
    client = db.relationship('Client', back_populates='scores')
    staff_user = db.relationship('User', back_populates='scores')

class ScoreRecord(db.Model):
    __tablename__ = 'score_records'

    id = db.Column(db.Integer, primary_key=True)

    staff_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 入力者
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)    # 利用者

    # 入力期間
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)

    # 様式2-1
    working_hours = db.Column(db.Integer, nullable=False)
    production_result = db.Column(db.Integer, nullable=False)
    
    # 多様な働き方
    diversity_license = db.Column(db.Boolean, default=False)
    diversity_promotion = db.Column(db.Boolean, default=False)
    diversity_sidejob = db.Column(db.Boolean, default=False)

    # 支援力向上
    support_training = db.Column(db.Boolean, default=False)
    support_seminar = db.Column(db.Boolean, default=False)
    support_eval_system = db.Column(db.Boolean, default=False)

    # 地域連携活動
    regional_activity_checked = db.Column(db.Boolean, default=False)
    
    # 経営改善計画
    improve_plan = db.Column(db.Integer, nullable=False)
    user_skill_up = db.Column(db.Integer, nullable=False)

    # 様式2-2
    num_users = db.Column(db.Integer, nullable=False)
    average_wage = db.Column(db.Integer, nullable=False)
    employment_rate = db.Column(db.Integer, nullable=True)

    # 生産活動 - 年度別収支（3年分）
    year_1 = db.Column(db.String(10), nullable=True)
    income_1 = db.Column(db.Integer, nullable=True)
    wage_1 = db.Column(db.Integer, nullable=True)
    note_income_1 = db.Column(db.String(200), nullable=True)

    year_2 = db.Column(db.String(10), nullable=True)
    income_2 = db.Column(db.Integer, nullable=True)
    wage_2 = db.Column(db.Integer, nullable=True)
    note_income_2 = db.Column(db.String(200), nullable=True)

    year_3 = db.Column(db.String(10), nullable=True)
    income_3 = db.Column(db.Integer, nullable=True)
    wage_3 = db.Column(db.Integer, nullable=True)
    note_income_3 = db.Column(db.String(200), nullable=True)

    # Ⅲ. 多様な働き方 具体的取組
    diversity_desc = db.Column(db.Text, nullable=True)
    # Ⅳ. 支援力向上 具体的取組
    support_desc = db.Column(db.Text, nullable=True)
    # Ⅴ. 地域連携活動 詳細
    regional_activity_desc = db.Column(db.Text, nullable=True)
    # Ⅵ. 経営改善計画 詳細
    plan_desc = db.Column(db.Text, nullable=True)
    # Ⅶ. 利用者の知識・能力向上 具体的支援
    skillup_desc = db.Column(db.Text, nullable=True)
    # 備考
    memo = db.Column(db.Text, nullable=True)

    # リレーション
    client = db.relationship('Client', back_populates='score_records')
    staff_user = db.relationship('User', back_populates='score_records')
