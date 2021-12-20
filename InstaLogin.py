import time, pickle, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login:

    def __init__(self, bot, uname, pwrd):
        self.__bot = bot
        self.__uname = uname
        self.__pword = pwrd

    def saveCookies(self, driver, file):
        pickle.dump(driver.get_cookies() , open(f"cookies/{file}.pkl","wb"))
        time.sleep(1)

    def readCookies(self, driver, file):
        cookies = pickle.load(open(f"cookies/{file}.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        time.sleep(1)

    def isLoggedInn(self, driver):
        selector = f"button.sqdOP.L3NKy.y3zKF"
        return self.check_exists_by_xpath(driver, selector)

    # check wether webElement of defined xpath exists
    def check_exists_by_xpath(self, driver, xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    # def __acceptCookies(self, bot):
    #     if not self.check_exists_by_xpath(bot, "//form[@id='loginForm']"):
    #         print("No cookies")
    #         self.__loginWithCreds()
    #     else:

    #         # bot.find_element_by_xpath("//button[text()='Accept']").click()
    #         print("Accepted cookies")

    # login checkdoor
    def login(self):
        self.__bot.get("https://www.instagram.com/accounts/login")
        time.sleep(1)
        try:
            self.readCookies(self.__bot, self.__uname)
            print("logged-in")
        except:
            self.__loginWithCreds()

    # # login checkdoor
    # def login(self):
    #     self.__bot.get("https://www.instagram.com/accounts/login")
    #     time.sleep(random.randrange(1, 4))
    #     self.__acceptCookies(self.__bot)
    #     time.sleep(random.randrange(1, 3))
    #     self.__loginWithCreds()

    # login with creds
    def __loginWithCreds(self):
        print("logging in...")
        unamePath = "//input[@name='username']"
        passPath = "//input[@name='password']"

        WebDriverWait(self.__bot, 10).until(EC.presence_of_element_located((By.XPATH, unamePath)))
        WebDriverWait(self.__bot, 10).until(EC.presence_of_element_located((By.XPATH, passPath)))

        username_field = self.__bot.find_element_by_xpath(unamePath)
        pass_field = self.__bot.find_element_by_xpath(passPath)

        username_field.send_keys(self.__uname)
        WebDriverWait(self.__bot, 50)
        pass_field.send_keys(self.__pword)
        self.__bot.find_element_by_xpath("//button[@type='submit']").click()

        saveInfoPath = "//button[@class='sqdOP  L3NKy   y3zKF     ']"
        WebDriverWait(self.__bot, 10).until(EC.presence_of_element_located((By.XPATH, saveInfoPath)))
        time.sleep(1)
        self.__bot.find_element_by_xpath(saveInfoPath).click()
        time.sleep(1)
        
        self.saveCookies(self.__bot, self.__uname)
        time.sleep(random.randrange(1, 3))


#   --------------------------------    TESTS   --------------------------------    #

