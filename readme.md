# SMS Spam Classification Project

## Overview
이 프로젝트는 한국어 SMS 데이터를 기반으로 스팸 문자 자동 분류 모델을 구축하는 것을 목표로 한다.  
실제 환경에서 수집된 대규모 스팸 문자와 정상 일상문자 데이터를 활용하여 텍스트 기반 머신러닝 모델을 학습하고, 스팸 여부를 자동 판별할 수 있는 시스템을 개발한다.

데이터 총 문장 수: **약 78만 문장 (스팸 38만 + 일반 40만)**

---

## Dataset

### 1. 정상(일반) SMS 데이터  
- 출처: AI-Hub 일상 대화 데이터  
- 링크: https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=543  
- 약 40만 문장 사용  
- 특징  
  - 일상 대화 기반  
  - 짧은 문장부터 긴 문장까지 다양  
  - 번호 형식(`1:`, `2:`)으로 구성된 텍스트를 전부 문장 단위로 정제함  
  - 개인정보 마스킹(예: `***`, `OOO`) 포함

### 2. 스팸 SMS 데이터  
- 출처: 경찰청 빅데이터 플랫폼 스팸문자 데이터  
- 링크: https://www.bigdata-policing.kr/product/view?product_id=PRDT_395  
- 약 38만 문장 사용  
- 특징  
  - 광고성, 금융사기, 피싱, URL 난독화, 특수문자 기반 스팸 포함  
  - 이모지·외국어·한자 포함 스팸 존재  
  - 개인정보, 전화번호 등은 `***` 등으로 마스킹  
  - 다양한 난독화 기법(ifg@, ○○○, 특수문자 섞기, URL 변형 등)이 포함됨

---

## Preprocessing

### 1. 정상 데이터 정제
- 각 txt 파일에 포함된 `1 : 문장`, `2 : 문장` 형식 제거  
- 번호를 제거하고 순수 문장만 추출  
- 공백 제거 및 비어있는 라인 필터링  
- 하나의 CSV(`normal_sms.csv`)로 통합

### 2. 스팸 데이터 정제
- 원본 CSV의 각 행에서 스팸 문장 추출  
- 특수문자, 이모지, URL 등 스팸 패턴을 손상시키지 않도록 **최소 전처리 전략** 적용  
- 하나의 CSV(`spam_sms.csv`)로 구성

### 3. 단일 통합 데이터셋 생성
- 두 데이터프레임 결합 후 셔플  
- `id`, `text`, `label` 구조로 통일  
  - label=0 → 정상  
  - label=1 → 스팸  
- 최종 CSV: `sms_all.csv`

---

## Modeling

### Feature Extraction (TF-IDF)
- 문자 기반 n-gram 적용  
- 설정: `char_wb`, ngram_range=(3,5)  
- 난독화 패턴, URL 변형, 기호 반복 등 스팸 특성을 반영하기 위한 방식  
- max_features=100,000 기준

### Models
- **Multinomial Naive Bayes**  
  - 빠른 베이스라인 구축용  
  - 대규모 텍스트 데이터에서도 효율적  
- **Linear Support Vector Machine (LinearSVC)**  
  - TF-IDF 문자 n-gram 기반 분류에서 강력한 성능  
  - 고차원 sparse feature에 최적화된 선형 분류기  

---