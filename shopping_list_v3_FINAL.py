import argparse

parser = argparse.ArgumentParser()    #Something that will process text and extract meaning from it

parser.add_argument("--name","-n",type=str,default=None,help="Enter the filename")

args = parser.parse_args()
print(args.name)

shopping_list = []

# ----- adding items -----
def add_items():
    print('\n----- Adding items -----')
    while True:
        new_item = input('Add item to shopping list:  ')

        shopping_list.append(new_item)
        print(f'Shopping List:{shopping_list}')

        repeat_add = input ('Would you like to add more items? y/n:  ')

        if repeat_add == 'n':
            print(f'Shopping List:{shopping_list}')
            break

        elif repeat_add != 'y':
            print('Invalid input. Returning to main menu')
            break

# ----- deleting items -----

def delete_items():
  if not shopping_list:
    print('List is empty. Returning to menu')
    return

  while True:
    print('\n----- Current Shopping List -----')
    for i, item in enumerate(shopping_list):
      print(f'[{i + 1}] {item}')

    try:
      deletion_choice = input('Enter the number of the item to delete it (0 to cancel): ')
      deletion_choice_int = int(deletion_choice)

      if deletion_choice_int == 0:
        print('Cancelling function')
        return

      deletion_index = deletion_choice_int - 1

      if 0 <= deletion_index < len(shopping_list):
        deleted_item = shopping_list.pop(deletion_index)
        print(f'Deleted *{deleted_item}* from list.')

        if not shopping_list:
          print('List is now empty.')
          return

        more_delete = input('Would you like to delete more? y/n:  ')
        if more_delete == 'n':
          print(f'Your shopping list is now:\n{shopping_list}')
          return

      else:
        print('Invalid number. Enter a number from the list or 0.')

    except ValueError:
      print('Invalid input. Enter a valid number.')

# ----- viewing list ------

def view_list():
  print('\n----- Current shopping list -----')
  if not shopping_list:
    print('Your list is currently empty.')
  else:
    for i, item in enumerate(shopping_list):
      print(f'[{i +1}]  {item}')
  print('------------------------------------')

# ----- saving list -----

def save_list():
  file_name = input('Enter file name for your list: ')
  try:
    with open(file_name, 'w') as f:
      for item in shopping_list:
        f.write(item + '\n')
    print(f'Saved list as *{file_name}*.')
  except Exception as e:
    print(f'An error occured when saving the list - {e}')

# ----- loading list -----

def load_list(file_name):
 
  loaded_list = []

  with open(file_name, 'r') as f:
    lines = f.readlines()

    for line in lines:
      item = line.strip()
      if item:
        loaded_list.append(item)

  print(f'Loaded from {file_name}.')
  return loaded_list

#----- clearing list -----
def clear_list():
      global shopping_list
      confirm = input('Are you sure? y/n:   ')
      if confirm == 'y':
        shopping_list = []
        print('Shopping list fully cleared')
      else:
        print('Clear cancelled.')
        return

# ----- MENU FUNCTIONS -----

def display_menu():
  print ('\n -----Shopping List Home-----')
  print ('1:  Add item(s) to list')
  print ('2:  Delete item(s) from list')
  print ('3:  View current list')
  print ('4:  Save current list')
  print ('5:  Load previous list')
  print ('6:  Clear list')
  print ('7.  Exit program')
  print ('-------------------------------')

def menu():
  global shopping_list
  while True:
    display_menu()
    choice = input('Enter your choice (1-7): ')

    try:
      choice_int = int(choice)

      if choice_int == 1:
        add_items()

      elif choice_int == 2:
        delete_items()

      elif choice_int == 3:
        view_list()

      elif choice_int == 4:
        save_list()

      elif choice_int == 5:
        file_name = input('Enter the name of the file you want to open: ')
        shopping_list = load_list(file_name)

      elif choice_int == 6:
        clear_list()  

      elif choice_int == 7:
        print ('Exiting program')
        break
      
      else:
        print('Invalid option. Please enter from numbers 1-6.')
    
    except ValueError:
      print('Invalid input. Try again')


if __name__ == '__main__':
  shopping_list = load_list(args.name)
  menu()