from openai import OpenAI
from mysite.config import OPENAI_API_KEY, DEFAULT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)
   
    #openai.api_key = OPENAI_API_KEY


# GPT-4 모델로 ChatCompletion 호출
def chat_gpt(prompt):
    response = client.chat.completions.create(
        model = DEFAULT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
# 함수 호출 및 응답 출력
result = chat_gpt("안녕하세요, 안녕하세요 2+1은 얼마일까요??")
print(result)
