from sqlite3 import connect
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from cx_Oracle import *
import matplotlib.pyplot as plt
import socket
import requests
import bs4

root = Tk()
root.title("S.M.S")
root.geometry("500x400+200+200")


def f1():
    root.withdraw()


adst.deiconify()


def f2():
    adst.withdraw()


root.deiconify()


def f3():
    stdata.delete(1.0, END)


root.withdraw()
vist.deiconify()
con = None
try:
    con = connect("system/abc123")
    cursor = con.cursor()
    sql = "select * from student1"
    cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)
    msg = ""
    for d in data:
        msg = msg + "Roll no: " + str(d[0]) + "  Name: " + d[1] + " Marks: " + str(d[2]) + "\n"

        stdata.insert(INSERT, msg)

except DatabaseError as e:
    print("issue ", e)

finally:
    if con is not None:
        con.close()


def f4():
    vist.withdraw()


root.deiconify()


def f5():
    con = None


try:
    con = connect("system/abc123")
    rno = entAddRno.get()
    name = entAddName.get()
    marks = entAddMarks.get()

    if rno == '' or name == '' or marks == '':
        messagebox.showerror("Issue", "feilds cannot be empty")
        entAddRno.delete(0, END)
        entAddName.focus()

    elif not name.isalpha():
        messagebox.showerror("Issue", "name should be a string")
        entAddRno.delete(0, END)
        entAddName.delete(0, END)
        entAddMarks.delete(0, END)
        entAddRno.focus()

    else:
        cursor = con.cursor()
        r = int(rno)
        m = int(marks)
        if m > 100 or m < 0:
            messagebox.showerror("Issue", "enter marks between 0 to 100")
            entAddRno.delete(0, END)
            entAddName.delete(0, END)
            entAddMarks.delete(0, END)
            entAddRno.focus()
        else:
            r = int(rno)
m = int(marks)
sql = "insert into student1 values('%d','%s','%d')"
args = (r, name, m)
cursor.execute(sql % args)
con.commit()
messagebox.showinfo("success", "record inserted")
entAddRno.delete(0, END)
entAddName.delete(0, END)
entAddMarks.delete(0, END)
entAddRno.focus()

except DatabaseError as e:
con.rollback()
messagebox.showerror(e)

except ValueError:
con.rollback()
messagebox.showerror("Issue", "Enter Integer for rollno and marks")
entAddRno.delete(0, END)
entAddName.delete(0, END)
entAddRno.focus()



finally:
if con is not None:
    con.close()


def f6():
    root.withdraw()


udst.deiconify()


def f7():
    udst.withdraw()


root.deiconify()


def f8():
    con = None


try:
    con = connect("system/abc123")
rno = entUpdateRno.get()
name = entUpdateName.get()
marks = entUpdateMarks.get()

if rno == '' or name == '' or marks == '':
    messagebox.showerror("Issue", "feilds cannot be empty")
entUpdateRno.delete(0, END)
entUpdateName.delete(0, END)
entUpdateMarks.delete(0, END)
entUpdateRno.focus()

elif not name.isalpha():
messagebox.showerror("Issue", "name should be a string")
entUpdateRno.delete(0, END)
entUpdateName.delete(0, END)
entUpdateMarks.delete(0, END)
entUpdateRno.focus()

else:
cursor = con.cursor()
r = int(rno)
m = int(marks)
if m > 100 or m < 0:
    messagebox.showerror("Issue", "enter marks between 0 to 100")
entUpdateRno.delete(0, END)
entUpdateName.delete(0, END)
entUpdateMarks.delete(0, END)
entUpdateRno.focus()
else:
sql = "update student1 set name='%s' ,marks='%d' where roll_no='%d'"
args = (name, m, r)
cursor.execute(sql % args)
con.commit()
messagebox.showinfo("success", "record updated")
entUpdateRno.delete(0, END)
entUpdateName.delete(0, END)
entUpdateMarks.delete(0, END)
entUpdateRno.focus()

except DatabaseError as e:
con.rollback()
messagebox.showerror("issue ", "" + e)

except ValueError:
con.rollback()
messagebox.showerror("Issue", "Enter Integer for rollno and marks")
entUpdateRno.delete(0, END)
entUpdateName.delete(0, END)
entUpdateRno.focus()



finally:
if con is not None:
    con.close()


def f9():
    root.withdraw()


dst.deiconify()


def f10():
    root.deiconify()


dst.withdraw()


def f12():
    n = []


m = []
con = None
try:
    con = connect("system/abc123")
cursor = con.cursor()
sql = "select * from student1"
cursor.execute(sql)
data = cursor.fetchall()

for d in data:
    n.append(d[1])
m.append(d[2])
print(n)
print(m)

plt.bar(n, m, width=0.5, color='blue')
plt.title("performance analysis")
plt.xlabel("Name")
plt.ylabel("Marks")
plt.legend()
plt.grid()
plt.show()




except DatabaseError as e:
con.rollback()
messagebox.showerror("issue ", "" + e)

except ValueError:
con.rollback()
messagebox.showerror("Issue", "Enter Integer for rollno and marks")
entUpdateRno.delete(0, END)
entUpdateName.delete(0, END)
entUpdateRno.focus()


def f11():
    con = None


try:
    con = connect("system/abc123")
rno = int(entDeleteRno.get())
cursor = con.cursor()
sql = "delete from student1 where roll_no='%d'"
args = (rno)
cursor.execute(sql % args)
con.commit()
messagebox.showinfo("success", "record deleted")
entDeleteRno.delete(0, END)
entDeleteRno.focus()

except DatabaseError as e:
con.rollback()
messagebox.showerror("issue ", "" + e)

except ValueError:
con.rollback()
messagebox.showerror("Issue", "Enter Integer for rollno and marks")
entDeleteRno.delete(0, END)
entDeleteRno.focus()



finally:
if con is not None:
    con.close()

res1 = requests.get("https://ipinfo.io")
data1 = res1.json()
print(data1)
c = data1['city']
print(c)
c = 'kalyan'
a1 = "https://api.openweathermap.org/data/2.5/weather?units=metric"
a2 = "&q=" + c
a3 = "&appid=c6e315d09197cec231495138183954bd"
api_address = a1 + a2 + a3
# print(api_address)
res = requests.get(api_address)
# print(res)
data = res.json()
print(data)
t1 = data['main']

l1 = t1['temp']
temp = str(l1)

res2 = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup = bs4.BeautifulSoup(res2.text, 'html.parser')
quote = soup.find('img', {"class": "p-qotd"})
msg = quote['alt']
# except Exception as e:
# pass


btnAdd = Button(root, text="Add", font=('arial', 16, 'bold'), width=10, command=f1)
btnView = Button(root, text="View", font=('arial', 16, 'bold'), width=10, command=f3)
btnUpdate = Button(root, text="Update", font=('arial', 16, 'bold'), width=10, command=f6)
btnDelete = Button(root, text="Delete", font=('arial', 16, 'bold'), width=10, command=f9)
btnGraph = Button(root, text="Graph", font=('arial', 16, 'bold'), width=10, command=f12)

lbCity = Label(root, text="City: " + c, font=('arial', 16, 'bold'))
lbTemp = Label(root, text="Temprature: " + temp, font=('arial', 16, 'bold'))
lbQuote = Label(root, text="Quote: " + msg, font=('arial', 16, 'bold'))

btnAdd.pack(pady=5)
btnView.pack(pady=5)
btnUpdate.pack(pady=5)
btnDelete.pack(pady=5)
btnGraph.pack(pady=5)
lbCity.pack(pady=5)
lbTemp.pack(pady=5)
lbQuote.pack(pady=5)

adst = Toplevel(root)
adst.title("Add student")
adst.geometry("500x400+200+200")

lbAddName = Label(adst, text="Enter Name", font=('arial', 16, 'bold'))
lbAddRno = Label(adst, text="Enter Roll no", font=('arial', 16, 'bold'))
lbAddMarks = Label(adst, text="Enter Marks", font=('arial', 16, 'bold'))

entAddName = Entry(adst, bd=5, font=('arial', 16, 'bold'))
entAddRno = Entry(adst, bd=5, font=('arial', 16, 'bold'))
entAddMarks = Entry(adst, bd=5, font=('arial', 16, 'bold'))

btnSave = Button(adst, text="Save", font=('arial', 16, 'bold'), command=f5)
btnAddBack = Button(adst, text="Back", font=('arial', 16, 'bold'), command=f2)

lbAddRno.pack(pady=5)
entAddRno.pack(pady=5)
lbAddName.pack(pady=5)
entAddName.pack(pady=5)
lbAddMarks.pack(pady=5)
entAddMarks.pack(pady=5)
btnSave.pack(pady=5)
btnAddBack.pack(pady=5)
adst.withdraw()

vist = Toplevel(root)
vist.title("View Student")
vist.geometry("500x400+200+200")

stdata = scrolledtext.ScrolledText(vist, width=30, height=20)
btnViewBack = Button(vist, text="Back", font=('arial', 16, 'bold'), command=f4)

stdata.pack(pady=10)
btnViewBack.pack(pady=10)

vist.withdraw()

udst = Toplevel(root)
udst.title("Update student")
udst.geometry("500x400+200+200")

lbUpdateName = Label(udst, text="Enter Name", font=('arial', 16, 'bold'))
lbUpdateRno = Label(udst, text="Enter Roll no", font=('arial', 16, 'bold'))
lbUpdateMarks = Label(udst, text="Enter Marks", font=('arial', 16, 'bold'))

entUpdateName = Entry(udst, bd=5, font=('arial', 16, 'bold'))
entUpdateRno = Entry(udst, bd=5, font=('arial', 16, 'bold'))
entUpdateMarks = Entry(udst, bd=5, font=('arial', 16, 'bold'))

btnSave = Button(udst, text="Update", font=('arial', 16, 'bold'), command=f8)
btnUpdateBack = Button(udst, text="Back", font=('arial', 16, 'bold'), command=f7)

lbUpdateRno.pack(pady=5)
entUpdateRno.pack(pady=5)
lbUpdateName.pack(pady=5)
entUpdateName.pack(pady=5)
lbUpdateMarks.pack(pady=5)
entUpdateMarks.pack(pady=5)
btnSave.pack(pady=5)
btnUpdateBack.pack(pady=5)
udst.withdraw()

dst = Toplevel(root)
dst.title("Delete  student")
dst.geometry("500x400+200+200")

lbDeleteRno = Label(dst, text="Enter Roll no", font=('arial', 16, 'bold'))
entDeleteRno = Entry(dst, bd=5, font=('arial', 16, 'bold'))

btnDelete = Button(dst, text="Delete", font=('arial', 16, 'bold'), command=f11)
btnDeleteBack = Button(dst, text="Back", font=('arial', 16, 'bold'), command=f10)

lbDeleteRno.pack(pady=10)
entDeleteRno.pack(pady=10)
btnDelete.pack(pady=10)
btnDeleteBack.pack(pady=10)
dst.withdraw()

root.mainloop()
