import requests
from bs4 import BeautifulSoup
import time
import urllib3
# import pygame;
# pygame.mixer.init()
# def play_buzzer():
#     pygame.mixer.music.load("buzzer.mp3")
#     pygame.mixer.music.play()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COURSE_PAGE_URL = "BASE_URL/YOUR_UNIQUE_URL"
REGISTRATION_BASE = "BASE_URL/YOUR_UNIQUE_URL"
REFRESH_INTERVAL = 5  # seconds

TARGET_COURSES = {
    "COURSE_NAME_YOU_WANT_TO_REG": "TOKEN_VALUE_FOR_CODE",
    
}

COOKIES = {
    "token": "ADD_YOUR_TOKEN_ID",
    "connect.sid": "ADD_YOUR_SESSION_ID"
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
                    # play_buzzer() 
                else:
                    print(f"Failed! Status:  {reg.status_code}")
                    print("Response:", reg.text)
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
