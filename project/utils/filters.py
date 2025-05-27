# utils/filters.py

DIVERSITY_LABELS = {
    "license": "①免許・資格取得支援制度",
    "promotion": "②職員への登用制度",
    "sidejob1": "③副業・兼業の容認",
    "flextime": "④フレックスタイム制に係る労働条件",
    "shorttime": "⑤短縮時間勤務に係る労働条件",
    "staggered": "⑥時差出勤制度に係る労働条件",
    "paidleave": "⑦有給休暇の時間単位取得又は計画的付与制度",
    "sickleave": "⑧傷病休暇等の取得に関する事項"
}

SUPPORT_SKILL_LABELS = {
    "training": "①研修計画に基づいた外部研修会又は内部研修会",
    "seminar": "②研修、学会等又は学会誌等において発表",
    "inspection": "③視察・実習の実施又は受け入れ",
    "trade_meeting": "④販路拡大の商談会等への参加",
    "evaluation_system": "⑤職員の人事評価制度",
    "peer_supporter": "⑥ピアサポーターの配置",
    "third_party_evaluation": "⑦第三者評価",
    "certification": "⑧国際標準化企画が定めた規格等の認証等"
}

def display_labels(csv_string, label_dict):
    if not csv_string:
        return "-"
    keys = [s.strip() for s in csv_string.split(',')]
    return ', '.join([label_dict.get(k, f"[{k}]") for k in keys])
