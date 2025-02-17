from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from dotenv import load_dotenv

import os

app = Flask(__name__)

CORS(app)
load_dotenv()
whitelisted_ips_str = os.getenv('WHITELISTED_IPS', '')
WHITELISTED_IPS = [ip.strip() for ip in whitelisted_ips_str.split(',') if ip.strip()]

@app.route('/KC', methods=['GET'])
def KC():
    client_ip = request.remote_addr
    if client_ip not in WHITELISTED_IPS:
        return jsonify({"error": "Unauthorized"}), 403

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
    }
    url = "https://www.transfermarkt.en/kingsley-coman/verletzungen/spieler/243714/plus/1"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        zentriert_cells = soup.find_all("td", attrs={"class": "zentriert"})
        hauptlink_cells = soup.find_all("td", attrs={"class": "hauptlink"})

        last_injury_date = zentriert_cells[2].text.strip()
        is_injured = last_injury_date == ""
        injury_type = hauptlink_cells[0].text.strip()

        injury_info = {
            "isInjured": is_injured,
            "lastInjuryDate": last_injury_date,
            "InjuryType": injury_type
        }

        return jsonify(injury_info)

    else:
        return "request_failed"


if __name__ == '__main__':
    app.run()