checkouts = []

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

class checkout():
    def __init__(self, student, book, timeOut):
        self.student = student
        self.book = book
        self.returnCode = self.student.redeemCode

        self.book.checkout(timeOut, self.returnCode, self)
        
        #Append to student's books
        if len(self.student.booksOut) == 0:
            self.student.booksOut.append(self.book)
        else:
            index = 0
            while index <= len(self.student.booksOut):
                if index == len(self.student.booksOut):
                    self.student.booksOut.append(self.book)
                    break
                if sortCheckString(self.book.name, self.student.booksOut[index].name, 0) == False:
                    self.student.booksOut.insert(index,self.book)
                    break
                index=index+1
                
        #Append self to checkouts by student name
        if len(checkouts) == 0:
            checkouts.append(self)
        else:
            index = 0
            while index <= len(checkouts):
                if index == len(checkouts):
                    checkouts.append(self)
                    break
                if sortCheckString(self.student.lName, checkouts[index].student.lName, 0) == False:
                    checkouts.insert(index,self)
                    break
                index=index+1
            
    def checkIn(self):
        for x in self.student.booksOut:
            if x == self.book:
                self.student.booksOut.remove(x)
        checkouts.remove(self)
        
        result= self.book.checkIn()
        return result #True if late
