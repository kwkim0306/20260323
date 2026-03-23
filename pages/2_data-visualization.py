import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os

# 한글 폰트 설정 - fonts 폴더의 NanumGothic 폰트 직접 로드
font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'NanumGothic-Regular.ttf')
if os.path.exists(font_path):
    # 폰트 파일을 matplotlib에 추가
    font_name = fm.FontProperties(fname=font_path).get_name()
    fm.fontManager.addfont(font_path)
    
    # matplotlib 설정
    plt.rcParams['font.family'] = font_name
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
else:
    # 폰트 파일이 없으면 경고 메시지
    st.warning("NanumGothic 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")

plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="데이터 시각화", layout="wide")
st.title("📊 데이터 시각화 예제")

st.write("다양한 데이터 시각화 예제입니다. matplotlib과 plotly를 사용했습니다.")

# 탭으로 구성
tab1, tab2, tab3, tab4 = st.tabs(["라인 차트", "막대 그래프", "산점도", "파이 차트"])

# ==================== Tab 1: 라인 차트 ====================
with tab1:
    st.header("📈 라인 차트")
    
    # 샘플 데이터
    months = ['1월', '2월', '3월', '4월', '5월', '6월']
    sales = [4000, 5200, 4800, 6100, 5900, 7200]
    
    # matplotlib으로 라인 차트
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(months, sales, marker='o', linewidth=2, markersize=8, color='#1f77b4')
    ax.set_xlabel('월', fontsize=12, fontweight='bold')
    ax.set_ylabel('판매량 (단위)', fontsize=12, fontweight='bold')
    ax.set_title('월별 판매량 추이', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    for i, (m, s) in enumerate(zip(months, sales)):
        ax.text(i, s + 150, str(s), ha='center', fontsize=10, fontweight='bold')
    
    st.pyplot(fig)

# ==================== Tab 2: 막대 그래프 ====================
with tab2:
    st.header("📊 막대 그래프")
    
    # 샘플 데이터
    categories = ['A 제품', 'B 제품', 'C 제품', 'D 제품', 'E 제품']
    values = [85, 72, 90, 78, 88]
    
    # matplotlib으로 막대 그래프
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('평가 점수', fontsize=12, fontweight='bold')
    ax.set_title('제품별 만족도 평가', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(True, axis='y', alpha=0.3)
    
    # 값 표시
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    st.pyplot(fig)

# ==================== Tab 3: 산점도 ====================
with tab3:
    st.header("🔵 산점도")
    
    # 샘플 데이터
    np.random.seed(42)
    df = pd.DataFrame({
        '공부시간': np.random.uniform(1, 10, 50),
        '성적': np.random.uniform(50, 100, 50)
    })
    
    # plotly로 산점도
    fig = px.scatter(df, x='공부시간', y='성적',
                     title='공부시간과 성적 관계',
                     labels={'공부시간': '공부시간 (시간)', '성적': '성적 (점)'},
                     size_max=8,
                     color='성적',
                     color_continuous_scale='Viridis')
    
    fig.update_layout(
        title_font_size=16,
        width=800,
        height=600,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================== Tab 4: 파이 차트 ====================
with tab4:
    st.header("🥧 파이 차트")
    
    # 샘플 데이터
    labels = ['전자제품', '의류', '식품', '도서', '기타']
    sizes = [30, 25, 20, 15, 10]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    # plotly로 파이 차트
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=sizes,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        hovertemplate='<b>%{label}</b><br>판매량: %{value}<br>비율: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title_text='카테고리별 판매량 분포',
        title_font_size=16,
        height=600,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================== 추가: 다중 라인 차트 ====================
st.divider()
st.header("📈 다중 라인 차트 (Plotly)")

# 샘플 데이터
df_multi = pd.DataFrame({
    '월': ['1월', '2월', '3월', '4월', '5월', '6월'],
    '서울': [15, 18, 17, 20, 22, 25],
    '부산': [12, 14, 16, 15, 18, 20],
    '대구': [10, 12, 13, 14, 16, 18]
})

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_multi['월'], y=df_multi['서울'],
    mode='lines+markers',
    name='서울',
    line=dict(color='#FF6B6B', width=3),
    marker=dict(size=8)
))

fig.add_trace(go.Scatter(
    x=df_multi['월'], y=df_multi['부산'],
    mode='lines+markers',
    name='부산',
    line=dict(color='#4ECDC4', width=3),
    marker=dict(size=8)
))

fig.add_trace(go.Scatter(
    x=df_multi['월'], y=df_multi['대구'],
    mode='lines+markers',
    name='대구',
    line=dict(color='#45B7D1', width=3),
    marker=dict(size=8)
))

fig.update_layout(
    title='도시별 월간 온도 추이',
    title_font_size=16,
    xaxis_title='월',
    yaxis_title='온도 (℃)',
    hovermode='x unified',
    height=500,
    width=900
)

st.plotly_chart(fig, use_container_width=True)
