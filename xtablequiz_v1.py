import random as rand
import tkinter as tk

root=tk.Tk()
root.geometry("900x900")
root.title("KidsXtables")
root.config(background = "sky blue")

score = 0
ticked = tk.IntVar()

##########################################


def my_random_mult():
    global random_ans, ans_list
    score_box.config(text=score)
    
    
    random_no1 = rand.randint(1,12)
    random_no2 = rand.randint(1,12)
    random_ans = random_no1 * random_no2

    random_x.config(text=random_no1)
    random_y.config(text=random_no2)
        
    red_herring = rand.randint(1,144)
    blue_herring = rand.randint(1,144)
    ans_list = [red_herring, blue_herring, random_ans]
    rand.shuffle(ans_list)

    r1_button.config(text=ans_list[0])
    r2_button.config(text=ans_list[1])
    r3_button.config(text=ans_list[2])

    ticked.set(0)
    feedback_label.config(text="")
    

#########################################################################

def check_answer():
    global score
    choice = ticked.get()

    if choice == 0:
        feedback_label.config(text="Please Select an option!", fg="orange")
        return
    
    selected_value = ans_list[choice - 1]

    if selected_value == random_ans:
        score += 1
        feedback_label.config(text="Correct answer! Well done", fg="green")
    else:
        feedback_label.config(text=f"Incorrect! The answer was {random_ans}.", fg="red")

    

    if score == 10:
        feedback_label.config(text="You win! Congratulations!",fg="green")
        root.after(3000, root.destroy) # Closes program after 3000ms
    else:
        root.after(1500, my_random_mult)

    score_box.config(text=score)
        
################################################# UI Elements ########################

title_label = tk.Label(root,text="Test your times tables skills!",font=("Comic Sans MS",20))
title_label.place(x=250,y=50)

random_x = tk.Label(root,width=17,height=7,text="",font=("Comic Sans MS",15))
random_x.place(x=150,y=300)

random_y = tk.Label(root,width=17,height=7,text="",font=("Comic Sans MS",15))
random_y.place(x=550,y=300)

times_label = tk.Label(root,background="sky blue",text="X",font=("Comic Sans MS",40))
times_label.place(x=440,y=350)

score_box = tk.Label(root,text="",width=8,height=3,font=("Comic Sans MS",15))
score_box.place(x=750,y=750)

score_label = tk.Label(root,text="Score:",background="sky blue",font=("Comic Sans MS",15))
score_label.place(x=750,y=700)

feedback_label = tk.Label(root, text="", font=("Comic Sans MS", 15), bg="sky blue")
feedback_label.place(x=350,y=850)

ticked=tk.IntVar()

r1_button = tk.Radiobutton(root, text="",variable=ticked,value=1)
r1_button.place(x=450,y=600)
r2_button = tk.Radiobutton(root, text="",variable=ticked,value=2)
r2_button.place(x=450,y=650)
r3_button = tk.Radiobutton(root, text="",variable=ticked,value=3,)
r3_button.place(x=450,y=700)

check_button = tk.Button(root,text="Submit",font=("Comic Sans MS",15), command=check_answer)
check_button.place(x=400,y=750)

my_random_mult()

root.mainloop()