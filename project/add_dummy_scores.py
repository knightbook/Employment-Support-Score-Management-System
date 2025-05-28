from app import app, db
from models import Score, Client
from datetime import datetime
import random
import math

user_list = [
    {"id": 1, "name": "テスト太郎"},
    {"id": 2, "name": "ダミー花子"},
    {"id": 3, "name": "モック三郎"},
]

with app.app_context():
    # ① 利用者レコード追加
    for user in user_list:
        client = Client.query.filter_by(id=user["id"]).first()
        if not client:
            client = Client(id=user["id"], name=user["name"])
            db.session.add(client)
    db.session.commit()

    # ② スコア・ダミーデータ
    for user in user_list:
        base_bias = random.randint(-20, 20)  # 各利用者で全体的に強弱をつける
        for month in range(1, 13):
            date = datetime(2024, month, 1)
            total_max = 200

            # 「周期性＋乱数」混ぜてランダム性を強調
            phase = random.uniform(-math.pi, math.pi)
            amplitude = random.randint(10, 25)
            # 各項目も波＋乱数で生成
            working_hours   = int(60 + amplitude * math.sin(month + phase) + random.randint(-15, 15) + base_bias)
            production_res  = int(25 + amplitude * math.cos(month * 1.5 + phase) + random.randint(-10, 10))
            diversity_vals  = [random.randint(1, 5) for _ in range(4)]
            support_skill_vals = [random.randint(1, 5) for _ in range(3)]
            regional_score  = random.randint(0, 20)
            improve_plan    = random.choice([0, random.randint(1, 15)])  # 0の月も
            skill_up        = random.choice([0, random.randint(5, 20)])

            # 必ず上限に収めるロジック
            tmp_total = (
                working_hours + production_res +
                sum(diversity_vals) * 5 +
                sum(support_skill_vals) * 5 +
                regional_score + improve_plan + skill_up
            )

            # 下限保証も(例: 80点未満は引き上げ)
            min_total = 80
            while tmp_total > total_max or tmp_total < min_total:
                # 上限超なら一部減算
                if tmp_total > total_max:
                    idx = random.randint(0, 3)
                    if diversity_vals[idx] > 1: diversity_vals[idx] -= 1
                    if support_skill_vals[idx % 3] > 1: support_skill_vals[idx % 3] -= 1
                    if working_hours > 40: working_hours -= 2
                    if production_res > 10: production_res -= 2
                    if regional_score > 0: regional_score -= 1
                    if improve_plan > 0: improve_plan -= 1
                    if skill_up > 0: skill_up -= 1
                # 下限割れは少し加算
                elif tmp_total < min_total:
                    idx = random.randint(0, 3)
                    if diversity_vals[idx] < 5: diversity_vals[idx] += 1
                    if support_skill_vals[idx % 3] < 5: support_skill_vals[idx % 3] += 1
                    if working_hours < 120: working_hours += 2
                    if production_res < 70: production_res += 2
                    if regional_score < 20: regional_score += 1
                    if improve_plan < 15: improve_plan += 1
                    if skill_up < 20: skill_up += 1
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
                client_id=user["id"],
                staff_user_id=1,  # 入力スタッフID（本番は適宜変更）
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
