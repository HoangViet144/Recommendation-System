class Attribute:
    similarAttributes = {}
    @staticmethod
    def addSimilarAttr(attr1, attr2):
        if attr1 not in Attribute.similarAttributes:
            Attribute.similarAttributes[attr1] = [attr2]
            Attribute.similarAttributes[attr2] = [attr1]
        else:
            Attribute.similarAttributes[attr1].append(attr2)
            Attribute.similarAttributes[attr2].append(attr1)
    @staticmethod
    def hasSimilar(attr1, attr2):
        if attr2.attrName in Attribute.similarAttributes[attr1.attrName]:
            satisfied = False
            if attr1.attrName == "Diện tích mong muốn":
                if attr1.attrValue1 <= attr2.attrValue1 and attr2.attrValue1 <= attr1.attrValue2:
                    satisfied = True
            else:
                if attr1.attrValue1 == attr2.attrValue1:
                    satisfied = True
            return satisfied
        return False
    def __init__(self, attrName, attrValue1 = None, attrValue2 = None,  attrScore  = None, attrWeight = None):
        self.attrName = attrName
        self.attrValue1 = attrValue1
        self.attrValue2 = attrValue2
        self.attrScore = attrScore
        self.attrWeight = attrWeight
        if attrWeight:
            self.attrWeight = attrWeight
        else:
            self.attrWeight = 1
        if attrScore:
            self.attrScore = attrScore
        else:
            self.attrScore = 1
   
class House:
    def __init__(self,id):
        self.id = id
        self.attr = []
        self.totalWeight = 0 # for normalization
    def appendAttr(self, attr):
        self.attr.append(attr)
        self.totalWeight += attr.attrWeight
    
    def lookup(self, attr):
        for i in range(len(self.attr)):
            if self.attr[i].attrName == attr.attrName:
                return i
class User:
    def __init__(self, id):
        self.id = id
        self.attr = []
        self.totalWeight = 0 # for normalization
    def appendAttr(self, attr):
        self.attr.append(attr)
        self.totalWeight += attr.attrWeight
    
    def lookup(self, attr):
        for i in range(len(self.attr)):
            if self.attr[i].attrName == attr.attrName:
                return i
class Matching:
    def __init__(self):
        self.users = {}
        self.houses = {}
    def addUser(self, user):
        self.users[user.id] = user
    def addHouse(self, house):
        self.houses[house.id] = house
    def updateWeightUserHouse(self, user, houseId):
        for attrU in user.attr:
            for attrH in self.houses[houseId].attr:
                if Attribute.hasSimilar(attrU, attrH):
                    ind = self.users[user.id].lookup(attrU)
                    self.users[user.id].attr[ind].attrWeight += 1
                    self.users[user.id].totalWeight += 1
                    ind = self.houses[houseId].lookup(attrH)
                    self.houses[houseId].attr[ind].attrWeight += 1
                    self.houses[houseId].totalWeight += 1
    def updateScoreHouse(self, house):
        for attr in house.attr:
            ind = self.houses[house.id].lookup(attr)
            self.houses[house.id].attr[ind].attrScore = attr.attrScore
    def updateScoreUser(self, user):
        for attr in user.attr:
            ind = self.houses[house.id].lookup(attr)
            self.houses[house.id].attr[ind].attrScore = attr.attrScore
    def getHousesByUser(self, user):
        querryAttrLst = user.attr
        historyAttrLst = self.users[user.id].attr

        tmp = []
        for historyAttr in historyAttrLst:
            check = False
            for queryAttr in querryAttrLst:
                if queryAttr.attrName == historyAttr.attrName:
                    check = True
                    break
            if not check:
                tmp.append(historyAttr)
        querryAttrLst += tmp

        scoreLst = {}
        for houseid, house in self.houses.items():
            curScore = 0
            for attrH in house.attr:
                for attrQ in querryAttrLst:
                    if Attribute.hasSimilar(attrQ, attrH):
                        #print(attrH.attrName, attrH.attrWeight, house.totalWeight, attrQ.attrWeight, attrQ.attrScore, self.users[user.id].totalWeight)
                        curScore += (attrH.attrWeight / house.totalWeight) * (attrQ.attrWeight * attrQ.attrScore / self.users[user.id].totalWeight)
            scoreLst[houseid] = curScore
        scoreLst = ( sorted(scoreLst.items(),key=lambda item: item[1], reverse=True))
        print("HouseId \t Score")
        for house in scoreLst:
            print("%d \t \t %f" %(house[0], house[1]))

if __name__ == "__main__":
    # create simliar attribute
    Attribute.addSimilarAttr("Phòng ngủ","Phòng ngủ mong muốn")
    Attribute.addSimilarAttr("Phòng tắm","Phòng tắm mong muốn")
    Attribute.addSimilarAttr("Diện tích","Diện tích mong muốn")

    userA = User(1)
    userA.appendAttr(Attribute("Phòng ngủ mong muốn", 5, None, 2, None))
    userA.appendAttr(Attribute("Phòng tắm mong muốn", 2, None, 1, None))
    userA.appendAttr(Attribute("Diện tích mong muốn", 25, 100, 7, None))

    houseA = House(1)
    houseA.appendAttr(Attribute("Phòng ngủ", 2, None, None, None))
    houseA.appendAttr(Attribute("Phòng tắm", 2, None, None, None))
    houseA.appendAttr(Attribute("Diện tích", 70, None, None, None))

    houseB = House(2)
    houseB.appendAttr(Attribute("Phòng ngủ", 5, None, None, None))
    houseB.appendAttr(Attribute("Phòng tắm", 2, None, None, None))
    houseB.appendAttr(Attribute("Diện tích", 150, None, None, None))

    houseC = House(3)
    houseC.appendAttr(Attribute("Phòng ngủ", 5, None, None, None))
    houseC.appendAttr(Attribute("Phòng tắm", 3, None, None, None))
    houseC.appendAttr(Attribute("Diện tích", 70, None, None, None))

    houseD = House(4)
    houseD.appendAttr(Attribute("Phòng ngủ", 2, None, None, None))
    houseD.appendAttr(Attribute("Phòng tắm", 3, None, None, None))
    houseD.appendAttr(Attribute("Diện tích", 200, None, None, None))

    matchWorker = Matching()
    matchWorker.addHouse(houseA)
    matchWorker.addHouse(houseB)
    matchWorker.addHouse(houseC)
    matchWorker.addHouse(houseD)
    matchWorker.addUser(userA)
    matchWorker.getHousesByUser(userA)
    
    userAUpdated = User(1)
    userAUpdated.appendAttr(Attribute("Phòng tắm mong muốn", 2, None, 1, None))
    matchWorker.updateWeightUserHouse(userAUpdated, 1)
    matchWorker.getHousesByUser(userA)
    matchWorker.updateWeightUserHouse(userAUpdated, 1)
    matchWorker.getHousesByUser(userA)





