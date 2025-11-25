#shopping list
#add delete view save load items

shopping_list=[]

def add_items():
    while True:
        item = input('Please input an item\n')
        shopping_list.append(item)
        print(f'Your shopping list is:\n {shopping_list}')
        repeat = input('Would you like to add more? y/n\n')
       
        if repeat == 'n':
            print(f'Your final shopping list:\n{shopping_list}')
            break
            
        elif repeat == 'y':
            continue

def delete_items():
    if not shopping_list:
        print('Your list is empty')
        return
    
    print("Current Shopping List:\n")
    for i, item in enumerate(shopping_list):
        print(f'[{i + 1}]{item}')

def menu_options():
    
        print('-----Welcome to the Shopping List-----')
        print('1.   Add Item/s')
        print('2.   Delete Item/s')
        print('3.   View List')
        print('4.   Save List')
        print('5.   Load List')
        print('6.   Exit Program')

def menu():
    while True:
        menu_options()   



    menu_choice = input('Choose an option')
    menu_choice = int(menu_choice)
    if menu_choice == 1:
        add_items()
        
    
    if menu_choice == 2:
       delete_items()
       pass

    if menu_choice == 3:
        # view_list()
        pass

    if menu_choice == 4:
        # save_list()
        pass

    if menu_choice == 5:
        # load_list()
        pass

    if menu_choice == 6:
        # exit_program()
        pass
    
    
    
    
    
    






















menu()
