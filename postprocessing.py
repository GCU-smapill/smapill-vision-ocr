import json
import requests
from google import genai

def extract_pills_from_text(text):
    """
    OpenAI API를 사용하여 알약 이름만 추출.
    """
    prompt = f"다음 텍스트에서 알약 이름만 추출하여 중복을 제거하고 JSON 형태로 반환해줘: {text}"
    response = genai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.5
    )
    result = response["choices"][0]["text"].strip()
    return json.loads(result)
