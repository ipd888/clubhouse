import re
import undetected_chromedriver as uc
import random
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


aws_txt = "AWS Email Verification"

SELECTORS = {
    "search": [
        "//input[@id='sbq']",
        "//input[@name='q']"
    ],

    "search_button": [
        "//input[@name='nvp_site_mail']",
        "//input[@class='search-form-submit']"
    ],

    "create_account": [
        "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 FliLIb uRo0Xe TrZEUc Xf9GD']",
        "//*[@class='JnOM6e TrZEUc kTeh9 KXbQ4b']"
    ],
    'for_my_personal_use': [
        "//span[@class='VfPpkd-StrnGf-rymPhb-b9t22c']",
    ],
    "username": [
        "//*[@name='identifier']",
        "//*[@id='identifierId']"
    ],
    "password": [
        "//*[@name='Passwd']",
        "//*[@class='whsOnd zHQkBf']"
    ],
    "next": [
        "//*[@id='identifierNext']",
        "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
        "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc LQeN7 xYnMae TrZEUc lw1w4b']",
        "//button[contains(text(),'Next')]",
        "//button[contains(text(),'次へ')]",
        "//button[contains(text(),'I agree')]",
        "//button[contains(text(),'Ich stimme zu')]"
    ],
    "Create_Gmail": [
        "//*[@id='selectionc2']",
        "//div[text()='Create your own Gmail address']",
        "//div[text()='Gmail-Adresse erstellen']",
        "//div[text()='自分で Gmail アドレスを作成']"
    ],
    "phone_number": "//*[@id='phoneNumberId']",
    "code": '//input[@name="code"]',
    "acc_phone_number": '//input[@id="phoneNumberId"]',
    "acc_day": '//input[@name="day"]',
    "acc_month": '//select[@id="month"]',
    "acc_year": '//input[@name="year"]',
    "acc_gender": '//select[@id="gender"]',
    "username_warning": '//*[@class="OyEIQ uSvLId"]',
    "recovery": "//*[@name='recovery']",
    "skip": [
        "//button[contains(text(),'Skip')]",
        "//button[contains(text(),'スキップ ')]",
        "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc LQeN7 xYnMae TrZEUc lw1w4b']"
    ],
    "confirm": [
        "//button[contains(text(),'Confirm')]",
        "//span[@class='RveJvd snByac']"
    ],
    "maia_button": [
        "//*[@class='maia-button maia-button-secondary']",
    ],
    "mail": [
        "//span[@class='ts']"
    ],
}

with open("code.txt", "r") as file:
    content = file.read().split("----")

if len(content) == 3:
    username = content[0]
    password = content[1]
    user2 = content[2]
    print("用户名:", username)
else:
    print("code.txt 文件格式不正确")

options = uc.ChromeOptions()
# s5代理
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
prefs = {"intl.accept_languages": "en-US"}
options.add_experimental_option("prefs", prefs)
# 修改语言为英文
options.add_argument('--lang=en')
# 读取 ua.txt 文件并随机选择一行 User Agent
with open("ua.txt", "r") as file:
    user_agents = file.readlines()
ua = random.choice(user_agents).strip()
options.add_argument(f"--user-agent={ua}")

driver = uc.Chrome(options=options)
driver.set_window_size(590, 900)
driver.get('https://mail.google.com/mail/u/0/h/?&')
WAIT = 10
print('################ 输入邮箱 ################')
username_input = driver.find_element(By.CSS_SELECTOR, '#identifierId')
username_input.send_keys(username)

print('################ 点击下一步 ################')
next_button = driver.find_element(By.CSS_SELECTOR, '#identifierNext')
next_button.click()

# 输入密码
print('################ 输入密码 ################')
driver.implicitly_wait(20)


password_input = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]'))
                                                 )
print("找到密码输入框")


password_input.send_keys(password)
print("输入密码")

next_button = driver.find_element(By.CSS_SELECTOR, '#passwordNext')
next_button.click()

try:
    challenge_elements = WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'lCoei.YZVTmd.SmR8'))
    )
    print("找到输入辅助邮箱选项")

    if len(challenge_elements) >= 3:

        challenge_element = challenge_elements[2]
        challenge_element.click()
        print("选择辅助邮箱")


        input_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'knowledge-preregistered-email-response'))
        )
        print("找到输入框")

        input_element.send_keys(user2)
        print("输入辅助邮箱")


        button_element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Next']"))
        )
        button_element.click()
        print("点击Next按钮")
    else:
        print("未元素'")

except TimeoutException:
    print("在5秒内未找到元素")

# 等待元素出现
try:
    WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class='maia-button maia-button-secondary']"))
    )

    # 点击 Create_Gmail
    create_gmail = WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@class='maia-button maia-button-secondary']"))
    )
    create_gmail.click()
    print("点击 Create_Gmail")
except TimeoutException:
    print("在6秒内未找到元素 Create_Gmail")


# 等待元素出现search
try:
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='sbq']"))
    )

    # 点击 search
    search = WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='sbq']"))
    )
    # 输入 txt2 变量的值
    search.send_keys(aws_txt)
    print("输入到搜索框")
    # 点击按钮 search_button
    search_button = WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='nvp_site_mail']",))
    )
    search_button.click()
    print("开始搜索")

except TimeoutException:
    print("在10秒内未找到元素 search")

# 等待元素出现
try:
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='ts']"))
    )
    # print("找到邮件")
except TimeoutException:
    print("在10秒内未找到元素 邮件")

# 等待元素出现
wait = WebDriverWait(driver, WAIT)
elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='ts']")))
print("找到邮件")

# 点击第一个邮件
elements[0].click()
print("点击第一个邮件")

email_body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[@valign='top']")))
print("找到邮件内容")


msg_elements = driver.find_elements(By.XPATH, "//div[@class='msg']")

pattern = r"\b(\d{6})\b"
found_codes = []

for msg_element in msg_elements:
    msg_html = msg_element.get_attribute("innerHTML")
    matches = re.findall(pattern, msg_html)
    for match in matches:
        if match not in ["000000", "555555"] and not match.startswith("#"):
            found_codes.append(match)

if found_codes:
    print("找到的验证码:")
    for code in found_codes:
        print(code)
else:
    print("未找到验证码")

driver.quit()
