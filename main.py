from bs4 import BeautifulSoup as bs
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# cors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/contests")
async def get_codeforces_contests():
    url = "https://codeforces.com/contests"
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    table = soup.find("table")
    rows = table.find_all("tr")
    contests = []
    for row in rows[1:]:
        cols = row.find_all("td")
        contest_name = cols[0].text.strip()
        contest_date = cols[2].text.strip()
        duration = cols[3].text.strip()
        register_link_col = cols[5]
        if register_link_col.find("a"):
            register_link = (
                f'https://codeforces.com{register_link_col.find("a")["href"]}'
            )
        else:
            register_link = "Not Available"
        contests.append(
            {
                "contest_name": contest_name,
                "contest_date": contest_date,
                "duration": duration,
                "register_link": register_link,
            }
        )
    contests = {
        "codeforces": contests,
        "gfg": "Every week sunday 8:00 PM",
        "codechef": "Every week wednesday 8:00 PM",
    }
    return contests  # returning contests in json format


def get_codechef_contests():
    url = "https://www.codechef.com/contests"
    response = requests.get(url)
    soup = bs(response.content, "lxml")
    table = soup.find_all("div", class_="_flex__container_1idej_522")
    print(table)
