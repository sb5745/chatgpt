# config.py
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
SHA_CODE = os.getenv("SHA_CODE")

DEFAULT_MODEL = "gpt-4-turbo"
