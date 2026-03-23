import streamlit as st

# 페이지 설정
st.set_page_config(page_title="My Profile", layout="wide")

# 헤더
st.title("👋 My Profile")

# 프로필 섹션
col1, col2 = st.columns(2)

with col1:
    st.header("소개")
    st.write("""
    안녕하세요! 저는 김관우입니다.
    
    여기에 간단한 자기소개를 작성할 수 있습니다.
    """)

with col2:
    st.header("📊 정보")
    st.write(f"""
    - **이름**: 김관우
    - **위치**: 인천대학교
    - **직업**: 대학생
    """)

# 구분선
st.divider()

# 관심사 섹션
st.header("💡 관심사 & 기술")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("관심사")
    st.write("• 항목 1\n• 항목 2\n• 항목 3")

with col2:
    st.subheader("기술")
    st.write("• 기술 1\n• 기술 2\n• 기술 3")

with col3:
    st.subheader("언어")
    st.write("• 한국어\n• English\n• 기타 언어")

# 구분선
st.divider()

# 연락처 섹션
st.header("📧 연락처")
col1, col2 = st.columns(2)

with col1:
    email = st.text_input("이메일을 입력하세요", placeholder="example@email.com")
    
with col2:
    message = st.text_area("메시지를 남겨주세요", height=100)

if st.button("메시지 보내기", use_container_width=True):
    st.success("메시지가 전송되었습니다! 🎉")

# 푸터
st.divider()
st.write("---")
st.write("© 2026. All rights reserved.")
