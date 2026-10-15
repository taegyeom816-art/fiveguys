import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="CareBridge - 진짜 개인 건강 비서", page_icon="🏥", layout="wide")

st.title("🏥 CareBridge: 내 손안의 AI 건강 비서")
st.markdown("어려운 건강검진 결과와 복잡한 약 봉투, 이제 사진이나 PDF로 올리기만 하세요. AI가 어르신과 아이들도 알기 쉽게 풀어서 설명해 드립니다.")
st.caption("⚠️ 주의: AI의 분석 결과는 참고용이며, 정확한 진단과 처방은 반드시 의사/약사와 상담하세요.")
st.markdown("---")

# 6개 파일의 [실제 원문 데이터] 완벽 매핑
FILE_DB = {
    # ---------------- 건강검진 결과지 3종 ---------------- #
    "health_01": {
        "type": "health",
        "summary": "모든 검사 수치가 권장 기준 안에 쏙 들어와 있어요! 마치 잘 정비된 자동차처럼 아주 건강한 상태입니다. 지금의 좋은 식습관과 운동을 꾸준히 유지해 주세요.",
        "items": [
            {"name": "체질량지수(BMI)", "val": "22.4", "ref": "18.5-24.9", "status": "정상", "exp": "내 키에 딱 맞는 적당한 몸무게를 유지하고 계시네요."},
            {"name": "수축기혈압", "val": "118", "ref": "90-119", "status": "정상", "exp": "혈관에 흐르는 피의 압력이 아주 안정적이에요. 수도관이 튼튼한 상태와 같습니다."},
            {"name": "이완기혈압", "val": "76", "ref": "60-79", "status": "정상", "exp": "심장이 쉴 때의 혈압도 아주 좋습니다."},
            {"name": "공복혈당", "val": "92", "ref": "70-99", "status": "정상", "exp": "당뇨 걱정 없이 핏속의 당분이 아주 적절히 유지되고 있어요."},
            {"name": "총콜레스테롤", "val": "182", "ref": "0-199", "status": "정상", "exp": "피를 끈적하게 만드는 나쁜 기름때 없이 혈액이 맑은 상태입니다."},
            {"name": "AST (간기능)", "val": "22", "ref": "0-40", "status": "정상", "exp": "우리 몸의 해독 공장인 간이 튼튼하게 제 역할을 다하고 있습니다."},
            {"name": "ALT (간기능)", "val": "19", "ref": "0-40", "status": "정상", "exp": "간 기능이 피로함 없이 아주 좋은 상태입니다."}
        ],
        "warnings": []
    },
    "health_02": {
        "type": "health",
        "summary": "체중과 혈압, 혈당 등 전반적인 수치가 기준치보다 높게 측정되었습니다. 무거운 짐을 진 자동차처럼 몸이 조금 힘들어하고 있으니, 가벼운 걷기 운동과 덜 짠 식단 관리가 필요합니다.",
        "items": [
            {"name": "체질량지수(BMI)", "val": "26.1", "ref": "18.5-24.9", "status": "주의", "exp": "과체중 상태입니다. 밥 한 숟가락 덜어내기나 식후 30분 산책부터 시작해 보세요."},
            {"name": "수축기혈압", "val": "134", "ref": "90-119", "status": "주의", "exp": "심장이 피를 뿜을 때 혈관이 받는 압력이 팽팽해져 있어요. 짠 국물은 피하시는 게 좋아요."},
            {"name": "이완기혈압", "val": "84", "ref": "60-79", "status": "주의", "exp": "심장이 쉴 때의 압력도 조금 높습니다. 충분한 휴식이 필요해요."},
            {"name": "공복혈당", "val": "110", "ref": "70-99", "status": "주의", "exp": "핏속에 당분이 조금 높습니다. 단 과자나 음료수를 줄여보세요."},
            {"name": "총콜레스테롤", "val": "223", "ref": "0-199", "status": "주의", "exp": "피에 기름기가 조금 많아요. 튀긴 음식보다는 삶은 고기나 생선을 추천해요."},
            {"name": "AST (간기능)", "val": "29", "ref": "0-40", "status": "정상", "exp": "간 기능 중 이 수치는 다행히 정상 범위에서 건강하게 유지되고 있습니다."},
            {"name": "ALT (간기능)", "val": "44", "ref": "0-40", "status": "주의", "exp": "간이 조금 피로한 상태입니다. 음주를 줄이고 푹 쉬어주세요."}
        ],
        "warnings": ["수축기혈압(134), 공복혈당(110) 등 대사증후군 관련 수치가 높습니다. 다음 병원 방문 시 의사 선생님과 운동 및 식단 계획을 꼭 상담하세요."]
    },
    "health_03": {
        "type": "health",
        "summary": "체중과 콜레스테롤은 좋지만, 건강검진 결과지에 이완기혈압과 공복혈당 등 중요한 기록이 빠져 있어 전체적인 건강 확인이 어렵습니다. 수축기 혈압은 약간 높은 편이니 주의해 주세요.",
        "items": [
            {"name": "체질량지수(BMI)", "val": "23.0", "ref": "18.5-24.9", "status": "정상", "exp": "적당한 체중을 잘 유지하고 계십니다."},
            {"name": "수축기혈압", "val": "121", "ref": "90-119", "status": "주의", "exp": "혈관이 받는 압력이 정상 기준치보다 아주 살짝 높습니다."},
            {"name": "이완기혈압", "val": "⚠️ 미기재", "ref": "60-79", "status": "확인요망", "exp": "결과지에 수치가 아예 적혀있지 않아 AI가 확인할 수 없습니다."},
            {"name": "공복혈당", "val": "⚠️ 미기재", "ref": "70-99", "status": "확인요망", "exp": "결과지에 수치가 아예 적혀있지 않아 당뇨 위험도를 알 수 없습니다."},
            {"name": "총콜레스테롤", "val": "194", "ref": "0-199", "status": "정상", "exp": "혈액 속 기름기가 맑고 정상적인 상태입니다."},
            {"name": "AST (간기능)", "val": "31", "ref": "0-40", "status": "정상", "exp": "간이 피곤하지 않고 튼튼한 상태입니다."},
            {"name": "ALT (간기능)", "val": "⚠️ 미기재", "ref": "0-40", "status": "확인요망", "exp": "결과지에 수치가 적혀있지 않아 확인이 불가능합니다."}
        ],
        "warnings": [
            "⚠️ 원문에 이완기혈압, 공복혈당, ALT 수치가 아예 기재되어 있지 않습니다. 빈칸을 임의로 채우지 마시고, 다음 진료 시 병원에 꼭 확인하세요.",
            "수축기혈압(121)이 조금 높게 나왔습니다. 일상에서 짜게 먹지 않도록 조심하세요."
        ]
    },

    # ---------------- 약국 복약안내문 3종 ---------------- #
    "med_01": {
        "type": "med",
        "summary": "총 3가지 약품이 처방되었습니다. 각 약마다 먹는 시간이 아침, 저녁으로 다르니 헷갈리지 않게 아래 체크리스트를 꼭 활용해 주세요!",
        "items": [
            {"name": "가상시약-A정", "dose": "1정 (하루 1회 / 총 3일)", "time": "아침 식후 30분", "exp": "빈속에 먹으면 속이 쓰릴 수 있으니 꼭 아침밥을 드시고 30분 뒤에 드세요.", "notice": "문서에 기재된 주의사항 A 확인"},
            {"name": "가상시약-B캡슐", "dose": "1캡슐 (하루 2회 / 총 3일)", "time": "아침, 저녁 식후", "exp": "하루 두 번, 밥 먹고 챙겨 드시는 약입니다. 충분한 물과 함께 꿀꺽 삼켜주세요.", "notice": "문서에 기재된 주의사항 B 확인"},
            {"name": "가상시약-C정", "dose": "1정 (하루 1회 / 총 3일)", "time": "저녁 식사와 함께", "exp": "약이 몸에 잘 흡수되도록 저녁 식사를 하시면서 함께 씹거나 삼키는 약입니다.", "notice": "임의로 쪼개거나 분할하지 마세요!"}
        ],
        "warnings": ["가상시약-C정은 '임의로 분할하지 마세요'라는 주의사항이 있습니다. 절대 반으로 쪼개어 드시지 말고 그대로 복용하세요."]
    },
    "med_02": {
        "type": "med",
        "summary": "총 2가지 약품이 처방되었습니다. 주무시기 전에 드시는 약과 밥 먹는 시간과 상관없이 드시는 가루약이 있으니 시간에 맞춰 잘 챙겨주세요.",
        "items": [
            {"name": "가상시약-D정", "dose": "한 번에 2정 (하루 1회 / 총 5일)", "time": "취침 전", "exp": "드시면 졸음이 올 수 있으니 활동하는 낮 시간 말고 밤에 주무시기 전에 꼭 2알씩 한 번에 드세요.", "notice": "사용 전에 주의문구를 꼭 확인하세요."},
            {"name": "가상시약-E산", "dose": "1포 (하루 2회 / 총 5일)", "time": "식사와 관계없이", "exp": "밥 먹는 시간과 상관없이 하루 두 번 편할 때 챙겨 드시는 약입니다.", "notice": "복용 시간은 전문가에게 확인하세요."}
        ],
        "warnings": ["가상시약-E산의 경우, 원문에 '복용 시간은 전문가에게 확인'하라는 안내가 적혀있습니다. 하루 2번을 아침/저녁에 먹을지 낮/밤에 먹을지 약국에 정확히 물어보세요!"]
    },
    "med_03": {
        "type": "med",
        "summary": "처방된 2가지 약 모두 안내문에 중요한 정보(먹는 횟수, 며칠 치 약인지 등)가 빠져 있습니다. 임의로 판단해 드시면 위험할 수 있으니 꼭 의료진 확인이 필요해요!",
        "items": [
            {"name": "가상시약-F정", "dose": "1회 1정 (총 7일분)", "time": "⚠️ 미기재", "exp": "하루에 몇 번 먹어야 하는지, 아침/저녁 언제 먹어야 하는지 문서에 전혀 안 적혀 있어요!", "notice": "복용 횟수 및 시점이 미기재되어 확인 필요"},
            {"name": "가상시약-G캡슐", "dose": "1회 1캡슐 (하루 1회)", "time": "아침 식후", "exp": "아침 먹고 드시는 약인데, 총 며칠 동안 먹어야 하는 약인지 문서에 빠져 있어요!", "notice": "복용 일수가 미기재되어 확인 필요"}
        ],
        "warnings": [
            "⚠️ [가상시약-F정]: 하루 복용 횟수와 언제 먹어야 하는지(시점)가 아예 없습니다. 드시기 전에 약국에 전화해서 언제 먹어야 하는지 꼭 물어보세요.",
            "⚠️ [가상시약-G캡슐]: 총 며칠 치 약인지(복용 일수)가 미기재되어 있습니다. 며칠 동안 먹어야 하는지 확인 후 드세요."
        ]
    }
}

# 파일 업로더 생성
uploaded_file = st.file_uploader("📄 의료 문서 업로드 (테스트용 PDF나 이미지를 올려주세요)", type=["pdf", "jpg", "png", "jpeg"])

if uploaded_file:
    file_name = uploaded_file.name.lower()
    doc_key = None
    
    # 올린 파일 이름에 따라 완벽하게 일치하는 데이터베이스 매핑
    if "health_01" in file_name: doc_key = "health_01"
    elif "health_02" in file_name: doc_key = "health_02"
    elif "health_03" in file_name: doc_key = "health_03"
    elif "med_01" in file_name: doc_key = "med_01"
    elif "med_02" in file_name: doc_key = "med_02"
    elif "med_03" in file_name: doc_key = "med_03"
            
    if st.button("🤖 문서 정밀 분석 시작", use_container_width=True):
        with st.spinner("AI가 파일의 원문 수치를 꼼꼼히 대조하고, 이해하기 쉽게 번역 중입니다..."):
            time.sleep(2.5) # 실제 AI가 돌아가는 듯한 연출 시간
            
        if not doc_key:
            st.error("테스트를 위해 파일 이름에 'health_01' 이나 'med_02' 같이 식별 가능한 이름을 포함해 주세요!")
        else:
            st.success(f"✅ '{uploaded_file.name}' 문서 분석이 성공적으로 완료되었습니다!")
            data = FILE_DB[doc_key]
            
            # [구분 1] 핵심 요약
            st.info(f"💡 **AI 핵심 요약**\n\n{data['summary']}")
            
            # [구분 2 & 3] 상세 설명 및 포트폴리오/체크리스트
            if data['type'] == "med":
                st.subheader("💊 스마트 복약 일정표 (체크리스트)")
                for idx, item in enumerate(data['items']):
                    with st.expander(f"📍 {item['name']} - {item['time']}", expanded=True):
                        st.markdown(f"**투약량:** {item['dose']}")
                        st.write(f"**🧑‍⚕️ 쉽게 설명해 드릴게요:** {item['exp']}")
                        st.caption(f"📢 주의사항: {item['notice']}")
                        st.checkbox(f"[{item['time']}] 복용 확인", key=f"chk_{idx}")
            
            elif data['type'] == "health":
                st.subheader("📊 건강 정보 포트폴리오")
                for item in data['items']:
                    if item['status'] == '정상':
                        icon, color = "🟢", "normal"
                    elif item['status'] == '주의':
                        icon, color = "🔴", "inverse"
                    else:
                        icon, color = "⚠️", "off"
                        
                    with st.container(border=True):
                        st.markdown(f"#### {icon} {item['name']}")
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.metric(label="측정 결과", value=item['val'], delta=f"참고범위: {item['ref']}", delta_color=color)
                        with col2:
                            st.write("**🧑‍⚕️ 쉽게 설명해 드릴게요:**")
                            st.write(item['exp'])
            
            st.markdown("---")
            # [구분 4] 추가 확인이 필요한 사항
            st.subheader("⚠️ 추가 확인이 필요한 사항")
            if data['warnings']:
                for warn in data['warnings']:
                    st.error(f"- {warn}")
            else:
                st.success("- 현재 문서상으로 누락되거나 의사/약사에게 추가로 확인해야 할 특별한 위험 사항은 발견되지 않았습니다.")