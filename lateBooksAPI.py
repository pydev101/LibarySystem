allLateBooks = []

class lateBook():
    def __init__(self, studentObj, bookObj):
        self.bookObj = bookObj
        
        self.studentLName = studentObj.lName
        self.studentFName = studentObj.fName
        self.studentMInit = studentObj.mInit
        self.studentRedeemCode = studentObj.redeemCode

        self.bookName = bookObj.name
        self.timeOut = bookObj.timeOut
        self.timeCheckedOutFor = bookObj.timeInHours
        self.redeemed = bookObj.redeemed
        
        allLateBooks.insert(0, self)
