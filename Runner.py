from User import User
import concurrent.futures
from Database import Database
from PostsListener import PostsListener
import sys, threading, sqlite3, time, multithreading
from AdapterConstants import ConstantsHandler


class Runner:

    def __init__(self, keepActive=True, commentFq = 4):
        self.__commentsFq = commentFq+1
        self.__tags = []
        self.__users = []
        self.__proxies = []
        self.__comments = []
        self.__db = ''
        self.__listener = ''
        self.__position = 0
        self.__initConstants()
        self.__keepActive = keepActive

    def __initTagsList(self, UsersData):
        temp = []
        for tag in UsersData:
            temp.append(tag[2])
        return temp

    # get Proxy From List
    def nextProxy(self, data):
        if len(data) > 0:
            if self.__position == len(data):
                self.__position = 0
            proxy = data[self.__position]
            self.__position += 1
            return proxy
        else:
            return ""

    def __initUsers(self, UsersData, db):
        temp = []
        for userData in UsersData:
            temp.append(User(userData[0], userData[1], userData[2], db,self.__comments,  proxy=self.nextProxy(self.__proxies), headless=True))
        return temp

    # Init Constants i.e. db, postsListener, users, tags
    def __initConstants(self):
        handler = ConstantsHandler()

        tempUsersData = handler.getUsersList()
        self.__proxies = handler.getProxiesList()
        self.__comments = handler.getComments()

        self.__tags = self.__initTagsList(tempUsersData)
        self.__db = Database(self.__tags)
        self.__listener = PostsListener(self.__db, headless=True)
        self.__users = self.__initUsers(tempUsersData, self.__db)

    # Start HashTagListener
    def startListening(self, minutes=1):
        listenerThread = threading.Thread(target=self.__listener.startListening)
        listenerThread.start()
        listenerThread.join()
        time.sleep(60*minutes)
        self.startListening()

    def __doComment(self, user):
        try:
            user.InitCommenting(self.__commentsFq)
        except:
            pass
    
    def __killCommenter(self, user):
        user.exit()

    # Start Commmenter for users
    def startCommenting(self):
        if __name__ != "__main__":
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
                print("Commenting....")
                exe.map(self.__doComment, self.__users)
        time.sleep(60)
        if self.__keepActive:
            self.startCommenting()

    def stopLooping(self):
        self.__keepActive = False

    def startLooping(self):
        self.__keepActive = True

    def exit(self):
        for user in self.__users:
            try:
                self.__killCommenter(user)
            except:
                pass
        try:
            self.__listener.exit()
        except:
            pass
        self.__db.exit()
        sys.exit()


#   ------------------  ------------------  ------------------  ------------------  Tests   ------------------  ------------------  ------------------  ------------------
