import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="처방 약 복용 안내", page_icon="💊", layout="centered")

# 메인 타이틀
st.title("💊 처방 약 복용 안내 시스템")
st.markdown("환자분께 처방된 약의 올바른 복용법과 주의사항을 확인해 주세요.")
st.markdown("---")

# 1. 가상알레르정 10mg
st.header("1. 가상알레르정 10mg")
col1, col2 = st.columns(2)
with col1:
    st.write("⏱️ **복용 횟수:** 1일 3회")
    st.write("🍽️ **복용 시간:** 식후 30분")
with col2:
    st.write("💊 **1회 복용량:** 1정")
    st.write("📅 **총 복용 기간:** 7일")
st.info("⚠️ **주의사항:** 약 복용 후 졸음이 올 수 있으므로 운전이나 위험한 기계 조작은 피해주세요.")

st.markdown("---")

# 2. 예시소화정
st.header("2. 예시소화정")
col3, col4 = st.columns(2)
with col3:
    st.write("⏱️ **복용 횟수:** 1일 2회 (아침, 저녁)")
    st.write("🍽️ **복용 시간:** 식전 30분")
with col4:
    st.write("💊 **1회 복용량:** 1정")
    st.write("📅 **총 복용 기간:** 5일")
st.warning("⚠️ **주의사항:** 약을 씹지 말고 통째로 삼켜서 복용하세요.")

st.markdown("---")

# 3. 샘플비타민C정
st.header("3. 샘플비타민C정")
col5, col6 = st.columns(2)
with col5:
    st.write("⏱️ **복용 횟수:** 1일 1회")
    st.write("🍽️ **복용 시간:** 취침 전")
with col6:
    st.write("💊 **1회 복용량:** 1정 (물과 함께)")
    st.write("📅 **총 복용 기간:** 14일")
st.success("✅ **안내사항:** 충분한 물과 함께 복용하시면 좋습니다.")

# 하단 푸터
st.markdown("---")
st.caption("※ 본 안내는 참고용이며, 특이증상이 발생할 경우 즉시 의사 또는 약사와 상담하세요.")