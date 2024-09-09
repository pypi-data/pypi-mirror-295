import os
import time
import json
import sys
import random
import string
import webbrowser
import uuid
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pyfiglet import Figlet
from subprocess import run
import argparse
import requests
from bs4 import BeautifulSoup

# color
blueVal = "94m"
redVal = "91m"
greenVal = "32m"
whiteVal = "97m"
yellowVal = "93m"
cyanVal = "96m"

# normal
normal = "\33["
# Bold
bold = "\033[1;"
# Color Normal
blue = normal + blueVal
red = normal + redVal
green = normal + greenVal
white = normal + whiteVal
yellow = normal + yellowVal
cyan = normal + cyanVal
# Color Bold
blueBold = bold + blueVal
redBold = bold + redVal
greenBold = bold + greenVal
whiteBold = bold + whiteVal
yellowBold = bold + yellowVal
cyanBold = bold + cyanVal

version = "13"

# color end
end = '\033[0m'
colorArr = ["\033[1;91m", "\033[1;92m", "\033[1;93m", "\033[1;94m", "\033[1;95m", "\033[1;96m"]

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def fb():
    if os.name == 'nt':
        webbrowser.open('https://www.facebook.com/skillsiam1245/')
    else:
        os.system('xdg-open https://www.facebook.com/skillsiam1245/')

def github():
    if os.name == 'nt':
        webbrowser.open('https://github.com/SIAMRAHMAN000/')
    else:
        os.system('xdg-open https://github.com/SIAMRAHMAN000/')

def chat():
    if os.name == 'nt':
        webbrowser.open('https://m.me/skillsiam1245')
    else:
        os.system('xdg-open https://m.me/skillsiam1245')

def insta():
    if os.name == 'nt':
        webbrowser.open('https://www.instagram.com/skillsiam/')
    else:
        os.system('xdg-open https://www.instagram.com/skillsiam/')

def printchar(w, t):
    for word in w + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(t)

def lolcat(text):
    run(["lolcat"], input=text, text=True)

def show_colors():
    for color in colorArr:
        lolcat(f"{color}Sample Text{end}")

# Import All Module
try:
    import requests
except:
    printchar(cyanBold + "installing requests.....", 0.05)
    time.sleep(2)
    os.system("pip install requests")
    import requests
    printchar(greenBold + "requests successfully installed.....", 0.05)
    time.sleep(2)
    clr()

def banner():
    front = Figlet(font='big')
    acii = front.renderText('S I A M ')
    lenc = base64.b64encode(acii.encode("ascii", "strict"))
    encl = repr(lenc)[2:-1]
    siaml = f'{encl}'
    msg = base64.b64decode(siaml)
    decoded_value = msg.decode('ascii', 'strict')
    siamlo = decoded_value.center(20, "O")
    
    infosiam = f'''
    ╔════════════════════════════════════╗
    ║                                    ║
    ║        AUTHOR => SIAM RAHMAN       ║
    ║        VERSION => {version}               ║
    ║        STATUS => FREE              ║ 
    ║        TOOL =>   LOOKUP            ║
    ║                                    ║
    ╚════════════════════════════════════╝
'''
    clr()
    lolcat(siamlo)
    lolcat(infosiam)
def bl():
    front = Figlet(font='big')
    acii = front.renderText('F B - A C C')
    lenc = base64.b64encode(acii.encode("ascii", "strict"))
    encl = repr(lenc)[2:-1]
    siaml = f'{encl}'
    msg = base64.b64decode(siaml)
    decoded_value = msg.decode('ascii', 'strict')
    siamlo = decoded_value.center(20, "O")
    infosiam = f'''
    ╔════════════════════════════════════╗
    ║        AUTHOR => SIAM RAHMAN       ║
    ╚════════════════════════════════════╝
'''
    lolcat(siamlo)
    lolcat(infosiam)
def banner_premium():
    front = Figlet(font='big')
    acii = front.renderText('S I A M ')
    lenc = base64.b64encode(acii.encode("ascii", "strict"))
    encl = repr(lenc)[2:-1]
    siaml = f'{encl}'
    msg = base64.b64decode(siaml)
    decoded_value = msg.decode('ascii', 'strict')
    siamlo = decoded_value.center(20, "O")
    
    infosiam = f'''
    ╔════════════════════════════════════╗
    ║                                    ║
    ║        AUTHOR => SIAM RAHMAN       ║
    ║        VERSION => {version}               ║
    ║        STATUS => PREMIUM           ║ 
    ║        TOOL =>   LOOKUP            ║
    ║                                    ║
    ╚════════════════════════════════════╝
'''
    clr()
    lolcat(siamlo)
    lolcat(infosiam)

def option():
    option = f'''{random.choice(colorArr)}
    [1] NUMBER TO FB
    ''' + end
    lolcat(option)

def siam():
    clr()
    banner()
    option()
    input_options = str(input(f"  {random.choice(colorArr)}  CHOOSE A OPTION: {random.choice(colorArr)}"))

    if input_options == "1":
        clr()
        banner()
        look()
    # elif input_options == "3":
    #     github()
    else:
        siam()

def fetch_all_accounts(phone_number):
    url = "https://mbasic.facebook.com/login/identify/?ctx=recover&c=/login/&search_attempts=1&ars=facebook_login&alternate_search=0&show_friend_search_filtered_list=0&birth_month_search=0&city_search=0"
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "datr=U1ncZpR3XN7pz-4YmvUIc4cN; sb=U1ncZvcCtDXfcgOzE-MLpQSi",
        "DNT": "1",
        "Host": "mbasic.facebook.com",
        "Origin": "https://mbasic.facebook.com",
        "Referer": "https://mbasic.facebook.com/login/identify/?ctx=recover&c=https%3A%2F%2Fmbasic.facebook.com%2Flogin&multiple_results=0&ars=facebook_login&from_login_screen=0&lwv=100&_rdr",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }
    
    data = {
        "lsd": "AVpCOwPKQKo",
        "jazoest": "2950",
        "email": phone_number,
        "did_submit": "Search"
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        # Parse the HTML response using BeautifulSoup with 'html.parser'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        names = [name.get_text() for name in soup.find_all('strong')]
        image_tags = soup.find_all('img', src=True)
        
        profile_images = [img_tag['src'] for img_tag in image_tags if img_tag['src'].startswith("https://www.facebook.com/profile/pic.php")]
        
        results = []
        for name, img_url in zip(names, profile_images):
            result = {
                "name": name,
                "profile": img_url,
                "developer": "Siam Rahman"
            }
            results.append(result)
        
        return results
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

def print_results_with_colors(results):
    for result in results:
        name_color = random.choice(colorArr)
        profile_color = random.choice(colorArr)
        
        lolcat(f"{name_color}NAME : {result['name']}{end}")
        lolcat(f"{profile_color}PROFILE: {result['profile']}{end}")
        print()

def look():
    target = input(f"  {random.choice(colorArr)} INPUT TARGET : {random.choice(colorArr)}")
    results = fetch_all_accounts(target)
    clr()
    bl()
    print()
    print_results_with_colors(results)
