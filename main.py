import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys

username = "fikrianitririer@gmail.com"
password = "d0qzks5dtcrq4w2q"
user2 = "v6ai2iimrotekcaq@gmx.com"
# 初始化Chrome选项
options = uc.ChromeOptions()
# s5 代理
# options.add_argument('--proxy-server=socks5://146.190.220.118:8989')
# chrome_options.add_argument('--headless')  # 如果您不需要可视化界面，可以使用无头模式
options.add_argument('--no-sandbox')
options.add_argument('--max-old-space-size=2048')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
prefs = {"intl.accept_languages": "en-US"}
options.add_experimental_option("prefs", prefs)
options.page_load_strategy = 'eager'

driver = uc.Chrome(options=options)
driver.set_window_size(950, 1000)

driver.get("https://accounts.google.com/")
print("打开谷歌登录页面")

# 找到用户名输入框并输入用户名
username_input = driver.find_element(By.CSS_SELECTOR, '#identifierId')
username_input.send_keys(username)
print("输入用户名")
# 单击“下一步”按钮
next_button = driver.find_element(By.CSS_SELECTOR, '#identifierNext')
next_button.click()
print("点击下一步")

# 等待页面加载
driver.implicitly_wait(20)

# 等待密码输入框出现并可编辑
password_input = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]'))
                                                 )
print("找到密码输入框")

# 输入密码
password_input.send_keys(password)
print("输入密码")
# 单击“下一步”按钮
next_button = driver.find_element(By.CSS_SELECTOR, '#passwordNext')
next_button.click()
print("点击下一步")

# 等待错误信息出现
try:
    error_message = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.OyEIQ span')))
    error_text = error_message.text.strip()
    if error_text == "Wrong password. Try again or click Forgot password to reset it.":
        print("密码错误，请重试或点击忘记密码进行重置")
        sys.exit()  # 终止当前操作
    else:
        print("出现其他错误信息")
except:
    print("登陆成功！")

try:
    challenge_elements = WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'lCoei.YZVTmd.SmR8'))
    )
    print("找到元素 class='lCoei YZVTmd SmR8'")

    if len(challenge_elements) >= 3:
        # 点击第三个元素
        challenge_element = challenge_elements[2]
        challenge_element.click()
        print("点击第三个 class='lCoei YZVTmd SmR8'")

        # 等待id="knowledge-preregistered-email-response"输入框出现并可编辑
        input_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'knowledge-preregistered-email-response'))
        )
        print("找到输入框")

        # 输入user2变量的值
        input_element.send_keys(user2)
        print("输入user2变量的值")

        # 查找并点击指定按钮
        button_element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Next']"))
        )
        button_element.click()
        print("点击Next按钮")
    else:
        print("未找到足够的元素 class='lCoei YZVTmd SmR8'")

except TimeoutException:
    print("在5秒内未找到元素 class='lCoei YZVTmd SmR8'")
    # 执行后续的代码


# 查找并点击 class="aho" 的元素
def find_aho_elements(driver):
    return driver.find_elements(By.CSS_SELECTOR, ".ahr")


def click_aho_element(driver, element):
    try:
        element.click()
        print("点击 class='ahr' 的元素")
        return True
    except Exception as e:
        print(f"无法点击 class='ahr' 的元素: {e}")
        return False


def click_button_element(driver):
    try:
        wait = WebDriverWait(driver, 10)  # 等待最长10秒
        button_element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name*='data_consent_dialog']")))  # 等待元素可点击
        button_element.click()
        print("点击 button 的元素")
    except Exception as e:
        print(f"无法点击 button 的元素: {e}")


def process_aho_elements(driver):
    while True:
        aho_elements = find_aho_elements(driver)
        if aho_elements:
            print("找到 class='ahr' 的元素")
            for _ in range(2):  # 循环执行两次
                if not click_aho_element(driver, aho_elements[0]):
                    break
                click_button_element(driver)
                time.sleep(2)  # 等待2秒
            aho_elements = find_aho_elements(driver)
            if not aho_elements:
                print("未找到 class='ahr' 的元素")
                break
        else:
            print("未找到 class='ahr' 的元素")
            break  # 跳出循环


driver.get("https://mail.google.com/")
print("打开谷歌邮箱页面")

# 等待进度条到达100%
wait = WebDriverWait(driver, 200)

try:
    # 等待进度条元素消失
    print("等待进度条元素消失")
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.la-e')))
    # 进度条已完成加载
    print("进度条已完成加载")
except:
    print("等待进度条超时")


def check_page(driver, wait):
    try:
        # 检查 "aho" 类的元素是否存在
        aho_elements = driver.find_elements(By.CLASS_NAME, 'aho')
        return bool(aho_elements)
    except Exception as e:
        print(f"检查页面出错: {e}")
        return False


def click_element_with_text_and_button(driver, wait, text, button_name):
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{text}')]")))
        element.click()
        print(f"点击包含文本'{text}'的元素")

        button_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"button[name*='{button_name}']")))
        button_element.click()
        print("点击 button 的元素")
    except TimeoutException:
        print(f"未找到包含文本'{text}'的元素")
        pass


if not check_page(driver, wait):
    print("未找到 class='aho' 的元素，跳过当前操作")
else:
    try:
        click_element_with_text_and_button(driver, wait, 'Continue with smart features', 'data_consent_dialog')
        click_element_with_text_and_button(driver, wait,
                                           'Personalise other Google products with my Gmail, Chat and Meet data',
                                           'data_consent_dialog')
        driver.refresh()
        print("刷新页面")
    except TimeoutException:
        print("操作超时，跳过该部分")

# 等待页面加载
timeout = 30  # 等待的时间限制，单位为秒
max_attempts = 3  # 最大尝试次数
found_element = False
attempts = 0

while not found_element and attempts < max_attempts:
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Compose')]"))
        )
        found_element = True
    except TimeoutException:
        # 超时后刷新网页
        driver.refresh()
        timeout -= 5  # 每次减少等待时间，这里设定为5秒
        print("刷新页面，重新等待元素出现")
        attempts += 1

if found_element:
    # 执行元素出现后的操作
    print("找到包含文字 'Compose' 的元素")
else:
    print("超时，未找到包含文字 'Compose' 的元素")

# time.sleep(3)
unread_emails = driver.find_elements(By.XPATH, "//tr[@class='zA zE']")
print("未读邮件数量：", len(unread_emails))

subject_xpath = "//div[@class='y6']//span[contains(text(), ' Your GitHub launch code')]"
email_subject = None

try:
    email_subject = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, subject_xpath)))
except Exception as e:
    print("发生异常:", e)

if email_subject:
    print("找到了包含验证码的邮件")
    email_subject.click()
    print("点击邮件主题")
else:
    print("未找到符合条件的元素")

# 如果未找到或发生异常，则点击按钮 class="aim ain"，然后执行查找邮件主题的代码
if not email_subject:
    max_attempts = 3  # 最大尝试次数
    attempts = 0
    timeout = 10  # 等待时间初始值

    found_element = False
    while not found_element and attempts < max_attempts:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Compose')]"))
            )
            found_element = True
        except TimeoutException:
            # 超时后刷新网页
            driver.refresh()
            timeout -= 5  # 每次减少等待时间，这里设定为5秒
            print("刷新页面，重新等待元素出现")
            attempts += 1

    if found_element:
        # 执行元素出现后的操作
        print("找到包含文字 'Compose' 的元素")
    else:
        print("超时，未找到包含文字 'Compose' 的元素")

# 等待元素出现在页面上，再进行后续的操作driver.find_element(By.XPATH, "//h2[@class='hP']")
email_body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[@valign='top']")))
print("找到邮件内容")

# 获取邮件内容并查找链接
email_content = driver.page_source
soup = BeautifulSoup(email_content, 'html.parser')
links = soup.find_all('a', href=True)
for link in links:
    href = link['href']
    if "https://github.com/users" in href:
        start_index = href.rfind("/") + 1
        end_index = href.find("?")
        verification_code = href[start_index:end_index]
        print("找到链接:", href)
        print("提取到的验证码:", verification_code)
        break

time.sleep(50)
