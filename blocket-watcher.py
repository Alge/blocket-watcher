import requests
import traceback
from bs4 import BeautifulSoup
from pprint import pprint
import re
import sys
import json
import config

def send_sms(t, f, message):
    response = requests.post(
      'https://api.46elks.com/a1/sms',
      auth = config.elks_auth,
      data = {
        'from': f,
        'to': t,
        'message': message,
        #'dryrun': 'yes'
      }
    )
    print("Sent sms")
    print(response.text)
    print(response.status_code)
    return response

def load_db(db_file):

    db = []
    try:
        db = json.load(open(db_file, "r"))
    except:
        pass

    return db

def save_db(db, db_file):
    open(db_file, "w").write(json.dumps(db))

db_file = "db.json"
db = load_db(db_file)

def check_searchlink(url):
    html_doc = requests.get(url).text

    soup = BeautifulSoup(html_doc, 'html.parser')

    result_list = soup.find(attrs={"data-cy":"search-results"})

    for child in result_list.children:
        try:
            try: # There's a extra empty(?) div we don't care about
                link = "https://blocket.se" + child['to']
            except:
                continue

            ad_id = link.split("/")[-1]

            title = child.find("span", attrs={'class': re.compile(".*styled__SubjectContainer.*")}).contents[0]
            try: # Some ads doesn't have a price
                price = child.find("div", attrs={'class': re.compile(".*Price__StyledPrice.*")}).contents[0]
            except:
                price = "No price set"

            added = child.find("p", attrs={'class': re.compile(".*styled__Time.*")}).contents[0]

            if ad_id in db: # Already found this one
                continue

            print(f"Title: {title}")
            print(f"ID: {ad_id}")
            print(f"Link: {link}")
            print(f"Added: {added}")
            print(f"Price: {price}")

            send_sms(config.notifyNumber, "Ny annons", f"{title}\n{price}\n{added}\n{link}")
            db.append(ad_id)

        except Exception as e:
            print(traceback.format_exc())
            print(e)
        print("\n#############################################################\n")


urls = [
    "https://www.blocket.se/annonser/stockholm/for_hemmet/bygg_tradgard?cg=2020&f=p&q=duschkabin&r=11",
]

for url in urls:
    check_searchlink(url)

save_db(db, db_file)


