from app import app, db
from models import Score, Client
from datetime import datetime
import random

user_list = [
    {"id": 1, "name": "テスト太郎"},
    {"id": 2, "name": "ダミー花子"},
    {"id": 3, "name": "モック三郎"},
]

with app.app_context():
    # ① 先に Client（利用者）レコードがDBに無い場合は必ず追加
    for user in user_list:
        client = Client.query.filter_by(id=user["id"]).first()
        if not client:
            client = Client(id=user["id"], name=user["name"])
            db.session.add(client)
    db.session.commit()

    # ② Score（スコア）ダミーデータ投入
    for user in user_list:
        for month in range(1, 13):
            date = datetime(2024, month, 1)
            total_max = 200

            # 値をランダム生成
            working_hours = random.randint(40, 120)
            production_res = random.randint(10, 70)
            diversity_vals = [random.randint(1, 5) for _ in range(4)]
            support_skill_vals = [random.randint(1, 5) for _ in range(3)]
            regional_score = random.randint(0, 20)
            improve_plan = random.randint(0, 15)
            skill_up = random.randint(0, 20)

            tmp_total = (
                working_hours + production_res +
                sum(diversity_vals) * 5 +
                sum(support_skill_vals) * 5 +
                regional_score + improve_plan + skill_up
            )

            while tmp_total > total_max:
                candidates = []
                if working_hours > 40: candidates.append('working_hours')
                if production_res > 10: candidates.append('production_res')
                if sum(diversity_vals) > 4: candidates.append('diversity')
                if sum(support_skill_vals) > 3: candidates.append('support_skill')
                if regional_score > 0: candidates.append('regional_score')
                if improve_plan > 0: candidates.append('improve_plan')
                if skill_up > 0: candidates.append('skill_up')
                if not candidates: break
                choice = random.choice(candidates)
                if choice == 'working_hours': working_hours -= 1
                elif choice == 'production_res': production_res -= 1
                elif choice == 'diversity':
                    i = diversity_vals.index(max(diversity_vals))
                    if diversity_vals[i] > 1: diversity_vals[i] -= 1
                elif choice == 'support_skill':
                    i = support_skill_vals.index(max(support_skill_vals))
                    if support_skill_vals[i] > 1: support_skill_vals[i] -= 1
                elif choice == 'regional_score': regional_score -= 1
                elif choice == 'improve_plan': improve_plan -= 1
                elif choice == 'skill_up': skill_up -= 1

                tmp_total = (
                    working_hours + production_res +
                    sum(diversity_vals) * 5 +
                    sum(support_skill_vals) * 5 +
                    regional_score + improve_plan + skill_up
                )

            diversity = ",".join(str(x) for x in diversity_vals)
            support_skill = ",".join(str(x) for x in support_skill_vals)
            num_users = random.randint(6, 20)
            average_wage = random.randint(47000, 55000)
            employment_rate = random.randint(60, 100)

            score = Score(
                client_id=user["id"],              # 利用者ID
                staff_user_id=1,                   # 入力スタッフID（本番は適宜変更）
                created_at=date,
                working_hours=working_hours,
                production_res=production_res,
                diversity=diversity,
                support_skill=support_skill,
                regional_score=regional_score,
                improve_plan=improve_plan,
                skill_up=skill_up,
                num_users=num_users,
                average_wage=average_wage,
                employment_rate=employment_rate,
                production_json='{}',
                memo=f"ダミーデータ（{user['name']})"
            )

            score.total = (
                score.working_hours + score.production_res +
                sum(int(x) for x in diversity.split(",")) * 5 +
                sum(int(x) for x in support_skill.split(",")) * 5 +
                score.regional_score + score.improve_plan + score.skill_up
            )
            db.session.add(score)
    db.session.commit()
    print("✅ 3名の利用者ごとに12ヶ月分ずつダミーデータを追加しました")
