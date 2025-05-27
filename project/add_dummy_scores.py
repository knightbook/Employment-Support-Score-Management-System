'''
ダミーデータを追加するスクリプト
このスクリプトは、2024年の各月に対してダミーデータを追加します。
'''

from app import app, db
from models import Score
from datetime import datetime
import random

with app.app_context():
    for month in range(1, 13):
        date = datetime(2024, month, 1)
        score = Score(
            user_id=1,  # 必要なら変更してください
            created_at=date,
            working_hours=90,
            production_res=50,
            diversity="1,1,1,1",
            support_skill="1,1,1",
            regional_score=10,
            improve_plan=0,
            skill_up=10,
            num_users=10,
            average_wage=50000,
            employment_rate=80,
            production_json='{}',
            memo="ダミーデータ",
            inputter_name="テスト太郎"
        )
        score.total = (
            score.working_hours + score.production_res +
            len(score.diversity.split(",")) * 5 +
            len(score.support_skill.split(",")) * 5 +
            score.regional_score + score.improve_plan + score.skill_up
        )
        db.session.add(score)
    db.session.commit()
    print("✅ ダミーデータを12件追加しました")
