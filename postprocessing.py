import re
import json
import requests
from datetime import datetime, timedelta
import cv2
from ocr import ocr_process

# 약물 정보 추출 함수
def extract_drug_info(text):
    """
    OCR 결과에서 약물 정보를 추출하여 JSON으로 변환.
    """
    # 약물 이름과 복용 정보 추출 정규식
    pattern = (
        r"(?P<name>[가-힣a-zA-Z0-9]+정\s*\d+mg)"  # 약물 이름 ('정' 포함 및 용량 mg 포함)
        r".*?1일\s*(?P<frequency>\d+)회"  # 1일 N회
        r".*?(?P<duration>\d+)일"  # N일 동안 복용
    )

    drugs = []
    matches = re.finditer(pattern, text, re.DOTALL)

    for match in matches:
        # 그룹 딕셔너리로 추출
        group_dict = match.groupdict()

        # 약물 이름이 지정된 약물 목록에 포함되는지 확인
        valid_names = ["덱사타펜정400mg", "덱시디펜정400mg", "코슈정", "베포타딘정10mg", "레바스타정", "타세놀8시간이알서방정"]
        name = group_dict.get("name", "Unknown")
        if name in valid_names:
            # 약물 정보 구성
            frequency = int(group_dict.get("frequency", 0))
            duration = int(group_dict.get("duration", 0))
            start_date = datetime.now().strftime("%Y-%m-%d")
            end_date = (datetime.now() + timedelta(days=duration)).strftime("%Y-%m-%d")
            instructions = f"{name}의 복용 정보를 확인하세요."

            drugs.append({
                "name": name,
                "frequency_per_day": frequency,
                "duration_days": duration,
                "instructions": instructions,
                "start_date": start_date,
                "end_date": end_date
            })

    return {"drugs": drugs}

# 바운딩 박스 그리기 함수
def draw_bounding_boxes(image_path, ocr_results):
    """
    OCR 결과에서 텍스트와 바운딩 박스를 이미지에 그립니다.
    """
    image = cv2.imread(image_path)
    for result in ocr_results:
        text = result['text']
        bbox = result['bbox']  # 바운딩 박스 좌표 [x, y, width, height]

        # 바운딩 박스 그리기
        x, y, w, h = bbox
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 텍스트 표시
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # 결과 이미지 저장
    output_path = "output_with_boxes.jpg"
    cv2.imwrite(output_path, image)
    print(f"Result saved to {output_path}")

# Flask 서버로 데이터 전송 함수
def send_to_flask_server(json_data, url):
    """
    JSON 데이터를 Flask 서버로 전송.
    """
    try:
        response = requests.post(url, json=json_data)
        response.raise_for_status()  # HTTP 상태 코드 검사
        print("Data sent successfully:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {e}")

# 메인 로직
if __name__ == "__main__":
    # 이미지 경로
    image_path = "/Users/yunseo/Desktop/development/smapill/ai_google_ocr/image/test01.jpeg"

    # 1. OCR 처리
    try:
        ocr_results = ocr_process(image_path)  # 텍스트와 바운딩 박스 정보를 반환
        ocr_text = "\n".join([res['text'] for res in ocr_results])
        print("OCR Result:\n", ocr_text)
    except Exception as e:
        print(f"Error in OCR process: {e}")
        exit(1)

    # 2. 약물 정보 추출
    try:
        drug_info = extract_drug_info(ocr_text)
        print("\nExtracted Drug Information:")
        print(json.dumps(drug_info, ensure_ascii=False, indent=4))
    except Exception as e:
        print(f"Error in extracting drug info: {e}")
        exit(1)

    # 3. 바운딩 박스 그리기
    draw_bounding_boxes(image_path, ocr_results)

    # 4. Flask 서버로 전송
    flask_server_url = "http://localhost:5001/api/process"
    send_to_flask_server(drug_info, flask_server_url)
