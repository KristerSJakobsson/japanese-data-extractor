### Constants used for analysing data are seperated into 4 types as per below
separators = dict()
prefixes = dict()
suffixes = dict()
special_values = dict()

### Values for the above types are defined per below
## General
separators["dash"] = ["-", "‐", "ー", "―", "－"]
separators["blank"] = [" ", "　"]
separators["slash"] = ["/"]
separators["left_parenthesis"] = ["(", "（"]
separators["right_parenthesis"] = [")", "）"]
separators["comma"] = [",", "、", "，"]
separators["colon"] = [":", "、", "："]

## Type specific
# Currency
prefixes["currency"] = ["￥", "\\", "JPY"]
suffixes["currency"] = ["円", "日本円", "Yen"]

# Age
suffixes["age"] = ["才", "歳"]
special_values["age_zero"] = ["ゼロ"]  # ゼロ歳

# Date
prefixes["date_relative_month"] = ["前月", "今月", "本月", "来月", "再来月"]
prefixes["date_relative_year"] = ["去年", "今年", "来年", "本年", "再来年"]
prefixes["date_japanese_year"] = ["平成", "昭和"]
suffixes["date_japanese_year"] = ["年"]
suffixes["date_japanese_month"] = ["月"]
suffixes["date_japanese_day"] = ["日"]   # These are suffixes that if found will be considered a date
suffixes["date_japanese_day_exceptions"] = ["日目", "日間"]

# Time
prefixes["time_hour"] = ["午後", "午前"]
suffixes["time_hour"] = ["時"]
suffixes["time_minute"] = ["分"]
suffixes["time_hour_like"] = ["時限", "時間"]
special_values["time_half_hour"] = ["半"]

# Postal Code
prefixes["postal_code"] = ["T", "〒", "🏣", "〶"]


