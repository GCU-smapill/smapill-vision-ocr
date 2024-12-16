import re

def clean_text(ocr_result):
    """
    텍스트 클리닝 함수: 불필요한 특수문자 제거 및 공백 정리
    """
    # 특수문자 제거 및 약물 관련 키워드 정규화
    cleaned_text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", ocr_result)  # 한글, 영문, 숫자만 남김
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()  # 공백 정리
    return cleaned_text


def extract_patient_name(cleaned_text):
    """
    환자 성명 뒤에 있는 이름 추출
    """
    # '환자성명' 뒤에 오는 이름을 정규식으로 추출
    match = re.search(r"환자성명\s([가-힣]+)", cleaned_text)
    if match:
        return match.group(1)
    return None


def filter_drug_names(cleaned_text):
    """
    약물 키워드 필터링 함수: 약물 이름만 추출
    """
    # 약물 관련 키워드
    drug_keywords = ["정", "캡슐", "시럽", "mg", "g"]
    
    # 약물 이름 추출
    words = cleaned_text.split()
    drugs = [word for word in words if any(keyword in word for keyword in drug_keywords)]
    return drugs

