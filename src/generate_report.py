import os
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from jinja2 import Template
import pytz

# Waxfoot Willy style phrases
GREETINGS = [
    "Yewww! Morning, wave wranglers!",
    "Top o’ the tide to ya, surf squad!",
    "Waxfoot Willy dropping in with your swell scoop!",
]
ADLIBS = [
    "Wax on, wax off… that surf is soft as a marshmallow!",
    "Time to wax that board—and maybe those toes!",
    "No worry, just paddle—and maybe hump back up the beach!",
]
CLOSINGS = [
    "That's a wrap from yer salty narrator, Waxfoot Willy.",
    "Stay waxed, stay stoked—‘til next swell!",
    "Catch ya on the next curl—Willy out!",
]
JOKES = [
    "Why did the surfer bring string to the beach? To tie the waves together!",
    "Surfing’s the only sport where wiping out is part of the ride!",
    "Why don’t surfers tell secrets? Because the ocean might leak ‘em!",
]

# URLs to scrape (non-API public websites)
SURF_URL = "https://deepswell.com/surf-report/US/South-Carolina/Folly-Beach-Southside/1163"
SURF_CAPTAIN_URL = "https://surfcaptain.com/forecast/folly-beach-south-carolina"

REPORT_TEMPLATE = """
🏄‍♂️ Surf Report – Folly Beach, SC – {{ date }}

{{ greeting }}

Surf Height: {{ surf_height }}
Buoy says: {{ buoy }}
Water Temp (approx): {{ water_temp }}
Tide Notes: {{ tide_notes }}

{{ adlib }}

Joke o’ the day:
"{{ joke }}"

{{ closing }}
"""

def fetch_deepswell():
    try:
        res = requests.get(SURF_URL, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        surf_height = "N/A"
        tide_notes = "N/A"

        # Find first mention of feet for surf height (simplified scraping)
        surf_elem = soup.find(string=lambda t: t and "ft" in t)
        if surf_elem:
            surf_height = surf_elem.strip()

        tide_notes = "Check tide charts online"

        return surf_height, tide_notes
    except Exception:
        return "N/A", "N/A"

def fetch_surfcaptain():
    try:
        res = requests.get(SURF_CAPTAIN_URL, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        buoy = "N/A"
        water_temp = "N/A"

        temp_elem = soup.find(string=lambda t: t and "Water Temp" in t)
        if temp_elem:
            water_temp = temp_elem.find_next().text.strip()

        return buoy, water_temp
    except Exception:
        return "N/A", "N/A"

def generate_report():
    surf_height, tide_notes = fetch_deepswell()
    buoy, water_temp = fetch_surfcaptain()

    est = pytz.timezone("US/Eastern")
    now_est = datetime.now(est)
    date_str = now_est.strftime("%A, %B %d, %Y %I:%M %p %Z")

    greeting = random.choice(GREETINGS)
    adlib = random.choice(ADLIBS)
    closing = random.choice(CLOSINGS)
    joke = random.choice(JOKES)

    template = Template(REPORT_TEMPLATE)
    report_text = template.render(
        date=date_str,
        greeting=greeting,
        surf_height=surf_height,
        buoy=buoy,
        water_temp=water_temp,
        tide_notes=tide_notes,
        adlib=adlib,
        joke=joke,
        closing=closing,
    )

    os.makedirs("site", exist_ok=True)
    with open("site/report.txt", "w") as f:
        f.write(report_text)

    print("Report generated and saved to site/report.txt")

if __name__ == "__main__":
    generate_report()
