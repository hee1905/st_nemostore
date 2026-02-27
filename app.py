import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 커스텀 모듈 임포트
from utils.loader import load_raw_data
from utils.preprocess import preprocess_data
import utils.charts as charts

# 1️⃣ 페이지 기본 설정
st.set_page_config(layout="wide", page_title="상업용 부동산 시장 분석 대시보드", page_icon="🏢")

def main():
    # 헤더 섹션
    st.title("🏙️ 상업용 부동산 시장 분석 대시보드")
    st.markdown("""
    이 대시보드는 상가 매물 데이터를 기반으로 가격 구조와 시장 트렌드를 분석합니다. 
    좌측 필터를 통해 관심 조건에 맞는 데이터를 실시간으로 탐색할 수 있습니다.
    """)

    # 2️⃣ 데이터 로드 및 전처리
    raw_df = load_raw_data("data/raw_data.json")
    if raw_df.empty:
        st.warning("데이터 로드 중 문제가 발생했습니다.")
        return

    df = preprocess_data(raw_df)

    # 3️⃣ Sidebar 필터 구성
    st.sidebar.header("🔍 분석 필터 설정")
    
    # 업종 선택
    all_business = sorted(df['businessMiddleCodeName'].unique())
    selected_business = st.sidebar.multiselect("업종(중분류) 선택", all_business, default=all_business)
    
    # 층 범위 선택
    min_floor, max_floor = int(df['floor'].min()), int(df['floor'].max())
    selected_floor = st.sidebar.slider("층 범위", min_floor, max_floor, (min_floor, max_floor))
    
    # 보증금 범위 선택
    min_dep, max_dep = int(df['deposit'].min()), int(df['deposit'].max())
    selected_deposit = st.sidebar.slider("보증금 범위 (만원)", min_dep, max_dep, (min_dep, max_dep))
    
    # 날짜 범위 선택
    min_date = df['date_only'].min()
    max_date = df['date_only'].max()
    selected_date_range = st.sidebar.date_input("등록 일자 범위", [min_date, max_date], min_value=min_date, max_value=max_date)

    # 필터링 적용
    # 날짜 필터는 리스트로 돌아올 때와 단일 값일 때를 처리
    if isinstance(selected_date_range, (list, tuple)) and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
    else:
        start_date = end_date = selected_date_range[0] if isinstance(selected_date_range, list) else selected_date_range

    mask = (
        df['businessMiddleCodeName'].isin(selected_business) &
        (df['floor'].between(selected_floor[0], selected_floor[1])) &
        (df['deposit'].between(selected_deposit[0], selected_deposit[1])) &
        (df['date_only'].between(start_date, end_date))
    )
    filtered_df = df[mask]

    if filtered_df.empty:
        st.warning("⚠️ 선택한 조건에 맞는 매물이 없습니다. 필터를 조정해 주세요.")
        return

    # 4️⃣ 상단 KPI 섹션
    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("총 매물 수", f"{len(filtered_df):,}개")
    with k2:
        avg_dep = filtered_df['deposit'].mean()
        st.metric("평균 보증금", f"{avg_dep:,.0f}만원")
    with k3:
        avg_rent = filtered_df['monthlyRent'].mean()
        st.metric("평균 월세", f"{avg_rent:,.0f}만원")
    with k4:
        avg_prem = filtered_df['premium'].mean()
        st.metric("평균 권리금", f"{avg_prem:,.0f}만원")

    st.markdown("---")

    # 5️⃣ 시각화 섹션 (구조화된 배치)
    
    # Row 1: 시계열 추이 및 월세 분포
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.plotly_chart(charts.render_timeseries_chart(filtered_df), use_container_width=True)
        st.caption("등록 시점별 평균 보증금의 흐름을 보여줍니다.")
    with col1_2:
        st.plotly_chart(charts.render_rent_histogram(filtered_df), use_container_width=True)
        st.caption("시장에 형성된 주요 월세 구간을 확인할 수 있습니다.")

    # Row 2: 업종별 비교 및 상관관계
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.plotly_chart(charts.render_business_avg_bar(filtered_df), use_container_width=True)
        st.caption("주요 업종별 보증금 규모의 차이를 비교합니다.")
    with col2_2:
        st.plotly_chart(charts.render_price_scatter(filtered_df), use_container_width=True)
        st.caption("보증금과 월세의 비례 관계 및 면적(버블 크기) 효과를 보여줍니다.")

    # Row 3: 투자 효율 분포 (Boxplot)
    st.plotly_chart(charts.render_ratio_boxplot(filtered_df), use_container_width=True)
    st.caption("보증금 대비 권리금의 비중을 통해 업종별 투자 위험도와 매몰 비용 수준을 가늠할 수 있습니다.")

    st.markdown("---")

    # 6️⃣ 추가 인사이트 및 Raw 데이터
    left_inf, right_inf = st.columns([2, 1])
    
    with left_inf:
        st.subheader("💡 자동 분석 인사이트")
        max_business = filtered_df.groupby('businessMiddleCodeName')['deposit'].mean().idxmax()
        highest_dep = filtered_df.groupby('businessMiddleCodeName')['deposit'].mean().max()
        
        insight_msg = f"""
        - 현재 필터링된 데이터 중 **{max_business}** 업종의 평균 보증금이 **{highest_dep:,.0f}만원**으로 가장 높게 형성되어 있습니다.
        - 보증금 대비 권리금 비율의 중앙값은 **{filtered_df['premium_ratio'].median():.2f}** 수준입니다.
        - 총 면적 대비 보증금 효율(단가)이 가장 높은 매물의 면적은 **{filtered_df.loc[filtered_df['deposit_per_sqm'].idxmax(), 'size']:.1f}㎡**입니다.
        """
        st.info(insight_msg)

    with right_inf:
        st.subheader("📥 데이터 내보내기")
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="CSV 파일 다운로드",
            data=csv,
            file_name=f"real_estate_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )

    with st.expander("🔍 원본 데이터 레이어 보기"):
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
