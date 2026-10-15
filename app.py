import streamlit as st
import google.generativeai as genai
import tempfile
import os
import json
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="CareBridge - 진짜 개인 건강 비서", page_icon="🏥", layout="wide")

# 사이드바: AI 엔진 연결 (API 키 입력)
st.sidebar.title("⚙️ AI 설정")
st.sidebar.markdown("CareBridge AI를 깨우기 위해 API 키를 입력해주세요.")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    st.sidebar.success("AI 엔진 연결 완료!")
else:
    st.sidebar.warning("API 키를 입력해야 분석이 시작됩니다.")

st.title("🏥 CareBridge: 내 손안의 AI 건강 비서")
st.markdown("어려운 건강검진 결과와 복잡한 약 봉투, 이제 사진이나 PDF로 올리기만 하세요. AI가 어르신과 아이들도 알기 쉽게 풀어서 설명해 드립니다.")
st.caption("⚠️ 주의: AI의 분석 결과는 참고용이며, 정확한 진단과 처방은 반드시 의사/약사와 상담하세요.")
st.markdown("---")

# 문서 분석 프롬프트 (AI에게 내리는 엄격한 명령)
SYSTEM_PROMPT = """
당신은 'CareBridge'라는 친절한 의료 전문 AI 비서입니다.
사용자가 올린 문서(건강검진 결과지 또는 복약안내문)를 읽고 아래의 JSON 형식으로만 정확히 대답하세요.

[필수 규칙]
1. 어려운 의학 용어는 초등학생이나 어르신도 이해할 수 있도록 아주 쉽고 따뜻한 비유를 들어 설명할 것.
2. 문서에 없는 내용을 절대 지어내지 말 것. (미기재된 경우 '확인 필요'로 표기)
3. 치료를 지시하거나 진단을 내리지 말 것.

[출력 JSON 구조]
{
  "document_type": "건강검진" 또는 "복약안내문" (문서 종류 판단),
  "summary": "어르신도 이해하기 쉬운 2~3문장의 따뜻한 핵심 요약",
  "items": [
    {
      "name": "검사항목명 또는 약품명",
      "value": "검사수치 또는 1회용량/하루횟수",
      "reference": "참고범위 또는 복용시점(아침/저녁 등)",
      "status": "정상/주의/확인필요 중 하나",
      "explanation": "이 항목(약)이 무엇인지, 현재 어떤 상태인지 어르신 눈높이에서 아주 쉽게 비유를 든 설명"
    }
  ],
  "warnings": [
    "문서에서 빠져 있어서 의사/약사에게 꼭 물어봐야 할 사항이나 주의점 (배열 형태로 여러 개 작성)"
  ]
}
반드시 JSON 중괄호 {} 로만 대답하고 마크다운 문법(```json 등)은 쓰지 마세요.
"""

uploaded_file = st.file_uploader("📄 건강검진 결과지나 약국 안내문 업로드 (PDF, JPG, PNG)", type=["pdf", "jpg", "png", "jpeg"])

if uploaded_file and api_key:
    if st.button("🤖 AI 문서 분석 시작", use_container_width=True):
        with st.spinner("AI가 문서를 꼼꼼히 읽고, 어르신도 이해하기 쉽게 번역 중입니다... (약 10~20초 소요)"):
            try:
                # 1. 업로드된 파일을 임시 저장 (AI가 읽을 수 있도록)
                file_extension = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # 2. AI에게 파일 전송 및 분석 요청
                myfile = genai.upload_file(tmp_path)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([myfile, SYSTEM_PROMPT])
                
                # 파일 정리
                os.remove(tmp_path)
                genai.delete_file(myfile.name)
                
                # 3. AI의 답변(JSON) 정리 및 화면 출력
                result_text = response.text.strip().replace("```json", "").replace("```", "")
                data = json.loads(result_text)
                
                # ======== 화면 출력 로직 ========
                st.success("✅ 문서 분석 완료!")
                
                st.info(f"💡 **AI 핵심 요약**\n\n{data['summary']}")
                
                if data['document_type'] == "복약안내문":
                    st.subheader("💊 스마트 복약 일정 (체크리스트)")
                    for i, item in enumerate(data['items']):
                        with st.expander(f"📍 {item['name']} ({item['reference']})", expanded=True):
                            st.markdown(f"**투약량:** {item['value']}")
                            st.write(f"**쉽게 설명해 드릴게요:** {item['explanation']}")
                            st.checkbox(f"[{item['reference']}] {item['name']} 복용 완료!", key=f"chk_{i}")
                
                elif data['document_type'] == "건강검진":
                    st.subheader("📊 건강 정보 포트폴리오")
                    for item in data['items']:
                        # 상태에 따른 색상/이모지
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
                                st.metric(label="나의 수치 (참고범위)", value=item['value'], delta=f"기준: {item['reference']}", delta_color=color)
                            with col2:
                                st.write("**🧑‍⚕️ AI의 쉬운 설명:**")
                                st.write(item['explanation'])
                
                st.markdown("---")
                st.subheader("⚠️ 꼭 확인하고 넘어가세요!")
                if data['warnings']:
                    for warn in data['warnings']:
                        st.error(f"- {warn}")
                else:
                    st.success("- 현재 문서상으로 누락되거나 특별히 경고할 만한 위험 사항은 발견되지 않았습니다.")
                
            except Exception as e:
                st.error("분석 중 오류가 발생했습니다. 파일이 흐리거나 API 키가 잘못되었을 수 있습니다.")
                st.write(e)
elif not api_key:
    st.warning("👈 왼쪽 사이드바에서 AI API 키를 먼저 입력해 주세요.")