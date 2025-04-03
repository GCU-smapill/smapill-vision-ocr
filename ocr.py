import os
import io
import json
from google.cloud import vision
import openai

# Google Cloud Vision API 인증 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/yunseo/Desktop/development/smapill/ai_google_ocr/google-cloud-key/pro-gecko-444007-a8-1364f6fccaef.json"

# OpenAI API 키 설정
openai.api_key = "YOUR_OPENAI_API_KEY"

def ocr_process(image_path):
    """
    Google Vision API를 사용하여 OCR 처리.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description  # OCR에서 추출된 전체 텍스트 반환
    return ""


def extract_pills_from_text(text):
    """
    Google Gemini API를 사용하여 알약 단어만 추출.
    """
    prompt = f"다음 텍스트에서 알약 이름만 추출하여 중복을 제거하고 JSON 형태로 반환해줘: {text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.5
    )

    result = response["choices"][0]["text"].strip()
    return json.loads(result)


def main(image_path):
    text = ocr_process(image_path)
    if text:
        pills = extract_pills_from_text(text)
        print("추출된 알약 목록 (JSON):", json.dumps(pills, ensure_ascii=False, indent=4))
    else:
        print("텍스트를 추출하지 못했습니다.")


if __name__ == "__main__":
    image_path = input("이미지 경로를 입력하세요: ")
    main(image_path)
