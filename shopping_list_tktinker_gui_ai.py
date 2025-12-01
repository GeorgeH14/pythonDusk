import tkinter as tk
from tkinter import messagebox, filedialog

shopping_list = []


# ---------------- ADD ITEM ----------------
def add_item():
    item = entry_item.get().strip()

    if not item:
        messagebox.showwarning("No input", "Please enter an item.")
        return

    shopping_list.append(item)
    update_listbox()
    entry_item.delete(0, tk.END)


# ---------------- DELETE ITEM ----------------
def delete_item():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No selection", "Please select an item to delete.")
        return

    index = selected[0]
    item = shopping_list[index]

    confirm = messagebox.askyesno("Confirm deletion", f"Delete '{item}'?")
    if confirm:
        shopping_list.pop(index)
        update_listbox()


# ---------------- CLEAR LIST ----------------
def clear_list():
    if messagebox.askyesno("Confirm", "Clear the entire shopping list?"):
        shopping_list.clear()
        update_listbox()


# ---------------- SAVE LIST ----------------
def save_list():
    if not shopping_list:
        messagebox.showinfo("Empty List", "Shopping list is empty — nothing to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if not file_path:
        return  # user cancelled

    try:
        with open(file_path, "w") as f:
            for item in shopping_list:
                f.write(item + "\n")
        messagebox.showinfo("Saved", f"List saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")


# ---------------- LOAD LIST ----------------
def load_list():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r") as f:
            lines = f.read().splitlines()

        shopping_list.clear()
        shopping_list.extend(lines)
        update_listbox()
        messagebox.showinfo("Loaded", f"Loaded list from:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")


# ---------------- UPDATE LISTBOX ----------------
def update_listbox():
    listbox.delete(0, tk.END)
    for item in shopping_list:
        listbox.insert(tk.END, item)


# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Shopping List Manager")
root.geometry("420x420")
root.resizable(False, False)

# --- Entry Frame ---
frame_entry = tk.Frame(root)
frame_entry.pack(pady=10)

entry_item = tk.Entry(frame_entry, width=30, font=("Arial", 14))
entry_item.pack(side=tk.LEFT, padx=5)

btn_add = tk.Button(frame_entry, text="Add Item", width=12, command=add_item)
btn_add.pack(side=tk.LEFT)

# --- Listbox ---
listbox = tk.Listbox(root, width=50, height=12, font=("Arial", 12))
listbox.pack(pady=10)

# --- Button Controls ---
frame_buttons = tk.Frame(root)
frame_buttons.pack()

btn_delete = tk.Button(frame_buttons, text="Delete Selected", width=15, command=delete_item)
btn_delete.grid(row=0, column=0, padx=5, pady=5)

btn_clear = tk.Button(frame_buttons, text="Clear List", width=15, command=clear_list)
btn_clear.grid(row=0, column=1, padx=5, pady=5)

btn_save = tk.Button(frame_buttons, text="Save List", width=15, command=save_list)
btn_save.grid(row=1, column=0, padx=5, pady=5)

btn_load = tk.Button(frame_buttons, text="Load List", width=15, command=load_list)
btn_load.grid(row=1, column=1, padx=5, pady=5)

# --- Exit Button ---
btn_exit = tk.Button(root, text="Exit", width=20, command=root.quit)
btn_exit.pack(pady=15)

root.mainloop()

