import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="CareBridge 복약 안내 시스템", page_icon="💊", layout="centered")

# 메인 타이틀
st.title("💊 CareBridge 처방 약 복용 안내")
st.markdown("처방받은 약의 이름을 검색하여 복용 방법과 주의사항을 확인하세요.")
st.markdown("---")

# CareBridge 복약안내문 기반 6가지 약품 데이터베이스
medicine_db = {
    "가상알레르정": {
        "name": "가상알레르정 10mg",
        "dose": "1정",
        "frequency": "1일 3회",
        "timing": "식후 30분에 복용하세요.",
        "duration": "7일",
        "precautions": "⚠️ [위장장애 주의 / 졸음 주의] 약 복용 후 졸음이 올 수 있으므로 운전이나 위험한 기계 조작은 피해주세요."
    },
    "예시소화정": {
        "name": "예시소화정",
        "dose": "1정",
        "frequency": "1일 2회 (아침, 저녁)",
        "timing": "식전 30분에 복용하세요.",
        "duration": "5일",
        "precautions": "⚠️ [씹지 마세요] 약을 씹지 말고 통째로 삼켜서 복용하세요."
    },
    "샘플비타민C정": {
        "name": "샘플비타민C정",
        "dose": "1정",
        "frequency": "1일 1회",
        "timing": "취침 전에 복용하세요.",
        "duration": "14일",
        "precautions": "✅ 충분한 물과 함께 복용하시면 좋습니다."
    },
    "케어진통정": {
        "name": "케어진통정 500mg",
        "dose": "2정",
        "frequency": "1일 3회",
        "timing": "식사와 관계없이 복용하세요.",
        "duration": "3일",
        "precautions": "⚠️ [위장장애 주의] 식후에 복용하시면 위장 부담을 줄일 수 있습니다."
    },
    "브릿지항생정": {
        "name": "브릿지항생정 250mg",
        "dose": "1정",
        "frequency": "1일 2회",
        "timing": "식후 30분에 복용하세요.",
        "duration": "7일",
        "precautions": "⚠️ [임신(계획) 시 주의 / 일정 시간 복용] 증상이 좋아져도 임의로 중단하지 말고 처방된 기간 동안 끝까지 복용하세요."
    },
    "안심혈압정": {
        "name": "안심혈압정 5mg",
        "dose": "1정",
        "frequency": "1일 1회",
        "timing": "아침 식전 복용하세요.",
        "duration": "30일",
        "precautions": "⚠️ [근육통 주의 / 일정 시간 복용] 매일 일정한 시간에 복용해야 효과가 좋습니다."
    }
}

# 검색 기능 구현
st.subheader("🔍 처방 약 검색")
search_query = st.text_input("약 이름을 입력하세요 (예: 가상알레르정, 케어진통정, 안심혈압정 등)", "")

if search_query:
    found = False
    for key, info in medicine_db.items():
        if search_query in key or search_query in info["name"]:
            found = True
            st.success(f"📌 **{info['name']}** 검색 결과입니다.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"⏱️ **복용 횟수:** {info['frequency']}")
                st.write(f"🍽️ **복용 방법:** {info['timing']}")
            with col2:
                st.write(f"💊 **1회 투약량:** {info['dose']}")
                st.write(f"📅 **복용 일수:** {info['duration']}")
                
            st.info(f"**주의사항 및 안내**\n\n{info['precautions']}")
            st.markdown("---")
            
    if not found:
        st.warning("❌ 일치하는 약 정보가 없습니다. 6가지 약 이름(가상알레르정, 예시소화정, 샘플비타민C정, 케어진통정, 브릿지항생정, 안심혈압정) 중 하나를 검색해 보세요.")

# 전체 6가지 약 목록 한눈에 보기
with st.expander("📋 처방된 6가지 약 목록 전체보기"):
    for key, info in medicine_db.items():
        st.markdown(f"### {info['name']}")
        st.write(f"- **복용법:** {info['frequency']} ({info['timing']}) / 총 {info['duration']}")
        st.write(f"- **주의사항:** {info['precautions']}")
        st.markdown("---")

# 하단 푸터
st.caption("※ 본 안내는 CareBridge 처방 기준 참고용이며, 특이증상이 발생할 경우 즉시 의사 또는 약사와 상담하세요.")