"""
팀원 업무현황 대시보드 — Streamlit
실행: streamlit run dashboard.py
"""
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="팀원 업무현황 대시보드", layout="wide")
st.title("📋 팀원 업무현황 대시보드")
st.caption("팀별 진행률 · 지연 태스크 추적")

df = pd.read_excel("files/팀원_업무현황.xlsx")
df.columns = [c.replace("(%)", "").strip() for c in df.columns]

col1, col2, col3, col4 = st.columns(4)
col1.metric("전체 태스크", len(df))
col2.metric("완료", (df["상태"] == "완료").sum())
col3.metric("진행중", (df["상태"] == "진행중").sum())
col4.metric("지연", (df["상태"] == "지연").sum(), delta_color="inverse")

# 팀별 진행률 막대그래프
st.subheader("팀별 평균 진행률")
team_progress = df.groupby("팀")["진행률"].mean().reset_index()
chart = alt.Chart(team_progress).mark_bar().encode(
    x=alt.X("팀:N", sort="-y"),
    y=alt.Y("진행률:Q", title="평균 진행률 (%)"),
    color=alt.Color("진행률:Q", scale=alt.Scale(scheme="greens"))
).properties(height=300)
st.altair_chart(chart, use_container_width=True)

# 지연 태스크 빨간색 강조
st.subheader("⚠️ 지연 태스크")
delayed = df[df["상태"] == "지연"]
if len(delayed) > 0:
    st.dataframe(
        delayed.style.applymap(lambda v: "background-color: #fee2e2", subset=["상태"]),
        use_container_width=True
    )
else:
    st.success("지연 태스크 없음 🎉")

# 전체 태스크 테이블
st.subheader("전체 태스크")
st.dataframe(df, use_container_width=True)
