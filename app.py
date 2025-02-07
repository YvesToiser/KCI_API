from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/KC', methods=['GET'])
def KC():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
    }
    url = "https://www.transfermarkt.fr/kingsley-coman/verletzungen/spieler/243714/plus/1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        zentriert_cells = soup.find_all("td", attrs={"class": "zentriert"})
        end_last = zentriert_cells[2].text.strip()
        if end_last == "":
            return "yes"
        else:
            return "no"
    else:
        return "request_failed"


if __name__ == '__main__':
    app.run()