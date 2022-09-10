# Title: BattleNet generator
#
# Description: Goes to battle net website an makes accounts
#
# Author: Mr_bond#2732


from playwright.sync_api import sync_playwright
from threading import Thread
import time
from webbrowser import get
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, expect
import time
import string
import json
import requests
import threading
import sys
import os
import random
import hashlib


def create_account():

    token = ''
    country = 'usa'
    operator = 'any'
    blizzard_country = 'USA'
    battle_tag = 'mrBond'
    secret_answer1 = 'San Diego'
    email_doamin = '@outlook.com'
    proxy = 'Yes'

    # checking if proxy is selected
    if proxy == "Yes":
        p = open('proxy.txt').read().splitlines()
        proxy1 = random.choice(p)

        print(proxy1)

    def random_char(char_num):
        return "".join(random.choice(string.ascii_letters) for _ in range(char_num))

    def random_num(charnum1):
        return "".join(random.choice(string.digits) for _ in range(charnum1))

    first_name = [
        "Nathania",
        "Narin",
        "Nan",
        "Nahshon",
        "Nafeesah",
        "Nadira",
        "Nadina",
        "Mystie",
        "Myrtle",
        "Mylinh",
        "Musa",
        "Morganne",
        "Montia",
        "Moncia",
        "Demaris",
        "Delynn",
        "Delmer",
        "Deisi",
        "Deanndra",
        "Deacon",
        "Daylan",
        "Azariah",
        "Aynsley",
        "Avia",
        "Avanti",
        "Aurielle",
    ]
    last_name = [
        "MENDEZ",
        "BUSH",
        "VAUGHN",
        "PARKS",
        "DAWSON",
        "SANTIAGO",
        "NORRIS",
        "LOVE",
        "STEELE",
        "CURRY",
        "POWERS",
        "SCHULTZ",
        "BARKER",
        "GUZMAN",
        "PAGE",
        "MUNOZ",
        "BALL",
        "GIBBS",
        "TYLER",
        "GROSS",
        "FITZGERALD",
        "STOKES",
        "DOYLE",
        "SHERMAN",
        "SAUNDERS",
        "WISE",
        "COLON",
        "GILL",
        "ALVARADO",
        "GREER",
        "PADILLA",
        "SIMON",
        "WATERS",
        "NUNEZ",
        "BOONE",
        "CORTEZ",
    ]
    random1 = ["01", "02", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    random1 = random.choice(random1)
    random2 = random.randint(10, 29)
    random3 = random.randint(1970, 2002)
    first_name1 = random.choice(first_name).lower()
    last_name1 = random.choice(last_name).lower()
    email = first_name1 + last_name1 + random_num(7)
    email1 = email + email_doamin
    password = random_char(7) + random_num(6)

    # start of playwright
    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=False)
    # launching playwright with proxy
    # if proxy == "Yes":
    #     browser = playwright.firefox.launch(headless=False, proxy={"server": proxy1})

    # launching playwright without proxy

    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context( viewport={"width": 500, "height": 400},device_scale_factor=2,)
    #        viewport={"width": 500, "height": 400},
        #device_scale_factor=2,
    page = context.new_page()
    page.set_default_timeout(9000000)
    page.goto("https://account.battle.net/creation/flow/creation-full")
    time.sleep(4)
    page.locator("//select[@id='capture-country']").select_option(blizzard_country)
    time.sleep(2)
    page.type(
        '//input[@name="dob-plain"]',
        str(random1) + str(random2) + str(random3),
        delay=100,
    )
    time.sleep(1)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    page.type('//input[@name="first-name"]', first_name1, delay=100)
    time.sleep(1)
    page.type('//input[@name="last-name"]', last_name1, delay=100)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    time.sleep(1)
    page.type('//input[@name="email"]', email1, delay=100)

    # request for 5sim number
    product = "blizzard"



    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
    }

    response = requests.get('https://5sim.net/v1/user/buy/activation/' + country + '/' + operator + '/' + product, headers=headers)
    time.sleep(1)
    data = json.loads(response.text)
    id = data["id"]
    phone_number = data["phone"]
    time.sleep(1)
    page.locator("//input[@id='capture-phone-number']").fill(phone_number)
    time.sleep(1)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(2)

    # checking if "phone number in use" pops up
    error = page.content()
    check_message = "Phone number is already in use"
    if check_message in error:
        time.sleep(2)
        requests.get("https://5sim.net/v1/user/cancel/" + str(id), headers=headers)
        time.sleep(2)
        browser.close()
        t1 = threading.Thread(target=create_account)
        t1.start()

    # start of 5sim sms code request
    sms_code = ""
    while True:
        response = requests.get(
            "https://5sim.net/v1/user/check/" + str(id), headers=headers
        )
        data = json.loads(response.text)
        sms_code = ""
        if data["status"] == "RECEIVED":
            page.click("//a[@id='resend-sms-verification']")
            time.sleep(11)
            if data["sms"]:
                sms_code = data["sms"][0]["code"]
                time.sleep(6)
                break
        elif data["status"] == "PENDING":
            page.click("//a[@id='resend-sms-verification']")
            time.sleep(6)
        else:
            requests.post("https://5sim.net/v1/user/cancel/" + id, headers=headers)

    page.locator("//input[@id='field-0']").fill(sms_code[0])
    page.locator("//input[@id='field-1']").fill(sms_code[1])
    page.locator("//input[@id='field-2']").fill(sms_code[2])
    page.locator("//input[@id='field-3']").fill(sms_code[3])
    page.locator("//input[@id='field-4']").fill(sms_code[4])
    page.locator("//input[@id='field-5']").fill(sms_code[5])

    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(2)
    # page.evaluate("document.getElementById('capture-opt-in-blizzard-news-special-offers').click();")
    page.evaluate("document.getElementsByClassName('step__checkbox')[1].click();")
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    page.type('//*[@id="capture-password"]', password, delay=200)
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(2)
    page.locator("//input[@id='capture-battletag']").fill(battle_tag)
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    page.goto("https://account.battle.net/security")
    time.sleep(3)
    page.goto("https://account.battle.net/security")
    time.sleep(3)
    page.locator("//input[@id='accountName']").type(email1, delay=100)
    time.sleep(1)
    page.locator("//input[@id='password']").type(password, delay=100)
    time.sleep(1)
    page.click("//button[@id='submit']")
    time.sleep(8)
    if page.title() == "Battle.net Login":
        page.click("//button[@id='submit']")
    time.sleep(3)
    page.click("//a[normalize-space()='Select a Secret Question']")
    time.sleep(1)
    page.locator('//*[@id="question-select"]').select_option("21")
    time.sleep(1)
    page.locator('//*[@id="answer"]').type(secret_answer1)
    time.sleep(1)
    time.sleep(1)
    page.click("//button[@id='sqa-submit']")
    time.sleep(2)
    

    # out putting accounts to .txt
    data_list = [email1, password, secret_answer1]
    with open("battlenet_accounts.txt", "a") as f:
        json.dump(data_list, f, indent=4)
        f.write("\n")
        f.close
    time.sleep(2)

    browser.close()


def main():
    acc = input("Accounts to make: ")
    acc1 = int(acc)



    for i  in range(0,acc1):
        t1 = threading.Thread(target=create_account)
        time.sleep(1)


        t1.start()

main()