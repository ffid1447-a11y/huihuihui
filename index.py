from flask import Flask, request, jsonify, make_response
import requests

app = Flask(__name__)

# ====================================
# CONFIG
# ====================================
HALFBLOOD_URL = "https://halfblood.famapp.in/vpa/verifyExt"

# ====================================
# NEW HEADERS (Updated by Alok)
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
# MAIN FUNCTION (IFSC REMOVED)
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
    except:
        return {"error": "Invalid JSON from HalfBlood", "raw": resp.text}, 502

    # ❌ No IFSC extraction
    # ❌ No IFSC API hit
    data["status"] = "success"

    return data, 200


# ====================================
# ROUTES
# ====================================
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


# ============ VERCEL ===============
def handler(request, response):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
