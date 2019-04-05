import os


python_path = 'venv\\Scripts\\python.exe'

menu_check = True
while menu_check:
    print('\nMenu:\n'
          '1) Read in data and store in database\n'
          '2) Perform machine learning experiments\n'
          '3) Output all experiment results\n'
          '4) Create, based on analysis of results, models and save to file\n'
          '5) Exit\n')
    selection = input('Select an option:')

    if selection == '1':
        print('This will take a long time to process and once started wipes all accounts from database!')
        check = input('Are you sure? (yes to proceed, anything else to go back)')
        if check == 'yes':
            os.system(python_path + ' read_store.py')
    elif selection == '2':
        os.system(python_path + ' machine_learning.py')
    elif selection == '3':
        os.system(python_path + ' read_results.py')
    elif selection == '4':
        os.system(python_path + ' create_save_models.py')
        print('Models created and saved to md_models directory')
    elif selection == '5':
        print('Goodbye\n')
        menu_check = False
    else:
        print('\nPlease enter a valid option')
