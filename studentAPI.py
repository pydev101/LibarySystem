class student():
    def __init__(self,lastName,firstName, mInit,grade,redeemCode):
        self.lName = lastName
        self.fName = firstName
        self.mInit = mInit
        self.grade = grade
        self.redeemCode = redeemCode
        self.booksOut = []
    
listOfStudents = []

def illiterate(funct):
    for x in listOfStudents:
        if funct(x):
            return x
    return False

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
    
def newStudent(lastName,firstName, mInit,grade,redeemCode):
    lastName = lastName.lower()
    firstName = firstName.lower()
    mInit = mInit.lower()
    
    obj = student(lastName,firstName, mInit,grade,redeemCode)
    if len(listOfStudents) == 0:
        listOfStudents.append(obj)
    else:
        x = 0
        while sortCheckString(lastName, listOfStudents[x].lName, 0):
            if x == (len(listOfStudents)-1):
                listOfStudents.append(obj)
                return
            x=x+1
        listOfStudents.insert(x,obj)
    return obj        

def removeStudent(studentObj):
    while len(studentObj.booksOut) > 0:
        studentObj.booksOut[len(studentObj.booksOut)-1].checkOutObj.checkIn()
    listOfStudents.remove(studentObj)
    del studentObj
