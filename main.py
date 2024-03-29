from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox

def main():
    root = Tk()
    root.title("PROJECT MANAGER")
    w = 1350
    h = 400
    root.geometry(f'{w}x{h}+{1}+{150}')
    root.config(bg='maroon')
    root.resizable(False, False)

    conn = sqlite3.connect('Memberlist.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS memberlist (
                  ID_NUMBER,
                  NAME,
                  STATUS,
                  TASK,
                  PROJECT_CODE
                  )""")

    c.execute("""CREATE TABLE IF NOT EXISTS projectlist (
                  PROJECT_CODE,
                  PROJECT
                  )""")
    c.execute("""CREATE TABLE IF NOT EXISTS tasklist (
                  TASK_NAME,
                  TASK_STATUS
                  )""")

    def filled_table():
        tree.delete(*tree.get_children())
        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()
        c.execute("""SELECT ID_NUMBER, NAME, STATUS, TASK, projectlist.PROJECT_CODE, projectlist.PROJECT FROM memberlist
                      INNER JOIN projectlist ON projectlist.PROJECT_CODE = memberlist.PROJECT_CODE;""")

        records = c.fetchall()

        for i in records:
            tree.insert('', 'end', value=i)

    def pclist():
        conn = sqlite3.connect("Memberlist.db")
        c = conn.cursor()
        c.execute('''SELECT PROJECT_CODE FROM projectlist''')
        result = c.fetchall()
        result = [i[0] for i in result]
        return result

    def pnlist():
        conn = sqlite3.connect("Memberlist.db")
        c = conn.cursor()
        c.execute('''SELECT PROJECT FROM projectlist''')
        result = c.fetchall()
        result = [i[0] for i in result]
        return result

    def tclist():
        conn = sqlite3.connect("Memberlist.db")
        c = conn.cursor()
        c.execute('''SELECT TASK_NAME FROM tasklist''')
        result = c.fetchall()
        result = [i[0] for i in result]
        return result
    def register():
        if E1.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif E2.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif task.get() == 'SELECT TASK':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif PROJECT_CODE.get() == 'SELECT PROJECT CODE':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif PROJECT_CODE.get() not in pclist():
            messagebox.showinfo("OH NO!", "PLEASE ENTER Project Name")
            reg_projectcode.insert(0, PROJECT_CODE.get())
            print(pclist())

        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()
        c.execute("INSERT INTO memberlist VALUES(:ID_NUMBER, :NAME, :status,:task,:PROJECT_CODE)",
                  {
                      'ID_NUMBER': E1.get(),
                      'NAME': E2.get(),
                      'status': status.get(),
                      'task': task.get(),
                      'PROJECT_CODE': PROJECT_CODE.get()
                  })

        conn.commit()
        if PROJECT_CODE.get() in pclist():
            messagebox.showinfo("REGISTRATION INFORMATION", "YEHEY! YOU JUST GOT REGISTERED!")
        conn.close()

        filled_table()

        E1.delete(0, END)
        E2.delete(0, END)
        status.set("SELECT STATUS")
        task.set("SELECT TASK")
        PROJECT_CODE.set("SELECT PROJECT CODE")

    def project_reg():
        if reg_projectcode.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif reg_project.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()

        c.execute("INSERT INTO projectlist VALUES(:PROJECT_CODE, :COURSE)",
                  {
                      'PROJECT_CODE': reg_projectcode.get(),
                      'COURSE': reg_project.get()
                  })

        conn.commit()
        messagebox.showinfo("PROJECT REGISTRATION", "YEHEY! PROJECT CREATED!")
        conn.close()

        filled_table()

        PROJECT_CODE['values'] = pclist()
        root_projectcode['values'] = pclist()
        edlt_projectcode['values'] = pclist()
        edlt_project['values'] = pnlist()


        reg_projectcode.delete(0, END)
        reg_project.delete(0, END)

    def reg_task():
        if reg_taskname.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif reg_taskstatus.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()

        c.execute("INSERT INTO tasklist VALUES(:TASK_NAME, :TASK_STATUS)",
                  {
                      'TASK_NAME': reg_taskname.get(),
                      'TASK_STATUS': reg_taskstatus.get()
                  })

        conn.commit()
        messagebox.showinfo("TASK REGISTRATION", "YEHEY! TASK CREATED!")
        conn.close()

        filled_table()

        task_name['values'] = tclist()
        root_taskname['values'] = tclist()
        edlt_taskname['values'] = tclist()
        edlt_taskstatus['values'] = tclist()

        reg_taskname.delete(0, END)
        reg_taskstatus.delete(0, END)

    def project_edit():
        if edlt_projectcode.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif edlt_project.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()
        data6 = edlt_projectcode.get()
        data7 = edlt_project.get()

        c.execute("UPDATE projectlist set PROJECT_CODE=?, PROJECT=?  WHERE PROJECT_CODE=? ",
                  (data6, data7, data6))

        conn.commit()
        messagebox.showinfo("PROJECT EDIT INFO", "YEHEY! PROJECT EDITED!")
        conn.close()

        filled_table()

        PROJECT_CODE['values'] = pclist()
        root_projectcode['values'] = pclist()

        edlt_projectcode['values'] = pclist()
        edlt_project['values'] = pnlist()

        edlt_projectcode.delete(0, END)
        edlt_project.delete(0, END)

    def project_list():
        top = Tk()
        top.title("PROJECT LIST")
        w = 370
        h = 250
        top.geometry(f'{w}x{h}+{970}+{380}')
        top.config(bg='maroon')
        top.resizable(False, False)

        def delete():
            selected_item = tree1.focus()

            if selected_item == "":
                messagebox.showwarning("ERROR!", "PLEASE SELECT INFORMATION TO DELETE")
                top.lift()
            else:
                if messagebox.askyesno("DELETE CONFIRMATION", "ARE YOU SURE?") == False:
                    return
                else:
                    messagebox.showinfo("DELETE CONFIRMATION", "DATA SUCCESSFULLY DELETED")
                    top.lift()
                    conn = sqlite3.connect("Memberlist.db")
                    c = conn.cursor()
                    for selected_item in tree1.selection():
                        c.execute("DELETE FROM projectlist WHERE PROJECT_CODE=?", (tree1.set(selected_item, '#1'),))
                        conn.commit()
                        tree1.delete(selected_item)
                    conn.close()

                    filled_table()

                    PROJECT_CODE['values'] = pclist()
                    root_projectcode['values'] = pclist()

                    edlt_projectcode['values'] = pclist()
                    edlt_project['values'] = pnlist()

                    top.lift()

        conn = sqlite3.connect("Memberlist.db")
        c = conn.cursor()
        c.execute("SELECT * FROM projectlist")
        projects = c.fetchall()

        Project_Dlt = Button(top, text="DELETE", font=("Lucida Console", 12, "bold"), command=delete)
        Project_Dlt.place(x=145, y=215)

        frm = Frame(top)
        frm.pack(side=LEFT, padx=0, pady=(0, 40))

        tree1 = ttk.Treeview(frm, columns=(1, 2), show="headings", height=9)
        tree1.pack()

        tree1.heading(1, text="PROJECT CODE", anchor=CENTER)
        tree1.column("1", minwidth=0, width=120)
        tree1.heading(2, text="PROJECT", anchor=CENTER)
        tree1.column("2", minwidth=0, width=245)

        for i in projects:
            tree1.insert('', 'end', value=i)

        top.mainloop()

    def task_edit():
        if edlt_task.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif edlt_status.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()

        c.execute("UPDATE tasklist set TASK_NAME=?, TASK_STATUS=?  WHERE TASK_NAME=? ",
                  (edlt_task.get(), edlt_status.get(), edlt_task.get()))

        conn.commit()
        messagebox.showinfo("TASK EDIT INFO", "YEHEY! COURSE EDITED!")
        conn.close()

        filled_table()

        TASK_NAME['values'] = tclist()
        root_taskname['values'] = tclist()

        edlt_task['values'] = tclist()


        edlt_task.delete(0, END)


    def task_list():
        top = Tk()
        top.title("TASK LIST")
        w = 370
        h = 250
        top.geometry(f'{w}x{h}+{970}+{380}')
        top.config(bg='maroon')
        top.resizable(False, False)

        def delete():
            selected_item = tree1.focus()

            if selected_item == "":
                messagebox.showwarning("ERROR!", "PLEASE SELECT INFORMATION TO DELETE")
                top.lift()
            else:
                if messagebox.askyesno("DELETE CONFIRMATION", "ARE YOU SURE?") == False:
                    return
                else:
                    messagebox.showinfo("DELETE CONFIRMATION", "DATA SUCCESSFULLY DELETED")
                    top.lift()
                    conn = sqlite3.connect("Memberlist.db")
                    c = conn.cursor()
                    for selected_item in tree1.selection():
                        c.execute("DELETE FROM tasklist WHERE TASK_NAME=?", (tree1.set(selected_item, '#1'),))
                        conn.commit()
                        tree1.delete(selected_item)
                    conn.close()

                    filled_table()

                    task_name['values'] = tclist()
                    root_taskname['values'] = tclist()

                    edlt_taskname['values'] = tclist()
                    edlt_taskstatus['values'] = tclist()

                    top.lift()

        conn = sqlite3.connect("Memberlist.db")
        c = conn.cursor()
        c.execute("SELECT * FROM tasklist")
        projects = c.fetchall()

        Project_Dlt = Button(top, text="DELETE", font=("Lucida Console", 12, "bold"), command=delete)
        Project_Dlt.place(x=145, y=215)

        frm = Frame(top)
        frm.pack(side=LEFT, padx=0, pady=(0, 40))

        tree1 = ttk.Treeview(frm, columns=(1, 2), show="headings", height=9)
        tree1.pack()

        tree1.heading(1, text="TASK NAME", anchor=CENTER)
        tree1.column("1", minwidth=0, width=120)
        tree1.heading(2, text="TASK STATUS", anchor=CENTER)
        tree1.column("2", minwidth=0, width=245)

        for i in projects:
            tree1.insert('', 'end', value=i)

        top.mainloop()

    def select():
        conn = sqlite3.connect('Memberlist.db')

        E3.delete(0, END)
        E4.delete(0, END)
        root_status.delete(0, END)
        root_task.delete(0, END)
        root_projectcode.delete(0, END)

        selected = tree.focus()
        values = tree.item(selected, 'values')

        E3.insert(0, values[0])
        E4.insert(0, values[1])
        root_status.insert(0, values[2])
        root_task.insert(0, values[3])
        root_projectcode.insert(0, values[4])

        conn.commit()
        conn.close()

    def update():
        if E3.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif E4.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_status.get() == 'SELECT STATUS':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_task.get() == 'SELECT TASK':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_projectcode.get() == 'SELECT PROJECT CODE':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()
        messagebox.showinfo("UPDATE INFORMATION", "YEHEY! DATA UPDATED")
        data1 = E3.get()
        data2 = E4.get()
        data3 = root_status.get()
        data4 = root_task.get()
        data5 = root_projectcode.get()

        selected = tree.selection()
        tree.item(selected, values=(data1, data2, data3, data4, data5))
        c.execute(
            "UPDATE memberlist set  ID_NUMBER=?, NAME=?, STATUS=?, TASK=?, PROJECT_CODE=?  WHERE ID_NUMBER=? ",
            (data1, data2, data3, data4, data5, data1))

        conn.commit()
        conn.close()
        filled_table()

        E3.delete(0, END)
        E4.delete(0, END)
        root_status.set("SELECT STATUS")
        root_task.set("SELECT TASK")
        root_projectcode.set("SELECT PROJECT CODE")

    def delete():
        selected_item = tree.focus()

        if selected_item == "":
            messagebox.showwarning("ERROR!", "PLEASE SELECT INFORMATION TO DELETE")

        else:
            if messagebox.askyesno("DELETE CONFIRMATION", "ARE YOU SURE?") == False:
                return
            else:
                messagebox.showinfo("DELETE CONFIRMATION", "DATA SUCCESSFULLY DELETED")
                conn = sqlite3.connect("Memberlist.db")
                c = conn.cursor()
                for selected_item in tree.selection():
                    c.execute("DELETE FROM memberlist WHERE ID_NUMBER=?", (tree.set(selected_item, '#1'),))
                    conn.commit()
                    tree.delete(selected_item)
                conn.close()

    def search():
        root1 = Tk()
        root1.title("MEMBER FOUND!")
        root1.geometry("1000x100")
        root1.config(bg='white')
        root1.resizable(False, False)

        conn = sqlite3.connect('Memberlist.db')
        c = conn.cursor()

        c.execute("""SELECT ID_NUMBER, NAME, status, task, projectlist.PROJECT_CODE, projectlist.COURSE FROM memberlist
                       INNER JOIN projectlist ON projectlist.PROJECT_CODE = memberlist.PROJECT_CODE WHERE ID_NUMBER=?""",
                  (E3.get(),))
        records = c.fetchall()

        frm = Frame(root1)
        frm.pack(side=LEFT, padx=5, pady=(0, 0))

        tree = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height=13)
        tree.pack()

        tree.heading(1, text="ID NUMBER", anchor=CENTER)
        tree.column("1", minwidth=0, width=150)
        tree.heading(2, text="NAME", anchor=CENTER)
        tree.heading(3, text="STATUS", anchor=CENTER)
        tree.column("3", minwidth=0, width=150)
        tree.heading(4, text="TASK", anchor=CENTER)
        tree.column("4", minwidth=0, width=150)
        tree.heading(5, text="PROJECT CODE", anchor=CENTER)
        tree.column("5", minwidth=0, width=150)
        tree.heading(6, text="COURSE", anchor=CENTER)

        for i in records:
            tree.insert('', 'end', value=i)

        if not records:
            root1.destroy()
            messagebox.showinfo("SEARCH INFORMATION", "MEMBER DOESN'T EXIST or ENTER ID NUMBER")

        root1.mainloop()

    # LABEL FRAMES
    Reg = LabelFrame(root, text="Member", width=360, height=200, bg="maroon", fg="white",
                     font=("Lucida Console", 8, "bold"), borderwidth=1, relief="groove")
    Reg.place(x=365, y=0)
    # Register Task Form
    Regtask = LabelFrame(root, text="Task", width=270, height=200, bg="maroon", fg="white",
                         font=("Lucida Console", 8, "bold"), borderwidth=1, relief="groove")
    Regtask.place(x=1075, y=0)
    Upd_Del = LabelFrame(root, text="Update/Delete", width=360, height=200, bg="maroon", fg="white",
                         font=("Lucida Console", 8, "bold"))
    Upd_Del.place(x=0, y=0)
    Project = LabelFrame(root, text="Project ", width=340, height=100, bg="maroon", fg="white",
                        font=("Lucida Console", 8, "bold"))
    Project.place(x=730, y=0)
    Project_Edlt = LabelFrame(root, text="Edit/Delete", width=340, height=100, bg="maroon", fg="white",
                             font=("Lucida Console", 8, "bold"))
    Project_Edlt.place(x=730, y=100)

    # REGISTRATION LABELS
    L1 = Label(root, text="ID NUMBER:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L1.place(x=368, y=35)
    L2 = Label(root, text="NAME:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L2.place(x=368, y=60)

    L4 = Label(root, text="TASK:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L4.place(x=368, y=90)
    L5 = Label(root, text="PROJECT CODE:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L5.place(x=368, y=115)

    # TASK FORM
    L6 = Label(root, text="TASK:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L6.place(x=1080, y=15)
    L7 = Label(root, text="STATUS:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L7.place(x=1080, y=55)


    # REGISTRATION ENTRIES
    E1 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E1.place(x=455, y=35)
    E2 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E2.place(x=415, y=60)

    PROJECT_CODE = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    PROJECT_CODE.set("SELECT PROJECT CODE")
    PROJECT_CODE['values'] = pclist()
    PROJECT_CODE.place(x=475, y=115)


    #TASK IN REGISTRATION
    task = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    task.set("SELECT TASK")
    task['values'] = tclist()
    task.place(x=460, y=90)

    #STATUS IN TASK FORM
    status = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    status.set("SELECT STATUS")
    status['values'] = ("Not Yet Started", "In Progress", "Done")
    status.place(x=1080, y=75)


    # BUTTONS
    Sel = Button(root, text="SELECT", font=("Lucida Console", 9, "bold"), command=select)
    Sel.place(x=165, y=15)
    Upd = Button(root, text="UPDATE", font=("Lucida Console", 9, "bold"), command=update)
    Upd.place(x=230, y=15)
    Del = Button(root, text="DELETE", font=("Lucida Console", 9, "bold"), command=delete)
    Del.place(x=295, y=15)
    Sea = Button(root, text="SEARCH", font=("Lucida Console", 9, "bold"), command=search)
    Sea.place(x=295, y=60)
    Reg = Button(root, text="REGISTER", font=("Lucida Console", 9, "bold"), command=register)
    Reg.place(x=640, y=170)
    Project_Reg = Button(root, text="REGISTER", font=("Lucida Console", 9, "bold"), command=project_reg)
    Project_Reg.place(x=735, y=75)
    Project_Edt = Button(root, text="EDIT", font=("Lucida Console", 9, "bold"), command=project_edit)
    Project_Edt.place(x=845, y=175)
    Project_Lst = Button(root, text="PROJECT LIST", font=("Lucida Console", 9, "bold"), command=project_list)
    Project_Lst.place(x=735, y=175)
    # Register Task Button
    task_Reg = Button(root, text="REGISTER", font=("Lucida Console", 9, "bold"), command=reg_task)
    task_Reg.place(x=1265, y=100)
    task_Lst = Button(root, text="TASK LIST", font=("Lucida Console", 9, "bold"), command=task_list)
    task_Lst.place(x=1085, y=175)

    conn = sqlite3.connect('Memberlist.db')
    c = conn.cursor()

    c.execute("""SELECT ID_NUMBER, NAME, STATUS, TASK, projectlist.PROJECT_CODE, projectlist.PROJECT FROM memberlist
              INNER JOIN projectlist ON projectlist.PROJECT_CODE = memberlist.PROJECT_CODE;""")

    records = c.fetchall()

    frm = Frame(root)
    frm.pack(side=LEFT, padx=5, pady=(200, 0))

    tree = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height=13)
    tree.pack()

    tree.heading(1, text="ID NUMBER", anchor=CENTER)
    tree.column("1", minwidth=0, width=200)
    tree.heading(2, text="NAME", anchor=CENTER)
    tree.column("2", minwidth=0, width=270)
    tree.heading(3, text="STATUS", anchor=CENTER)
    tree.column("3", minwidth=0, width=200)
    tree.heading(4, text="TASK", anchor=CENTER)
    tree.column("4", minwidth=0, width=200)
    tree.heading(5, text="PROJECT CODE", anchor=CENTER)
    tree.column("5", minwidth=0, width=200)
    tree.heading(6, text="PROJECT", anchor=CENTER)
    tree.column("6", minwidth=0, width=270)

    for i in records:
        tree.insert('', 'end', value=i)

    # UPDATE AND DELETE ENTRIES
    E3 = Entry(root, bd=2, width=27, font=("Lucida Console", 8))
    E3.place(x=160, y=40)
    E4 = Entry(root, bd=2, width=27, font=("Lucida Console", 8))
    E4.place(x=50, y=75)

    root_status = ttk.Combobox(root, width=25, font=("Lucida Console", 8))
    root_status.set("SELECT STATUS")
    root_status['values'] = ("Not Yet Started", "In Progress", "Done")
    root_status.place(x=70, y=100)

    root_task = ttk.Combobox(root, width=25, font=("Lucida Console", 8))
    root_task.set("SELECT TASK")
    root_task['values'] = tclist()
    root_task.place(x=100, y=125)

    root_projectcode = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_projectcode.set("SELECT PROJECT CODE")
    root_projectcode['values'] = pclist()
    root_projectcode.place(x=120, y=150)

    # UPDATE AND DELETE LABELS
    L7 = Label(root, text="ID NUMBER TO FIND:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L7.place(x=5, y=38)
    L8 = Label(root, text="NAME:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L8.place(x=5, y=75)
    L9 = Label(root, text="STATUS:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L9.place(x=5, y=100)
    L10 = Label(root, text="TASK:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L10.place(x=5, y=125)
    L11 = Label(root, text="PROJECT CODE:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L11.place(x=5, y=150)

    #PROJECT REGISTRATION LABELS
    L12 = Label(root, text="PROJECT CODE:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L12.place(x=735, y=25)
    L13 = Label(root, text="PROJECT NAME:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L13.place(x=735, y=50)

    # PROJECT REGISTRATION ENRTRIES
    reg_projectcode = Entry(root, bd=2, width=27, font=("Lucida Console", 8))
    reg_projectcode.place(x=845, y=25)
    reg_project = Entry(root, bd=2, width=27, font=("Lucida Console", 8))
    reg_project.place(x=800, y=50)

    # PROJECT EDIT/DELETE LABELS
    L14 = Label(root, text="PROJECT CODE:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L14.place(x=735, y=125)
    L15 = Label(root, text="PROJECT:", bg="maroon", fg="white", font=("Lucida Console", 8, "bold"))
    L15.place(x=735, y=150)

    ##PROJECT EDIT/DELETE ENRTRIES
    edlt_projectcode = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    edlt_projectcode.set("SELECT PROJECT CODE")
    edlt_projectcode['values'] = pclist()
    edlt_projectcode.place(x=843, y=125)

    edlt_project = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    edlt_project['values'] = pnlist()
    edlt_project.place(x=810, y=150)

    # TASK REGISTRATION ENTRIES
    reg_taskname = Entry(root, bd=2, width=27, font=("Lucida Console", 8))
    reg_taskname.place(x=1080, y=35)

    reg_taskstatus = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    reg_taskstatus.set("SELECT STATUS")
    reg_taskstatus['values'] = ("Not Yet Started", "In Progress", "Done")
    reg_taskstatus.place(x=1080, y=75)

    conn.commit()
    conn.close()

    root.mainloop()

main()
