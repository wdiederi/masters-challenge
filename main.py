from bs4 import BeautifulSoup
from flask import Flask

import requests

def convertToInt(string: str):
    if (string == "E"):
        return 0
    elif (string.startswith("+")):
        return int(string[1:])
    elif (string.startswith("-")):
        return int(string)
    else: 
        return 0



app = Flask(__name__)

@app.route("/")
def display_totals():
    html = requests.get("https://www.espn.com/golf/leaderboard").text

    soup = BeautifulSoup(html, "html.parser")

    teams = {
    "Kappy": ["Jon Rahm", "Joaquin Niemann", "Tiger Woods", "Abraham Ancer", "Russell Henley", "Kevin Kisner"],
    "Jimmy": ["Justin Thomas", "Louis Oosthuizen", "Adam Scott", "Tommy Fleetwood", "Patrick Reed", "Cameron Young"],
    "Cam": ["Jordan Spieth", "Will Zalatoris", "Sam Burns", "Corey Conners", "Marc Leishman", "Luke List"],
    "Schleith": ["Cameron Smith", "Patrick Cantlay", "Tony Finau", "Sungjae Im", "Si Woo Kim", "Robert MacIntyre"],
    "Cotter": ["Rory McIlroy", "Viktor Hovland", "Shane Lowry", "Hideki Matsuyama", "Gary Woodland", "Harold Varner III"],
    "Perry": ["Dustin Johnson", "Xander Schauffele", "Tyrrell Hatton", "Justin Rose", "Bubba Watson", "Billy Horschel"],
    "Dylan": ["Collin Morikawa", "Bryson DeChambeau", "Max Homa", "Tom Hoge", "Talor Gooch", "Cameron Champ"],
    "Will": ["Brooks Koepka", "Scottie Scheffler", "Matt Fitzpatrick", "Daniel Berger", "Sergio Garcia", "Webb Simpson"],
}

    scores = {}

    total_scores = []

    for tag in soup.find_all("tr", class_="PlayerRow__Overview PlayerRow__Overview--expandable Table__TR Table__even"):
        data = tag.find_all("td")
        if data[6].text.strip() == "CUT":
            scores[data[3].text.strip()] = int(data[8].text.strip()) + int(data[7].text.strip()) - 144
        else:
            score = convertToInt(data[4].text.strip())
            if score > 4:
                score = 4
            scores[data[3].text.strip()] = score
        
    scores["Louis Oosthuizen"] = 4
    
    for team in teams:
        sum = 0
        for player in teams[team]: 
            sum += scores[player]
        total_scores.append((team, sum))

    total_scores.sort(key=lambda x: x[1])

    output = ""
    for team in total_scores:
        output += team[0] + " " + str(team[1]) + "<br/>"
    return output

display_totals()
