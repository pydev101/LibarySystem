import pickle as pick
import checkout
import EBookAPI
import studentAPI
import csv
import time
from datetime import datetime
import os
import lateBooksAPI

class saveClass():
    def __init__(self, books, students, checkouts, allLateBooks):
        self.books = books
        self.students = students
        self.checkouts = checkouts
        self.allLateBooks = allLateBooks
        
def save():
    file = open("saveData.config", mode='wb')
    pick.dump(saveClass(EBookAPI.allEBookCopies, studentAPI.listOfStudents, checkout.checkouts, lateBooksAPI.allLateBooks), file)
    file.close()

def load():
    file = open("saveData.config", mode='rb')
    info = pick.load(file)
    file.close()
    EBookAPI.allEBookCopies = info.books
    studentAPI.listOfStudents = info.students
    checkout.checkouts = info.checkouts
    lateBooksAPI.allLateBooks = info.allLateBooks
    
def masterReport():
    with open('report.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #Report Late Books
        filewriter.writerow(['Late Books'])
        filewriter.writerow(['Book Name', 'Student Last Name', 'Student First Name', 'Student Redeem Code', 'Time out', 'Time out for', 'Redeemed']) #Labels
        for x in lateBooksAPI.allLateBooks:
            filewriter.writerow([x.bookName, x.studentLName, x.studentFName, str(x.studentRedeemCode), str(datetime.utcfromtimestamp(x.timeOut).strftime('%Y-%m-%d %H:%M:%S')), str(x.timeCheckedOutFor), str(x.redeemed)])
            
        #Report Checkouts
        filewriter.writerow(['Checkouts'])
        filewriter.writerow(['Book Name', 'Student Last Name', 'Student Redeem Code', 'Time out', 'Time out for', 'Late', 'Redeemed']) #Labels
        for x in checkout.checkouts:
            book = x.book
            output = []
            output.append(book.name)
            output.append(book.checkOutObj.student.lName)
            output.append(str(book.checkOutObj.student.redeemCode))
            output.append(str(datetime.utcfromtimestamp(book.timeOut).strftime('%Y-%m-%d %H:%M:%S')))
            output.append(str(book.timeInHours)+' hours')
            output.append(str(book.checkLate()))
            output.append(str(book.redeemed))
            filewriter.writerow(output)
    os.startfile('report.csv')
