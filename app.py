import streamlit as st
import pandas as pd
import time

# 페이지 기본 설정
st.set_page_config(page_title="CareBridge - 개인 건강관리 서비스", page_icon="🏥", layout="wide")

# 세션 상태 초기화
if 'analyzed_data' not in st.session_state:
    st.session_state.analyzed_data = None

st.title("🏥 CareBridge")
st.markdown("#### 내 손안의 꼼꼼한 건강 비서: 문서 기반 개인 건강관리 서비스")
st.caption("⚠️ 데모 안내: 현재 시연 버전에서는 파일 업로드 시 서비스의 흐름(UI/UX)을 보여주기 위해 준비된 가상 분석 결과가 표출됩니다. AI는 진단을 내리지 않으며, 원문 확인이 필요합니다.")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📂 1. 문서 업로드", "💊 2. 스마트 복약 일정표", "📊 3. 건강 정보 포트폴리오"])

# ==========================================
# 탭 1: 실제 파일 업로드 (우선순위 1)
# ==========================================
with tab1:
    st.subheader("의료 문서 업로드")
    st.markdown("건강검진 결과지 또는 약국 복약안내문을 업로드해주세요. (PDF, JPG, PNG 지원)")
    
    # 실제 파일 업로더 적용
    uploaded_file = st.file_uploader("파일을 이곳으로 드래그하거나 클릭하여 업로드하세요.", type=["pdf", "jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.info(f"📄 '{uploaded_file.name}' 파일이 준비되었습니다.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💊 복약안내문 분석 시작", use_container_width=True):
                with st.spinner("AI가 문서를 분류하고 복약 정보를 추출 중입니다 (Parse ➡️ Classify ➡️ Extract)..."):
                    time.sleep(2.5) # 시연용 로딩 연출
                    st.session_state.analyzed_data = "med"
                st.success("✅ 복약안내문 분석이 완료되었습니다! '스마트 복약 일정표' 탭을 확인하세요.")
        with col2:
            if st.button("📊 건강검진 결과 분석 시작", use_container_width=True):
                with st.spinner("AI가 문서를 분류하고 건강 수치를 구조화 중입니다 (Parse ➡️ Classify ➡️ Extract)..."):
                    time.sleep(2.5)
                    st.session_state.analyzed_data = "health"
                st.success("✅ 건강검진 결과 분석이 완료되었습니다! '건강 정보 포트폴리오' 탭을 확인하세요.")

# ==========================================
# 탭 2: 복약 일정표 및 체크리스트 (우선순위 2)
# ==========================================
with tab2:
    st.subheader("💊 스마트 복약 일정표")
    if st.session_state.analyzed_data != "med":
        st.info("문서 업로드 탭에서 복약안내문을 업로드하고 분석을 진행하면, 스마트 복약 일정이 생성됩니다.")
    else:
        st.success("🤖 **AI 핵심 요약:** 총 4가지 약품이 처방되었습니다. 복용 시점이 아침, 저녁, 취침 전으로 나뉘어 있으니 아래 일정을 참고해 제때 복용하세요.")
        
        # 시간대별 복약 체크리스트 (지속적인 건강관리 연결)
        st.markdown("### ⏰ 오늘의 복약 체크리스트")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("🌅 **아침 식후 (08:00)**")
            st.checkbox("가상시약-A정 (1정)", key="m1")
            st.checkbox("가상시약-B캡슐 (1캡슐)", key="m2")
        with c2:
            st.warning("🌇 **저녁 식후 (19:00)**")
            st.checkbox("가상시약-B캡슐 (1캡슐)", key="e1")
            st.checkbox("가상시약-C정 (1정)", key="e2")
        with c3:
            st.error("🌙 **취침 전 (22:00)**")
            st.checkbox("가상시약-D정 (2정)", key="n1")
            
        st.markdown("---")
        # 개별 약품 상세 정보
        st.markdown("### 🔍 약품별 상세 정보 및 주의사항")
        med_details = pd.DataFrame([
            {"약명": "가상시약-A정", "1회량": "1정", "횟수/일": "1회", "일수": "3일", "복용 시점": "아침 식후", "추가 확인사항": "문서에 기재된 주의사항 A 확인"},
            {"약명": "가상시약-B캡슐", "1회량": "1캡슐", "횟수/일": "2회", "일수": "3일", "복용 시점": "아침/저녁 식후", "추가 확인사항": "문서에 기재된 주의사항 B 확인"},
            {"약명": "가상시약-C정", "1회량": "1정", "횟수/일": "1회", "일수": "3일", "복용 시점": "저녁 식사", "추가 확인사항": "임의로 분할하지 마세요"},
            {"약명": "가상시약-D정", "1회량": "2정", "횟수/일": "1회", "일수": "5일", "복용 시점": "취침 전", "추가 확인사항": "⚠️ 사용 전에 주의문구를 꼭 확인하세요"}
        ])
        st.dataframe(med_details, use_container_width=True)

# ==========================================
# 탭 3: 건강 정보 포트폴리오
# ==========================================
with tab3:
    st.subheader("📊 건강 정보 포트폴리오")
    if st.session_state.analyzed_data != "health":
        st.info("문서 업로드 탭에서 건강검진 결과지를 업로드하고 분석을 진행하면, 포트폴리오가 생성됩니다.")
    else:
        st.success("🤖 **AI 핵심 요약:** 대사 증후군 관련 지표(혈압, 체질량지수)에 주의가 필요합니다. 지속적인 추적 관찰과 의료진 상담을 권장합니다.")
        
        st.markdown("### 🔍 개별 검사항목 상세 해설")
        health_details = pd.DataFrame([
            {"검사항목": "체질량지수(BMI)", "결과값": "26.1", "참고범위": "18.5-24.9", "상태": "🔴 주의", "AI 쉬운 설명": "비만도를 나타내는 지표로, 참고범위를 벗어났습니다."},
            {"검사항목": "수축기혈압", "결과값": "134", "참고범위": "90-119", "상태": "🔴 주의", "AI 쉬운 설명": "심장이 수축할 때의 혈압이 다소 높습니다."},
            {"검사항목": "공복혈당", "결과값": "110", "참고범위": "70-99", "상태": "🔴 주의", "AI 쉬운 설명": "당뇨 위험을 확인하는 혈당 수치가 높습니다."},
            {"검사항목": "AST", "결과값": "29", "참고범위": "0-40", "상태": "🟢 정상", "AI 쉬운 설명": "간 기능 수치로 정상입니다."}
        ])
        st.dataframe(health_details, use_container_width=True)
        
        st.markdown("### 🧑‍⚕️ 진료 시 의료진에게 물어보세요 (추가 확인)")
        st.warning("1. 체중과 혈압을 함께 관리할 수 있는 운동 계획이 있을까요?\n2. 현재 혈당 수치에서 주의해야 할 음식이 있나요?")