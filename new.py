import requests
from bs4 import BeautifulSoup
import time
import urllib3
import pygame;
pygame.mixer.init()
def play_buzzer():
    pygame.mixer.music.load("buzzer.mp3")
    pygame.mixer.music.play()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COURSE_PAGE_URL = "https://reg.exam.dtu.ac.in/student/courseRegistration/6497168af608d957ec3b5778"
REGISTRATION_BASE = "https://reg.exam.dtu.ac.in/student/courseRegister/6497168af608d957ec3b5778/"
REFRESH_INTERVAL = 5  # seconds

TARGET_COURSES = {
    "CYBER LAWS":"686e5513d00bc35c8c12b7ef",
    "INDIAN ECONOMY": "686e5513d00bc35c8c12b73b",
    "BASIC COMMUNICATION SKILLS":"686e5513d00bc35c8c12b73f",
    "MARKETING MANAGEMENT":"686e5513d00bc35c8c12b747",
    "BASIC ECONOMETRICS": "686e5513d00bc35c8c12b7f3",
    "LOGISTICS MANAGEMENT": "686e5513d00bc35c8c12b7f7",
    "MACROECONOMICS": "686e5513d00bc35c8c12b813",
    "CREATIVE WRITING SKILLS": "686e5513d00bc35c8c12b817",
    "MARKETING RESEARCH": "686e5513d00bc35c8c12b81f",
    "TOTAL QUALITY MANAGEMENT": "686e5513d00bc35c8c12b823",
}

COOKIES = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NDk3MTY4YWY2MDhkOTU3ZWMzYjU3NzgiLCJzc2lkIjozMDc0LCJpYXQiOjE3NTI2MzMxODV9.IRYQpJoU3OvMqwPp5XxhPVc0XwbjhrH6_nN3mB8eoKo",
    "connect.sid": "s%3AH5JQBo0DaAYDq0WS9lMrjhv9BSUicUXS.CbwWLxzvLH4A0zheJG97%2FE%2B1vA4j9R6wS9FwaUfBbgc"
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
                # print("✅ Registered!" if reg.status_code == 200 else f"⚠️ Failed! Status: {reg.status_code}")
                if reg.status_code ==200:
                    print("Registered!! Yay")
                    play_buzzer()
                else:
                    print(f"Failed! Status:  {reg.status_code}")
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
