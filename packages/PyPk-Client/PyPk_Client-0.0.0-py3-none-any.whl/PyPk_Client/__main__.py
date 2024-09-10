import socketio
import tkinter
from tkinter import ttk
import ttkbootstrap as tb
import socket
import pickle

def reset_db():
    sio.emit('DbRst')
    sio.emit('requestDatabaseFetch')

class Lbl:
    def __init__(self, Master, text : str, col : int, row : int):
        self.lbl = tkinter.Label(Master, text=text)
        self.lbl.grid(column=col, row=row, padx=20, pady=20)

class Ent:
    def __init__(self, Master, col : int, row : int):
        self.ent = tkinter.Entry(Master)
        self.ent.grid(column=col, row=row, padx=20, pady=20)
    def __getitem__(self, index):
        if index == 'GET':
            return self.ent.get()

class Spn:
    def __init__(self, Masterry, col : int, row : int, _from : int, to_ : int):
        self.spn = tb.Spinbox(Masterry, from_=_from, to=to_)
        self.spn.grid(column=col, row=row, padx=20, pady=20)
    def __getitem__(self, index):
        if index == 'GET':
            return int(self.spn.get())

class Name:
    def __init__(self, Master):
        Lbl(Master, "Name", 0, 0)
        self.entry = Ent(Master, 0, 1)
    def __repr__(self) -> str:
        return self.entry['GET']

class Age:
    def __init__(self, Master):
        Lbl(Master, "Age", 1, 0)
        self.spnb = Spn(Master, 1, 1, 18, 25)
    def __repr__(self):
        return self.spnb['GET']

class LearningIn:
    def __init__(self, Master):
        Lbl(Master, "Learning In/Major", 2, 0)
        self.entr = Ent(Master, 2, 1)
    def __repr__(self):
        return self.entr['GET']

class FloorNum:
    def __init__(self, Master):
        Lbl(Master, "Floor Number", 3, 0)
        self.spnb = Spn(Master, 3, 1, 1, 6)
    def __repr__(self):
        return self.spnb['GET']

class Grade:
    def __init__(self, Master):
        Lbl(Master, "Grade", 5, 0)
        self.spnb = Spn(Master, 5, 1, 1, 100)

class Year:
    def __init__(self, Master):
        Lbl(Master, "Year", 4, 0)
        self.spnb = Spn(Master, 4, 1, 1, 4)
    def __repr__(self):
        return self.spnb['GET']

class DbInsert:
    def __init__(self):
        self.win = tb.Window("New Database entry")

        self.ne = Name(self.win)
        self.ag = Age(self.win)
        self.ln = LearningIn(self.win)
        self.fm = FloorNum(self.win)
        self.yr = Year(self.win)
        self.ge = Grade(self.win)

        self.btn = tkinter.Button(self.win, text="Upload to Server", padx=20, pady=35, command=self.dbinsert)
        self.btn.grid(column=6, row=0)

        self.win.mainloop()
    def dbinsert(self):
        listy = [
            self.ne.entry['GET'],
            self.ag.spnb['GET'],
            self.ln.entr['GET'],
            self.fm.spnb['GET'],
            self.yr.spnb['GET'],
            self.ge.spnb['GET']
        ]
        nlisty = pickle.dumps(listy)
        sio.emit("DbInsert", nlisty)
        sio.emit("requestDatabaseFetch")
        self.win.destroy()
def IPv4():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

sio = socketio.Client()

@sio.event
def connect():
    pass

@sio.event
def disconnect():
    sio.emit("disconnect")

def send_dt():
    sio.emit("DbInsert", ["hassan", 9, "python", 1, 4, 100])

@sio.event
def DatabaseFetchTree(msg):
    dbt.delete(*dbt.get_children())
    print(msg)
    for count, value in enumerate(msg):
        dbt.insert(parent='', index='end', iid=count, text='', values=(value[0], value[1], value[2], value[3], value[4], value[5], value[5]))

nickname = input("Give yourself a nickname\n")

port = IPv4()

sio.connect(f'http://{port}:5000')

sio.emit('nnHello', nickname)

root = tb.Window(themename="solar")
root.title("PyPK Client Database Contents")

menu = tkinter.Menu(root)
CommandsMenu = tkinter.Menu(menu)
menu.add_cascade(menu=CommandsMenu, label="Commands")
CommandsMenu.add_command(label="Add a student to the database", command=DbInsert)
CommandsMenu.add_command(label="Reset Database", command=reset_db)

dbt = ttk.Treeview(root)

dbt['columns'] = ("Name", "Age", "Major", "Floorn", "year", "grade")

dbt.column("#0", minwidth=0, width=0, stretch=False)
dbt.column("Name", minwidth=120, anchor="center")
dbt.column("Age", minwidth=120, anchor="center")
dbt.column("Major", minwidth=120, anchor="center")
dbt.column("Floorn", minwidth=120, anchor="center")
dbt.column("year", minwidth=120, anchor="center")
dbt.column("grade", minwidth=120, anchor="center")

dbt.heading("#0", text="", anchor="w")
dbt.heading("Name", text="Name")
dbt.heading("Age", text="Age")
dbt.heading("Major", text="Studying in")
dbt.heading("Floorn", text="Floor Number")
dbt.heading("year", text="Year")
dbt.heading("grade", text="Grade")

sio.emit("requestDatabaseFetch")

dbt.pack()

root.configure(menu=menu)
root.mainloop()