import json 
import os

settings_file = "settings.json"
leaderboard_file = "leaderboard.json"

#load game settings from file
def load_settings():
    if not os.path.exists(settings_file):
        return {
            "sound": True,
            "car_color": "blue",
            "difficulty": "normal"
        }
    
    with open(settings_file, "r", encoding="utf-8") as file:
        return json.load(file)
    

#save game settings to file
def save_settings(settings):
    with open(settings_file, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


#load leaderboard from file
def load_leaderboard():
    if not os.path.exists(leaderboard_file):
        return[]
    
    with open(leaderboard_file, "r", encoding="utf-8") as file:
        return json.load(file)
    
#save leaderboard to file
def save_leaderboard(leaderboard):
    with open(leaderboard_file, "w", encoding="utf-8") as file:
        json.dump(leaderboard, file, indent=4)


#add new score and keep only top 10
def add_score(name, score, distance):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    leaderboard.sort(key=lambda x: x["score"], reverse = True)
    leaderboard = leaderboard[:10]

    save_leaderboard(leaderboard)