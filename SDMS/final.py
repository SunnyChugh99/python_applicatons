from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import ImD

# # Create the connection object
# myconn = mysql.connector.connect(host="localhost", user="root", passwd="google")
#
# # printing the connection object
# print(myconn)



root= Tk()
root.geometry("800x537+100+100")
root.title("STUDENT DATABASE MANAGEMENT")

def exit():
    ans = messagebox.askyesno("EXIT","Are you sure you want to exit?")
    if ans:
        quit()

#creating a new window for adding data
def put_addwin():
    add = Toplevel(root)
    add.geometry("500x400+200+100")
    add.title("ADD")
    add.configure(bg='beige')

    namelabel = Label(add, text="Enter Name", height=1, width=15)
    namelabel.pack()
    namelabel.place(x=50, y=50)
    namelabel.configure(bg='grey',fg='black')

    nameent = Entry(add)
    nameent.pack()
    nameent.place(x=200, y=50)

    rnolabel = Label(add, text="Enter Roll No.", height=1, width=15)
    rnolabel.pack()
    rnolabel.place(x=50, y=100)
    rnolabel.configure(bg='grey', fg='black')

    rnoent = Entry(add)
    rnoent.pack()
    rnoent.place(x=200, y=100)

    emaillabel = Label(add, text="Enter email id", height=1, width=15)
    emaillabel.pack()
    emaillabel.place(x=50, y=150)
    emaillabel.configure(bg='grey', fg='black')

    emailentry = Entry(add)
    emailentry.pack()
    emailentry.place(x=200, y=150)

    nolabel = Label(add, text="Enter phone number", height=1, width=15)
    nolabel.pack()
    nolabel.place(x=50, y=200)
    nolabel.configure(bg='grey', fg='black')

    noentry = Entry(add)
    noentry.pack()
    noentry.place(x=200, y=200)

    doblabel = Label(add, text="DATE OF BIRTH")
    doblabel.pack()
    doblabel.place(x=50, y=250)
    doblabel.configure(bg='grey', fg='black')

    dobentry = Entry(add)
    dobentry.pack()
    dobentry.place(x=200, y=250)
#function for adding the entered data to the database
    def connect():
        con = None
        try:

            con = mysql.connector.connect(host="localhost", user="root", passwd="root@123456")
            cursor = con.cursor()
            #cursor.execute("CREATE DATABASE test")
            # printing the connection object

            s1 = nameent.get()
            if (s1 == ''):
                messagebox.showerror("Incomplete", 'Name is empty')
                return
            s2 = rnoent.get()
            t = s2.isdigit()
            if (s2 == ''):
                messagebox.showerror("Incomplete", 'Rno is empty')
                return
            elif(t!=1):
                messagebox.showerror("Error","Roll number should be an integer")
                return
            s3 = emailentry.get()
            if(s3==''):
                messagebox.showerror("Incomplete","Email is empty")
                return
            s4 = noentry.get()
            if(s4==''):
                messagebox.showerror("Incomplete", "Phone number is empty")
                return

            elif(s4.isdigit()!=1):
                messagebox.showerror("Error", "Phone number should be a number")
                return
            s5 = dobentry.get()
            if(s5==''):
                messagebox.showerror("Incomplete","Date of birth is empty")
                return

            rno = int(rnoent.get())
            name =nameent.get()
            email =emailentry.get()
            phone=int(noentry.get())
            dob =dobentry.get()

            sql = "insert into test.studentm values('%d','%s','%s','%s','%s')"
            args = (rno, name, email, phone, dob)
            cursor.execute(sql%args)
            con.commit()
            msg = str(cursor.rowcount) + "entry inserted"
            messagebox.showinfo("Success", msg)
        except Exception as e:
            msg = 'Issue' + str(e)
            messagebox.showerror('Issue', msg)
            con.rollback()
        finally:
            cursor.close()
            if con is not None:
                con.close()
            rnoent.delete(0, END)
            nameent.delete(0, END)
            emailentry.delete(0, END)
            noentry.delete(0, END)
            dobentry.delete(0, END)

    savebutton=Button(add,text="SAVE",height=2,width=8,command=connect)
    savebutton.pack()
    savebutton.place(x=245,y=350)
    savebutton.configure(bg='grey', fg='black')

    def closeadd():
        add.withdraw()
        root.deiconify()

    backbutton=Button(add,text="<- BACK",height=2,width=8,command=closeadd)
    backbutton.pack()
    backbutton.place(x=50,y=350)
    backbutton.configure(bg='grey', fg='black')
    add.deiconify()
    root.withdraw()
    add.protocol("WM_DELETE_WINDOW", exit)
    return add

def put_viewwin():
    view = Toplevel(root)
    view.geometry("500x400+200+100")
    view.title("VIEW")
    view.configure(bg='grey')
    #to add scrollbar in the window
    stData = scrolledtext.ScrolledText(view,width=500, height=100)
    stData.pack()
    con = None
    try:
        con = mysql.connector.connect(host="localhost", user="root", passwd="root@123456")
        cursor = con.cursor()
        #for the database be able to write in the view window
        #stData.config(state=NORMAL)
        sql = "select * from test.studentm"
        cursor.execute(sql)
        rows = cursor.fetchall()
        data = ""
        for r in rows:
            rno = r[0]
            name = r[1]
            email = r[2]
            phone = r[3]
            dob = r[4]
            data = data + "Rno:" + str(rno) + " Name:" + str(name) + "\n" "Email:" + email + " Phone no.:" + str(phone) + "\n" "DOB: " +str(dob) + "\n\n"
        stData.insert(INSERT, data)
        #once the database is done writing the entries in the window the window should not be editable
        stData.config(state=DISABLED)
    except Exception as e:
        msg = 'Issue' + str(e)
        messagebox.showError('Issue', msg)
    finally:
        cursor.close()
        if con is not None:
            con.close()
    def closeview():
        view.withdraw()
        root.deiconify()


    backbutton = Button(view, text="<- BACK", height=2, width=8, command=closeview)
    backbutton.pack()
    backbutton.place(x=50, y=350)
    view.deiconify()
    root.withdraw()
    view.protocol("WM_DELETE_WINDOW", exit)
    return view


def put_updatewin():
    update = Toplevel(root)
    update.geometry("500x400+200+100")
    update.title("UPDATE")
    update.configure(bg='beige')

    namelabel = Label(update, text="ENTER NAME", height=1, width=15)
    namelabel.pack()
    namelabel.place(x=50, y=50)
    namelabel.configure(bg='grey', fg='black')

    nameent = Entry(update)
    nameent.pack()
    nameent.place(x=200, y=50)

    rnolabel = Label(update, text="ENTER ROll NO.", height=1, width=15)
    rnolabel.pack()
    rnolabel.place(x=50, y=100)
    rnolabel.configure(bg='grey', fg='black')

    rnoent = Entry(update)
    rnoent.pack()
    rnoent.place(x=200, y=100)

    emaillabel = Label(update, text="Enter email id", height=1, width=15)
    emaillabel.pack()
    emaillabel.place(x=50, y=150)
    emaillabel.configure(bg='grey', fg='black')

    emailentry = Entry(update)
    emailentry.pack()
    emailentry.place(x=200, y=150)

    nolabel = Label(update, text="Enter phone number", height=1, width=15)
    nolabel.pack()
    nolabel.place(x=50, y=200)
    nolabel.configure(bg='grey', fg='black')

    noentry = Entry(update)
    noentry.pack()
    noentry.place(x=200, y=200)

    doblabel = Label(update, text="DATE OF BIRTH")
    doblabel.pack()
    doblabel.place(x=50, y=250)
    doblabel.configure(bg='grey', fg='black')

    dobentry = Entry(update)
    dobentry.pack()
    dobentry.place(x=200, y=250)

    def connect():
        con = None
        try:
            con = mysql.connector.connect(host="localhost", user="root", passwd="root@123456")
            cursor = con.cursor()
            s1 = nameent.get()
            if (s1 == ''):
                messagebox.showerror("Incomplete", 'Name is empty')
                nameent.focus()
                return
            s2 = rnoent.get()
            t = s2.isdigit()
            if (s2 == ''):
                messagebox.showerror("Incomplete", 'Rno is empty')
                #rnoent.focus()
                return
            elif (t != 1):
                messagebox.showerror("Error", "Roll number should be an integer")
                return
            s3 = emailentry.get()
            if (s3 == ''):
                messagebox.showerror("Incomplete", "Email is empty")
                return
            s4 = noentry.get()
            if (s4 == ''):
                messagebox.showerror("Incomplete", "Phone number is empty")
                return
            elif (s4.isdigit() != 1):
                messagebox.showerror("Error", "Phone number should be a number")
                return
            s5 = dobentry.get()
            if (s5 == ''):
                messagebox.showerror("Incomplete", "Date of birth is empty")
                return
            rno = int(rnoent.get())
            name = nameent.get()
            email = emailentry.get()
            phone = int(noentry.get())
            dob = dobentry.get()

            sql = "update test.studentm set name='%s',email='%s',phone='%d',dob='%s'  where rno='%d'"
            args = (name, email, phone, dob, rno)
            cursor.execute(sql % args)
            con.commit()
            msg = str(cursor.rowcount) + " entry updated."
            messagebox.showinfo("Success", msg)
        except Exception as e:
            msg = 'Issue' + str(e)
            messagebox.showerror('Issue', msg)
            con.rollback()
        finally:
            cursor.close()
            if con is not None:
                con.close()
            rnoent.delete(0, END)
            nameent.delete(0, END)
            emailentry.delete(0, END)
            noentry.delete(0, END)
            dobentry.delete(0, END)



    updtbutton = Button(update, text="UPDATE", height=2, width=8, command=connect)
    updtbutton.pack()
    updtbutton.place(x=245, y=350)
    updtbutton.configure(bg='grey', fg='black')

    def closeupdate():
        update.withdraw()
        root.deiconify()


    backbutton = Button(update, text="<- BACK", height=2, width=8, command=closeupdate)
    backbutton.pack()
    backbutton.place(x=50, y=350)
    backbutton.configure(bg='grey', fg='black')

    root.withdraw()
    update.deiconify()
    update.protocol("WM_DELETE_WINDOW", exit)
    return update



def put_delwin():
    delete = Toplevel(root)
    delete.geometry("300x300+200+100")
    delete.title("DELETE")
    delete.configure(bg='beige')

    rnolabel = Label(delete, text="ENTER ROll NO.", height=1, width=15)
    rnolabel.pack()
    rnolabel.place(x=25, y=50)
    rnolabel.configure(bg='grey', fg='black')

    rnoent = Entry(delete)
    rnoent.pack()
    rnoent.place(x=50, y=100)

    def connect():
        con = None
        try:
            con = mysql.connector.connect(host="localhost", user="root", passwd="root@123456")
            cursor = con.cursor()
            s1 = rnoent.get()
            t=s1.isdigit()
            if s1 == '':
                messagebox.showerror("Incomplete", 'Rno is empty')
                rnoent.focus()
                return
            elif t != 1:
                messagebox.showerror("Error", "Roll number should be an integer")
                return

            rno = int(rnoent.get())
            sql = "delete from test.studentm where rno='%d'"
            args = (rno)
            cursor.execute(sql % args)
            con.commit()
            msg = str(cursor.rowcount) + " entry deleted."
            messagebox.showinfo("Success", msg)
        except Exception as e:
            msg = 'Issue' + str(e)
            messagebox.showError('Issue', msg)
            con.rollback()
        finally:
            cursor.close()
            if con is not None:
                con.close()
        rnoent.delete(0, END)
        rnoent.focus()

    deletebutton = Button(delete, text="DELETE", height=2, width=8,command=connect)
    deletebutton.pack()
    deletebutton.place(x=150, y=200)

    deletebutton.configure(bg='grey', fg='black')

    def closedel():
        delete.withdraw()
        root.deiconify()


    backbutton = Button(delete,text="<- BACK", height=2, width=8, command=closedel)
    backbutton.pack()
    backbutton.place(x=50, y=200)
    backbutton.configure(bg='grey', fg='black')

    delete.deiconify()
    root.withdraw()
    delete.protocol("WM_DELETE_WINDOW", exit)
    return delete


# photo2=ImageTk.PhotoImage(Image.open("data.jpg"))
# panel2=Label(root,image=photo2)
# panel2.place(x=0,y=0)

addbutton=Button(root,text="ADD DATA",height=2,width=10,command=put_addwin)
addbutton.configure(bg='blue',fg='white')
addbutton.pack()
addbutton.place(x=20,y=50)

viewbutton=Button(root,text="VIEW",height=2,width=10,command=put_viewwin)
viewbutton.configure(bg='blue',fg='white')
viewbutton.pack()
viewbutton.place(x=20,y=150)

updatebutton=Button(root,text="UPDATE",height=2,width=10,command=put_updatewin)
updatebutton.configure(bg='blue',fg='white')
updatebutton.pack()
updatebutton.place(x=20,y=250)

delbutton=Button(root,text="DELETE",height=2,width=10,command=put_delwin)
delbutton.configure(bg='blue',fg='white')
delbutton.pack()
delbutton.place(x=20,y=350)


exitbutton=Button(root,text="EXIT",height=2,width=10,command=exit)
exitbutton.configure(bg='blue',fg='white')
exitbutton.pack()
exitbutton.place(x=20,y=450)


label = Label(root,text="STUDENT DATABASE MANAGEMENT",bg='blue',fg='white',font='18')
label.pack()
label.place(x=300,y=10)

root.protocol("WM_DELETE_WINDOW",exit)

root.mainloop()