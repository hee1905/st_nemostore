import plotly.express as px
import pandas as pd

def render_timeseries_chart(df: pd.DataFrame):
    """1. 보증금 평균 시계열 추이"""
    # 날짜별 평균 보증금 계산
    daily_avg = df.groupby('date_only')['deposit'].mean().reset_index()
    fig = px.line(daily_avg, x='date_only', y='deposit',
                  title="📅 등록 일자별 평균 보증금 추이",
                  labels={'date_only': '등록일', 'deposit': '평균 보증금 (만원)'},
                  markers=True,
                  template="plotly_white")
    return fig

def render_rent_histogram(df: pd.DataFrame):
    """2. 월세 분포 히스토그램"""
    fig = px.histogram(df, x='monthlyRent',
                       title="📊 월세 금액대 분포",
                       labels={'monthlyRent': '월세 (만원)', 'count': '매물 수'},
                       nbins=15,
                       template="plotly_white",
                       color_discrete_sequence=['#636EFA'])
    fig.update_layout(yaxis_title="매물 수")
    return fig

def render_business_avg_bar(df: pd.DataFrame):
    """3. 업종별 평균 보증금 바 차트"""
    avg_deposit = df.groupby('businessMiddleCodeName')['deposit'].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(avg_deposit, x='businessMiddleCodeName', y='deposit',
                 title="🏢 업종별 평균 보증금",
                 labels={'businessMiddleCodeName': '업종', 'deposit': '평균 보증금 (만원)'},
                 color='deposit',
                 color_continuous_scale='Viridis',
                 template="plotly_white")
    return fig

def render_price_scatter(df: pd.DataFrame):
    """4. 보증금 vs 월세 관계 산점도"""
    fig = px.scatter(df, x='deposit', y='monthlyRent',
                     color='businessMiddleCodeName',
                     size='size',
                     title="💰 보증금 vs 월세 상관관계 (버블 크기=면적)",
                     labels={'deposit': '보증금 (만원)', 'monthlyRent': '월세 (만원)', 'businessMiddleCodeName': '업종'},
                     hover_data=['title', 'floor', 'nearSubwayStation'],
                     template="plotly_white")
    return fig

def render_ratio_boxplot(df: pd.DataFrame):
    """5. 권리금/보증금 비율 분포 박스플롯"""
    fig = px.box(df, x='businessMiddleCodeName', y='premium_ratio',
                 title="📉 업종별 권리금 대비 보증금 비율 분포",
                 labels={'businessMiddleCodeName': '업종', 'premium_ratio': '권리금/보증금 비율'},
                 points="all",
                 hover_data=['title', 'premium', 'deposit'],
                 template="plotly_white")
    return fig
