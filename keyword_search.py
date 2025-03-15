import requests
import hashlib
import hmac
import base64
import time

# ✅ 네이버 검색광고 API 정보
ACCESS_LICENSE = "010000000039f3308a8d2e337716e523a074db84239929b065bed138e761ec3feb247c005c"
SECRET_KEY = "AQAAAAA58zCKjS4zdxblI6B024QjaHgijUCO1QHsxka/z0dvag=="
CUSTOMER_ID = "2502559"  # 👉 여기에 본인의 고객 ID 입력 (숫자)

# ✅ 키워드 목록
keywords = ["로또", "주식", "부동산"]

# ✅ API 요청 URL
url = "https://api.searchad.naver.com/keywordstool"

# ✅ 현재 시간(timestamp) 생성 (밀리초 단위)
timestamp = str(int(time.time() * 1000))

# ✅ `X-Signature` 값 생성 함수
def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

# ✅ `X-Signature` 값 생성
uri = "/keywordstool"
method = "GET"
signature = generate_signature(timestamp, method, uri, SECRET_KEY)

# ✅ 요청 헤더 설정
headers = {
    "X-Timestamp": timestamp,         # 요청 시간 (밀리초)
    "X-API-KEY": ACCESS_LICENSE,      # API 키
    "X-CUSTOMER": CUSTOMER_ID,        # 고객 ID (숫자)
    "X-Signature": signature,         # 서명 추가
    "Content-Type": "application/json",
    "Accept-Charset": "utf-8"
}

# ✅ API 요청 파라미터 설정
params = {"hintKeywords": ",".join(keywords), "showDetail": 1}

# ✅ API 호출
response = requests.get(url, headers=headers, params=params)

# ✅ 응답 데이터 출력
if response.status_code == 200:
    print("✅ 키워드 조회 결과:")
    print(response.json())  # JSON 데이터를 출력
else:
    print(f"❌ 오류 발생: {response.status_code}")
    print(response.text)
