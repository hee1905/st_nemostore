import pandas as pd
import re
from typing import Optional

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    데이터 타입 변환 및 분석을 위한 파생 변수를 생성합니다.
    """
    if df.empty:
        return df
    
    # 1. 숫자 컬럼 변환
    numeric_cols = ['deposit', 'monthlyRent', 'premium', 'maintenanceFee', 'size', 'floor']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 2. 날짜 컬럼 변환
    if 'createdDateUtc' in df.columns:
        df['createdDateUtc'] = pd.to_datetime(df['createdDateUtc'])
        df['date_only'] = df['createdDateUtc'].dt.date
    
    # 3. 파생 변수 생성
    # 면적당 보증금 (deposit / size)
    df['deposit_per_sqm'] = df['deposit'] / df['size']
    
    # 권리금/보증금 비율 (premium / deposit)
    # 분모가 0인 경우 처리
    df['premium_ratio'] = df.apply(lambda x: x['premium'] / x['deposit'] if x['deposit'] > 0 else 0, axis=1)
    
    # 도보 시간 추출 (nearSubwayStation 문자열 파싱)
    def extract_walk_time(text: Optional[str]) -> Optional[int]:
        if pd.isna(text) or text is None:
            return None
        match = re.search(r'도보\s*(\d+)분', str(text))
        return int(match.group(1)) if match else None
    
    if 'nearSubwayStation' in df.columns:
        df['subway_minutes'] = df['nearSubwayStation'].apply(extract_walk_time)
    
    # 결측치 처리 (수치형 0으로 채우기 등)
    df = df.fillna({
        'deposit': 0,
        'monthlyRent': 0,
        'premium': 0,
        'maintenanceFee': 0,
        'subway_minutes': pd.NA # 도보 시간은 NA 유지 (추세선용)
    })
    
    return df
