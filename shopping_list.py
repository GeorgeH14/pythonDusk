import tkinter as tk

root = tk.Tk()
root.geometry("600x900")
root.title("Shopping List")
root.config(background="gray65")

user_shopping_list = []

def shopping_list_append():
    global user_shopping_list
    quantity = item_qty.get()
    user_shopping_list.append(user_input.get())

























##################################### GUI Elements #####################################

title_label = tk.Label(root, text="SHOPPING LIST", font=("Courier New",20))
title_label.place(x=200,y=50)


add_list_button = tk.Button(root, text="Add to list", font=("Courier New", 16))
add_list_button.place(x=230,y=250)

question_label = tk.Label(root, text="What would you like to add?", font=("Courier New",12))
question_label.place(x=170,y=100)

user_input = tk.Entry(root,font=("Courier New", 20))
user_input.place(x=80,y=200)

item_qty = tk.Spinbox(root, from_=0, to=99)
item_qty.place(x=450, y=205)

item_label= tk.Label(root,text="Item",font=("Courier New",12))
item_label.place(x=200,y=170)

qty_label =tk.Label(root,text="QTY",font=("Courier New",12))
qty_label.place(x=500,y=170)

shopping_list= tk.Listbox(root)
shopping_list.place(x=110,y=500, width=400,height=300)




































































root.mainloop()