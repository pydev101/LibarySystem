import time
import lateBooksAPI as lateAPI

class EBook():
    name = ""
    
    def __init__(self,Name):
        self.name = Name
        self.checkedOut = False
        self.redeemed = False
                        
    def checkout(self, timeInHours, returnCode, checkOutObj):
        if self.checkedOut==False:
            self.checkedOut = True
            self.timeOut = time.time()
            self.timeInHours = timeInHours
            self.returnCode = returnCode
            self.checkOutObj = checkOutObj
        else:
            return False
    def checkIn(self):
        late = self.checkLate()
        self.checkedOut = False
        self.timeInHours = -2
        self.returnCode = -2
        self.redeemed = False
        self.checkOutObj = None
        return late #True if late
    
    def redeem(self):
        if self.redeemed == False:
            self.timeOut = time.time()
            for x in lateAPI.allLateBooks:
                if x.bookObj == self:
                    lateAPI.allLateBooks.remove(x)
            self.redeemed = True
            return True
        else:
            return False
        
    def checkLate(self):
        if self.checkedOut:
            if self.checkedOut:
                checkTime = time.time()
                if ((checkTime/3600)-(self.timeOut/3600)) > self.timeInHours:
                    for x in lateAPI.allLateBooks:
                        if x.bookObj == self:
                            return True
                    lateAPI.lateBook(self.checkOutObj.student, self)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
allEBookCopies = []

def illiterate(funct):
    matches = []
    for x in allEBookCopies:
        if funct(x):
            matches.append(x)
    if len(matches) == 0:
        return False
    else:
        return matches
    
#lambda x: True if x.name == name else False    
def createBookCopies(Name, numOfCopies):
    x = 0
    while x<numOfCopies:
        allEBookCopies.append(EBook(Name))
        x=x+1
AN = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':1,'w':22,'x':23,'y':24,'z':25}
#True is greator, False is less when comparing A to B
def sortCheckString(A, B, illit):
    if (illit == len(A)) or (illit == len(B)):
        if illit == len(A):
            return False
        else:
            return True
    
    aNum = A[illit]
    bNum = B[illit]

    if aNum > bNum:
        return True
    if bNum > aNum:
        return False
    if aNum == bNum:
        return sortCheckString(A, B, illit+1)
    
def makeBookCopies(name, numOfCopies):
    name=name.lower()
    if len(allEBookCopies) == 0:
        for z in range(numOfCopies):
            allEBookCopies.append(EBook(name))
    else:
        x = 0
        while sortCheckString(name, allEBookCopies[x].name, 0):
            if x == (len(allEBookCopies)-1):
                for z in range(numOfCopies):
                    allEBookCopies.append(EBook(name))
                return
            x=x+1
        for z in range(numOfCopies):
            allEBookCopies.insert(x,EBook(name))
        
def deleteCopiesFromBookList(name, numOfCopies):
    name=name.lower()
    result = illiterate(lambda x: True if x.name == name else False)
    if result == False:
        return False
    elif len(result)<numOfCopies:
        return False

    for x in result:
        del x
        
def getAvalibleCopy(name):
    name=name.lower()
    for x in allEBookCopies:
        if x.name == name:
            if x.checkedOut == False:
                return x
    return False
