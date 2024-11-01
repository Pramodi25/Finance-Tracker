import json
from datetime import datetime
import sample_code_1

#---------------------------------------------------------------------------------------------------Global dictionary to store transactions
transactions = {}

#---------------------------------------------------------------------------------------------------File handling functions

def load_transactions():
    """Load transactions from the 'transactions.json' file."""
    try:
        with open('transactions.json', 'r') as file:
            transactions.update(json.load(file))
            print("Transactions loaded successfully.")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("transactions.json Not found or empty. Creating a new dictionary.")
        transactions.clear()
    return transactions


#--------------------------------------------------------------------------------------------------Save function for save details in transactions dictionary
def save_transactions():
    """Save the transactions dictionary to the 'transactions.json' file."""
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)#--------------------------------------------------Dump the transactions list to the file in a readable format


def read_bulk_transactions_from_file(filename):
    """Read bulk transactions from a text file and add them to the transactions dictionary.
    Args:
    - filename: The name of the file containing the bulk data.
    Returns:
    - transactions: The updated transactions dictionary."""
    
    try:
        with open(filename, 'r') as file: #-----------------------Open the file in read mode
            for line in file:
                parts = line.strip().split(',')#------------------Split the line into parts based on commas
                
                if len(parts) != 3: #-----------------------------Check if the line has exactly 3 parts
                    raise ValueError("Invalid data format in the file. Ensure each line has expense type, amount, and date separated by commas.")
                
                expense_type, amount, date = parts #--------------Extract the expense type, amount, and date from the parts
                amount = float(amount)
                
                if expense_type not in transactions: #------------If the expense type is not already in the transactions dictionary, create a new empty list for it
                    transactions[expense_type] = []
                    
                transactions[expense_type].append({'amount': amount, 'date': date})
                
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        
    except ValueError as e:
        print(f"Error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    return transactions
   

def get_valid_date():
    """Get a valid date from user input."""
    
    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        
        try:
            datetime.strptime(date, "%Y-%m-%d") #-----------------------------------------------------Try to convert input to datetime
            return date
        
        except ValueError:
            print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")


#------------------------------------------------------------------------------------------------------Feature implementations
def add_transaction():
    """Add a new transaction to the transactions dictionary."""
    
    #--------------------------------------------------------------------------------------------------Initialize transaction ID,amount,category,date
    id = len(transactions) + 1 
    amount = 0
    category = ""
    date = ""

    #---------------------------------------------------------------------------------------------------Get inputs from user
    category = input("Enter category: ")
    
    while True:
        try: 
            amount = float(input("Enter amount: "))
            break
        
        except ValueError:
            print("Invalid input. Please enter a valid number for the amount.")

    if category not in transactions: #----------------------------Check if category exists
        transactions[category] = []  #----------------------------Initialize category list
        
    date = get_valid_date()
    transactions[category].append({  #----------------------------Add transaction to category list
        "amount": amount,
        "date": date
    })
    
    print("Transaction added successfully.\n")
        

def view_transactions():
    """View all transactions in the transactions dictionary."""
    
    if len(transactions) != 0: #---------------------------------------------------------Check if there are any transactions in the dictionary
        print("All transactions.")
        category_count = 1
        
        #--------------------------------------------------------------------------------Iterate over each category and its transaction list
        for category, transaction_list in transactions.items():
            print("----------------------------------------")
            print(f"{category_count}) Expense type: {category}")
            
            count = 1
            category_count = category_count + 1
            
            #----------------------------------------------------------------------------Iterate over each transaction in the transaction list
            for transaction in transaction_list:
                if isinstance(transaction, dict):  #-------------------------------------Check if transaction is a dictionary
                    
                    print(f"\n{count}")
                    print(f"Amount  : {transaction.get('amount')}")
                    print(f"Date    : {transaction.get('date')}")
                    count = count + 1
                    
                else:
                    print(f"Invalid transaction format: {transaction}")
                    
        print("----------------------------------------")
        
    else:
        print("No transactions found to display.")



def update_transaction():
    """Update an existing transaction in the transactions list."""
    
    view_transactions() # Display all transactions for user reference
    global transactions
    if transactions: # Check if there are any transactions
        try:
            # Get the index of the category to update
            category_index = int(input("\nEnter the ID of the category to update: "))
            category_index = category_index - 1
            category_list = list(transactions.keys())

            # Check if the category index is valid
            if 0 <= category_index < len(category_list):
                category = category_list[category_index]
                transactions_list = transactions[category]
                
                # Get the index of the transaction within the category to update
                transaction_index = int(input(f"Enter the sub ID of the transaction in '{category}' to update: "))
                transaction_index = transaction_index - 1

                # Check if the transaction index is valid
                if 0 <= transaction_index < len(transactions_list):
                    transaction_details = transactions_list[transaction_index]
                    #print(transactions(14))
                    print(transaction_details)
                    #---------------------------------------------------------------------------------------------------------Get new transaction details from the user
                    choice = input("What do you want to change? (category -'c'/amount-'a'/date-'d'): ").lower()

                    if choice == "a":
                        new_amount = float(input("Enter the new amount: "))
                        transaction_details["amount"] = new_amount

                    elif choice == "d":
                        new_date = get_valid_date()
                        transaction_details["Enter new date"] = new_date

                    elif choice == "c":
                        new_category = input("Enter the new category: ")
                        updated_expenses = {}
                        
                        # Loop over the dictionary and update the key name
                        for key, value in transactions.items():
                            if key == category:
                                updated_expenses[new_category] = value
                            else:
                                updated_expenses[key] = value  # Copy other keys unchanged
                        transactions.clear()
                        transactions = updated_expenses
                        print(updated_expenses)
                        
                        #print(transactions)
                        #transactions.clear()
                        #transactions = updated_expenses
                        
                    else:
                        print("Invalid option!")
                        return

                    save_transactions()
                    
                    print("\nTransaction updated successfully.")
                    
                else:
                    print("\nInvalid transaction index.")
                    
            else:
                print("\nInvalid category index.")
                
        except ValueError:
            print("\nInvalid input. Please enter a valid index.")
            
    else:
        print("\nNo transactions yet.")



def delete_transaction():
    """Delete an existing transaction from the transactions list."""
    view_transactions()
    
    if transactions: #--------------------------------------------------------------------Check if there are any transactions
        try:
            #-----------------------------------------------------------------------------Ask user if they want to delete a full category or a transaction
            delete_choice = input("Do you want to delete a full category? (Y/N): ").upper()
            if delete_choice == "Y":
                
                #-------------------------------------------------------------------------Delete a full category
                category_index = int(input("Enter the ID of the category to delete: "))
                category_index = category_index - 1
                category_list = list(transactions.keys())

                 #------------------------------------------------------------------------Check if the category index is valid
                if 0 <= category_index < len(category_list):
                    category = category_list[category_index]
                    
                    del transactions[category]
                    
                    save_transactions()
                    
                    print("\nCategory deleted successfully.")
                    
                else:
                    print("\nInvalid category index.")
                    
            elif delete_choice == "N": #--------------------------------------------------Delete a transaction from a category
                category_index = int(input("Enter the ID of the category to delete transaction from: "))
                category_index = category_index - 1
                category_list = list(transactions.keys())
                
                if 0 <= category_index < len(category_list): #-----------------------------Check if the category index is valid
                    category = category_list[category_index]
                    transactions_list = transactions[category]

                    transaction_index = int(input(f"\nEnter the sub ID of the transaction in '{category}' to delete: "))
                    transaction_index = transaction_index - 1
                    
                    #----------------------------------------------------------------------Check if the transaction index is valid
                    if 0 <= transaction_index < len(transactions_list):
                        del transactions_list[transaction_index]
                        
                        save_transactions()
                        
                        print("\nTransaction deleted successfully.")
                        
                    else:
                        print("\nInvalid transaction index.")
                        
                else:
                    print("\nInvalid category index.")
                    
            else:
                print("\nInvalid choice. Please enter 'Y' or 'N'.")
                
        except ValueError:
            print("\nInvalid input. Please enter a valid integer index.")
            
    else:
        print("\nNo transactions found.")


def get_transaction_index(transactions, id):
    """Get the index of a transaction with a given ID."""
    for key, transaction in transactions.items():
        if key == id:
            return key
         
    #If no transaction was found, return None
    return None


def display_summary():
    """Display a summary of income, expense, and balance."""
    
    if not transactions:
        print("No transactions found.")
        return

    total_expenses = 0
    category_totals = {}

    #---------------------------------------------------------------------Calculate total expenses and category-wise totals
    for category, category_transactions in transactions.items():
        category_total = sum(transaction["amount"] for transaction in category_transactions)
        category_totals[category] = category_total
        total_expenses += category_total

    print()
    
    print("Total Expenses: Rs.", total_expenses)
    print("------------------------------")

    #----------------------------------------------------------------------Print category-wise expenses
    print("\n--Category wise Expenses--")
    for category, total in category_totals.items():
        print(f"\n{category}: Rs. {total}")

    print("")



def transactions_id_check(message):
    """Get a valid integer input from the user for a transaction ID."""
    while True:
        try:
            value = int(input(message))
            return value
        
        except ValueError:
            print("Invalid transaction ID! Please Enter valid transaction ID")
            


def search_transactions():
    """Search transactions by category."""
    
    category = input("Enter category to search: ")  #--------------------------------------------------------------------------------Ask the user to input the category they want to search for

     #-------------------------------------------------------------------------------------------------------------------------------Filter transactions by category
    filtered_transactions = {id: transaction for id, transaction in transactions.items() if transaction['category'] == category}

    if not filtered_transactions:
        print("No transactions found.")
        
    else:
        print(f"\nNumber of transactions found for category '{category}': {len(filtered_transactions)}")
        total_amount = sum(transaction['amount'] for transaction in filtered_transactions.values())
        print(f"Total amount for category '{category}': {total_amount}")
        
        for id, transaction in filtered_transactions.items():
            print("----------------------------------------")
            print(f"Transaction {id}")
            print(f"Amount: {transaction['amount']}")
            print(f"Category: {transaction['category']}")
            print(f"Date: {transaction['date']}")


#----------------------------------------------------------------------------------------------------------------Starting main program
def main_menu():
    """Display the main menu and handle user choices."""
    transactions.update(load_transactions())

    #------------------------------------------------------------------------------------------------------------Ask user for input method
    method = input("\nHow you gonna input data? \n For Bulk - B \n For get main menu - M \n For open GUI (You can also open GUI later from main menu) - G \n = ").upper()
    
    if method == "M":
        display_main_menu() #------------------------------------------------------------------------------------For get the main menu
        
    elif method == "B":
        bulk_file = input("Enter the file name(txt) : ")#--------------------------------------------------------for bulk method
        
        read_bulk_transactions_from_file(bulk_file)#------------------------------------------------------------call the bulk function
        display_main_menu()

    elif method == "G":
        sample_code_1.main()
        display_main_menu()
        
        
def display_main_menu():
    
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Search Transactions")
        print("7. Add another Bulk File")
        print("8. Open GUI")
        print("9. Exit")
        
        choice = input("Enter your choice: ")

        #If the user chose to add a transaction, add it and print the new summary
        if choice == '1':
            add_transaction()

        # If the user chose to view transactions, print them    
        elif choice == '2':
            view_transactions()

        # If the user chose to update a transaction, update it and print the new summary
        elif choice == '3':
            update_transaction()
            display_summary()

        # If the user chose to delete a transaction, delete it and print the new summary    
        elif choice == '4':
            delete_transaction()

        # If the user chose to display a summary, print it    
        elif choice == '5':
            display_summary()

        #If the user can search the transaction to view usign this option
        elif choice == '6':
            search_transactions()

        #If the user can get again to load the bulk data file   
        elif choice == '7':
            bulk_file = input("Enter the file name(txt) : ")
            read_bulk_transactions_from_file(bulk_file)

        elif choice == '8':
            sample_code_1.main()
            
        # If the user chose to exit, break the loop    
        elif choice == '9':
            print("Exiting program.")
            save_transactions()
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
