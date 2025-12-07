import requests

HALFBLOOD_URL = "https://halfblood.famapp.in/vpa/verifyExt"

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

def handler(request):
    # GET num= OR POST body
    if request.method == "GET":
        number = request.query.get("num") or request.query.get("number")
    else:
        body = request.json()
        number = body.get("num") or body.get("number") or body.get("upi_number")

    if not number:
        return { "error": "Missing number" }

    payload = { "upi_number": number }

    try:
        resp = requests.post(HALFBLOOD_URL, headers=HALFBLOOD_HEADERS, json=payload, timeout=12)
        data = resp.json()
    except Exception as e:
        return { "error": "HalfBlood API failed", "details": str(e) }

    data["status"] = "success"  # IFSC REMOVED
    return data
