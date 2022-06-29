from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys

from alchemy.server import Server

def main():
    server = Server()

    # Root window
    root = Tk()
    root.title("Alchemy Server 1.1.0")
    root.geometry("400x500")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Frame for content
    content = ttk.Frame(root)
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    content.columnconfigure(0, weight=1)

    # Title Label
    titlelabel = ttk.Label(content, justify=CENTER)
    titlelabel['text'] = "Alchemy Server"
    titlelabel.config(font=("Arial", 20))
    titlelabel.grid(column=0, row=0, pady=12)

    # Message Label
    messagelabel = ttk.Label(content, justify=CENTER)
    messagelabel['text'] = "Vítejte!"
    messagelabel.config(font=("Courier", 10))
    messagelabel.grid(column=0, row=1, pady=12)

    # Number of Items (Multiplicity) Box
    multiplicitylabel = ttk.Label(content, justify=CENTER)
    multiplicitylabel['text'] = "Počet surovin na žeton:"
    multiplicitylabel.grid(column=0, row=2)

    multiplicityvar = StringVar()
    multiplicitybox = Spinbox(content, from_=1, to=10000, textvariable=multiplicityvar, justify=CENTER, width=8)
    multiplicitybox.grid(column=0, row=3)

    # Test Team Box
    teamframes = []
    teamitemvars = []
    teamitems = []
    teambuttons = []

    # Add Team Button
    addteambutton = ttk.Button(content, text="Přidat nový tým")
    addteambutton['command'] = lambda: add_team(server, root, content, teamframes, teamitemvars, teamitems, teambuttons, multiplicityvar, messagelabel)
    addteambutton.grid(column=0, row=1000, pady=12)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

def update_message(messagelabel, text):
    messagelabel['text'] = text

def add_item(server, teamnumber, item, multiplicityvar, messagelabel):
    count = multiplicityvar.get()
    data = ' '.join(['add', item, count, '\n'])

    try:
        server.send(int(teamnumber), bytes(data, 'utf-8'))
        update_message(messagelabel, "Posláno týmu " + str(teamnumber))
    except ConnectionError:
        update_message(messagelabel, "Spojení s týmem " + str(teamnumber) + " je přerušené")

def add_team(server, root, content, teamframes, teamitemvars, teamitems, teambuttons, multiplicityvar, messagelabel):
    teamnumber = len(teamframes)

    (result, teamname) = server.connect_new()

    if result:
        teamframes.append(ttk.LabelFrame(content, text="Tým " + str(teamnumber) + ": " + teamname))
        teamframes[-1].grid(column=0, row=teamnumber+4, pady=8)

        teambuttons.append(ttk.Button(teamframes[-1], text="Kamen"))
        teambuttons[-1]['command'] = lambda: add_item(server, teamnumber, "kamen", multiplicityvar, messagelabel)
        teambuttons[-1].grid(column=0, row=0)

        teambuttons.append(ttk.Button(teamframes[-1], text="Voda"))
        teambuttons[-1]['command'] = lambda: add_item(server, teamnumber, "voda", multiplicityvar, messagelabel)
        teambuttons[-1].grid(column=1, row=0)

        teambuttons.append(ttk.Button(teamframes[-1], text="Vzduch"))
        teambuttons[-1]['command'] = lambda: add_item(server, teamnumber, "vzduch", multiplicityvar, messagelabel)
        teambuttons[-1].grid(column=0, row=1)

        teambuttons.append(ttk.Button(teamframes[-1], text="Zeme"))
        teambuttons[-1]['command'] = lambda: add_item(server, teamnumber, "zeme", multiplicityvar, messagelabel)
        teambuttons[-1].grid(column=1, row=1)

        update_message(messagelabel, "Přidán tým "+str(teamnumber))
    else: 
        update_message(messagelabel, "Žádný tým nečeká na přidání")

def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

if __name__ == "__main__":
    main()