import pandas as pd

# 스팸 파일 4개 경로 (실제 파일명에 맞게 수정)
spam_files = [
    "spam1.csv",
    "spam2.csv",
    "spam3.csv",
    "spam4.csv",
]

dfs = []

for path in spam_files:
    df = pd.read_csv(path)  # 인코딩 문제 있으면 encoding="cp949" 또는 "utf-8-sig" 시도
    # CN 컬럼만 가져오고 이름을 text로 통일
    df = df[["CN"]].rename(columns={"CN": "text"})
    dfs.append(df)

# 하나로 합치기 + 인덱스 리셋
spam_all = pd.concat(dfs, ignore_index=True)

# id, label 컬럼 생성
spam_all.insert(0, "id", spam_all.index + 1)  # 1부터 시작
spam_all["label"] = 1  # 스팸 = 1

# 저장
spam_all.to_csv("spam_sms.csv", index=False, encoding="utf-8-sig")

print(spam_all.head())
print("완료! → spam_sms.csv 생성됨")
