from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys

from alchemy.controller import Controller


def main(team_name, ip_address, log_file_name, recipes_file_name):
    controller = Controller(team_name=team_name, recipes=recipes_file_name, start_log_file_name=log_file_name, client=ip_address)

    # Root window
    root = Tk()
    root.title("Alchemy 1.3.0 - " + team_name)
    root.geometry("700x500")
    root.wm_attributes("-topmost", True)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Frame for content
    content = ttk.Frame(root)
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    content.columnconfigure(0, weight=2)
    content.columnconfigure(1, weight=1)
    content.columnconfigure(3, weight=1)
    content.rowconfigure(0, weight=1)

    # Frame for left side boxes
    crafting = ttk.Frame(content, padding=15)
    crafting.grid(column=0, row=0, pady=3)

    # Message Box
    messageframe = ttk.Frame(crafting, borderwidth=2, width=25)
    messageframe.grid(column=0, row=0, pady=12) 
    
    messagelabel = ttk.Label(messageframe, justify=CENTER)
    messagelabel['text'] = "Vítejte!"
    messagelabel.grid(column=0, row=0, pady=3, sticky=(N, S, W, E))

    # Craft Items Box
    craftframe = ttk.LabelFrame(crafting, text="Testovací laboratoř")
    craftframe.grid(column=0, row=2, pady=8)

    craftitem1var = StringVar()
    craftitem1 = ttk.Entry(craftframe, textvariable=craftitem1var)
    craftitem1.grid(column=0, row=0)
    craftitem1.bind('<Return>', lambda event: craft(controller, craftitem1var, craftitem2var, itemstext, triedtext, messagelabel))

    craftitem2var = StringVar()
    craftitem2 = ttk.Entry(craftframe, textvariable=craftitem2var)
    craftitem2.grid(column=0, row=1)
    craftitem2.bind('<Return>', lambda event: craft(controller, craftitem1var, craftitem2var, itemstext, triedtext, messagelabel))

    craftbutton = ttk.Button(craftframe, text="Experimentovat", \
        command=lambda: craft(controller, craftitem1var, craftitem2var, itemstext, triedtext, messagelabel))
    craftbutton.grid(column=0, row=2)
    craftbutton.bind('<Return>', lambda event: craft(controller, craftitem1var, craftitem2var, itemstext, triedtext, messagelabel))

    # Text field for inventory
    itemsscroll = Scrollbar(content)
    itemsscroll.grid(column=2, row=0, sticky=(N, S, W, E))

    itemstext = Text(content, width=30, height=30, yscrollcommand=itemsscroll.set)
    itemstext['state'] = 'disabled'
    itemstext.grid(column=1, row=0, sticky=(N, S, W, E))
    update_items_text(controller, itemstext)

    itemsscroll.config(command=itemstext.yview)

    # Text field for tried combinations
    triedscroll = Scrollbar(content)
    triedscroll.grid(column=4, row=0, sticky=(N, S, W, E))

    triedtext = Text(content, width=30, height=30, yscrollcommand=triedscroll.set)
    triedtext.grid(column=3, row=0, sticky=(N, S, W, E))
    update_tried_text(controller, triedtext)

    triedscroll.config(command=triedtext.yview)

    # Binding for server_check
    root.bind_all('<Return>', lambda event: check_server(controller, messagelabel, itemstext))
    root.bind_all('<Button-1>', lambda event: check_server(controller, messagelabel, itemstext))
    root.bind_all('<Control-F11>', lambda event: toggle_full_screen(root))

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(controller, root))
    root.mainloop()

def update_message(messagelabel, text):
    messagelabel['text'] = text

def update_tried_text(controller, triedtext):
    triedtext['state'] = 'normal'
    triedtext.delete('1.0', 'end')
    triedtext.insert('1.0', 'Zkoušené kombinace: \n')
    triedtext.insert('end', '\n'.join(controller.get_tried_combinations()))
    triedtext['state'] = 'disabled'

def update_items_text(controller, itemstext):
    itemstext['state'] = 'normal'
    itemstext.delete('1.0', 'end')
    itemstext.insert('1.0', controller.get_inventory_as_list())
    itemstext['state'] = 'disabled'

def craft(controller, craftitem1var, craftitem2var, itemstext, triedtext, messagelabel):
    item1 = craftitem1var.get()
    item2 = craftitem2var.get()

    success, result = controller.experiment(item1, item2)

    if success:
        update_items_text(controller, itemstext)
        update_tried_text(controller, triedtext)
        message_text = "Vytvořili jste: " + ", ".join(result)
        update_message(messagelabel, message_text)
    else:
        if not result:
            message_text = "Tyto suroviny neznáte"
            update_message(messagelabel, message_text)
        else:
            message_text = "Chybí: \n" + '\n'.join([miss_item + ': ' + str(miss_count) for (miss_item, miss_count) in result.items()])
            update_message(messagelabel, message_text)

def check_server(controller, messagelabel, itemstext):
    try:
        controller.check_server()
        update_items_text(controller, itemstext)
    except ConnectionError:
        update_message(messagelabel, "Spojení bylo přerušeno :(")

def toggle_full_screen(root):
    fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not fullscreen)

def on_closing(controller, root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        controller.log_inventory()
        root.destroy()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        team_name = sys.argv[1]
    else:
        team_name = input("Jméno týmu: ")
    
    if len(sys.argv) > 2:
        ip_address = sys.argv[2]
    else:
        ip_address = input("IP Adresa serveru (nechat prázdné pro localhost): ") or True   
        # Takes True iff input left empty

    if len(sys.argv) > 3:
        log_file_name = sys.argv[3]
    else:
        log_file_name = input("Jméno souboru logu (nechat prázdné pro start nové hry): ")

    if len(sys.argv) > 4:
        recipes_file_name = sys.argv[4]
    else:
        recipes_file_name = "recipes.txt"
    main(team_name, ip_address, log_file_name, recipes_file_name)