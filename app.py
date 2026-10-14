import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="CareBridge - 개인 건강관리 서비스", page_icon="🏥", layout="wide")

# 가상 추출 데이터베이스 (보내주신 파일 데이터 연동)
EXTRACTED_DATA = {
    "health_01.pdf": {
        "type": "health",
        "date": "2026-09-10",
        "data": [
            {"검사항목": "체질량지수(BMI)", "결과값": "22.4", "단위": "kg/m²", "참고범위": "18.5-24.9", "비고": "검토용"},
            {"검사항목": "수축기혈압", "결과값": "118", "단위": "mmHg", "참고범위": "90-119", "비고": "검토용"},
            {"검사항목": "이완기혈압", "결과값": "76", "단위": "mmHg", "참고범위": "60-79", "비고": "검토용"},
            {"검사항목": "공복혈당", "결과값": "92", "단위": "mg/dL", "참고범위": "70-99", "비고": "검토용"},
            {"검사항목": "총콜레스테롤", "결과값": "182", "단위": "mg/dL", "참고범위": "0-199", "비고": "검토용"},
            {"검사항목": "AST", "결과값": "22", "단위": "U/L", "참고범위": "0-40", "비고": "검토용"},
            {"검사항목": "ALT", "결과값": "19", "단위": "U/L", "참고범위": "0-40", "비고": "검토용"}
        ]
    },
    "health_02.pdf": {
        "type": "health",
        "date": "2026-09-18",
        "data": [
            {"검사항목": "체질량지수(BMI)", "결과값": "26.1", "단위": "kg/m²", "참고범위": "18.5-24.9", "비고": "범위 초과"},
            {"검사항목": "수축기혈압", "결과값": "134", "단위": "mmHg", "참고범위": "90-119", "비고": "범위 초과"},
            {"검사항목": "이완기혈압", "결과값": "84", "단위": "mmHg", "참고범위": "60-79", "비고": "범위 초과"},
            {"검사항목": "공복혈당", "결과값": "110", "단위": "mg/dL", "참고범위": "70-99", "비고": "범위 초과"},
            {"검사항목": "총콜레스테롤", "결과값": "223", "단위": "mg/dL", "참고범위": "0-199", "비고": "범위 초과"},
            {"검사항목": "AST", "결과값": "29", "단위": "U/L", "참고범위": "0-40", "비고": "-"},
            {"검사항목": "ALT", "결과값": "44", "단위": "U/L", "참고범위": "0-40", "비고": "범위 초과"}
        ]
    },
    "health_03.pdf": {
        "type": "health",
        "date": "2026-10-02",
        "data": [
            {"검사항목": "체질량지수(BMI)", "결과값": "23.0", "단위": "kg/m²", "참고범위": "18.5-24.9", "비고": "-"},
            {"검사항목": "수축기혈압", "결과값": "121", "단위": "mmHg", "참고범위": "90-119", "비고": "범위 초과"},
            {"검사항목": "이완기혈압", "결과값": "측정값 미기재", "단위": "-", "참고범위": "60-79", "비고": "원문 누락 확인"},
            {"검사항목": "공복혈당", "결과값": "측정값 미기재", "단위": "-", "참고범위": "70-99", "비고": "원문 누락 확인"},
            {"검사항목": "총콜레스테롤", "결과값": "194", "단위": "mg/dL", "참고범위": "0-199", "비고": "-"},
            {"검사항목": "AST", "결과값": "31", "단위": "U/L", "참고범위": "0-40", "비고": "-"},
            {"검사항목": "ALT", "결과값": "측정값 미기재", "단위": "-", "참고범위": "0-40", "비고": "원문 누락 확인"}
        ]
    },
    "med_01.pdf": {
        "type": "med",
        "date": "2026-10-01",
        "data": [
            {"약명": "가상시약-A정", "1회량": "1정", "횟수/일": "1", "일수": "3", "복용 시점": "아침 식후 30분", "주의사항": "문서에 기재된 주의사항 A 확인"},
            {"약명": "가상시약-B캡슐", "1회량": "1캡슐", "횟수/일": "2", "일수": "3", "복용 시점": "아침, 저녁 식후", "주의사항": "문서에 기재된 주의사항 B 확인"},
            {"약명": "가상시약-C정", "1회량": "1정", "횟수/일": "1", "일수": "3", "복용 시점": "저녁 식사와 함께", "주의사항": "임의로 분할하지 마세요"}
        ]
    },
    "med_02.pdf": {
        "type": "med",
        "date": "2026-10-03",
        "data": [
            {"약명": "가상시약-D정", "1회량": "2정", "횟수/일": "1", "일수": "5", "복용 시점": "취침 전", "주의사항": "사용 전에 주의문구를 확인"},
            {"약명": "가상시약-E산", "1회량": "1포", "횟수/일": "2", "일수": "5", "복용 시점": "식사와 관계없이", "주의사항": "복용 시간은 전문가에게 확인"}
        ]
    },
    "med_03.pdf": {
        "type": "med",
        "date": "2026-10-05",
        "data": [
            {"약명": "가상시약-F정", "1회량": "1정", "횟수/일": "미기재", "일수": "7", "복용 시점": "미기재", "주의사항": "복용 횟수 및 시점이 미기재되어 확인 필요"},
            {"약명": "가상시약-G캡슐", "1회량": "1캡슐", "횟수/일": "1", "일수": "미기재", "복용 시점": "아침 식후", "주의사항": "복용 일수가 미기재되어 확인 필요"}
        ]
    }
}

# 세션 상태 초기화
if 'uploaded_health' not in st.session_state:
    st.session_state.uploaded_health = []
if 'uploaded_med' not in st.session_state:
    st.session_state.uploaded_med = []

st.title("🏥 CareBridge")
st.markdown("#### 내 손안의 꼼꼼한 건강 비서: 문서 기반 개인 건강관리 서비스")
st.caption("⚠️ **안내:** 본 서비스는 AI를 활용해 문서를 구조화하여 보여줄 뿐, 의학적 진단이나 처방 수정을 하지 않습니다. 누락·상충 정보는 원문을 대조하세요.")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📂 1. 문서 업로드", "📊 2. 건강 정보 포트폴리오", "💊 3. 복약 일정 및 알림"])

with tab1:
    st.subheader("의료 문서 업로드 (데모)")
    st.markdown("AI가 문서를 분류하고 핵심 정보를 추출합니다. 테스트를 위해 가상 PDF 파일 이름을 선택해 업로드해보세요.")
    
    selected_file = st.selectbox("업로드할 파일 선택", ["선택 안함"] + list(EXTRACTED_DATA.keys()))
    
    if st.button("파일 업로드 및 분석 시작"):
        if selected_file != "선택 안함":
            with st.spinner("AI가 문서를 분석 중입니다 (Parse ➡️ Classify ➡️ Extract)..."):
                data_info = EXTRACTED_DATA[selected_file]
                if data_info["type"] == "health":
                    st.session_state.uploaded_health.append(data_info)
                else:
                    st.session_state.uploaded_med.append(data_info)
            st.success(f"✅ '{selected_file}' 문서 분류 및 구조화 완료! 각 탭에서 결과를 확인하세요.")
        else:
            st.warning("파일을 선택해주세요.")

with tab2:
    st.subheader("📊 개인 건강 정보 포트폴리오")
    if not st.session_state.uploaded_health:
        st.info("업로드된 건강검진 기록이 없습니다. '문서 업로드' 탭에서 건강검진 결과지(health_01 ~ 03)를 업로드하세요.")
    else:
        all_health_records = []
        for h_data in st.session_state.uploaded_health:
            date = h_data["date"]
            for row in h_data["data"]:
                row_copy = row.copy()
                row_copy["검사 일자"] = date
                all_health_records.append(row_copy)
        
        df_health = pd.DataFrame(all_health_records)
        df_health = df_health[["검사 일자", "검사항목", "결과값", "단위", "참고범위", "비고"]]
        st.dataframe(df_health, use_container_width=True)
        st.caption("※ '측정값 미기재' 항목은 원문에 결과 수치가 없음을 뜻하며, AI가 임의로 채우지 않았습니다.")

with tab3:
    st.subheader("💊 복약 일정표 및 알림")
    if not st.session_state.uploaded_med:
        st.info("업로드된 복약안내문이 없습니다. '문서 업로드' 탭에서 약국 복약안내문(med_01 ~ 03)을 업로드하세요.")
    else:
        for m_data in st.session_state.uploaded_med:
            date = m_data["date"]
            with st.expander(f"📌 {date} 처방 약품 목록", expanded=True):
                df_med = pd.DataFrame(m_data["data"])
                st.dataframe(df_med, use_container_width=True)
                st.caption("※ 미기재된 복용 횟수, 시점, 일수는 주의사항 항목에 확인 대상으로 명시되었습니다.")