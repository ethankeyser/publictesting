import subprocess
from selenium import webdriver
import time
import zipfile
import requests
from numpy import random
import threading
import names
import json
import random
import csv
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.common.by import By


def send_webhook_forward(email, forward_email):
    with open('settings.json', 'r') as f:
        data = json.load(f)

    webhook_url_f = data['DISCORD_WEBHOOK']
    webhook = DiscordWebhook(
        url=webhook_url_f,
        username="Genned Mails")

    embed = DiscordEmbed(title="Account Forwarded :tada:", color=242424)

    embed.add_embed_field(name="Email", value=f"|| {email} ||", inline=True)
    embed.add_embed_field(name="Forwarded to", value=f"|| {forward_email} ||", inline=True)

    embed.set_image(file='gmail_logo.png')

    date_and_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    embed.set_footer(text=f"BOUNDLESS GENS {date_and_time}")

    webhook.add_embed(embed)

    response = webhook.execute()
    if response.ok:
        print('Webhook Sent!')
    else:
        print('Webhook Failed to Send.')


def send_webhook_public_forward():
    webhook = DiscordWebhook(
        url='https://discordapp.com/api/webhooks/960231662959067246/UehgCp_BHs0caE9AW0WVDkOuwCnbV6ADAew5yDUjTO5Dah8Z_EXHpZebNbGtykrKl2qX',
        username="Google Gen")

    embed = DiscordEmbed(title="Account Forwarded :tada:", color=242424)

    embed.add_embed_field(name="Type", value=f"Gmail", inline=True)

    embed.set_image(file='gmail_logo.png')

    date_and_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    embed.set_footer(text=f"BOUNDLESS GENS {date_and_time}")

    webhook.add_embed(embed)

    response = webhook.execute()
    if response.ok:
        print('Webhook Sent!')
    else:
        print('Webhook Failed to Send.')


stop = False

API_KEY = 'pk_HR4eQXNHA1yYaJAAx2Yeq9pVsaL0uAks'


def get_random_time():
    picker = random.randint(1, 3)
    if picker == 1:
        rand_time = random.uniform(2, 3)
    else:
        rand_time = random.uniform(3, 4)
    return rand_time


def get_random_time_text():
    rand_time_text = random.uniform(0.5, 1.5)
    return rand_time_text


def update_license(license_key, hardware_id):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'metadata': {
            'hwid': hardware_id
        }
    }

    req = requests.patch(f'https://api.hyper.co/v6/licenses/{license_key}/metadata', headers=headers, json=payload)
    if req.status_code == 200:
        return True

    return None


def get_license(license_key):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    req = requests.get(f'https://api.hyper.co/v6/licenses/{license_key}', headers=headers)
    if req.status_code == 200:
        return req.json()

    return None


license_authenticated = True
# key = input('Please Enter Your License Key: ')
# license_data = get_license(key)
# if license_data:
#     if license_data.get('metadata') != {}:
#         print('License is already in use on another machine!')
#         input('Press Any Key to Continue...')
#     else:
#         hwid = str(subprocess.check_output(
#             'wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
#         if update_license(key, hwid):
#             license_authenticated = True
#             print('License is good to go!')
# else:
#     print('License not found!')
#     input('Press any key to continue...')
#     exit()

indexes = []


def confirm_setup(accounts_to_forward):
    with open('settings.json', 'r') as f:
        data_confirm = json.load(f)

    master_mail = data_confirm['MASTER_MAIL']
    master_pass = data_confirm['MASTER_PASS']
    master_phone = data_confirm["MASTER_PHONE_NUMBER"]
    master_proxy = data_confirm["MASTER_PROXY"]

    using_proxy = False

    PROXY_HOST = ''
    PROXY_PORT = ''
    PROXY_USER = ''
    PROXY_PASS = ''

    if master_proxy == '':
        using_proxy = False
    else:
        proxy_vals = master_proxy.split(':')

        PROXY_HOST = proxy_vals[0]
        PROXY_PORT = proxy_vals[1]
        PROXY_USER = proxy_vals[2]
        PROXY_PASS = proxy_vals[3]
        using_proxy = True

    def send_input(text, element):
        for m in range(len(text)):
            element.send_keys(text[m])
            time.sleep(get_random_time_text())

    manifest_json = """
                    {
                        "version": "1.0.0",
                        "manifest_version": 2,
                        "name": "Chrome Proxy",
                        "permissions": [
                            "proxy",
                            "tabs",
                            "unlimitedStorage",
                            "storage",
                            "<all_urls>",
                            "webRequest",
                            "webRequestBlocking"
                        ],
                        "background": {
                            "scripts": ["background.js"]
                        },
                        "minimum_chrome_version":"22.0.0"
                    }
                    """

    background_js = """
                    var config = {
                            mode: "fixed_servers",
                            rules: {
                            singleProxy: {
                                scheme: "http",
                                host: "%s",
                                port: parseInt(%s)
                            },
                            bypassList: ["localhost"]
                            }
                        };
                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
                    function callbackFn(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    }
                    chrome.webRequest.onAuthRequired.addListener(
                                callbackFn,
                                {urls: ["<all_urls>"]},
                                ['blocking']
                    );
                    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    def get_chromedriver(use_proxy=False):
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("window-size=1280,800")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
        return driver

    browser = get_chromedriver(use_proxy=using_proxy)

    def verify():
        browser.get('https://google.com')

        time.sleep(get_random_time())

        try:
            elem = browser.find_element(By.XPATH, '//*[@id="vc3jof"]')
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.XPATH, '//*[@id="tbTubd"]/div/li[12]')
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.ID, 'L2AGLb')
            elem.click()

            time.sleep(get_random_time())
        except:
            print(f"thread[No popup found...")

        try:
            english = browser.find_element(By.XPATH, '//*[@id="SIvCob"]/a')
            english.click()
            time.sleep(get_random_time())
        except:
            print(f'Already in English...')

        sign_in = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[2]/a')
        sign_in.click()

        time.sleep(get_random_time())

        email_input = browser.find_element(By.XPATH, '//*[@id="identifierId"]')
        send_input(master_mail, email_input)

        time.sleep(get_random_time())

        next_btn = browser.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
        next_btn.click()

        time.sleep(4)

        cap_solved = False
        while not cap_solved:
            try:
                pass_input = browser.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
                send_input(master_pass, pass_input)
                time.sleep(get_random_time())
                next_btn_2 = browser.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
                next_btn_2.click()
                cap_solved = True
                break
            except:
                print('Catcha Detected, Please Solve and Click Next...')
                time.sleep(3)

        time.sleep(get_random_time())

        time.sleep(get_random_time())

        found = False
        found_count = 0
        while not found:
            try:
                gmail_button = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[1]/div/div[1]/a')
                gmail_button.click()
                found = True
                break
            except:
                found_count = found_count + 1
                found = False
                time.sleep(3)
                print('loading...')
                if found_count > 5:
                    found = True
                    break

        if found_count > 5:
            verify_num = browser.find_element(By.XPATH,
                                              '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[4]/div')
            verify_num.click()
            time.sleep(5)
            phone_input = browser.find_element(By.XPATH, '//*[@id="phoneNumberId"]')
            send_input(master_phone, phone_input)
            time.sleep(3)
            next_phone = browser.find_element(By.XPATH,
                                              '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
            next_phone.click()
            time.sleep(10)
            mail_button = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[1]/div/div[1]/a')
            mail_button.click()

        time.sleep(get_random_time())

        found_email = False
        accounts_forwarded = 0
        for n in range(accounts_to_forward):
            while not found_email:
                try:
                    unread_mails = browser.find_elements(By.CLASS_NAME, 'zE')
                    verify_tr = unread_mails[0].find_element(By.CLASS_NAME, 'a4W')
                    span_text = verify_tr.find_element(By.CLASS_NAME, 'bog')
                    title_email = span_text.text
                    print('Waiting for email...')
                    if 'Gmail Forwarding Confirmation' in title_email:
                        verify_tr.click()
                        found_email = True
                    time.sleep(3)
                except:
                    print('Waiting for email...')
                    time.sleep(3)

            time.sleep(get_random_time())

            # try:
            mail_table = browser.find_elements(By.CLASS_NAME, 'bAt')
            mail_tr = mail_table[0].find_elements(By.CLASS_NAME, 'aTN')
            mail_td = mail_tr[0].find_elements(By.CLASS_NAME, 'bAn')
            confirm_div = mail_td[0].find_elements(By.CLASS_NAME, 'a3s')
            confirm_link = confirm_div[0].find_element(By.XPATH, '//a[4]')
            confirm_link.click()
            # except:
            #     input('kjj')

            time.sleep(get_random_time())

            confirm_window = browser.window_handles[1]
            browser.switch_to.window(confirm_window)

            time.sleep(get_random_time())

            confirm_click = browser.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td/form/p/input')
            confirm_click.click()

            time.sleep(get_random_time())

            print('Success!')

            time.sleep(get_random_time())

            # with open('accounts_to_forward.csv', 'r') as actf:
            #     readeratf = csv.reader(actf)
            #     for rowf in readeratf:
            #         if rowf[0] ==
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

            r_csv = csv.reader(open('genned_gmails.csv'))
            content = list(r_csv)
            desired_row = 0
            for i in range(len(content)):
                if i != 0:
                    if content[i][0] in title_email:
                        desired_row = i

            content[desired_row][8] = 'Y'

            ff = open('genned_gmails.csv', 'w', newline='')
            writer = csv.writer(ff)
            writer.writerows(content)

            ff.close()
            time.sleep(get_random_time())
            browser.back()
            send_webhook_forward(content[desired_row][0], master_mail)
            send_webhook_public_forward()
            found_email = False
            accounts_forwarded = accounts_forwarded + 1
            if accounts_forwarded == accounts_to_forward:
                return

    v1 = threading.Thread(target=verify)
    v1.start()
    v1.join()


def forward_setup(accounts_to_forward, same_proxy):
    account_user = []
    account_pass = []
    account_recovery = []
    account_phone = []
    forward_proxies = []
    index = 0
    with open('genned_gmails.csv', 'r') as af:
        reader = csv.reader(af)
        for row in reader:
            if row[0] != 'email':
                if row[8] == 'N':
                    account_user.append(row[0])
                    account_pass.append(row[1])
                    account_recovery.append(row[4])
                    account_phone.append(row[6])
                    forward_proxies.append(row[5])
                    indexes.append(index)
            index = index + 1

    ip = []
    port = []
    user = []
    passwords = []

    if not same_proxy:
        with open('forward_proxies.txt', 'r') as f:
            forward_proxies = [line.strip() for line in f]

        difference = accounts_to_forward - len(forward_proxies)
        if difference >= 0:
            for p in range(len(accounts_to_forward)):
                if p == len(forward_proxies) - 1:
                    p = p - difference
                proxy = forward_proxies[p].split(':')
                ip.append(proxy[0])
                port.append(proxy[1])
                user.append(proxy[2])
                passwords.append(proxy[3])
        else:
            for p in range(len(forward_proxies)):
                proxy = forward_proxies[p].split(':')
                ip.append(proxy[0])
                port.append(proxy[1])
                user.append(proxy[2])
                passwords.append(proxy[3])
    else:
        for g in range(len(forward_proxies)):
            forward_proxy = forward_proxies[g].split(':')
            ip.append(forward_proxy[0])
            port.append((forward_proxy[1]))
            user.append(forward_proxy[2])
            passwords.append(forward_proxy[3])

    with open('settings.json', 'r') as f:
        data_forward = json.load(f)

    master_mail = data_forward['MASTER_MAIL']

    WEBHOOK_FORWARD = data_forward['DISCORD_WEBHOOK']

    if WEBHOOK_FORWARD == '':
        yn = input('Are you sure you want to generate without using your discord webhook? (y/n)')
        if yn != 'y':
            return

    def forward_google(task):

        PROXY_HOST = ip[task]  # rotating proxy or host
        PROXY_PORT = port[task]  # port
        PROXY_USER = user[task]  # username
        PROXY_PASS = passwords[task]  # password

        def send_input(text, element):
            for g in range(len(text)):
                element.send_keys(text[g])
                time.sleep(get_random_time_text())

        manifest_json = """
                {
                    "version": "1.0.0",
                    "manifest_version": 2,
                    "name": "Chrome Proxy",
                    "permissions": [
                        "proxy",
                        "tabs",
                        "unlimitedStorage",
                        "storage",
                        "<all_urls>",
                        "webRequest",
                        "webRequestBlocking"
                    ],
                    "background": {
                        "scripts": ["background.js"]
                    },
                    "minimum_chrome_version":"22.0.0"
                }
                """

        background_js = """
                var config = {
                        mode: "fixed_servers",
                        rules: {
                        singleProxy: {
                            scheme: "http",
                            host: "%s",
                            port: parseInt(%s)
                        },
                        bypassList: ["localhost"]
                        }
                    };
                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "%s",
                            password: "%s"
                        }
                    };
                }
                chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                );
                """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        def get_chromedriver(use_proxy=False):
            chrome_options = webdriver.ChromeOptions()
            if use_proxy:
                pluginfile = 'proxy_auth_plugin.zip'

                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument("window-size=1280,800")
            chrome_options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
            return driver

        browser = get_chromedriver(use_proxy=True)

        browser.get('https://google.com')

        time.sleep(get_random_time())

        try:
            elem = browser.find_element(By.XPATH, '//*[@id="vc3jof"]')
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.XPATH, '//*[@id="tbTubd"]/div/li[12]')
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.ID, 'L2AGLb')
            elem.click()

            time.sleep(get_random_time())
        except:
            print(f"thread[No popup found...")

        sign_in = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[2]/a')
        sign_in.click()

        time.sleep(get_random_time())

        email_input = browser.find_element(By.XPATH, '//*[@id="identifierId"]')
        send_input(account_user[task], email_input)

        time.sleep(get_random_time())

        next_btn = browser.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
        next_btn.click()

        time.sleep(4)

        pass_input = browser.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        send_input(account_pass[task], pass_input)

        time.sleep(get_random_time())

        next_btn_2 = browser.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
        next_btn_2.click()

        get_random_time()

        try:
            not_now = browser.find_element(By.XPATH, '//button[contains(text( ), "Not now")]')
            not_now.click()
        except Exception as e:
            try:
                not_now = browser.find_element(By.XPATH, '//a[contains(text( ), "Not now")]')
                not_now.click()
            except Exception as e:
                print('Not Now Button not found, moving on...')

        try:
            confirm_ = browser.find_element(By.XPATH, '//span[contains(text( ), "CONFIRM")]')
        except:
            print('Security does not need to be reviewed')
        found = False
        found_count = 0
        while not found:
            try:
                gmail_button = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[1]/div/div[1]/a')
                gmail_button.click()
                found = True
                break
            except:
                found_count = found_count + 1
                found = False
                time.sleep(3)
                print('loading...')
                if found_count > 5:
                    found = True
                    break

        if found_count > 5:
            verify_num = browser.find_element(By.XPATH,
                                              '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[4]/div')
            verify_num.click()
            time.sleep(5)
            phone_input = browser.find_element(By.XPATH, '//*[@id="phoneNumberId"]')
            send_input(account_phone[task], phone_input)
            time.sleep(3)
            next_phone = browser.find_element(By.XPATH,
                                              '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
            next_phone.click()
            time.sleep(10)
            mail_button = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[1]/div/div[1]/a')
            mail_button.click()

        time.sleep(get_random_time())
        try:
            settings_btn = browser.find_element(By.CLASS_NAME, 'FH')
            settings_btn.click()
        except:
            try:
                time.sleep(get_random_time())
                radio_button = browser.find_elements(By.CLASS_NAME, 'aho')
                radio_button[0].click()
                time.sleep(get_random_time())
                next_btn = browser.find_element(By.XPATH, '/html/body/div[19]/div[3]/button')
                next_btn.click()
                time.sleep(get_random_time())
                radio_button_2 = browser.find_elements(By.CLASS_NAME, 'aho')
                radio_button_2[2].click()
                time.sleep(get_random_time())
                done_button = browser.find_element(By.XPATH, '/html/body/div[19]/div[3]/button[1]')
                done_button.click()
                time.sleep(get_random_time())
                print('Popup completed...')
                try:
                    refresh = browser.find_element(By.XPATH, '/html/body/div[26]/div[3]/button')
                    refresh.click()
                except:
                    print("Refresh not needed...")

                settings_btn = browser.find_element(By.CLASS_NAME, 'FH')
                settings_btn.click()
            except:
                print("no popup...")

        time.sleep(get_random_time())

        found_all = False
        found_all_count = 0
        while not found_all:
            try:
                all_settings = browser.find_element(By.XPATH, '//button[contains(text( ), "See all settings")]')
                all_settings.click()
                found_all = True
                break
            except:
                found_all_count = found_all_count + 1
                print('loading...')
                if found_all_count > 5:
                    found_all = True
                    break
                time.sleep(2)
        if found_all_count > 5:
            try:
                twofa_frame = browser.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div[2]/iframe')
                browser.switch_to.frame(twofa_frame)
                cwiz1 = browser.find_element(By.XPATH, '/html/body/div/c-wiz')
                cwiz2 = cwiz1.find_element(By.XPATH, '//div/div/c-wiz')
                already_on_button = cwiz2.find_element(By.XPATH, '//button[contains(text( ), "No thanks")]')
                already_on_button.click()
                time.sleep(get_random_time())
                browser.switch_to.default_content()
                all_settings = browser.find_element(By.XPATH, '//button[contains(text( ), "See all settings")]')
                all_settings.click()
            except Exception as e:
                print(e)
                time.sleep(10000)

        time.sleep(get_random_time())

        found_imap_count = 0
        found_imap = False
        while not found_imap:
            try:
                forwarding_imap = browser.find_element(By.XPATH, '//a[contains(text( ), "Forwarding and POP/IMAP")]')
                forwarding_imap.click()
                found_imap = True
                break
            except:
                print('loading...')
                time.sleep(3)
                found_imap_count = found_imap_count + 1
                if found_imap_count > 6:
                    print('Took too long to load...')
                    found_imap = True
                    return

        time.sleep(get_random_time())

        isImap = False
        imap_status = browser.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[6]/div/table/tbody/tr[3]/td[2]/div[1]/span[2]')

        if imap_status.text == 'IMAP is enabled':
            isImap = True
        if not isImap:
            try:
                enable_imap = browser.find_element(By.XPATH,
                                                   '//*[@id=":1"]/div/div/div/div/div/div/div[6]/div/table/tbody/tr[3]/td[2]/div[1]/table[1]/tbody/tr/td[2]/label')
                enable_imap.click()

                time.sleep(get_random_time())

                save_changes = browser.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[6]/div/table/tbody/tr[4]/td/div/button[1]')
                save_changes.click()

                time.sleep(get_random_time())
                time.sleep(get_random_time())

                settings_btn = browser.find_element(By.CLASS_NAME, 'FH')
                settings_btn.click()

                time.sleep(get_random_time())

                try:
                    all_settings = browser.find_element(By.XPATH, '//button[contains(text( ), "See all settings")]')
                    all_settings.click()
                except:
                    try:
                        twofa_frame = browser.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div[2]/iframe')
                        browser.switch_to.frame(twofa_frame)
                        cwiz1 = browser.find_element(By.XPATH, '/html/body/div/c-wiz')
                        cwiz2 = cwiz1.find_element(By.XPATH, '//div/div/c-wiz')
                        already_on_button = cwiz2.find_element(By.XPATH, '//button[contains(text( ), "Already on")]')
                        already_on_button.click()
                        time.sleep(get_random_time())
                        browser.switch_to.default_content()
                        all_settings = browser.find_element(By.XPATH, '//button[contains(text( ), "See all settings")]')
                        all_settings.click()
                    except Exception as e:
                        print(e)
                        time.sleep(10000)
            except:
                print('IMAP Already Enabled...')

        time.sleep(get_random_time())

        forwarding_imap = browser.find_element(By.XPATH, '//a[contains(text( ), "Forwarding and POP/IMAP")]')
        forwarding_imap.click()

        time.sleep(get_random_time())

        try:
            forward_table = browser.find_elements(By.CLASS_NAME, 'cf')
            # forward_tr = forward_table[0].find_elements(By.CLASS_NAME, 'r7')
            # print('tr')
            # forward_td = forward_tr[0].find_elements(By.CLASS_NAME, 'r9')
            # print('td')
            add_forwarding = forward_table[0].find_element(By.XPATH, '//tbody/tr/td[2]/div/div[2]/input')
            add_forwarding.click()
        except Exception as e:
            print(e)

        time.sleep(get_random_time())

        try:
            # forwarding_address = browser.find_element(By.XPATH, '//div[contains(text( ), "Please enter a new forwarding email address:")]')
            forwarding_address = browser.find_elements(By.CLASS_NAME, 'PN')
            forwarding_address_input = browser.find_element(By.XPATH, '//div[@class="PN"]/input')
            send_input(master_mail, forwarding_address_input)
        except Exception as e:
            print(e)
            print('Send above error code to dev')

        time.sleep(get_random_time())

        next_btn_forward = browser.find_element(By.XPATH, '//button[contains(text( ), "Next")]')
        next_btn_forward.click()

        time.sleep(get_random_time())

        main_page = browser.current_window_handle
        try:
            popup = browser.window_handles[1]
            browser.switch_to.window(popup)
        except:
            print('Account already forwarding...')
            return

        time.sleep(get_random_time())

        proceed = browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr/td/input[3]')
        proceed.click()

        time.sleep(get_random_time())

        browser.switch_to.window(main_page)

        print("Email sent.")

    for r in range(accounts_to_forward):
        fwd1 = threading.Thread(target=forward_google, args=[r])
        fwd1.start()
        fwd1.join()


accounts_created = []


def gen_google(task, tasks_to_run, concurrent_tasks, proxies_available):

    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]

    if len(proxies) == 0:
        print('Please Insert Proxies into proxies.txt...')
        input('Press Any Key to Continue...')
        return
    elif proxies[0] == '---Insert Proxies Here---':
        print('Please Insert Proxies into proxies.txt...')
        input('Press Any Key to Continue...')
        return

    with open('settings.json', 'r') as f:
        data = json.load(f)

    API_KEY = data['API_KEY']
    CATCHALL = data['CATCHALL']
    WEBHOOK = data['DISCORD_WEBHOOK']
    if API_KEY == 'Insert sms-gen API Key Here':
        print('Please enter sms-gen api key. If you do not have an account or funds, please visit https://sms-gen.com/')
        input('Press any key to continue...')
        return

    if CATCHALL == 'Insert Catchall Here' or CATCHALL == '':
        yn = input('Are you sure you want to generate without adding a recovery email? (y/n)')
        if yn != 'y':
            return

    if WEBHOOK == '':
        yn = input('Are you sure you want to generate without using your discord webhook? (y/n)')
        if yn != 'y':
            return

    with open('settings.json', 'r') as f:
        data = json.load(f)

    api_key = data['API_KEY']
    catchall = data['CATCHALL']
    webhook_url = data["DISCORD_WEBHOOK"]

    def send_webhook(email, password, recovery, phone, gen_proxy):
        webhook = DiscordWebhook(
            url=webhook_url,
            username="Genned Mails")

        embed = DiscordEmbed(title="Account Created :tada:", color=242424)

        embed.add_embed_field(name="Email", value=f"|| {email} ||", inline=True)
        embed.add_embed_field(name="Password", value=f"|| {password} ||", inline=True)
        embed.add_embed_field(name="Recovery", value=f"|| {recovery} ||", inline=True)
        embed.add_embed_field(name="Proxy", value=f"|| {gen_proxy} ||", inline=True)
        embed.add_embed_field(name="Phone", value=f"|| {phone} ||", inline=True)

        embed.set_image(file='gmail_logo.png')

        date_and_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        embed.set_footer(text=f"BOUNDLESS GENS {date_and_time}")

        webhook.add_embed(embed)

        response = webhook.execute()
        if response.ok:
            print('Webhook Sent!')
        else:
            print('Webhook Failed to Send.')

    def send_webhook_public():
        webhook = DiscordWebhook(
            url='https://discordapp.com/api/webhooks/960231662959067246/UehgCp_BHs0caE9AW0WVDkOuwCnbV6ADAew5yDUjTO5Dah8Z_EXHpZebNbGtykrKl2qX',
            username="Google Gen")

        embed = DiscordEmbed(title="Account Created :tada:", color=242424)

        embed.add_embed_field(name="Type", value=f"Gmail", inline=True)
        embed.add_embed_field(name="Verification", value=f"PVA + Recovery", inline=True)

        embed.set_image(file='gmail_logo.png')

        date_and_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        embed.set_footer(text=f"BOUNDLESS GENS {date_and_time}")

        webhook.add_embed(embed)

        response = webhook.execute()
        if response.ok:
            print('Webhook Sent!')
        else:
            print('Webhook Failed to Send.')

    if int(concurrent_tasks) > 1:
        proxies_available = proxies_available.split(',')
        start = 0
        finish = 0
        total = 0

        for i in range(task - 1):
            total = total + int(proxies_available[i])

        start = total
        finish = (total + int(proxies_available[task - 1])) - 1
    else:
        proxies_available = int(proxies_available)
        start = 0
        finish = proxies_available - 1

    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]

    number_of_proxies = len(proxies)

    ip = []
    port = []
    user = []
    passwords = []

    for p in range(start, finish + 1):
        proxy = proxies[p].split(':')
        ip.append(proxy[0])
        port.append(proxy[1])
        user.append(proxy[2])
        passwords.append(proxy[3])

    def gen_account(task_num):
        f_name = names.get_first_name('male')
        l_name = names.get_last_name()
        rand_pass = ''
        for k in range(8):
            letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            index = random.randrange(len(letters))
            rand_pass += letters[index]
        for t in range(2):
            numbers = '1234567890'
            index = random.randrange(len(numbers))
            rand_pass += numbers[index]

        email_name = f_name + l_name

        PROXY_HOST = ip[task_num]  # rotating proxy or host
        PROXY_PORT = port[task_num]  # port
        PROXY_USER = user[task_num]  # username
        PROXY_PASS = passwords[task_num]  # password

        def send_input(text, element):
            for m in range(len(text)):
                element.send_keys(text[m])
                time.sleep(get_random_time_text())

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        def get_chromedriver(use_proxy=False):
            chrome_options = webdriver.ChromeOptions()
            if use_proxy:
                pluginfile = 'proxy_auth_plugin.zip'

                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument("window-size=1280,800")
            chrome_options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
            return driver

        browser = get_chromedriver(use_proxy=True)

        def generate_activity():
            gmail_button = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[1]/div/div[1]/a')
            gmail_button.click()
            time.sleep(get_random_time())
            crisis_averted = False
            while not crisis_averted:
                try:
                    unread_mails = browser.find_elements(By.CLASS_NAME, 'zE')
                    unread_mails[len(unread_mails) - 1].click()
                    crisis_averted = True
                    break
                except:
                    try:
                        time.sleep(get_random_time())
                        radio_button = browser.find_elements(By.CLASS_NAME, 'aho')
                        radio_button[0].click()
                        time.sleep(get_random_time())
                        next_btn = browser.find_element(By.XPATH, '//button[contains(text( ), "Next")]')
                        next_btn.click()
                        time.sleep(get_random_time())
                        radio_button_2 = browser.find_elements(By.CLASS_NAME, 'aho')
                        radio_button_2[2].click()
                        time.sleep(get_random_time())
                        done_button = browser.find_element(By.XPATH, '//button[contains(text( ), "Done")]')
                        done_button.click()
                        time.sleep(get_random_time())
                        print('Popup completed...')
                        try:
                            refresh = browser.find_element(By.XPATH, '//button[contains(text( ), "Reload")]')
                            refresh.click()
                            unread_mails = browser.find_elements(By.CLASS_NAME, 'zE')
                            unread_mails[len(unread_mails) - 1].click()
                            crisis_averted = True
                            break
                        except:
                            print("Refresh not needed...")
                            unread_mails = browser.find_elements(By.CLASS_NAME, 'zE')
                            unread_mails[len(unread_mails) - 1].click()
                            crisis_averted = True
                    except:
                        browser.refresh()
                        time.sleep(get_random_time())
                        crisis_averted = False

            time.sleep(get_random_time())
            try:
                frame1 = browser.find_elements(By.CLASS_NAME, 'bu5')
                browser.switch_to.frame(frame1[0])
                time.sleep(get_random_time())
                frame2 = browser.find_element(By.XPATH, '//*[@id="amp-iframe"]')
                browser.switch_to.frame(frame2)
                time.sleep(get_random_time())
                # table1 = browser.find_element(By.XPATH, '//table/tbody/tr[11]/td/table/tbody/tr[8]/td/table/tbody/tr/td')
                # confirm_privacy = browser.find_element(By.XPATH, '//td[contains(text( ), "Confirm")]')
                # confirm_privacy.click()
                confirm_privacy = browser.find_element(By.XPATH,
                                                       '/html/body/table/tbody/tr[11]/td/table/tbody/tr[8]/td/table/tbody/tr/td/div/a')
                confirm_privacy.click()
                time.sleep(get_random_time())
                # '//*[@id=":6v"]/div[1]/section/center/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[4]/td/div/a')
                p = browser.current_window_handle
                parent = browser.window_handles[0]
                child = browser.window_handles[1]
                browser.switch_to.window(child)
                time.sleep(get_random_time())
            except Exception as e:
                print(e)
            found_make = False
            found_make_count = 0
            while not found_make:
                try:
                    privacy_check = browser.find_elements(By.CLASS_NAME, 'VfPpkd-ksKsZd-XxIAqe')
                    try:
                        privacy_check[2].click()
                    except:
                        privacy_check[1].click()
                    time.sleep(get_random_time())
                    make_plan = browser.find_element(By.XPATH,
                                                     '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div/div/div/c-wiz/div/div[2]/div[2]/c-wiz[1]/div/div/div[1]/div[3]/div/div/div/button')
                    make_plan.click()
                    time.sleep(get_random_time())
                    browser.back()
                    found_make = True
                except Exception as e:
                    print(e)
                    found_make_count = found_make_count + 1
                    if found_make_count > 5:
                        found_make = True
                        break
                    print('finding element')

            next_count = 0
            next_ = False
            while not next_:
                try:
                    time.sleep(get_random_time())
                    next_arrow_1 = browser.find_element(By.XPATH,
                                                        '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div/div/div/c-wiz/div/div[2]/div[3]/div/button')
                    next_arrow_1.click()
                    next_ = True
                except:
                    if next_count > 5:
                        print('took too long to load...')
                    print('loading...')
                    time.sleep(3)
                    next_count = next_count + 1

            next_count = 0
            next_ = False
            while not next_:
                try:
                    time.sleep(get_random_time())
                    next_arrow_2 = browser.find_element(By.XPATH,
                                                        '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div/div/div/c-wiz/div/div[2]/div[3]/div/button')
                    next_arrow_2.click()
                    next_ = True
                except:
                    if next_count > 5:
                        print('took too long to load...')

                    print('loading...')
                    time.sleep(3)
                    next_count = next_count + 1
            time.sleep(get_random_time())

            next_count = 0
            next_ = False
            while not next_:
                try:
                    time.sleep(get_random_time())
                    next_arrow_3 = browser.find_element(By.XPATH,
                                                        '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div/div/div/c-wiz/div/div[2]/div[3]/div/button')
                    next_arrow_3.click()
                    next_ = True
                except:
                    if next_count > 5:
                        print('took too long to load...')

                    print('loading...')
                    time.sleep(3)
                    next_count = next_count + 1
            time.sleep(get_random_time())

            next_count = 0
            next_ = False
            while not next_:
                try:
                    time.sleep(get_random_time())
                    next_arrow_4 = browser.find_element(By.XPATH,
                                                        '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div/div/div/c-wiz/div/div[2]/div[3]/div/button')
                    next_arrow_4.click()
                    next_ = True
                except:
                    if next_count > 5:
                        print('took too long to load...')

                    print('loading...')
                    time.sleep(3)
                    next_count = next_count + 1
            time.sleep(get_random_time())

            next_count = 0
            next_ = False
            while not next_:
                try:
                    time.sleep(get_random_time())
                    next_arrow_5 = browser.find_element(By.XPATH,
                                                        '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div/div/div/c-wiz/div/div[2]/div[3]/div/button')
                    next_arrow_5.click()
                    next_ = True
                except Exception as e:
                    print(e)
                    if next_count > 5:
                        print('took too long to load...')

                    print('loading...')
                    time.sleep(3)
                    next_count = next_count + 1
            time.sleep(get_random_time())

            next_count = 0
            next_ = False
            while not next_:
                try:
                    time.sleep(get_random_time())
                    checkbox = browser.find_elements(By.CLASS_NAME,
                                                     'VfPpkd-muHVFf-bMcfAe')
                    checkbox[0].click()
                    next_ = True
                except Exception as e:
                    print(e)
                    if next_count > 5:
                        print('took too long to load...')

                    print('loading...')
                    time.sleep(3)
                    next_count = next_count + 1
            time.sleep(get_random_time())

            time.sleep(get_random_time())
            browser.switch_to.window(parent)
            time.sleep(get_random_time())
            # security_check = browser.find_element(By.XPATH, '//td[contains( text( ), "Check Security Status")]')
            # security_check.click()
            # time.sleep(get_random_time())
            # child2 = browser.window_handles[2]
            # browser.switch_to.window(child2)
            # time.sleep(get_random_time())
            # found_section = False
            # found_section_count = 0
            # while not found_section:
            #     try:
            #         continue_sec = browser.find_element(By.XPATH, '//*[@id="i6"]/div/div/div/div[3]/div[2]/div/button')
            #         continue_sec.click()
            #         time.sleep(get_random_time())
            #         turn_on = browser.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[7]/div/div[2]/div[3]/div[2]/button')
            #         turn_on.click()
            #         found_section = True
            #         break
            #     except:
            #         if found_section_count > 5:
            #             found_section = True
            #             break
            #         found_section_count = found_section_count + 1
            #         time.sleep(2)
            #
            # if found_section_count > 5:
            #     cont_g_acc = browser.find_element(By.XPATH,
            #                                       '//*[@id="yDmH0d"]/c-wiz/div/c-wiz/div/div/div/div/div[4]/div/a')
            #     cont_g_acc.click()
            # time.sleep(get_random_time())
            browser.switch_to.window(parent)
            time.sleep(get_random_time())
            frame1 = browser.find_element(By.CLASS_NAME, 'bu5')
            browser.switch_to.frame(frame1)
            time.sleep(get_random_time())
            frame2 = browser.find_element(By.XPATH, '//*[@id="amp-iframe"]')
            browser.switch_to.frame(frame2)
            time.sleep(get_random_time())
            newsletter = browser.find_element(By.XPATH, '//button[contains(text( ), "Yes, keep me updated")]')
            newsletter.click()
            time.sleep(5)
            print("Activity Done")

        print('Generation Started...')

        browser.get('https://google.com')

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}] Looking for popup...")

        try:
            elem = browser.find_element(By.XPATH, '//*[@id="vc3jof"]')
            print(f"thread[{task}] task[{task_num + 1}] Popup Found...")
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.XPATH, '//*[@id="tbTubd"]/div/li[12]')
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.ID, 'L2AGLb')
            elem.click()

            time.sleep(get_random_time())
        except:
            print(f"thread[{task}] task[{task_num + 1}] No popup found...")
            try:
                english = browser.find_element(By.XPATH, '//*[@id="SIvCob"]/a')
                english.click()
                print(f'thread[{task}] task[{task_num + 1}]Converting to English...')
                time.sleep(get_random_time())
            except:
                print(f'thread[{task}] task[{task_num + 1}] Already in English...')

        elem = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[2]/a')
        elem.click()

        time.sleep(get_random_time())
        create_elem_count = 0
        create_elem_found = False
        while not create_elem_found:
            try:
                create_acc_btn = browser.find_element(By.CSS_SELECTOR,
                                                      '.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.ksBjEc.lKxP2d.qfvgSe.FliLIb.uRo0Xe.TrZEUc.t29vte')
                create_acc_btn.click()

                time.sleep(get_random_time())

                for_myself = browser.find_element(By.XPATH,
                                                  '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div/ul/li[1]')
                for_myself.click()

                time.sleep(get_random_time())
                create_elem_found = True
                break
            except:
                print(f"thread[{task}] task[{task_num}]Waiting for page to load...")
                time.sleep(get_random_time())
                if create_elem_count > 5:
                    print(f"thread[{task}] task[{task_num}] page took too long to load (potential proxy issue), terminating task...")
                    return
                create_elem_count = create_elem_count + 1

        info_elem_count = 0
        elem_info_found = False
        while not elem_info_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}]: Entering First Name...")
                first_name = browser.find_element(By.XPATH, '//*[@id="firstName"]')
                send_input(f_name, first_name)

                time.sleep(get_random_time())
                elem_info_found = True
                break
            except:
                if info_elem_count > 5:
                    print(f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                info_elem_count = info_elem_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Last Name...")
        last_name = browser.find_element(By.XPATH, '//*[@id="lastName"]')
        send_input(l_name, last_name)

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Email...")
        email = browser.find_element(By.XPATH, '//*[@id="username"]')
        if email.get_attribute('value') == "":
            send_input(email_name, email)

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Password...")
        password = browser.find_element(By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input')
        send_input(rand_pass, password)

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Password(2)...")
        confirm_password = browser.find_element(By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input')
        send_input(rand_pass, confirm_password)

        time.sleep(get_random_time())
        genned_mail_address = ''
        found_suggestion = False
        name_taken = True
        while name_taken:
            try:
                message = browser.find_element(By.XPATH,
                                               '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/div[2]/div')
                if message.is_displayed():
                    name_taken = True
            except:
                name_taken = False

            if name_taken:
                try:
                    suggested_name = browser.find_element(By.XPATH,
                                                          '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[2]/div/ul/li[2]/button')
                    found_suggestion = True
                except:
                    found_suggestion = False

                if found_suggestion:
                    print(f"thread[{task}] task[{task_num + 1}] Email Taken, Trying Suggested Option...")
                    genned_mail_address = suggested_name.text
                    suggested_name.click()
                    time.sleep(get_random_time())
                    print(genned_mail_address)
                    time.sleep(get_random_time())
                else:
                    print(f"thread[{task}] task[{task_num}] No Suggestion Found, Adding Numbers...")
                    email_num1 = random.randrange(1, 10)
                    email_num2 = random.randrange(1, 10)
                    email_num3 = random.randrange(1, 10)
                    send_input(str(email_num1) + str(email_num2) + str(email_num3), email)
                    genned_mail_address = email.get_attribute('value')
                    time.sleep(get_random_time())
                    next_button = browser.find_element(By.XPATH, '//*[@id="accountDetailsNext"]/div/button')
                    next_button.click()
                    time.sleep(get_random_time())
                    try:
                        message = browser.find_element(By.XPATH,
                                                       '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/div[2]/div')
                        if message.is_displayed():
                            name_taken = True
                        else:
                            name_taken = False
                            genned_mail_address = email.get_attribute('value')
                            break
                    except:
                        name_taken = False
                        break
            else:
                genned_mail_address = email.get_attribute('value')
                next_button = browser.find_element(By.XPATH, '//*[@id="accountDetailsNext"]/div/button')
                next_button.click()
                time.sleep(get_random_time())
                break

        time.sleep(get_random_time())

        phone_session = requests.session()

        get_phone_count = 0
        is_error = True
        while is_error:
            if get_phone_count > 3:
                print(f"thread[{task}] task[{task_num + 1}] Max Retry Reached, Stopping Task...")
                return
            print(f"thread[{task}] task[{task_num + 1}] Getting Phone Number...")
            res = phone_session.post(
                f"https://public.sms-gen.com/v1/sms/number?country=US&service=Google&channel=1&apikey={api_key}&ref=3929432")
            error_get = res.json()['isError']

            if not error_get:
                print(f"thread[{task}] task[{task_num + 1}]Phone Number Found!")
                phone_number = res.json()['number']
                phone_id = res.json()['id']
                print(f"thread[{task}] task[{task_num + 1}] Phone Number: {phone_number}")
                if '+' in phone_number:
                    phone_num = phone_number[2:len(phone_number)]
                else:
                    phone_num = phone_number[1:len(phone_number)]

                phone_page_count = 0
                phone_page_loaded = False
                while not phone_page_loaded:
                    try:
                        country_btn = browser.find_element(By.XPATH, '//*[@id="countryList"]/div/div[1]')
                        country_btn.click()

                        time.sleep(get_random_time())

                        country_code = browser.find_element(By.XPATH, '//*[@id="countryList"]/div/div[2]/ul/li[227]')
                        country_code.click()

                        time.sleep(get_random_time())

                        phone_page_loaded = True
                        break
                    except:
                        if phone_page_count > 5:
                            print(
                                f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                            return
                        phone_page_count = phone_page_count + 1
                        print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                        time.sleep(2)

                print(f"thread[{task}] task[{task_num + 1}] Inserting Phone Number...")
                phone_input = browser.find_element(By.XPATH, '//*[@id="phoneNumberId"]')
                send_input(phone_num, phone_input)

                time.sleep(get_random_time())

                next_button = browser.find_element(By.XPATH,
                                                   '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
                next_button.click()

                time.sleep(get_random_time())

                try:
                    error_message = browser.find_element(By.XPATH,
                                                         '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div/div[2]/div[2]/div')
                    if error_message.is_displayed():
                        print(f"thread[{task}] task[{task_num + 1}] Phone Number Cant Be Used... Retry")
                        ban_res = phone_session.post(
                            f"https://public.sms-gen.com/v1/sms/bannumber?id={phone_id}&apikey={api_key}&ref=3929432")
                        phone_input.clear()
                        is_error = True
                    else:
                        print(f"thread[{task}] task[{task_num + 1}] Phone Number Valid!")
                        is_error = False
                        break
                except:
                    print(f"thread[{task}] task[{task_num + 1}] Phone Number Valid!")
                    is_error = False
                    break
            else:
                if res.json()['error'] == 'ERROR_NOT_ENOUGH_BALANCE':
                    print('Not Enough Balance Stopping all tasks...')
                    return
                print(f"thread[{task}] task[{task_num + 1}] Phone Number Request Failed, Retry")
                get_phone_count = get_phone_count + 1

        time.sleep(get_random_time())

        retry = True
        time_count = 0
        while retry:
            print(f"thread[{task}] task[{task_num + 1}] Getting Code...")
            code_res = phone_session.get(
                f"https://public.sms-gen.com/v1/sms/code?id={phone_id}&apikey={api_key}&ref=3929432")
            retry = code_res.json()['retry']
            if not retry:
                print(f"thread[{task}] task[{task_num + 1}] Code found!")
                phone_code = code_res.json()['sms']
            else:
                print(f"thread[{task}] task[{task_num + 1}] Still waiting for code")
                time.sleep(6)
                time_count = time_count + 1
                if time_count > 3:
                    cancel_res = phone_session.post(
                        f"https://public.sms-gen.com/v1/sms/cancelnumber?id={phone_id}&apikey={api_key}&ref=3929432")
                    print(f"thread[{task}] task[{task_num + 1}] Code took too long to receive, terminating task & canceling number...")
                    return

        code_page_found = False
        code_page_count = 0
        while not code_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Inserting Code...")
                code_input = browser.find_element(By.XPATH, '//*[@id="code"]')
                send_input(phone_code, code_input)

                time.sleep(get_random_time())
                code_page_found = True
                break
            except:
                if code_page_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                code_page_count = code_page_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(get_random_time())

        verify_button = browser.find_element(By.XPATH,
                                             '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button')
        verify_button.click()

        time.sleep(get_random_time())

        personal_page_found = False
        personal_page_count = 0
        while not personal_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Entering Personal Information")
                email_nums = random.randint(1, 10)
                email_nums2 = random.randint(1, 10)
                email_nums3 = random.randint(1, 10)
                if '@' in catchall:
                    recovery_email = f_name + l_name + str(email_nums) + str(email_nums2) + str(
                        email_nums3) + catchall
                else:
                    recovery_email = f_name + l_name + str(email_nums) + str(email_nums2) + str(
                        email_nums3) + '@' + catchall


                recovery_email_input = browser.find_element(By.XPATH,
                                                            '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input')
                send_input(recovery_email, recovery_email_input)

                personal_page_found = True
                break
            except:
                if personal_page_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                personal_page_count = personal_page_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(get_random_time())

        time.sleep(get_random_time())
        birth_month_dd = browser.find_element(By.XPATH, '//*[@id="month"]')
        birth_month_dd.click()

        time.sleep(get_random_time())

        month = random.randint(2, 12)
        birth_month = browser.find_element(By.XPATH, f"//*[@id='month']/option[{month}]")
        birth_month.click()

        time.sleep(get_random_time())

        birth_day_input = browser.find_element(By.XPATH, '//*[@id="day"]')
        birth_day_input.send_keys(random.randint(1, 2))
        time.sleep(get_random_time())
        birth_day_input.send_keys(random.randint(1, 8))

        time.sleep(get_random_time())

        birth_year_input = browser.find_element(By.XPATH, '//*[@id="year"]')
        first_num = random.randint(1, 2)
        birth_year_input.send_keys(first_num)
        time.sleep(get_random_time())
        if first_num == 1:
            birth_year_input.send_keys('9')
            time.sleep(get_random_time_text())
            birth_year_input.send_keys(random.randint(7, 9))
            time.sleep(get_random_time_text())
            birth_year_input.send_keys(random.randint(1, 9))
        elif first_num == 2:
            birth_year_input.send_keys('0')
            time.sleep(get_random_time_text())
            birth_year_input.send_keys('0')
            time.sleep(get_random_time_text())
            birth_year_input.send_keys(0, 4)

        time.sleep(get_random_time())

        gender_dd = browser.find_element(By.XPATH, '//*[@id="gender"]')
        gender_dd.click()

        time.sleep(get_random_time())

        gender = browser.find_element(By.XPATH, '//*[@id="gender"]/option[3]')
        gender.click()

        time.sleep(get_random_time())

        next_button = browser.find_element(By.XPATH,
                                           '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
        next_button.click()

        time.sleep(get_random_time())

        preferences_page_found = False
        preferences_count = 0
        while not preferences_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Selecting Preferences...")
                yes_im_in = browser.find_element(By.XPATH,
                                                 '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button')
                yes_im_in.click()

                preferences_page_found = True
                break
            except:
                if preferences_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                preferences_count = preferences_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(2)

        time.sleep(get_random_time())
        personalization_page_found = False
        personalization_count = 0
        while not personalization_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Selecting Preferences [2]...")
                personalization_settings = browser.find_element(By.XPATH,
                                                                '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/div[1]/div/span/div[1]/div/div[1]')
                personalization_settings.click()

                personalization_page_found = True
                break
            except:
                if personalization_count > 1:
                    print(
                        f"thread[{task}] task[{task_num + 1}] personalization button not found, moving on...")
                    break
                personalization_count = personalization_count + 1
                print(f"thread[{task}]task[{task_num + 1}] Finding Personalization Settings...")
                time.sleep(2)

        time.sleep(get_random_time())
        next_button_found = False
        next_button_count = 0
        while not next_button_found:
            try:
                next_button = browser.find_element(By.XPATH,
                                                   '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
                next_button.click()

                next_button_found = True
                break
            except:
                if next_button_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                next_button_count = next_button_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Trying to find personalization settings...")
                time.sleep(2)

        time.sleep(get_random_time())
        confirm_found = False
        confirm_count = 0
        while not confirm_found:
            try:
                confirm_button = browser.find_element(By.XPATH,
                                                      '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/button')
                confirm_button.click()

                confirm_found = True
                break
            except:
                if confirm_count > 1:
                    print(
                        f"thread[{task}] task[{task_num + 1}] no personalization pages found, moving on...")
                    break
                confirm_count = confirm_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Trying to find personalization settings...")
                time.sleep(2)

        time.sleep(get_random_time())
        agree_found = False
        agree_count = 0
        while not agree_found:
            try:
                agree_button = browser.find_element(By.XPATH,
                                                    '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
                agree_button.click()

                agree_found = True
                break
            except:
                if agree_count > 1:
                    print(
                        f"thread[{task}] task[{task_num + 1}] no personalization pages found, moving on...")
                    break
                agree_count = agree_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Trying to find personalization settings...")
                time.sleep(get_random_time())

        time.sleep(get_random_time())
        with open('genned_gmails.csv', 'a', encoding='UTF8', newline='') as gm:
            content = [genned_mail_address + "@gmail.com", rand_pass, f_name, l_name, recovery_email, PROXY_HOST + ":" + PROXY_PORT + ":" + PROXY_USER + ":" + PROXY_PASS, phone_number, datetime.date.today(), 'N']
            writer = csv.writer(gm)

            writer.writerow(content)

        print(f"thread[{task}] task[{task_num + 1}] Gmail Account Successfully Created.")
        format_proxy = PROXY_HOST + ":" + PROXY_PORT + ":" + PROXY_USER + ":" + PROXY_PASS
        send_webhook(genned_mail_address + '@gmail.com', rand_pass, recovery_email, phone_number, format_proxy)
        send_webhook_public()
        accounts_created[task - 1] = accounts_created[task - 1] + 1
        time.sleep(get_random_time())
        try:
            generate_activity()
        except Exception as e:
            print(e)

    k = 0
    while k < tasks_to_run:
        t1 = threading.Thread(target=gen_account, args=[k])
        t1.start()
        t1.join()
        if accounts_created[task-1] != (k+1):
            k = k - 1
        k = k + 1


while not stop and license_authenticated:
    accounts_created = []
    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]

    amount_of_proxies = len(proxies)

    print('Welcome to Account Gen. Please Select a Module from the List Below.')
    print('1) Google Gen')
    print('2) Gmail Forwarder')
    print('0) Exit')
    correct = False
    while not correct:
        option = input('Option: ')
        if option != '1' and option != '0' and option != '2':
            correct = False
        else:
            correct = True
            break

    if option == '0':
        exit(0)

    if option == '2':
        accs_to_forward = 0
        row_number = 0
        with open('genned_gmails.csv', 'r') as atf:
            reader = csv.reader(atf)
            for row in reader:
                if row_number != 0:
                    if row[8] == 'N':
                        accs_to_forward = accs_to_forward + 1
                row_number = row_number + 1

        is_correct = False
        same_proxy = False
        while not is_correct:
            yn = input(
                'Would you like to use the same proxies as the proxies used to generate the accounts while forwarding? (y/n): ')
            if yn == 'y':
                is_correct = True
                same_proxy = True
                break
            elif yn == 'n':
                is_correct = True
                same_proxy = False
                break

        f1 = threading.Thread(target=confirm_setup, args=[accs_to_forward])
        f1.start()

        f2 = threading.Thread(target=forward_setup, args=[accs_to_forward, same_proxy])
        f2.start()
        f1.join()
        f2.join()

    else:

        with open('settings.json', 'r') as f:
            data = json.load(f)

        API_KEY = data['API_KEY']
        CATCHALL = data['CATCHALL']
        WEBHOOK = data['DISCORD_WEBHOOK']

        concurrent_tasks = int(input('Enter the amount of tasks you would like to run concurrently (Max 10): '))
        number_of_accounts = int(input('How many accounts would you like to create? '))

        accs_to_gen = []

        if concurrent_tasks > 10:
            print()

        if number_of_accounts % concurrent_tasks != 0:
            remainder = number_of_accounts % concurrent_tasks
            divisible_num = (number_of_accounts - remainder) // concurrent_tasks
            for i in range(concurrent_tasks):
                accs_to_gen.append(int(divisible_num))

            for i in range(remainder):
                accs_to_gen[i] = accs_to_gen[i] + 1
        else:
            for m in range(concurrent_tasks):
                accs_to_gen.append(int(number_of_accounts // concurrent_tasks))

        proxies_available = []

        if amount_of_proxies % concurrent_tasks != 0:
            remainder = amount_of_proxies % concurrent_tasks
            divisible_num = (amount_of_proxies - remainder) // concurrent_tasks
            for l in range(concurrent_tasks):
                proxies_available.append(divisible_num)

            for z in range(remainder):
                proxies_available[z] = proxies_available[z] + 1
        else:
            for s in range(concurrent_tasks):
                proxies_available.append(int(amount_of_proxies // concurrent_tasks))

        proxies_available_string = ''
        for l in range(len(proxies_available)):
            if l != len(proxies_available) - 1:
                proxies_available_string = proxies_available_string + str(proxies_available[l]) + ','
            else:
                proxies_available_string = proxies_available_string + str(proxies_available[l])

        def run_task(task, number_of_accs):
            gen_google(task=task, tasks_to_run=number_of_accs, concurrent_tasks=concurrent_tasks, proxies_available=proxies_available_string)


        if concurrent_tasks == 1:
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t1.start()
            t1.join()
            print('Generation Complete...')

        if concurrent_tasks == 2:
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            t1.join()
            t2.join()
            print('Generation Complete...')

        if concurrent_tasks == 3:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            t1.join()
            t2.join()
            t3.join()
            print('Generation Complete...')

        if concurrent_tasks == 4:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            time.sleep(get_random_time())
            t4.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            print('Generation Complete...')

        if concurrent_tasks == 5:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
            t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            time.sleep(get_random_time())
            t4.start()
            time.sleep(get_random_time())
            t5.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            print('Generation Complete...')

        if concurrent_tasks == 6:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
            t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
            t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            time.sleep(get_random_time())
            t4.start()
            time.sleep(get_random_time())
            t5.start()
            time.sleep(get_random_time())
            t6.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            t6.join()
            print('Generation Complete...')

        if concurrent_tasks == 7:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
            t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
            t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
            t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            time.sleep(get_random_time())
            t4.start()
            time.sleep(get_random_time())
            t5.start()
            time.sleep(get_random_time())
            t6.start()
            time.sleep(get_random_time())
            t7.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            t6.join()
            t7.join()
            print('Generation Complete...')

        if concurrent_tasks == 8:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
            t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
            t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
            t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
            t8 = threading.Thread(target=run_task, args=[8, accs_to_gen[7]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            time.sleep(get_random_time())
            t4.start()
            time.sleep(get_random_time())
            t5.start()
            time.sleep(get_random_time())
            t6.start()
            time.sleep(get_random_time())
            t7.start()
            time.sleep(get_random_time())
            t8.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            t6.join()
            t7.join()
            t8.join()
            print('Generation Complete...')

        if concurrent_tasks == 9:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
            t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
            t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
            t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
            t8 = threading.Thread(target=run_task, args=[8, accs_to_gen[7]])
            t9 = threading.Thread(target=run_task, args=[9, accs_to_gen[8]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            time.sleep(get_random_time())
            t4.start()
            time.sleep(get_random_time())
            t5.start()
            time.sleep(get_random_time())
            t6.start()
            time.sleep(get_random_time())
            t7.start()
            time.sleep(get_random_time())
            t8.start()
            time.sleep(get_random_time())
            t9.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            t6.join()
            t7.join()
            t8.join()
            t9.join()
            print('Generation Complete...')

        if concurrent_tasks == 10:
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            accounts_created.append(0)
            t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
            t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
            t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
            t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
            t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
            t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
            t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
            t8 = threading.Thread(target=run_task, args=[8, accs_to_gen[7]])
            t9 = threading.Thread(target=run_task, args=[9, accs_to_gen[8]])
            t10 = threading.Thread(target=run_task, args=[10, accs_to_gen[9]])
            t1.start()
            time.sleep(get_random_time())
            t2.start()
            time.sleep(get_random_time())
            t3.start()
            time.sleep(get_random_time())
            t4.start()
            time.sleep(get_random_time())
            t5.start()
            time.sleep(get_random_time())
            t6.start()
            time.sleep(get_random_time())
            t7.start()
            time.sleep(get_random_time())
            t8.start()
            time.sleep(get_random_time())
            t9.start()
            time.sleep(get_random_time())
            t10.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            t6.join()
            t7.join()
            t8.join()
            t9.join()
            t10.join()
            print('Generation Complete...')