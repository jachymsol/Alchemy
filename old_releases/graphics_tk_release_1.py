from tkinter import *
from tkinter import ttk

from alchemy.controller import Controller


def main():
    controller = Controller("recipes_testovani.txt")

    # Root window
    root = Tk()
    root.title("Alchemy 1.1.0")
    root.geometry("700x500")
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

    # Add Item Box
    addframe = ttk.LabelFrame(crafting, text="Přidat suroviny")
    addframe.grid(column=0, row=1, pady=8)

    additemvar = StringVar()
    # additem = Entry(addframe, textvariable=additemvar, justify=CENTER)
    additem = ttk.Combobox(addframe, values=('kamen', 'voda', 'vzduch', 'zeme'), textvariable=additemvar, justify=CENTER, width=15)
    # additem.state(['readonly'])
    additem.grid(column=0, row=0)
    additem.bind('<Return>', lambda event: add(controller, additemvar, addcountvar, itemstext, messagelabel))

    addcountvar = StringVar()
    addcount = Spinbox(addframe, from_=1, to=10000, textvariable=addcountvar, justify=RIGHT, width=4)
    addcount.grid(column=0, row=1)
    addcount.bind('<Return>', lambda event: add(controller, additemvar, addcountvar, itemstext, messagelabel))

    addbutton = ttk.Button(addframe, text="Přidat", \
        command=lambda: add(controller, additemvar, addcountvar, itemstext, messagelabel))
    addbutton.grid(column=0, row=2)
    addbutton.bind('<Return>', lambda event: add(controller, additemvar, addcountvar, itemstext, messagelabel))

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

    # Make Known Items Box
    makeframe = ttk.LabelFrame(crafting, text="Výroba známých věcí")
    makeframe.grid(column=0, row=3, pady=8)

    makeitemvar = StringVar()
    makeitem = ttk.Entry(makeframe, textvariable=makeitemvar)
    # makeitem = ttk.Combobox(makeframe, values=controller.get_inventory_items, textvariable=makeitemvar)
    # makeitem.state(['readonly'])
    makeitem.grid(column=0, row=0)
    makeitem.bind('<Return>', lambda event: make(controller, makeitemvar, makecountvar, itemstext, messagelabel))

    makecountvar = StringVar()
    makecount = Spinbox(makeframe, from_=1, to=100, textvariable=makecountvar, justify=RIGHT, width=4)
    makecount.grid(column=0, row=1)
    makecount.bind('<Return>', lambda event: make(controller, makeitemvar, makecountvar, itemstext, messagelabel))

    makebutton = ttk.Button(makeframe, text="Vyrobit", \
        command=lambda: make(controller, makeitemvar, makecountvar, itemstext, messagelabel))
    makebutton.grid(column=0, row=2)
    makebutton.bind('<Return>', lambda event: make(controller, makeitemvar, makecountvar, itemstext, messagelabel))

    # Text field for inventory
    itemsscroll = Scrollbar(content)
    itemsscroll.grid(column=2, row=0, sticky=(N, S, W, E))

    itemstext = Text(content, width=30, height=30, yscrollcommand=itemsscroll.set)
    itemstext.insert('1.0', 'Ještě nic nemáte... \n')
    itemstext['state'] = 'disabled'
    itemstext.grid(column=1, row=0, sticky=(N, S, W, E))

    itemsscroll.config(command=itemstext.yview)

    # Text field for tried combinations
    triedscroll = Scrollbar(content)
    triedscroll.grid(column=4, row=0, sticky=(N, S, W, E))

    triedtext = Text(content, width=30, height=30, yscrollcommand=triedscroll.set)
    triedtext.insert('1.0', 'Zkoušené kombinace: \n')
    triedtext['state'] = 'disabled'
    triedtext.grid(column=3, row=0, sticky=(N, S, W, E))

    triedscroll.config(command=triedtext.yview)

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

def add(controller, additemvar, addcountvar, itemstext, messagelabel):
    item = additemvar.get()
    count = addcountvar.get()

    controller.add_item(item, int(count))
    update_items_text(controller, itemstext)

    message_text = "Přidáno " + count + "x " + item
    update_message(messagelabel, message_text)

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

def make(controller, makeitemvar, makecountvar, itemstext, messagelabel):
    item = makeitemvar.get()
    count = makecountvar.get()

    success, missing = controller.craft_discovered(item, int(count))

    if success:
        update_items_text(controller, itemstext)
        message_text = "Vytvořeno " + count + "x " + item
        update_message(messagelabel, message_text)
    else:
        message_text = "Chybí: \n" + '\n'.join([miss_item + ': ' + str(miss_count) for (miss_item, miss_count) in missing.items()])
        update_message(messagelabel, message_text)

if __name__ == "__main__":
    main()
