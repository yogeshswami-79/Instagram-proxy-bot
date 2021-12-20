from User import User

class ConstantsHandler:

    def __getDataFromFile(self, fileName):
        loc = f"Models/{fileName}"
        # loc = f"sept9\Models\{fileName}"
        # Reading data from file lineWise
        with open(loc, "r") as file:
            data = file.readlines()
            file.close()
            return data

    def __getLinesFromFiles(self, file):
        temp = [line.strip('\n').split(',')
                for line in self.__getDataFromFile(file)]
        return temp

    def getUsersList(self):
        users = []
        temp = self.__getLinesFromFiles("users.txt")

        for data in temp:
            uName, pWord, hTag = data[0].strip(
            ), data[1].strip(), data[2].strip()
            users.append((uName, pWord, hTag))
        return users

    def getProxiesList(self):
        proxies = []
        temp = self.__getLinesFromFiles("proxies.txt")
        [proxies.append(t[0]) for t in temp]
        return proxies

    def getComments(self):
        comments = []
        temp = self.__getLinesFromFiles("comments.txt")
        [comments.append(t[0]) for t in temp]
        return comments


# -------------------   Test    -------------------#
