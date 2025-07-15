import requests
import os
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://reg.exam.dtu.ac.in"
TOKEN = os.getenv("TOKEN")

HEADERS = {
    "Content-Type": "application/json",
    "Cookie": f"token={TOKEN}"
}

COURSE_PAGE = "/student/courseRegistration/649716b8f608d957ec3b68e4"
REGISTRATION_BASE = "/student/courseRegister/6497168af608d957ec3b5778/"

# Course names with their corresponding registration endpoint suffix
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

def check_courses():
    try:
        response = requests.get(BASE_URL + COURSE_PAGE, headers=HEADERS, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find rows with exactly 6 <td> columns
        rows = soup.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            if len(tds) == 6:
                course_name = tds[0].get_text(strip=True).replace("\n", " ")
                seats = int(tds[4].get_text(strip=True))

                if course_name in TARGET_COURSES and seats > 0:
                    print(f"🎯 Seat Available: {course_name} → {seats} → Registering now...")

                    register_url = BASE_URL + REGISTRATION_BASE + TARGET_COURSES[course_name]
                    post_res = requests.post(register_url, headers=HEADERS, verify=False)

                    if post_res.status_code == 200:
                        print("✅ Registration Attempt Sent. Exiting...")
                        exit(0)
                    else:
                        print("⚠️ Registration failed. Status:", post_res.status_code)

        print("No seat updates yet. Retrying in 5s...")

    except Exception as e:
        print("❌ Error occurred:", e)

if __name__ == "__main__":
    while True:
        check_courses()
        time.sleep(5)
