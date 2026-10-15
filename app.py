import streamlit as st
import pandas as pd
import time

# 페이지 기본 설정
st.set_page_config(page_title="CareBridge - 개인 건강관리 서비스", page_icon="🏥", layout="wide")

# 세션 상태 초기화
if 'analysis_type' not in st.session_state:
    st.session_state.analysis_type = None

st.title("🏥 CareBridge")
st.markdown("#### 내 손안의 꼼꼼한 건강 비서: 문서 기반 개인 건강관리 서비스")
st.caption("⚠️ 안내: 본 서비스는 AI를 활용해 어려운 건강 수치와 복약 안내를 쉽게 풀어 설명합니다. 진단이나 처방을 대체하지 않으며, 추가 확인이 필요한 사항은 반드시 전문가와 상의하세요.")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📂 1. 의료 문서 직접 업로드", "💊 2. 복약안내 분석 결과", "📊 3. 건강검진 분석 결과"])

# ==========================================
# 탭 1: 실제 문서 업로드
# ==========================================
with tab1:
    st.subheader("의료 문서 직접 업로드")
    st.markdown("가지고 계신 건강검진 결과지나 약국 복약안내문을 직접 업로드해 주세요. (PDF, JPG, PNG 지원)")
    
    # 실제 파일 업로더 생성
    uploaded_file = st.file_uploader("파일을 드래그하거나 클릭하여 업로드하세요.", type=["pdf", "jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.success(f"📄 '{uploaded_file.name}' 파일이 성공적으로 업로드되었습니다.")
        
        st.markdown("**업로드한 문서의 종류에 맞게 분석 버튼을 눌러주세요:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💊 복약안내문으로 분석 시작", use_container_width=True):
                with st.spinner("AI가 약품 정보와 복용법을 추출하고 있습니다..."):
                    time.sleep(2) # 데모용 로딩 시뮬레이션
                    st.session_state.analysis_type = "med"
                st.success("분석 완료! '복약안내 분석 결과' 탭을 확인하세요.")
        with col2:
            if st.button("📊 건강검진 결과지로 분석 시작", use_container_width=True):
                with st.spinner("AI가 검사 수치와 참고범위를 비교 분석하고 있습니다..."):
                    time.sleep(2)
                    st.session_state.analysis_type = "health"
                st.success("분석 완료! '건강검진 분석 결과' 탭을 확인하세요.")

# ==========================================
# 탭 2: 복약안내 분석 결과
# ==========================================
with tab2:
    if st.session_state.analysis_type == "med":
        st.subheader("💊 복약안내 분석 결과")
        
        # 1. 핵심 요약
        st.info("💡 **핵심 요약**\n\n총 3가지 약품이 처방되었습니다. 아침 식후, 저녁 식후, 취침 전으로 복용 시점이 다르므로 시간에 맞춰 꼼꼼히 복용해 주세요.")
        
        # 2. 개별 약품에 대한 설명
        st.markdown("### 🔍 개별 약품에 대한 설명")
        med_data = [
            {"약품명": "가상시약-A정", "1회 용량": "1정", "복용 시점": "아침 식후", "설명": "위장장애를 줄이기 위해 반드시 식후에 복용하세요."},
            {"약품명": "가상시약-B캡슐", "1회 용량": "1캡슐", "복용 시점": "저녁 식후", "설명": "충분한 물과 함께 복용하는 것이 좋습니다."},
            {"약품명": "가상시약-C정", "1회 용량": "2정", "복용 시점": "취침 전", "설명": "복용 후 졸음이 올 수 있으므로 취침 전에 복용하세요."}
        ]
        st.dataframe(pd.DataFrame(med_data), use_container_width=True)
        
        # 3. 추가 확인이 필요한 사항
        st.markdown("### ⚠️ 추가 확인이 필요한 사항")
        st.error("""
        - **가상시약-A정 (복용 일수 미기재):** 원문에 며칠 동안 먹어야 하는지 적혀있지 않습니다. 약국에 며칠 치 약인지 꼭 확인하세요.
        - **가상시약-C정 (분할 주의):** 약을 쪼개거나 씹어 먹어도 되는지 전문가의 확인이 필요합니다.
        """)
    else:
        st.info("문서를 업로드하고 '복약안내문으로 분석' 버튼을 눌러주세요.")

# ==========================================
# 탭 3: 건강검진 분석 결과
# ==========================================
with tab3:
    if st.session_state.analysis_type == "health":
        st.subheader("📊 건강검진 분석 결과")
        
        # 1. 핵심 요약
        st.info("💡 **핵심 요약**\n\n체질량지수(BMI)와 혈압이 참고범위를 다소 벗어나 주의가 필요합니다. 그 외 간 기능(AST) 수치 등은 정상 범위 내에 안정적으로 유지되고 있습니다.")
        
        # 2. 개별 검사항목에 대한 설명
        st.markdown("### 🔍 개별 검사항목에 대한 설명")
        health_data = [
            {"검사항목": "체질량지수(BMI)", "결과값": "26.1", "참고범위": "18.5-24.9", "상태": "🔴 주의", "설명": "비만도를 나타내는 지표입니다. 체중 관리가 필요한 수치입니다."},
            {"검사항목": "수축기혈압", "결과값": "134", "참고범위": "90-119", "상태": "🔴 주의", "설명": "심장이 수축할 때의 혈압으로, 정상 기준보다 다소 높습니다."},
            {"검사항목": "AST", "결과값": "29", "참고범위": "0-40", "상태": "🟢 정상", "설명": "간세포 손상 여부를 확인하는 간 기능 효소 수치입니다."}
        ]
        st.dataframe(pd.DataFrame(health_data), use_container_width=True)
        
        # 3. 추가 확인이 필요한 사항
        st.markdown("### ⚠️ 추가 확인이 필요한 사항")
        st.error("""
        - **공복혈당 (측정값 누락):** 원문에 공복혈당 수치가 기재되어 있지 않습니다. 이전 검사 결과가 있다면 비교해 보시거나, 다음 진료 시 꼭 검사를 요청하세요.
        - **혈압 관리 (의료진 상담 권장):** 수축기 혈압이 지속적으로 높게 측정된다면, 진료 시 혈압 강하를 위한 생활 습관 개선에 대해 상담해 보세요.
        """)
    else:
        st.info("문서를 업로드하고 '건강검진 결과지로 분석' 버튼을 눌러주세요.")