import streamlit as st
import pandas as pd
import altair as alt

# --- 데이터 불러오기 (캐싱 적용) ---
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# --- 사이드바 / 사용자 선택 ---
st.set_page_config(page_title="MBTI 국가별 분석", page_icon="🌍")
st.title("🌍 국가별 MBTI 분포 TOP 3")
st.markdown("국가를 선택하면 해당 국가에서 **비율이 가장 높은 MBTI 3가지 유형**을 확인할 수 있어요.")

# 국가 선택
countries = df["Country"].tolist()
selected_country = st.selectbox("📌 분석할 국가를 선택하세요", countries)

# --- 선택한 국가의 데이터 처리 ---
row = df[df["Country"] == selected_country].iloc[0]
mbti_scores = row.drop("Country")
top3 = mbti_scores.sort_values(ascending=False).head(3).reset_index()
top3.columns = ["MBTI", "비율"]

# --- 시각화 ---
st.subheader(f"📈 {selected_country}에서 가장 높은 MBTI 유형")

chart = alt.Chart(top3).mark_bar(color="mediumseagreen").encode(
    x=alt.X("MBTI", sort="-y"),
    y=alt.Y("비율", title="비율"),
    tooltip=["MBTI", "비율"]
).properties(
    width=500,
    height=300
)

st.altair_chart(chart, use_container_width=True)

# --- 비율 텍스트로도 표시 ---
for i, row in top3.iterrows():
    st.write(f"{i+1}. **{row['MBTI']}** — {row['비율']:.2%}")

# 푸터
st.markdown("---")
st.caption("📘 데이터: 국가별 MBTI 분포 / 제작: ChatGPT")
