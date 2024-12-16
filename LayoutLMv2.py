import os
from google.cloud import vision
from PIL import Image, ImageDraw


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/yunseo/Desktop/development/smapill/ai_google_ocr/google-cloud-key/pro-gecko-444007-a8-1364f6fccaef.json"


def get_ocr_data(image_path):
    # Google Vision API 클라이언트 생성
    client = vision.ImageAnnotatorClient()

    # 이미지 읽기
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # OCR 요청
    response = client.document_text_detection(image=image)

    # 텍스트와 Bounding Box 추출
    ocr_data = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    ocr_data.append({
                        "text": word_text,
                        "bounding_box": [(v.x, v.y) for v in word.bounding_box.vertices]
                    })
    return ocr_data


from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification
import torch

# LayoutLMv2 초기화
processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased")
model = LayoutLMv2ForTokenClassification.from_pretrained("microsoft/layoutlmv2-base-uncased")

def analyze_layout(image_path, ocr_data):
    # 이미지 로드 및 전처리
    image = Image.open(image_path).convert("RGB")
    words = [data["text"] for data in ocr_data]
    boxes = [data["bounding_box"] for data in ocr_data]

    # LayoutLMv2 입력 처리
    encoding = processor(image, words, boxes=boxes, return_tensors="pt")

    # 레이아웃 분석 수행
    outputs = model(**encoding)
    predictions = outputs.logits.argmax(-1).squeeze().tolist()

    # 예측 결과 반환
    return predictions


def process_prescription(image_path):
    # 1. OCR 데이터 추출
    ocr_data = get_ocr_data(image_path)

    # 2. LayoutLMv2로 레이아웃 분석
    predictions = analyze_layout(image_path, ocr_data)

    # 3. OCR 데이터와 레이아웃 결과 매핑
    structured_data = []
    for i, data in enumerate(ocr_data):
        structured_data.append({
            "text": data["text"],
            "bounding_box": data["bounding_box"],
            "label": predictions[i]  # 레이아웃 분석 레이블
        })

    return structured_data


import pandas as pd

def save_to_csv(structured_data, output_file):
    # DataFrame으로 변환
    df = pd.DataFrame(structured_data)

    # CSV로 저장
    df.to_csv(output_file, index=False)

# 예제 실행
image_path = "/Users/yunseo/Desktop/development/smapill/ai_google_ocr/image/test01.jpeg"
output_file = "structured_prescription_data.csv"

structured_data = process_prescription(image_path)
save_to_csv(structured_data, output_file)
