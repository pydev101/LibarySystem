from tkinter import *
import checkout
import EBookAPI as book
import studentAPI as student
import fileAPI as fileManager
from tkinter import messagebox
import time
import lateBooksAPI as lateBooks
from datetime import datetime

mainWindow = None
studentManagerOpened = None
bookManagerOpened = None
checkoutManagerOpened = None
studentCheckoutManager = None
studentObjectEditorWindowOpened = None
lateBookWindowOpened = None
#GUI Helper------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def updateLists():
    #Main window
    mainWindow.infoBookList.update()
    #Booklist
    if not (bookManagerOpened == None):
        bookManagerOpened.update()
    #Studentlist
    if not (studentManagerOpened == None):
        studentManagerOpened.update()
    #Checkoutlist
    if not (checkoutManagerOpened == None):
        checkoutManagerOpened.update()
    #Student Checkout
    if not (studentCheckoutManager == None):
        studentCheckoutManager.update()
    #Late book window
    if not (lateBookWindowOpened == None):
       lateBookWindowOpened.update()

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                       anchor=NW)

        self.canvas = canvas
        
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        self._configure_interior = _configure_interior
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        self._configure_canvas = _configure_canvas
        canvas.bind('<Configure>', _configure_canvas)

#Checkout windowManager----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class checkoutEditorWindow(Toplevel):
    def __init__(self, checkOutObj, mainObj, mode, *args, **kw):
        Toplevel.__init__(self, *args, **kw)
        self.title('View')
        self.resizable(0,0)
        
        self.checkOutObj = checkOutObj
        self.mainObj = mainObj
        self.mode = mode
        
        Label(self, text="Book Name: "+self.checkOutObj.book.name).grid(sticky=W)
        Label(self, text="Late: "+str(self.checkOutObj.book.checkLate())).grid(row=1,sticky=W)
        self.redeemLabel = Label(self, text="Redeemed: "+str(self.checkOutObj.book.redeemed))
        self.redeemLabel.grid(row=2,sticky=W)
        Label(self, text="-------------------").grid(row=3,sticky=W)
        Label(self, text="Student last name: "+self.checkOutObj.student.lName).grid(row=4,sticky=W)
        Label(self, text="Student first name: "+self.checkOutObj.student.fName).grid(row=5,sticky=W)
        Label(self, text="Student middle inital: "+self.checkOutObj.student.mInit).grid(row=6,sticky=W)
        Label(self, text="Return Code: "+str(self.checkOutObj.returnCode)).grid(row=7,sticky=W)
        Button(self,text="Check In",command=self.checkIN).grid(row=8,sticky=W)
        Button(self,text="Redeem",command=self.redeem).grid(row=8,column=1,sticky=W)
        
    def checkIN(self):
        if self.checkOutObj.checkIn():
            messagebox.showinfo("WARNING", "This book has been turned in late.")

        updateLists()
        self.destroy()
    def redeem(self):
        if self.checkOutObj.book.redeem() == False:
            messagebox.showinfo("Warning", "The book has already been redeemed or an error as occured.")
        else:
            self.redeemLabel.config(text="Redeemed: "+str(self.checkOutObj.book.redeemed))
            updateLists()
            
class checkOutListEntry(Frame):
    def __init__(self, parent, checkOutObj, mainObj, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.checkOutObj = checkOutObj
        self.mainObj = mainObj
        
        textFormat = self.checkOutObj.book.name + '  ||  ' + str(self.checkOutObj.book.checkLate()) + '  ||  ' + self.checkOutObj.student.lName + ', ' + self.checkOutObj.student.fName + '  ||  ' + str(self.checkOutObj.returnCode)

        self.button = Button(self, text="View", command=self.buttonFunct)
        self.textLabel = Label(self,text=textFormat)
        self.button.pack(side=LEFT)
        self.textLabel.pack(side=LEFT)
        
    def buttonFunct(self):
        checkoutEditorWindow(self.checkOutObj, self.mainObj, True)

class checkoutWindowManager(Toplevel):
    def __init__(self, *args, **kw):
        Toplevel.__init__(self, *args, **kw)
        self.title("Checkout Manager")
        self.geometry("500x500")
        self.resizable(0,0)
        Label(self,text='Book Name || Late || Student Lastname, Firstname || Return Code').pack(side=TOP,anchor=NW)
        self.scrollFrame = VerticalScrolledFrame(self)
        self.scrollFrame.pack(side=TOP, fill = Y,anchor=W,expand=1)
        self.button = Button(self, text='Generate Report (CSV File)', command=fileManager.masterReport)
        self.button.pack(side=TOP, fill = X)
        self.update()

        self.protocol("WM_DELETE_WINDOW", self.closing)
    def update(self):
        self.scrollFrame.destroy()
        self.scrollFrame = VerticalScrolledFrame(self)
        self.scrollFrame.pack(side=TOP, fill = Y,anchor=W,expand=1)
        self.button.destroy()
        self.button = Button(self, text='Generate Report (CSV File)', command=fileManager.masterReport)
        self.button.pack(side=TOP, fill = X)
        index = 0
        for x in checkout.checkouts:
            checkOutListEntry(self.scrollFrame.interior,x,self).grid(row=index,sticky=W)
            index=index+1

    def closing(self):
        global checkoutManagerOpened
        checkoutManagerOpened = None
        self.destroy()    

#Book Manager Window------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
class bookListing(Frame):
    def __init__(self, parent, bookObj, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.bookObj = bookObj

        Button(self,text='Remove', fg="red", command=self.remove).pack(side=LEFT)
        Label(self, text="Name: "+self.bookObj.name+" | Checked out: "+str(self.bookObj.checkedOut)).pack(side=LEFT)
        if self.bookObj.checkedOut:
            Label(self, text="by: "+self.bookObj.checkOutObj.student.lName+', '+self.bookObj.checkOutObj.student.fName).pack(side=LEFT)
    def remove(self):
        if self.bookObj.checkedOut:
            self.bookObj.checkOutObj.checkIn()
        book.allEBookCopies.remove(self.bookObj)
        del self.bookObj
        updateLists()


class bookWindowManager(Toplevel):
    def __init__(self, *args, **kw):
        Toplevel.__init__(self, *args, **kw)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.title("Book Manager")
        self.geometry("500x500")
        self.resizable(0,0)

        self.scrollFrame = VerticalScrolledFrame(self, borderwidth=3, relief=SUNKEN)
        self.scrollFrame.pack(side=TOP, fill=BOTH)

        self.createButton = Button(self, command=self.create, text = "Add book")
        self.createButton.pack(side=TOP, fill=X)
        
        self.buttonActive = False
        self.inputWindow = None
        self.bookTitleVar = StringVar()
        self.numCopiesVar = StringVar()
        self.errorLabel = None
        
        self.update()
    def create(self):
        if self.buttonActive == False:
            self.buttonActive = True
            self.inputWindow = Toplevel()
            
            self.inputWindow.title("Add book")
            self.inputWindow.resizable(0,0)
            self.inputWindow.protocol("WM_DELETE_WINDOW", self.closeInputWindow)
            self.inputWindow.geometry("300x200")
            
            Label(self.inputWindow, text='Book Title: ').grid(sticky=W)

            self.tempE = Entry(self.inputWindow, textvariable=self.bookTitleVar)
            self.tempE.bind("<Return>", self.inputEvent)
            self.tempE.grid(sticky = W, row = 1)

            Label(self.inputWindow, text='Number of copies: ').grid(sticky=W)
            
            self.tempEA = Entry(self.inputWindow, textvariable=self.numCopiesVar)
            self.tempEA.bind("<Return>", self.inputEvent)
            self.tempEA.grid(sticky = W, row = 3)

            Button(self.inputWindow, text="Confirmation", fg='green', command=self.confirmation).grid(sticky = W, row = 4)
            
            self.errorLabel = Label(self.inputWindow, fg='red')
            self.errorLabel.grid(sticky = W, row = 5)

    def checkInput(self):
        self.inputWindow.focus_set()
        if self.tempE.get() == '':
            self.tempE.focus_set()
            return False
        if self.tempEA.get() == '':
            self.tempEA.focus_set()
            return False
        if self.tempEA.get().isdigit():
            self.errorLabel.configure(text='')
        else:
            self.errorLabel.configure(text='"Number of copies" may only contain numbers')
            return False
        return True
    def inputEvent(self, event):
        self.checkInput()
                
    def confirmation(self):
        if self.checkInput():
            book.makeBookCopies(self.tempE.get(),int(self.tempEA.get()))
            self.update()
            self.closeInputWindow()
            
    def closeInputWindow(self):
        self.buttonActive = False
        self.inputWindow.destroy()
        self.errorLabel = None
        self.inputWindow = None
        self.tempE = None
        self.tempEA = None
        self.bookTitleVar.set('')
        self.numCopiesVar.set('')
        
    def update(self):
        self.scrollFrame.destroy()
        self.scrollFrame = VerticalScrolledFrame(self, borderwidth=3, relief=SUNKEN)
        self.scrollFrame.pack(side=TOP, fill=BOTH, anchor=N)
        self.createButton.destroy()
        self.createButton = Button(self, command=self.create, text = "Add book")
        self.createButton.pack(side=TOP, fill=X)
        for x in book.allEBookCopies:
            bookListing(self.scrollFrame.interior, x).pack(side=TOP, anchor=W)
            
    def closing(self):
       global bookManagerOpened
       bookManagerOpened = None
       self.destroy()
       
#STUDENT CHECKOUT LIST ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class bookListingMod(Frame):
    def __init__(self, parent, bookObj, student, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.bookObj = bookObj
        self.student = student
        
        Button(self,text='Checkout', command=self.checkout).pack(side=LEFT)
        Label(self, text="Name: "+self.bookObj.name).pack(side=LEFT)
    def checkout(self):
        checkout.checkout(self.student, book.getAvalibleCopy(self.bookObj.name), 48) #Default time of 2 days out
        updateLists()
        
class checkOutWindowStudent(Toplevel):
    def __init__(self, student, *args, **kw):
        Toplevel.__init__(self, *args, **kw)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.title("Checkout Window")
        self.resizable(0,0)

        self.student = student
        
        self.scrollFrame = VerticalScrolledFrame(self, borderwidth=3, relief=SUNKEN)
        self.scrollFrame.pack(side=TOP, fill=BOTH)

        self.update()
    def update(self):
        self.scrollFrame.destroy()
        self.scrollFrame = VerticalScrolledFrame(self, borderwidth=3, relief=SUNKEN)
        self.scrollFrame.pack(side=TOP, fill=BOTH)
        for x in book.allEBookCopies:
            if x.checkedOut == False:
                bookListingMod(self.scrollFrame.interior, x, self.student).pack(side=TOP, anchor=W)
        
    def closing(self):
       global studentCheckoutManager
       studentCheckoutManager = None
       self.destroy()

#Student Manager Window-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class studentObjectEditorWindow(Toplevel):
    def __init__(self, student, *args, **kw):
        Toplevel.__init__(self, *args, **kw)
        self.title("Student Object Editor")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.closing)

        self.student = student
        
        self.lastName = StringVar()
        self.firstName = StringVar()
        self.mInit = StringVar()
        self.grade = StringVar()
        self.redeemCode = StringVar()
        
        if student == None:
            self.createMode = True
        else:
            self.createMode = False
            self.lastName.set(self.student.lName)
            self.firstName.set(self.student.fName)
            self.mInit.set(self.student.mInit)
            self.grade.set(str(self.student.grade))
            self.redeemCode.set(str(self.student.redeemCode))

        #Last Name
        Label(self, text='Enter last name:').grid(row = 0, column=0,sticky=W)
        self.lastNameEntryField = Entry(self,textvariable=self.lastName)
        self.lastNameEntryField.bind("<Return>", self.onEntry)
        self.lastNameEntryField.grid(row = 0, column = 1)

        #First Name
        Label(self, text='Enter first name:').grid(row = 1, column=0,sticky=W)
        self.firstNameEntryField = Entry(self,textvariable=self.firstName)
        self.firstNameEntryField.bind("<Return>", self.onEntry)
        self.firstNameEntryField.grid(row = 1, column = 1)

        #Middle inital
        Label(self, text='Enter middle inital:').grid(row = 2, column=0,sticky=W)
        self.mInitNameEntryField = Entry(self,textvariable=self.mInit)
        self.mInitNameEntryField.bind("<Return>", self.onEntry)
        self.mInitNameEntryField.grid(row = 2, column = 1)

        #Grade
        Label(self, text='Enter grade:').grid(row = 3, column=0,sticky=W)
        self.gradeEntryField = Entry(self,textvariable=self.grade)
        self.gradeEntryField.bind("<Return>", self.onEntry)
        self.gradeEntryField.grid(row = 3, column = 1)

        #Redeem code
        Label(self, text='Enter redeem code:').grid(row = 4, column=0,sticky=W)
        self.redeemCodeEntryField = Entry(self,textvariable=self.redeemCode)
        self.redeemCodeEntryField.bind("<Return>", self.onEntry)
        self.redeemCodeEntryField.grid(row = 4, column = 1)

        #Error Message
        self.errorMessage = Label(self, text="Placeholder", fg='red')
        self.errorMessage.grid(row=5,sticky=W,columnspan=2)
        self.errorMessage.grid_remove()
        
        #Confirm Button
        Button(self, text="Confirmation", fg='green', command=self.confirm).grid(row=6,sticky=W+E,columnspan=2)
        
    def onEntry(self, event):
        self.checkInput()
        
    def checkInput(self):
        self.focus_set()
        self.errorMessage.grid_remove()
        if self.lastNameEntryField.get() == '':
            self.lastNameEntryField.focus_set()
            return False
        if self.firstNameEntryField.get() == '':
            self.firstNameEntryField.focus_set()
            return False
        if self.mInitNameEntryField.get() == '':
            self.mInitNameEntryField.focus_set()
            return False
        if self.gradeEntryField.get() == '':
            self.gradeEntryField.focus_set()
            return False
        if self.redeemCodeEntryField.get() == '':
            self.redeemCodeEntryField.focus_set()
            return False
        if self.gradeEntryField.get().isdigit() == False:
            self.errorMessage.configure(text='"Grade" must be a number')
            self.errorMessage.grid()
            self.gradeEntryField.focus_set()
            return False
        if self.redeemCodeEntryField.get().isdigit() == False:
            self.errorMessage.configure(text='"Redeem code" must be a number')
            self.errorMessage.grid()
            self.redeemCodeEntryField.focus_set()
            return False
        return True

    def confirm(self):
        if self.checkInput():
            #Check for identical redeem code / last name pairs
            for x in student.listOfStudents:
                if (x.redeemCode == int(self.redeemCode.get())) and (x.lName == self.lastName.get()):
                    if self.createMode == True:
                        #Error Duplicate Student Might Be Created
                        self.errorMessage.configure(text='Student cannot have the same redeem code and last name as another student')
                        self.errorMessage.grid()
                        return
                    else:
                        if not (self.student == x):
                            #Error Duplicate Student Might Be Created
                            self.errorMessage.configure(text='Student cannot have the same redeem code and last name as another student')
                            self.errorMessage.grid()
                            return
                        
            if self.createMode == True:
                student.newStudent(self.lastName.get(),self.firstName.get(), self.mInit.get(), int(self.grade.get()), int(self.redeemCode.get()))
            else:
                self.student.fName = self.lastName.get()
                self.student.lName = self.firstName.get()
                self.student.mInit = self.mInit.get()
                self.student.grade = int(self.grade.get())
                self.student.redeemCode = int(self.redeemCode.get())
            self.closing()
            updateLists()
            mainWindow.logout()
    def closing(self):
        global studentObjectEditorWindowOpened
        studentObjectEditorWindowOpened = None
        self.destroy()
        
class studentManagmentEntryList(Frame):
    def __init__(self, parent, student, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.student = student

        Button(self, text='Remove', fg='red', command=self.remove).pack(side=LEFT, anchor=W)
        Button(self, text='Edit', command=self.edit).pack(side=LEFT, anchor=W)
        Label(self, text="Name: "+self.student.lName+', '+self.student.fName+', '+self.student.mInit+' | Redeem Code: '+str(self.student.redeemCode)+' | Grade: '+str(self.student.grade)).pack(side = LEFT, anchor=W)

    def edit(self):
        global studentObjectEditorWindowOpened
        if studentObjectEditorWindowOpened==None:
            studentObjectEditorWindowOpened = studentObjectEditorWindow(self.student)
            
    def remove(self):
        if messagebox.askokcancel("Student Manager","Are you sure you want to remove this student?"):
            if mainWindow.currStudent == self.student:
                mainWindow.logout()
            student.removeStudent(self.student)
            updateLists()
        if not (studentManagerOpened == None):
            studentManagerOpened.focus_set()
        
class studentManagerWindow(Toplevel):
    def __init__(self, *args, **kw):
        Toplevel.__init__(self, *args, **kw)
        self.title("Student Manager")
        self.geometry("500x500")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        
        self.scrollFrame = VerticalScrolledFrame(self)
        self.scrollFrame.pack(fill=BOTH, side = TOP, anchor=W)

        self.button = Button(self, text="Add Student", command=self.create)
        self.button.pack(side=TOP, fill=X)

        
        self.update()
    def create(self):
        global studentObjectEditorWindowOpened
        if studentObjectEditorWindowOpened==None:
            studentObjectEditorWindowOpened = studentObjectEditorWindow(None)
        
    def update(self):
        self.scrollFrame.destroy()
        self.scrollFrame = VerticalScrolledFrame(self)
        self.scrollFrame.pack(fill=BOTH, side = TOP, anchor=W)
        self.button.destroy()
        self.button = Button(self, text="Add Student", command=self.create)
        self.button.pack(side=TOP, fill=X)
        for x in student.listOfStudents:
            studentManagmentEntryList(self.scrollFrame.interior, x).pack(side=TOP, anchor=W)

    def closing(self):
       global studentManagerOpened
       studentManagerOpened = None
       self.destroy()
#Late Window -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class lateBookEntryFrame(Frame):
    def __init__(self, parent, x, window, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.window = window
        self.obj = x

        Button(self, text='Remove', command=self.remove, fg='red').pack(side=LEFT)
        Label(self, text=self.obj.studentLName+' | '+self.obj.studentFName+' | '+self.obj.studentMInit+' | '+str(self.obj.studentRedeemCode)+' | '+self.obj.bookName+' | '+str(datetime.utcfromtimestamp(self.obj.timeOut).strftime('%Y-%m-%d %H:%M:%S'))+' | '+str(self.obj.timeCheckedOutFor)+' hours | '+str(self.obj.redeemed)).pack(side=LEFT)

        
    def remove(self):
        lateBooks.allLateBooks.remove(self.obj)
        self.window.update()    
    
class lateCheckoutsWindow(Toplevel):
    def __init__(self, *args, **kw):
        Toplevel.__init__(self, *args, **kw)
        self.title("Late Checkouts")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        
        self.label = Label(self,text='Student Last Name | Student First Name | Student Redeem Code | Book Name | Time checked out | Time checked out for | Redeemed').pack(side=TOP)
        
        self.scrollFrame = VerticalScrolledFrame(self)
        
        self.update()
    def update(self):
        self.scrollFrame.destroy()
        self.scrollFrame = VerticalScrolledFrame(self)
        self.scrollFrame.pack(side=TOP, fill=BOTH)
        for x in lateBooks.allLateBooks:
            lateBookEntryFrame(self.scrollFrame.interior, x, self).pack(anchor=W, side=TOP)
            
    def closing(self):
        global lateBookWindowOpened
        lateBookWindowOpened = None
        self.destroy()
#Main Manager ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class checkOutListEntryMOD(Frame):
    def __init__(self, parent, checkOutObj, mainObj, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.checkOutObj = checkOutObj
        self.mainObj = mainObj

        textFormat = self.checkOutObj.book.name + '  ||  ' + str(self.checkOutObj.book.checkLate())

        self.button = Button(self, text="View", command=self.buttonFunct)
        self.textLabel = Label(self,text=textFormat)
        self.button.pack(side=LEFT)
        self.textLabel.pack(side=LEFT)
        self.pack()

        
    def buttonFunct(self):
        checkoutEditorWindow(self.checkOutObj, self.mainObj, False)
        
class studentBookManagerFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        self.parent = parent
        self.scrollFrame = VerticalScrolledFrame(self)
        self.scrollFrame.pack()
    def update(self):
        student = mainWindow.currStudent

        self.scrollFrame.destroy()
        self.scrollFrame = VerticalScrolledFrame(self)
        self.scrollFrame.pack()
        if not (student==None):
            for x in student.booksOut:
                checkOutListEntryMOD(self.scrollFrame.interior, x.checkOutObj, self).pack(side=TOP, anchor=W)
        
class mainWindow(Tk):
    def __init__(self, *args, **kw):

        fileManager.load()
        
        Tk.__init__(self, *args, **kw)
        self.title("General Manager")
        self.geometry("500x500")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.closing)

        self.dataFrame = Frame(self)
        Label(self.dataFrame, text='Enter return code:').grid(sticky=W)
        self.redeemCodeInputString = StringVar()
        self.redeemCodeEntryField = Entry(self.dataFrame,textvariable=self.redeemCodeInputString)
        self.redeemCodeEntryField.bind("<Return>", self.onEntry)
        self.redeemCodeEntryField.grid(row = 0, column = 1)


        Label(self.dataFrame, text='Enter last name:').grid(row = 1, column=0,sticky=W)
        self.lastNameInputString = StringVar()
        self.lastNameEntryField = Entry(self.dataFrame,textvariable=self.lastNameInputString)
        self.lastNameEntryField.bind("<Return>", self.onEntry)
        self.lastNameEntryField.grid(row = 1, column = 1)

        
        self.info = Frame(self, borderwidth=3, relief=SUNKEN)
        Grid.rowconfigure(self.info, 0, weight=1)
        
        self.infoName = Label(self.info,text='Name: ')
        self.infoName.grid(row=0,sticky=W)

        Button(self.info, text='Checkout a book', command=self.checkoutBook).grid(row = 1, sticky=W)
        Button(self.info, text='Log out', command=self.logout).grid(row = 2, sticky=W)
        
        self.infoBookList = studentBookManagerFrame(self.info)
        self.infoBookList.grid(row=3,sticky=W+E)

        self.dataFrame.grid(row=0,column=0,sticky=W)
        self.info.grid(row=1,column=0,sticky=W)

        self.currStudent = None
        self.info.grid_remove()

        self.mainMenu = Menu(self)
        
        self.menubar = Menu(self.mainMenu)
        self.menubar.add_command(label="Checkout Manager", command=self.checkoutManagerWindowOpen)
        self.menubar.add_command(label="Book Manager",  command=self.bookManagerWindowOpen)
        self.menubar.add_command(label="Student Manager", command=self.openStudentManagerWindow)
        self.menubar.add_command(label="Latebook Manager", command=self.openLateBookWindow)
        self.mainMenu.add_cascade(label="Manager", menu=self.menubar)

        self.filebar = Menu(self.mainMenu)
        self.filebar.add_command(label="Save", command=fileManager.save)
        self.filebar.add_command(label="Load",  command=self.loadFromFile)
        self.mainMenu.add_cascade(label="Save/Load", menu=self.filebar)
        
        self.config(menu=self.mainMenu)

        global mainWindow
        mainWindow = self
    def loadFromFile(event):
        fileManager.load()
        updateLists()
    def onEntry(self, event):
        try:
            self.focus_set()
            if self.lastNameEntryField.get() == '':
                self.lastNameEntryField.focus_set()
                return
            if self.redeemCodeEntryField.get() == '':
                self.redeemCodeEntryField.focus_set()
                return
            for x in student.listOfStudents:
                if x.redeemCode == int(self.redeemCodeInputString.get()):
                    if x.lName == self.lastNameInputString.get().lower():
                        self.currStudent = x
                        self.infoName.configure(text = 'Name: '+x.lName+', '+x.mInit+', '+x.fName)
                        self.infoBookList.update()
                        self.info.grid()
                        break
        except:
            pass
    def logout(self):
        self.currStudent = None
        self.info.grid_remove()
        self.lastNameInputString.set('')
        self.redeemCodeInputString.set('')
        self.infoName.configure(text = 'Name: ')
        self.infoBookList.update()
        
        global studentCheckoutManager
        if not (studentCheckoutManager == None):
            studentCheckoutManager.destroy()
            studentCheckoutManager == None
        
    def checkoutBook(self):
        global studentCheckoutManager
        if studentCheckoutManager == None:
            studentCheckoutManager = checkOutWindowStudent(self.currStudent)    
    def checkoutManagerWindowOpen(self):
        global checkoutManagerOpened
        if checkoutManagerOpened == None:
            checkoutManagerOpened = checkoutWindowManager()
    def bookManagerWindowOpen(self):
        global bookManagerOpened
        if bookManagerOpened == None:
            bookManagerOpened = bookWindowManager()
    def openStudentManagerWindow(self):
        global studentManagerOpened
        if studentManagerOpened == None:
            studentManagerOpened = studentManagerWindow()
    def openLateBookWindow(self):
        global lateBookWindowOpened
        if lateBookWindowOpened == None:
            lateBookWindowOpened = lateCheckoutsWindow()
    def closing(self):
        fileManager.save()
        self.destroy()
        exit()

main = mainWindow()
main.mainloop()
