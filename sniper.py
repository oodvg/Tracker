import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
import time
import json
import pygame
import requests
import pyperclip
from colorama import init, Fore

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def copy_to_clipboard(text):
    pyperclip.copy(text)

def ascii_vro():
    clear()
    print(f'''
     {Fore.RED}/ **/|        
     | == /        
      |  |         
      |  |         
      |  /         
       |/  







    ''')
    time.sleep(0.3)
    clear()
    print(f'''



     / **/|        
     | == /        
      |  |         
      |  |         
      |  /         
       |/  


    ''')
    time.sleep(0.3)
    clear()
    print(f'''







     / **/|        
     | == /        
      |  |                  

    ''')
    time.sleep(0.3)
    clear()
    print(f"""

     _.-^^---....,,--       
 _--                  --_  
<                        >)
|                         | 
 \._                   _./  
    ```--. . , ; .--'''       
          | |   |             
       .-=||  | |=-.   
       `-=#$%&%$#=-'   
          | ;  :|     
 _____.,-#%&$@%#&#~,._____
    """)
    time.sleep(0.6)
    clear()

ascii_vro()

init(autoreset=True)

CONFIG_FILE = "config.json"

def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while loading config file: {e}")
    return {}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while saving config file: {e}")

def get_api_key():
    try:
        config = load_config()
        api_key = config.get("api_key")
        if not api_key:
            api_key = input(f"{Fore.LIGHTBLUE_EX}✦ {Fore.GREEN} Hypixel API Key: {Fore.RESET}")
            config["api_key"] = api_key
            save_config(config)
        return api_key
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while getting API key: {e}")
        return None

def check_api_key_validity(api_key):
    try:
        url = f"https://api.hypixel.net/v2/leaderboards?key={api_key}"
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while checking API key validity: {e}")
        return False

def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{Fore.RED} > Opps, an unexpected error occurred while fetching data: Status Code {response.status_code}")
            return None
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while fetching data: {e}")
        return None

def fetch_uuid(username):
    try:
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        data = fetch_data(url)
        if data:
            return data.get("id")
        print(f"{Fore.RED} > Opps, I don't think {username} is born yet!")
        return None
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while fetching UUID: {e}")
        return None

def fetch_hypixel_status(api_key, uuid):
    try:
        url = f"https://api.hypixel.net/v2/status?key={api_key}&uuid={uuid}"
        return fetch_data(url)
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while fetching Hypixel status: {e}")
        return None
 
def fetch_player_stats(api_key, uuid):
    try:
        url = f"https://api.hypixel.net/v2/player?key={api_key}&uuid={uuid}"
        return fetch_data(url)
    except Exception as e:
        print(f"{Fore.RED} > Opps, an unexpected error occurred while fetching player stats: {e}")
        return None

def loading_animation():
    try:
        animation = "|/-\\"
        for _ in range(10):
            for char in animation:
                sys.stdout.write(f"\r {char}  {Fore.GREEN}Auto Refreshing")
                sys.stdout.flush()
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

def initialize_pygame():
    try:
        pygame.mixer.init()
    except Exception as e:
        print("")
        print(f"{Fore.RED} > Opps, an unexpected error occurred while initializing pygame: {e}")

def main():
    try:
        config = load_config()
        api_key = get_api_key()
        if not api_key:
            return

        if len(sys.argv) > 1:
            username = sys.argv[1]
        else:
            username = input(f"{Fore.LIGHTBLUE_EX}✦ {Fore.GREEN} Minecraft Username: {Fore.RESET}")

        alert = config.get("alert", True)
        if alert and not os.path.exists("alert.mp3"):
            print(f"{Fore.RED}alert.mp3 not found.")
            alert = False

        delay = config.get("delay", 0.5)
        clipboard = config.get("clipboard", True)

        uuid = fetch_uuid(username)
        if uuid:
            previous_map = None
            while True:
                status_data = fetch_hypixel_status(api_key, uuid)
                player_data = fetch_player_stats(api_key, uuid)
                if status_data:
                    session = status_data.get("session", {})
                    winstreak = player_data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("winstreak", 0)
                    star = player_data.get("player", {}).get("achievements", {}).get("bedwars_level", 0)
                    fkdr = player_data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_kills_bedwars", 0) / player_data.get("player", {}).get("stats", {}).get("Bedwars", {}).get("final_deaths_bedwars", 1)
                    online_status = "ONLINE" if session.get("online") else f"{Fore.RED}OFFLINE"
                    game_type = session.get("gameType", f"{Fore.RED}null")
                    mode = session.get("mode", f"{Fore.RED}null")
                    if clipboard:
                        copy_to_clipboard(f"/play {mode}")
                    map_name = session.get("map", f"{Fore.RED}null")

                    clear()
                    print(f"  {Fore.RED}╭────────────────╮")
                    print(f"  {Fore.RED}│ {Fore.RESET}Hypixel Sniper {Fore.RED}│ {Fore.LIGHTGREEN_EX}- made by {Fore.RESET}YongSheng {Fore.LIGHTGREEN_EX}with love <3")
                    print(f"  {Fore.RED}╰────────────────╯ ")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Username{Fore.RESET}: {Fore.RESET}{username}")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Star{Fore.RESET}: {Fore.RESET}{star}★")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} FKDR{Fore.RESET}: {Fore.RESET}{fkdr:.2f}")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Winstreak{Fore.RESET}: {Fore.RESET}{winstreak}")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Session{Fore.RESET}: {Fore.RESET}{online_status}")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Game{Fore.RESET}: {Fore.RESET}{game_type}")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Mode{Fore.RESET}: {Fore.RESET}{mode}")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Map{Fore.RESET}: {Fore.RESET}{map_name}")
                    print(f"{Fore.RESET} - {Fore.LIGHTRED_EX} Interval{Fore.RESET}: {Fore.RESET}{delay}")
                    loading_animation()

                    if alert and map_name != previous_map and previous_map is not None:
                        pygame.mixer.music.load("alert.mp3")
                        pygame.mixer.music.play()

                    previous_map = map_name

                time.sleep(delay)

    except KeyboardInterrupt:
        print(" ")
        print(f"{Fore.RED} > Program terminated by user.")
    except Exception as e:
        print(" ")
        print(f"{Fore.RED} > Opps, an unexpected error occurred: {e}")

if __name__ == "__main__":
    initialize_pygame()
    main()
