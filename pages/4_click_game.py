import streamlit as st
import time
import random
import json
import os
from datetime import datetime

st.set_page_config(page_title="클릭 게임", layout="wide")
st.title("🎯 마우스 클릭 게임")

st.write("화면에 나타나는 버튼들을 빠르게 클릭해서 점수를 얻으세요!")

# 점수 저장 파일 경로
SCORES_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'game_scores.json')

# 데이터 디렉토리 생성
os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)

# 점수 로드 함수
def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

# 점수 저장 함수
def save_score(score, player_name="플레이어"):
    scores = load_scores()
    new_score = {
        'score': score,
        'player': player_name,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    scores.append(new_score)

    # 점수로 정렬 (내림차순)
    scores.sort(key=lambda x: x['score'], reverse=True)

    # 상위 10개만 유지
    scores = scores[:10]

    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'time_left' not in st.session_state:
    st.session_state.time_left = 30
if 'buttons' not in st.session_state:
    st.session_state.buttons = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# 게임 시작 함수
def start_game():
    st.session_state.game_started = True
    st.session_state.score = 0
    st.session_state.time_left = 30
    st.session_state.start_time = time.time()
    generate_buttons()

# 게임 종료 함수
def end_game():
    st.session_state.game_started = False
    if st.session_state.score > 0:  # 점수가 0보다 크면 저장
        save_score(st.session_state.score)
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

# 버튼 생성 함수
def generate_buttons():
    st.session_state.buttons = []
    for i in range(3):  # 3개의 버튼으로 줄임 (쉬워짐)
        button_id = f"btn_{i}_{random.randint(1000, 9999)}"
        st.session_state.buttons.append({
            'id': button_id,
            'clicked': False,
            'x': random.randint(0, 3),  # 그리드 위치
            'y': random.randint(0, 2)
        })

# 버튼 클릭 함수
def click_button(button_id):
    if st.session_state.game_started:
        for btn in st.session_state.buttons:
            if btn['id'] == button_id and not btn['clicked']:
                btn['clicked'] = True
                st.session_state.score += 10
                break
        # 모든 버튼이 클릭되었으면 새 버튼 생성
        if all(btn['clicked'] for btn in st.session_state.buttons):
            generate_buttons()

# 게임 UI
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.subheader("📊 점수")
    st.metric("현재 점수", st.session_state.score)
    st.metric("최고 점수", st.session_state.high_score)

    if st.session_state.game_started:
        elapsed = time.time() - st.session_state.start_time
        st.session_state.time_left = max(0, 30 - int(elapsed))

        if st.session_state.time_left > 0:
            st.metric("남은 시간", f"{st.session_state.time_left}초")
            st.progress(st.session_state.time_left / 30)
        else:
            st.error("⏰ 시간 종료!")
            end_game()
            st.rerun()

with col2:
    st.subheader("🎮 게임판")

    if not st.session_state.game_started:
        st.write("### 게임을 시작하려면 아래 버튼을 클릭하세요!")
        if st.button("🎯 게임 시작", use_container_width=True, type="primary"):
            start_game()
            st.rerun()
    else:
        # 4x3 그리드 생성
        for row in range(3):
            cols = st.columns(4)
            for col in range(4):
                with cols[col]:
                    # 현재 위치에 버튼이 있는지 확인
                    button_here = None
                    for btn in st.session_state.buttons:
                        if btn['x'] == col and btn['y'] == row and not btn['clicked']:
                            button_here = btn
                            break

                    if button_here:
                        if st.button("🎯", key=button_here['id'], use_container_width=True):
                            click_button(button_here['id'])
                            st.rerun()
                    else:
                        # 빈 공간
                        st.write("")

with col3:
    st.subheader("📋 게임 규칙")
    st.write("""
    **🎯 목표:** 30초 동안 최대한 많은 버튼을 클릭하세요!

    **⚡ 규칙:**
    - 화면에 나타나는 🎯 버튼을 클릭
    - 각 버튼 클릭시 +10점
    - 모든 버튼을 클릭하면 새로운 버튼들 등장
    - 시간 종료시 게임 종료

    **🏆 점수:** 클릭한 버튼 수 × 10
    """)

    if st.session_state.game_started:
        if st.button("⏹️ 게임 종료", use_container_width=True):
            end_game()
            st.rerun()

# 게임 결과 표시
if not st.session_state.game_started and st.session_state.score > 0:
    st.success(f"🎉 게임 종료! 최종 점수: {st.session_state.score}점")
    if st.session_state.score == st.session_state.high_score:
        st.balloons()
        st.success("🎊 새로운 최고 기록 달성!")

# 푸터
st.divider()
st.write("© 2026. 마우스 클릭 게임")