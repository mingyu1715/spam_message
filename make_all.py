import pandas as pd

normal_df = pd.read_csv("normal_sms.csv")  # text, label(0)
spam_df   = pd.read_csv("spam_sms.csv")    # text, label(1)

print("normal:", len(normal_df), "spam:", len(spam_df))

# 혹시 필요없는 컬럼 있으면 여기서 정리
normal_df = normal_df[["text", "label"]]
spam_df   = spam_df[["text", "label"]]

# 합치기
all_df = pd.concat([normal_df, spam_df], ignore_index=True)

# 셔플
all_df = all_df.sample(frac=1, random_state=42).reset_index(drop=True)

# id 새로 부여
all_df.insert(0, "id", all_df.index + 1)

all_df.to_csv("sms_all.csv", index=False, encoding="utf-8-sig")
print("총 샘플 수:", len(all_df))
