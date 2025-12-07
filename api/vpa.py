from flask import Flask, request, jsonify, make_response
import requests

app = Flask(__name__)

# ====================================
# CONFIG
# ====================================
HALFBLOOD_URL = "https://halfblood.famapp.in/vpa/verifyExt"

# ====================================
# HEADERS (As given by you)
# ====================================
HALFBLOOD_HEADERS = {
    "user-agent": "2312DRAABI | Android 15 | Dalvik/2.1.0 | gold | 2EF4F924D8CD3764269BD3548C4E7BF4FA070E7B | 3.11.5 (Build 525) | U78TN5J23U",
    "x-device-details": "2312DRAABI | Android 15 | Dalvik/2.1.0 | gold | 2EF4F924D8CD3764269BD3548C4E7BF4FA070E7B | 3.11.5 (Build 525) | U78TN5J23U",
    "x-app-version": "525",
    "x-platform": "1",
    "device-id": "adb84e9925c4f17a",
    "authorization": "Token eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiZXBrIjp7Imt0eSI6Ik9LUCIsImNydiI6Ilg0NDgiLCJ4IjoiOGttZkdRTlNITER2ajBJUEZja2puLWRfM1pzVVpsU05IRFhLWFRBQ3U5dWp4WldkTURjcGtpTTA5ZHM2RmRNMnVrdGI5bmk4WVRBIn0sImFsZyI6IkVDREgtRVMifQ..2m08j-LIKvBDntB0QWCRcw.FPY_Roo_CcDymuZg89S61QypL3RSEIMzN7jf1ZJKk4PIa47Vl8LMHBxVKTYd61RekOYaUUINiLUGXGzb_EPIbj1QJiU8BnbR7Hyb1j_Jn0YiRFt6Yfixy01D6EIY4894KAtQJi6kufIY7uK1jLcAx-LOZpGRYXbPSmyOPhjgtYyd83lMqkmHzbm89aX_1Wt71uf22gagdxmp4V1d2OY2QnM11DdWud-RbN0hYqFv8EGxvPzpBP5ye_VyZJzFSDFwejDK6hUofORr0eJ8BYCRXA.RL4l9X8H3h-nfp24rcCY30el9IMLXkoJuHxJoZOZNek",
    "accept-encoding": "gzip",
    "accept": "application/json",
    "Content-Type": "application/json"
}

# ====================================
# MAIN LOGIC (NO IFSC)
# ====================================
def process_number(number: str):
    if not number:
        return {"error": "Missing number"}, 400

    payload = {"upi_number": number}

    try:
        resp = requests.post(
            HALFBLOOD_URL,
            headers=HALFBLOOD_HEADERS,
            json=payload,
            timeout=12
        )
    except requests.RequestException as e:
        return {"error": "HalfBlood API request failed", "details": str(e)}, 502

    try:
        data = resp.json()
    except Exception:
        return {"error": "Invalid JSON from HalfBlood", "raw": resp.text}, 502

    # ✅ IFSC extraction hata diya
    # ✅ Kisi IFSC API ko hit nahi kar rahe
    data["status"] = "success"
    return data, 200


# ====================================
# ROUTES (for Vercel Python runtime)
# ====================================
# Vercel jab is file ko run karega to /api/vpa pe aayega
# Isliye yahan "/" bhi handle kar lete hain.
@app.route("/", methods=["GET", "POST"])
@app.route("/vpa", methods=["GET", "POST"])
@app.route("/vnum", methods=["GET", "POST"])
def number_to_vpa():
    if request.method == "GET":
        number = request.args.get("num") or request.args.get("number")
    else:
        body = request.get_json(silent=True) or {}
        number = body.get("num") or body.get("number") or body.get("upi_number")

    data, status = process_number(str(number).strip() if number else None)
    return make_response(jsonify(data), status)

# ❌ Koi `handler(request, response)` nahi
# ❌ Koi `if __name__ == "__main__": app.run(...)` nahi
# Vercel khud `app` (Flask WSGI app) ko use karega.
