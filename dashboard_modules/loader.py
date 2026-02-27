import json
import pandas as pd
import streamlit as st
from typing import Optional

@st.cache_data
def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    JSON 파일에서 'items' 데이터를 로드하여 DataFrame으로 변환합니다.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # items 키 내부의 리스트를 평면화하여 로드
        df = pd.json_normalize(data["items"])
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()
