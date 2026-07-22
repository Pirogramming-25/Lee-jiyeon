# Django GPT – Hugging Face AI 웹 서비스

Hugging Face `pipeline()`을 활용해 세 가지 AI 기능을 각각 다른 URL/탭으로 제공하는 Django 웹 서비스입니다.

## 기능 및 사용 모델

| 탭 | URL | 기능 | 모델 ID | Task | 접근 권한 |
| --- | --- | --- | --- | --- | --- |
| 감정 분석 | `/sentiment/` | 영어 문장 감정 분석 | cardiffnlp/twitter-roberta-base-sentiment-latest | text-classification | 비로그인 허용 |
| 문서 요약 | `/summarize/` | 영어 문서 요약 | sshleifer/distilbart-cnn-6-6 | summarization | 로그인 필요 |
| 유해 표현 분석 | `/moderate/` | 영어 문장 유해성 분석 | unitary/toxic-bert | text-classification | 로그인 필요 |

- **입력 언어:** 전 기능 영어
- **출력 레이블**
  - 감정 분석: negative / neutral / positive (레이블 + 신뢰도)
  - 문서 요약: 요약문 + 원문/요약문 길이 + 요약 비율
  - 유해 표현: toxic / severe_toxic / obscene / threat / insult / identity_hate (멀티 레이블 점수)

## 모델 라이선스

- cardiffnlp/twitter-roberta-base-sentiment-latest — (모델 카드 확인 후 기재)
- sshleifer/distilbart-cnn-6-6 — (모델 카드 확인 후 기재)
- unitary/toxic-bert — (모델 카드 확인 후 기재)

## 실행 방법

```bash
# 1. 가상환경
python -m venv venv
source venv/Scripts/activate   # macOS: source venv/bin/activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 환경변수 설정 (.env.example 복사)
cp .env.example .env

# 4. DB 마이그레이션 + 관리자 계정 생성
python manage.py migrate
python manage.py createsuperuser

# 5. 서버 실행
python manage.py runserver --noreload
```

## 환경변수

| 변수 | 설명 |
| --- | --- |
| `SECRET_KEY` | Django 시크릿 키. `.env`에서 관리합니다. |
| `HF_TOKEN` | Hugging Face 토큰. 공개 모델만 사용하므로 비워도 동작합니다. |

## 참고

- 루트(`/`) 접속 시 `/sentiment/`로 자동 이동합니다.
- `/summarize/`, `/moderate/`는 로그인이 필요하며, 비로그인 접근 시 로그인 페이지로 이동한 뒤 로그인하면 원래 페이지로 복귀합니다.
- 회원가입 기능은 제공하지 않으며, `createsuperuser` 또는 Django Admin에서 계정을 생성합니다.