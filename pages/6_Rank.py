import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="게임 랭킹", layout="wide")
st.title("🏆 게임 랭킹")

st.write("클릭 게임의 최고 점수들을 확인하세요!")

# 점수 파일 경로
SCORES_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'game_scores.json')

# 점수 로드 함수
def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

# 점수 데이터 로드
scores = load_scores()

# 메인 컨텐츠
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 클릭 게임 랭킹")

    if not scores:
        st.info("아직 플레이한 게임이 없습니다. 게임을 플레이해보세요!")
    else:
        # 상위 7개 점수 표시
        top_scores = scores[:7]

        # 랭킹 표시
        for i, score_data in enumerate(top_scores, 1):
            with st.container():
                # 등수에 따른 이모지
                rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

                col_rank, col_score, col_player, col_date = st.columns([1, 2, 2, 2])

                with col_rank:
                    st.write(f"**{rank_emojis[i-1]} {i}위**")

                with col_score:
                    st.metric("점수", f"{score_data['score']}점")

                with col_player:
                    st.write(f"**플레이어:** {score_data['player']}")

                with col_date:
                    st.write(f"**날짜:** {score_data['date']}")

                st.divider()

        # 통계 정보
        st.subheader("📊 통계")
        total_games = len(scores)
        avg_score = sum(s['score'] for s in scores) / total_games if total_games > 0 else 0
        highest_score = max((s['score'] for s in scores), default=0)

        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("총 게임 수", total_games)
        with col_stat2:
            st.metric("평균 점수", ".1f")
        with col_stat3:
            st.metric("최고 점수", highest_score)

with col2:
    st.subheader("🎮 게임 정보")

    st.write("""
    **게임 규칙:**
    - 30초 동안 버튼 클릭
    - 각 버튼: +10점
    - 빠를수록 높은 점수!

    **랭킹 기준:**
    - 점수 높은 순
    - 동점일 경우 먼저 플레이한 순서
    """)

    # 새로고침 버튼
    if st.button("🔄 랭킹 새로고침", use_container_width=True):
        st.rerun()

    # 점수 초기화 버튼 (관리용)
    if st.button("🗑️ 랭킹 초기화", use_container_width=True, type="secondary"):
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)
        st.success("랭킹이 초기화되었습니다!")
        st.rerun()

# 최근 게임 기록
if scores:
    st.subheader("📅 최근 게임 기록")

    # 최근 5게임 표시
    recent_scores = scores[-5:] if len(scores) >= 5 else scores
    recent_scores.reverse()  # 최신순으로 표시

    for i, score_data in enumerate(recent_scores, 1):
        with st.container():
            st.write(f"**게임 {len(scores) - len(recent_scores) + i}**")
            st.write(f"점수: {score_data['score']}점 | 플레이어: {score_data['player']} | {score_data['timestamp']}")
            if i < len(recent_scores):
                st.divider()

# 푸터
st.divider()
st.write("© 2026. 클릭 게임 랭킹 시스템")

# 스타일링
st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)