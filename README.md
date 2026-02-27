# 🏢 상업용 부동산 시장 분석 대시보드 (Real Estate Analysis Dashboard)

본 프로젝트는 상업용 부동산 매물 데이터를 인터랙티브하게 분석하고 시각화하는 **포트폴리오용 Streamlit 대시보드**입니다. 실무 수준의 코드 구조(Module Separation)와 데이터 전처리 파이프라인을 갖추고 있습니다.

## 🚀 프로젝트 개요
*   **목표**: 파편화된 매물 데이터를 정규화하고, 창업가 및 투자자 관점에서 핵심적인 지표(보증금, 월세, 권리금 비율 등)를 시각화하여 제공합니다.
*   **데이터 출처**: `data/raw_data.json` (가상의 상가 매물 샘플 데이터)

## 🛠️ 주요 기술 스택
*   **Language**: Python 3.10+
*   **Framework**: [Streamlit](https://streamlit.io/)
*   **Data Analysis**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
*   **Visualization**: [Plotly Express](https://plotly.com/python/plotly-express/)

## 📊 주요 분석 포인트
1.  **시장 스냅샷 (KPI)**: 총 매물 수 및 평균 가격 지표 실시간 추적.
2.  **보증금 시계열 분석**: 등록 시점별 시장 보증금 흐름 파악.
3.  **입지 기반 상관관계 분석**: 보증금 vs 월세의 비례 관계 및 면적/도보 소요 시간의 영향 시각화.
4.  **권리금 투자 위험도 분석**: 보증금 대비 권리금 비율(Premium Ratio) 분포 분석.

## 📁 프로젝트 구조
```text
real-estate-dashboard/
├── app.py                  # 메인 대시보드 어플리케이션
├── data/
│   └── raw_data.json       # 원본 JSON 데이터
├── dashboard_modules/      # (기존 utils) 핵심 분석 모듈 폴더
│   ├── __init__.py         # 패키지 인식 파일
│   ├── loader.py           # 데이터 로딩 및 정규화
│   ├── preprocess.py       # 데이터 전처리 및 파생 변수 생성
│   └── charts.py           # Plotly 시각화 관련 함수
├── requirements.txt         # 파이썬 의존성 패키지
├── README.md                # 프로젝트 문서
└── .gitignore               # 버전 관리 제외 설정
```

## 🛠️ 실행 방법 (Local)
1.  저장소 클론: `git clone <your-repository-url>`
2.  의존성 설치: `pip install -r requirements.txt`
3.  앱 실행: `streamlit run app.py`

## 🚀 배포 가이드 (GitHub & Streamlit Cloud)

### 1. GitHub 업로드
*   GitHub에 새로운 Public Repository를 생성합니다.
*   로컬 프로젝트 폴더에서 Git을 초기화하고 푸시합니다:
    ```bash
    git init
    git add .
    git commit -m "Initial commit: Real estate dashboard"
    git branch -M main
    git remote add origin <your-repo-url>
    git push -u origin main
    ```

### 2. Streamlit Cloud 연결
*   [Streamlit Cloud](https://share.streamlit.io/)에 접속하여 GitHub 계정으로 로그인합니다.
*   **'New app'** 버튼을 클릭합니다.
*   연결된 GitHub 저장소(`real-estate-dashboard`)와 브랜치(`main`)를 선택합니다.
*   **'Main file path'**에 `app.py`를 지정하고 **'Deploy!'**를 클릭합니다.

---
*Developed as a portfolio project by Antigravity Assistant.*
