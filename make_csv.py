import pandas as pd
import glob
import re
import multiprocessing as mp

DATA_DIR = "/Users/mingyu/Downloads/020.주제별_텍스트_일상_대화_데이터/01.데이터/1.Training/원천데이터/TS_01._KAKAO(1)"

pattern = re.compile(r'^\s*\d+\s*[:：]\s*(.*)$')

def process_file(file_path):
    """하나의 txt 파일을 읽어서 '번호 제거된 문장' 리스트로 반환."""
    texts = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            m = pattern.match(line)
            clean_text = m.group(1) if m else line
            texts.append(clean_text)
    return texts


if __name__ == "__main__":
    txt_files = glob.glob(f"{DATA_DIR}/*.txt")
    print(f"총 txt 파일 개수: {len(txt_files)}")

    # 프로세스 개수 (기본: CPU 코어 수)
    num_workers = 4
    print(f"multiprocessing workers: {num_workers}")

    with mp.Pool(processes=num_workers) as pool:
        # 각 파일을 병렬로 처리
        results = pool.map(process_file, txt_files)

    # 결과 flatten
    all_texts = [text for file_texts in results for text in file_texts]

    # id, text, label 구성
    df = pd.DataFrame({
        "id": range(1, len(all_texts) + 1),
        "text": all_texts,
        "label": 0  # 정상 문자는 0
    })

    df.to_csv("normal_sms.csv", index=False, encoding="utf-8-sig")
    print(f"완료! → normal_sms.csv 생성됨 (총 {len(df)} 문장)")
