import requests
from bs4 import BeautifulSoup
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COURSE_PAGE_URL = "https://reg.exam.dtu.ac.in/student/courseRegistration/6497168af608d957ec3b5778"
REGISTRATION_BASE = "https://reg.exam.dtu.ac.in/student/courseRegister/6497168af608d957ec3b5778/"
REFRESH_INTERVAL = 5  # seconds

TARGET_COURSES = {
    "BASIC ECONOMETRICS": "686e5513d00bc35c8c12b7f3",
    "LOGISTICS MANAGEMENT": "686e5513d00bc35c8c12b7f7",
    "MACROECONOMICS": "686e5513d00bc35c8c12b813",
    "CREATIVE WRITING SKILLS": "686e5513d00bc35c8c12b817",
    "MARKETING RESEARCH": "686e5513d00bc35c8c12b81f",
    "TOTAL QUALITY MANAGEMENT": "686e5513d00bc35c8c12b823",
    "MALWARE ANALYSIS": "686e5513d00bc35c8c12b86f",
    "SECURE CODING": "686e5513d00bc35c8c12b873",
    "MULTI MODAL DATA PROCESSING": "686e5513d00bc35c8c12b893",
}

COOKIES = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NDk3MTY4YWY2MDhkOTU3ZWMzYjU3NzgiLCJzc2lkIjo2NjMzLCJpYXQiOjE3NTI1NDc4MDd9.HIocmpEwm3uGn97gSiLIybbSngzIUQzgUwXxh1DzaYk",  # <- Replace this with your token
    "connect.sid": "s%3A-nKZRRcs8shgv8vNRHjdWeSmEiahC4Ad.QZLD7aWcg67gynUKdEfXmNslaUKJypTIFpQnJeTP5Os",  # <- Replace this with your session ID
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": COURSE_PAGE_URL,
}

def check_and_register():
    res = requests.get(COURSE_PAGE_URL, headers=HEADERS, cookies=COOKIES, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 6:
            course_name = cols[0].text.strip().replace("\n", " ").replace("  ", " ")
            seat_text = cols[4].text.strip()

            if course_name in TARGET_COURSES and seat_text.isdigit() and int(seat_text) > 0:
                print(f"🎯 Seat Available: {course_name} → {seat_text} → Registering now...")
                reg_url = REGISTRATION_BASE + TARGET_COURSES[course_name]
                reg = requests.post(reg_url, headers=HEADERS, cookies=COOKIES, verify=False)
                print("✅ Registered!" if reg.status_code == 200 else f"⚠️ Failed! Status: {reg.status_code}")
                return True
    return False

while True:
    try:
        if check_and_register():
            break
        print("⏳ No seat yet. Retrying in 5s...")
        time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("👋 Exiting manually.")
        break
    except Exception as e:
        print("❌ Error:", str(e))
        time.sleep(REFRESH_INTERVAL)
