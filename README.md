# 알약 정보 추출 API 서비스

이 프로젝트는 이미지에서 OCR을 수행하고 추출된 텍스트에서 알약 이름을 식별하는 Flask 기반 API 서비스입니다.

## 📌 주요 기능
- **이미지 업로드** 처리 (JPG, PNG 지원)
- **Google Vision API** 기반 **OCR 텍스트 추출**
- **AI 모델** 활용 알약 이름 필터링(현재 OpenAI 사용, Gemini 전환 가능)
- JSON 형식의 구조화된 응답

## 🛠 기술 스택
- **Backend**: Python 3.9+, Flask
- **OCR**: Google Cloud Vision API
- **NLP**: OpenAI/Gemini(변경 가능)
- **배포**: Docker 호환 구성

## ⚙️ 설치 및 실행
