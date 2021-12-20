import uuid
import sqlite3


class Database:
    # Constructor
    def __init__(self, tags):
        self.__tags = tags
        self.__connection = sqlite3.connect("Tags.db", check_same_thread=False)
        self.__cursor = self.__connection.cursor()
        self.__setupTags()

    def getTags(self):
        return self.__tags

    def filterName(self, name):
        temp = name
        for char in spclchars:
            temp = name.strip(" ").replace(char,"")
        return name

    # SetUp Tags Table
    def __setupTags(self):
        for tag in self.__tags:
            q = f"CREATE TABLE IF NOT EXISTS {tag}(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, link TEXT NOT NULL UNIQUE)"
            self.__executeQuery(q)

    # SetUp UserCommented Table
    def __setupTable(self, name):
        q = f"CREATE TABLE IF NOT EXISTS {name}(link TEXT NOT NULL UNIQUE)"
        self.__cursor.execute(q)

    # Delete Table From Database
    def deleteTable(self, table):
        query = f"DROP TABLE IF EXISTS {table};"
        self.__executeQuery(query)

    # Get All Links
    def getAllLinks(self, tag):
        q = f"SELECT * FROM {tag} ORDER BY id DESC"
        self.__executeQuery(q)
        return self.__cursor.fetchall()


    # Add User to Users Table
    def __addUser(self, user):
        uid = f"a{str(uuid.uuid4())}".replace('-', '')
        q = f"CREATE TABLE IF NOT EXISTS Users(uid TEXT NOT NULL PRIMARY KEY UNIQUE, user TEXT NOT NULL UNIQUE);"
        self.__executeQuery(q)
        q = f"INSERT INTO Users(uid, user) VALUES ('{uid}','{user}');"
        self.__executeQuery(q)
        # self.__executeQuery(q)

    # Get User From Users Table
    def __getUser(self, user):
        q = f"SELECT * FROM Users WHERE user= '{user}'"
        self.__executeQuery(q)
        return self.__cursor.fetchone()

    # returns list of Links of given Tag
    def getLinks(self, tag, uname):
        user = self.__getUser(uname)
        if None != user:
            tableName = user[0]
            self.__setupTable(tableName)
            q = f"SELECT * FROM {tag} WHERE link NOT IN (SELECT link FROM {tableName}) ORDER BY id DESC"
            self.__executeQuery(q)
            return self.__cursor.fetchall()
        else:
            return []

    # Add Link to Given Tag Table
    def addLink(self, tag, link):
        q = f"INSERT INTO {tag}(link) VALUES ('{link}')"
        self.__executeQuery(q)

    # Add link to comment Table
    def doneWithComment(self, uname, link):
        self.__addUser(uname)
        user = self.__getUser(uname)

        if user != None:
            tableName = user[0]
            self.__setupTable(tableName)
            q = f"INSERT INTO {tableName}(link) VALUES ('{link}');"
            self.__executeQuery(q)

    # Get User Commented Posts
    def getCommentedData(self, uname):
        user = self.__getUser(uname)
        if None != user:
            tableName = user[0]
            self.__setupTable(tableName)
            q = f"SELECT * FROM {tableName};"
            self.__executeQuery(q)
            # self.__cursor.execute(q)
            return self.__cursor.fetchall()
        return []

    # Execute Given Query
    def __executeQuery(self, query):
        try:
            self.__cursor.execute(query)
            self.__connection.commit()
        except:
            pass

    # Close The Connection
    def exit(self):
        self.__connection.close()


#   ----------------------------    TEST    ----------------------------
# uname = f"we.code_"
# tags = ["bike", "code", "java"]
# db = Database(tags)

# db.doneWithComment("we.code_","https://www.instagram.com/p/CT4TZgiqglb/")
# [print(data) for data in db.("bike","we.code_")]
# print(len(db.getCommentedData("we.code_")))
# con = sqlite3.connect("Tags.db")
# print(db.getLinks("bike", "_eliana_motivation12"))
# [print(data) for data in db.getLinks("bike", "_eliana_motivation12")]
# print(db.getU("_eliana_motivation12"))

# cur = con.cursor()

# q = f"SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
# cur.execute(q)
# [print(data) for data in cur.fetchall()]