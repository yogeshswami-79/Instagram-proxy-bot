from Database import Database
from selenium import webdriver
import time, random, sys, sqlite3, pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class PostsListener:
    def __init__(self, database, headless=False):
        self.__db = database
        self.__tags = self.__db.getTags()
        self.__bot = ''
        self.__headless = headless

# Log To File
    def log(self, text):
        with open("Listener-log.txt",'a') as file:
            file.write(f"{text}\n")
            file.close()

# Get Browser Instance
    def getDriverInstance(self, headless):
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        option = Options()
        if headless:
            option.add_argument('--headless')
        bot = webdriver.Firefox(profile, options=option)
        bot.set_window_size(500, 950)
        return bot

    #load cache
    def loadCache(self, driver):
        driver.get("https://instagram.com/accounts/login/")
        time.sleep(2)
        cookies = pickle.load(open(f"cookies/listener.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        time.sleep(1)

    # listen to given hashtags lists
    def startListening(self):
        self.log(f"\n Started ---------------- \n")
        self.__bot = self.getDriverInstance(self.__headless)
        self.loadCache(self.__bot)
        for tag in self.__tags:
            self.addToDB(tag, self.__getPosts(tag))
        self.log("Done\n\n")
        self.exit()

    # Add Posts To Db
    def addToDB(self, tag, posts):
        for link in posts:
            self.__db.addLink(tag, link)

    # check Wether webelement of defined tag exists
    def __check_exists_by_tag(self, driver, tag):
        try:
            driver.find_element_by_tag_name(tag)
        except NoSuchElementException:
            return False
        return True

    # get Posts from given hashtag
    def __getPosts(self, tag):
        self.log(f"\n getting Posts of {tag}")
        link = 'https://www.instagram.com/explore/tags/' + tag
        posts = []
        self.__bot.get(link)
        time.sleep(random.randrange(4, 6))
        x = self.__bot.find_elements_by_css_selector(
            ".KC1QD > div:nth-child(3) > div:nth-child(1) > div > div")
        for a in x:
            if self.__check_exists_by_tag(self.__bot, 'a'):
                posts.append(a.find_element_by_tag_name(
                    'a').get_attribute('href'))
            else:
                self.log(' \n posts not found! \n')
        self.log(f"\n{posts}\n")
        return posts

    def work(self):
        self.startListening()

    # Exit Bot/WebDiver
    def exit(self):
        self.__bot.quit()
        sys.exit()


# -----------------------   Test    ----------------------- #


# tags = ["bike", "code", "java", "cars"]

# db = Database(tags)

# listener = PostsListener(db)
# listener.startListening()
