from flask import Flask, request, jsonify
import requests
import hashlib
import hmac
import base64
import time

app = Flask(__name__)

# ✅ 네이버 검색광고 API 정보
ACCESS_LICENSE = "010000000039f3308a8d2e337716e523a074db84239929b065bed138e761ec3feb247c005c"
SECRET_KEY = "AQAAAAA58zCKjS4zdxblI6B024QjaHgijUCO1QHsxka/z0dvag=="
CUSTOMER_ID = "2502559"  # 👉 본인의 고객 ID 입력 (숫자)

# ✅ X-Signature 생성 함수
def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

@app.route('/search_keywords', methods=['GET'])
def search_keywords():
    keywords = request.args.get("keywords")  # GTPs에서 전달할 키워드 목록
    if not keywords:
        return jsonify({"error": "키워드를 입력하세요."}), 400

    url = "https://api.searchad.naver.com/keywordstool"
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    uri = "/keywordstool"
    signature = generate_signature(timestamp, method, uri, SECRET_KEY)

    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": ACCESS_LICENSE,
        "X-CUSTOMER": CUSTOMER_ID,
        "X-Signature": signature,
        "Content-Type": "application/json",
        "Accept-Charset": "utf-8"
    }
    params = {"hintKeywords": keywords, "showDetail": 1}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "API 요청 실패", "status": response.status_code, "message": response.text}), response.status_code

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))  # Railway가 8080을 기본으로 요청할 수도 있음
    app.run(host="0.0.0.0", port=port, debug=True)
