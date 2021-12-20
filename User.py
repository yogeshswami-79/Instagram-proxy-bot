import time
import random
import sqlite3
from InstaLogin import Login
from Database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC


class User:

#   ----------------    Constructor ----------------    #
    def __init__(self, uname, pword, tag, db, comments, proxy="", headless= False):
        self.__proxy = proxy
        self.__headless = headless
        self.__comments = comments
        self.__db = db
        self.__uname = uname
        self.__pword = pword
        self.__tag = tag
        self.__posts = []
        self.__bot = ''
        self.log(self.__proxy)
        self.time_sleep = 0
        self.user_agent = "Mozilla/5.0 (Linux; Android 9; SM-A102U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Instagram 155.0.0.37.107 Android (28/9; 320dpi; 720x1468; samsung; SM-A102U; a10e; exynos7885; en_US; 239490550)"
        self.__hasCommented('')

#   ----------------    Get Proxy Instance   ----------------   #
    def __getProxy(self, prxy):
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = prxy
        proxy.ssl_proxy = prxy
        return proxy

#   ----------------    Get Browser Instance   ----------------    #
    def getBotInstance(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", self.user_agent)

        option = Options()
        if self.__headless:
            option.add_argument('--headless')

        proxy = self.__getProxy(self.__proxy)
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        proxy.add_to_capabilities(capabilities)

        bot = webdriver.Firefox(profile, options=option,
                                desired_capabilities=capabilities)
        bot.set_window_size(1000, 650)
        if(self.__proxy!=""):
            time.sleep(30)
        return bot

#   ----------------    Log To Log.txt  ----------------    #
    def log(self, text="\n"):
        (text)
        with open("log.txt",'a') as file:
            file.write(f"{text}\n")
            file.close()

#   ----------------    Check Existance Of Element  ----------------    #
    def check_exists_by_xpath(self, driver, xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_bt_tag(self, driver, tag):
        try:
            driver.find_element_by_tag_name(tag)
        except NoSuchElementException:
            return False
        return True

#   ----------------    Login With Creds
    def login(self, bot, uname, pwrd):
        Login(bot, uname, pwrd)

#   ----------------    get posts from hashtag  ----------------    #
    def getPosts(self):
        links =self.__db.getLinks(self.__tag, self.getUser()) 
        return links

#   ----------------    Click On LIke Button   ----------------    #
    def __ClickLikeBtn(self):
        likeBtnXtag = "//span[@class='fr66n']"
        if self.check_exists_by_xpath(self.__bot, likeBtnXtag):
            try:
                self.__bot.find_element_by_xpath(likeBtnXtag).click()
            except:
                pass
            time.sleep(random.randrange(1, 3))

#   ----------------    has Limited Comment    ----------------    #
    def __isCommentsLimited(self, bot):
        xpath = "//div[@class='MhyEU']"
        return self.check_exists_by_xpath(bot, xpath)

#   ----------------    has Comment Button   ----------------    #
    def __hasCommentsSection(self):
        commentPath = "//span[@class='_15y0l']"
        return self.check_exists_by_xpath(self.__bot, commentPath)

#   ----------------    Has Comments textArea   ----------------    #
    def __hasCommentsTextArea(self):
        commentTextAreaXtag = "//textarea[@class='Ypffh']"
        return self.check_exists_by_xpath(self.__bot, commentTextAreaXtag)

#   ----------------    Write Comment in text Area  ----------------    #
    def __writeComment(self, comment):
        commentTextAreaXtag = "//textarea[@class='Ypffh']"
        cmntArea = self.__bot.find_element_by_xpath(commentTextAreaXtag)
        cmntArea.send_keys(comment)
        return cmntArea

#   ----------------    Comment Upload Progress ----------------    #
    def __commentUploadWait(self):
        find_upload_svg = (By.XPATH, '/html/body/div[1]/section/main/section/div/form/div')
        try:
            WebDriverWait(self.__bot, 10).until(EC.presence_of_element_located(find_upload_svg))
            WebDriverWait(self.__bot, 50).until_not(EC.presence_of_element_located(find_upload_svg))
        except:
            pass
        time.sleep(random.randrange(2, 4))

#   ----------------    Comment on given Post   ----------------    #
    def __commentOnPost(self, post, comment):
        commentPostBtnXtag = "//button[@class='sqdOP yWX7d    y3zKF     ']"

        if self.__hasCommentsSection():
            self.__bot.get(post + 'comments')
            time.sleep(random.randrange(4, 9))

            if self.__hasCommentsTextArea() and not self.__checkComment(self.__uname):
                cmntArea = self.__writeComment(comment)

#   ----------------    Try to Comment  ----------------
                try:
                    self.__bot.find_element_by_xpath(commentPostBtnXtag).click()
                    self.__commentUploadWait()
                except:
                    pass

#   ----------------    Comment Upload Check  ----------------
                if (cmntArea.text != ""):
                    cmntArea.submit()
                    self.__commentUploadWait()
                # time.sleep(random.randrange(1, 4))

#   ----------------    Conclusion  ----------------
                if (cmntArea.text != "") or self.__isCommentsLimited(self.__bot):
                    self.log("Instagram isn't posting comment.. skipped ")
                    return False
                else:
                    self.log(self.__uname + " :commented")
                    self.__hasCommented(post)
                    return True
            else:
                self.log(f"Post UnCommentable :: {post}")
                self.__hasCommented(post)
                return True
        else:
            self.log(f"Post UnCommentable :: {post}")
            self.__hasCommented(post)
            return True
        self.log()

#   ----------------    Add Commented Post To commentedTable in database    ----------------
    def __hasCommented(self, post):
        self.__db.doneWithComment(self.__uname, post)

#   ----------------    Check Pre Commented on Post ----------------
    def __checkComment(self, uid):
        time.sleep(1)
        csss = "ul.Mr508:nth-child(n) > div:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)"
        elements =None
        try:
            elements = self.__bot.find_elements_by_css_selector(csss)
            if elements !=None:
                for ele in elements:
                    if ele==uid:
                        return True
        except:
            return False

#   ----------------    Like and comment on given user post ----------------
    def likeAndCommentOnPost(self, post, comment):
        post = post[1]
        self.log(f"On Post: {post}")
        self.__bot.get(post)
        time.sleep(random.randrange(3, 6))
        self.__ClickLikeBtn()
        return self.__commentOnPost(post, comment)

#   ----------------    Get Random Comment from Comments List   ----------------
    def __randomComment(self):
        return random.choice(self.__comments)

#   ----------------    Start Commenting on Users Post  ----------------
    def __startCommenting(self, limit):
        posts = self.getPosts()
        self.log("posts Found: " + str(len(posts)))

        if len(posts) < 1:
            self.__bot.quit()
            self.log('Done')
            self.log()

        else:
            # Set Limit Var
            if (len(posts) < limit):
                limit = len(posts)

            indexTemp = 0
            for post in posts:
                indexTemp += 1
                self.likeAndCommentOnPost(post, self.__randomComment())
                if indexTemp == (limit - 1):
                    break

            self.__bot.quit()
            self.log('Done')
            self.log()

#   ----------------    Get UID ----------------
    def getUser(self):
        return self.__uname

    def exit(self):
        self.__bot.exit()
#   ----------------    Initialize BOT  ----------------
    def InitCommenting(self, limit):
        self.__bot = self.getBotInstance()
        # time.sleep(60)
        Login(self.__bot, self.__uname, self.__pword).login()
        self.__startCommenting(limit)

    def work(self):
        self.InitCommenting(5)


#   ---------------------------------   TESTS   ---------------------------------   #

# comments=["awesome"]
# tags = ["bike", "code", "java", "cars"]

# db = Database(tags)
# user = User("we.code_", "#samosaman9","code",db, comments, proxy = "191.101.148.25:45785")

# user.InitCommenting(5)
