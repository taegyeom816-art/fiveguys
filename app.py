import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="CareBridge - 내 손안의 건강 비서", page_icon="🏥", layout="wide")

st.title("🏥 CareBridge: 내 손안의 AI 건강 비서")
st.markdown("어려운 건강검진 결과와 복잡한 약 봉투, 이제 사진이나 PDF로 올리기만 하세요. AI가 어르신과 아이들도 알기 쉽게 풀어서 설명해 드립니다.")
st.caption("⚠️ 주의: AI의 분석 결과는 참고용이며, 정확한 진단과 처방은 반드시 의사/약사와 상담하세요.")
st.markdown("---")

# 파일 업로더
uploaded_file = st.file_uploader("📄 건강검진 결과지나 약국 안내문 업로드 (PDF, JPG, PNG)", type=["pdf", "jpg", "png", "jpeg"])

if uploaded_file:
    if st.button("🤖 AI 문서 분석 시작", use_container_width=True):
        # 진짜 AI가 생각하는 것처럼 로딩 연출
        with st.spinner("AI가 문서를 꼼꼼히 읽고, 어르신도 이해하기 쉽게 번역 중입니다..."):
            time.sleep(3.5) # 3.5초 대기 (시연용)
            
        st.success("✅ 문서 분석 완료!")
        
        # 파일 이름에 'health'가 들어가면 건강검진 결과로, 아니면 복약안내문으로 인식하도록 연출
        is_health_doc = "health" in uploaded_file.name.lower()
        
        if not is_health_doc:
            # ==========================================
            # 복약안내문 시연 화면
            # ==========================================
            st.info("💡 **AI 핵심 요약**\n\n총 2가지 약품이 분석되었습니다. 염증을 가라앉히는 약과 위장약이 처방되었네요. 하루 한 번, 시간에 맞춰 꼼꼼히 복용해 주세요.")
            
            st.subheader("💊 스마트 복약 일정 (체크리스트)")
            
            with st.expander("📍 가상시약-G캡슐 (아침 식후)", expanded=True):
                st.markdown("**투약량:** 1캡슐 (하루 1회)")
                st.write("**🧑‍⚕️ 쉽게 설명해 드릴게요:** 아침 식사 후 위장 부담이 적을 때 드시는 약입니다. 식사하시고 30분 뒤에 물과 함께 드세요.")
                st.checkbox("[아침 식후] 가상시약-G캡슐 복용 완료!", key="chk_1")
                
            with st.expander("📍 가상시약-F정 (복용 시점 미기재)", expanded=True):
                st.markdown("**투약량:** 1정 (총 7일분)")
                st.write("**🧑‍⚕️ 쉽게 설명해 드릴게요:** 통증을 줄여주는 약인데, 언제 먹어야 하는지 안 적혀 있네요. 임의로 드시지 마시고 꼭 약국에 물어보세요!")
                st.checkbox("[확인 후 복용] 가상시약-F정 복용 완료!", key="chk_2")
                
            st.markdown("---")
            st.subheader("⚠️ 꼭 확인하고 넘어가세요!")
            st.error("- **가상시약-F정:** 하루에 몇 번, 언제 먹어야 하는지 문서에 빠져 있습니다. 약국에 꼭 확인하세요.")
            st.error("- **가상시약-G캡슐:** 며칠 동안 먹어야 하는지(복용 일수)가 빠져 있습니다.")

        else:
            # ==========================================
            # 건강검진 결과지 시연 화면
            # ==========================================
            st.info("💡 **AI 핵심 요약**\n\n혈압과 체중이 권장 기준보다 조금 높아 관리가 필요합니다. 마치 자동차 타이어에 공기가 너무 빵빵하게 들어간 것과 같으니, 가벼운 걷기 운동부터 시작해 보세요!")
            
            st.subheader("📊 건강 정보 포트폴리오")
            
            with st.container(border=True):
                st.markdown("#### 🔴 체질량지수(BMI) 및 수축기혈압")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric(label="나의 BMI 수치", value="26.1 kg/m²", delta="기준치 초과", delta_color="inverse")
                    st.metric(label="나의 혈압 수치", value="134 mmHg", delta="기준치 초과", delta_color="inverse")
                with col2:
                    st.write("**🧑‍⚕️ 쉽게 설명해 드릴게요:**")
                    st.write("BMI는 내 키에 비해 체중이 얼마나 나가는지 보여주는 수치인데, 현재 과체중 상태입니다. 혈압 역시 심장이 피를 뿜어낼 때 혈관이 받는 압력이 조금 높은 상태예요. 짠 음식을 줄이시는 것이 좋습니다.")
                    
            with st.container(border=True):
                st.markdown("#### 🟢 간 기능 수치 (AST)")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric(label="나의 AST 수치", value="29 U/L", delta="정상 범위 내", delta_color="normal")
                with col2:
                    st.write("**🧑‍⚕️ 쉽게 설명해 드릴게요:**")
                    st.write("간이 얼마나 건강한지 보여주는 수치인데, 아주 건강하고 튼튼하게 잘 유지되고 있습니다!")
                    
            st.markdown("---")
            st.subheader("⚠️ 꼭 확인하고 넘어가세요!")
            st.warning("- **공복혈당 누락:** 이번 검사지에 당뇨를 확인하는 '공복혈당' 수치가 빠져 있습니다. 다음번 병원에 가실 때 꼭 추가로 확인해 보세요.")