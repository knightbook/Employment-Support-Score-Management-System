from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class ScoreRecord(db.Model):
    __tablename__ = 'score_records'

    id = db.Column(db.Integer, primary_key=True)

    # スタッフ名（ログインユーザー）
    staff_name = db.Column(db.String(100), nullable=False)

    # 入力期間
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)

    # 利用者（client_id と新規利用者名のどちらかが入る）
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    new_client_name = db.Column(db.String(100), nullable=True)

    # 様式2-1
    working_hours = db.Column(db.Integer, nullable=False)  # 90, 80, ...
    production_result = db.Column(db.Integer, nullable=False)  # 60, 50, ...
    
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
    improve_plan = db.Column(db.Integer, nullable=False)  # 0 or -50

    # 利用者の知識・能力向上
    user_skill_up = db.Column(db.Integer, nullable=False)  # 10 or 0

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
