import openai
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets["API_KEY"]
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title("🔮 MBTI AI 탐정봇")
st.caption("한 문장만 입력하면 당신의 성향을 추리해줄게요!")

keyword = st.text_area("당신을 표현하는 문장을 입력해보세요 ✍️")

if st.button("MBTI 예측하기"):
    if keyword == "":
        st.warning("텍스트를 입력해 주세요!")
    else:
        with st.spinner("당신의 성향 파악하는 중..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """너는 입력 받은 내용을 기반으로 유저의 16가지 중 가장 가까운 하나의 MBTI를 맞추는 탐정이야. 우선 유저의 성격을 분석하여, 하나의 MBTI를 예측해. 다음으로 예측한 MBTI와 관련한 특징들을 500자 이내로 친근한 반말의 탐정 말투로 흥미진진하게 작성해. 작성 할 때는 반드시 아래 3가지 형식을 지켜. 1. MBTI 유형은 대문자로 작성해줘. 2. MBTI 유형은 반드시 문장 첫머리에 '당신의 MBTI는 바로 "유추한 MBTI"'!로 작성 3. 첫 문장 다음은 꼭 줄바꿈을 해줘."""},
                    {"role": "user", "content": keyword}
                ],
                temperature=0.7,
            )

            mbti_text = response.choices[0].message.content

            img_response = client.images.generate(
                model="dall-e-3",
                prompt=f"""내가 전달하는 [인물 성향 설명]을 바탕으로 해당 인물의 성격과 분위기를 반영한 장면을 아래 기준에 맞춰 이미지로 표현할 것.
                [인물 성향 설명]: {mbti_text}""",
                size="1024x1024",
                quality="standard",
                n=1,
            )

            st.write(mbti_text)
            st.image(img_response.data[0].url)
