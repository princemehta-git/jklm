from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--app=https://www.google.com")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--mute-audio")
# options.headless = True

def get_syll(driver, name):
    return driver.find_element_by_class_name(name).text


if __name__ == "__main__":
    url = input('Enter the URL')
    dic_url = 'https://www.thefreedictionary.com/words-containing-'

    seen = {}

    text_file = open("words.txt", "r")
    words = text_file.read().split('\n')

    dicdriver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(), options=options)
    dicdriver.implicitly_wait(2)
    driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install())
    driver.implicitly_wait(60)

    driver.get(url)

    # time.sleep(10)
    while True:

        try:
            frame_ref = driver.find_elements_by_tag_name("iframe")[0]
            iframe = driver.switch_to.frame(frame_ref)

            prev = 'none'
            while True:
                try:
                    time.sleep(0.5)

                    syll = get_syll(driver, "syllable")
                    other_turn = get_syll(driver, "otherTurn")
                    print(other_turn)

                    if len(other_turn) == 0 and len(syll) > 0:
                        print(syll)
                        print(other_turn)
                        if prev != syll or prev == syll:

                            # find the word
                            dic_url = 'https://www.thefreedictionary.com/words-containing-' + syll
                            dicdriver.get(dic_url)

                            pointer = 5

                            for i in (range(6, 15)):
                                dic_web = dicdriver.find_elements_by_xpath('//*[@id="w' + str(i) + '"]/ul/li[1]')

                                if dic_web is not None:
                                    dic_word = dic_web[0].text
                                    pointer = i
                                    break

                            if dic_word in seen:
                                seen[dic_word] = seen[dic_word] + 1

                                word_xpath = '//*[@id="w' + str(pointer) + '"]/ul/li[' + str(seen[dic_word]) + ']'
                                dic_word = dicdriver.find_elements_by_xpath(word_xpath)[0].text

                            else:
                                seen[dic_word] = 1

                            # print(seen)
                            print(dic_word)

                            # input the word
                            input_box = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/form/input')

                            for letter in dic_word:
                                # time.sleep(random.uniform(.06, .09))
                                input_box[0].send_keys(letter)
                            input_box[0].send_keys(Keys.ENTER)
                        prev = syll
                except:
                    pass

        except:
            pass