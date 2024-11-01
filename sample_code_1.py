import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime 

# Transaction class to represent a single transaction
class Transaction:
    def __init__(self, date, transaction_type, description, amount):
        self.date = date
        self.transaction_type = transaction_type
        self.description = description
        self.amount = amount
        
# FinanceTrackerGUI class for creating the graphical user interfaceclass FinanceTrackerGUI:
class FinanceTrackerGUI:  
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions("transactions.json") #------------------------------------------------------------Load transactions from a JSON file
        self.display_transactions(self.transactions)
        self.sort_column = None #------------------------------------------------------------------------------------------------Variable to store the column to sort by
        self.sort_reverse = False #-----------------------------------------------------------------------------------------------------Variable to store the sort order

    def create_widgets(self):
        '''Create all the widgets for the GUI'''
        
        '''Main title label''' 
        hellolabel = tk.Label(self.root, text="Welcome To Personal Finance Tracker", font=("Math sans", 16, "bold"))
        hellolabel.pack()
        
        #----------------------------------------------------------------------------------------------------------------------------------Frame for table and scrollbar
        transactions_frame = ttk.Frame(self.root)
        transactions_frame.pack(pady=10)

        #---------------------------------------------------------------------------------------------------------------------------Treeview for displaying transactions
        self.transactions_tree = ttk.Treeview(transactions_frame, columns=('Category','Date','Amount'))
        self.transactions_tree.column("#0", width=0, stretch=tk.NO)
        self.transactions_tree.heading("#0", text="", anchor=tk.W)
        self.transactions_tree.heading('Category', text='Category')
        self.transactions_tree.heading('Date', text='Date')
        self.transactions_tree.heading('Amount', text='Amount')
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) #----------------------------------------Pack the Treeview to the left side of the frame and fill the frame
        
        #-------------------------------------------------------------------------------------------------------------------------------------Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(transactions_frame, orient="vertical", command=self.transactions_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.transactions_tree.configure(yscrollcommand=scrollbar.set) #-----------------------------------------------------Configure the Treeview to use the scrollbar

        #------------------------------------------------------------------------------------------------------------------------------------------Search bar and button
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left")

        #--------------------------------------------------------------------------------------------------------------------------------------------------Search button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_transactions)
        search_button.pack(side="left", padx=5)

        #--------------------------------------------------------------------------------------------------------------------------------------------------Sort combobox
        sort_options = ['Category', 'Date', 'Amount']
        self.sort_var = tk.StringVar()
        self.sort_var.set(sort_options[0])  #----------------------------------------------------------------------------------------------------------Set default value
        sort_combobox = ttk.Combobox(self.root, textvariable=self.sort_var, values=sort_options)
        sort_combobox.pack(pady=6)

        #----------------------------------------------------------------------------------------------------------------------------------------------------Sort button
        sort_button = ttk.Button(self.root, text="Sort", command=self.sort_transactions)
        sort_button.pack(pady=6)

        #----------------------------------------------------------------------------------------------------------------Refresh button to refresh the transaction table
        self.refresh_button = ttk.Button(self.root, text="Refresh", command=lambda: self.display_transactions(self.transactions), width=7, padding=(3, 3))
        self.refresh_button.pack(pady=6)

        #---------------------------------------------------------------------------------------------------------------------------------Bind events to column headings
        self.transactions_tree.heading('Category', text='Category', command=lambda: self.sort_by_column(0))
        self.transactions_tree.heading('Date', text='Date', command=lambda: self.sort_by_column(1))
        self.transactions_tree.heading('Amount', text='Amount', command=lambda: self.sort_by_column(2))

        
    def load_transactions(self, filename):
        '''Load transactions from a JSON file'''
        
        try:
            with open(filename, 'r') as file:
                transaction = json.load(file) #-------------------------------------------------------------------------------------Load transactions from the JSON file
                return transaction
        except FileNotFoundError:
            return {}

    def display_transactions(self, transactions):
        '''Display transactions in the Treeview'''
        
        #------------------------------------------------------------------------------------------------------------------Clear existing transactions from the treeview
        self.transactions_tree.delete(*self.transactions_tree.get_children())

        #-------------------------------------------------------------------------------------------------------------------------------Add transactions to the treeview
        for category, category_transactions in transactions.items():
            for transaction in category_transactions:
                date = transaction['date']
                amount = transaction['amount']
                self.transactions_tree.insert("", 'end', values=(category, date, amount)) #------------------------------------ Insert the transaction into the Treeview
        
    def search_transactions(self):
        '''Search transactions based on user input'''
        
        search_query = self.search_entry.get().lower() #----------------------------------------------------------------------Get the search query from the entry widget
        filtered_transactions = {} #-------------------------------------------------------------------------------------------Dictionary to store filtered transactions

        for category, category_transactions in self.transactions.items():
            filtered_category_transactions = [] #---------------------------------------------------------------------List to store filtered transactions for a category
            
            for transaction in category_transactions:
                try:
                    amount = float(search_query) #---------------------------------------------------------------------------Check if the search query is a valid number
                except ValueError:
                    amount = None
                    
                if search_query in category.lower() or (amount is not None and amount == transaction['amount']): #------------Check if the search query matches the category or amount
                    filtered_category_transactions.append(transaction)
                    
            if filtered_category_transactions:
                filtered_transactions[category] = filtered_category_transactions #-------------------------------------------Add filtered transactions to the dictionary

        
        if not filtered_transactions: #-----------------------------------------------------------------------------------------------------If no transactions are found
            messagebox.showinfo("No Results", "No transactions found matching your search.")
        else:
            self.display_transactions(filtered_transactions)

            
    def sort_by_column(self, col, reverse=False):
        '''Sort transactions by column'''
        
        data = [(self.transactions_tree.set(child, col), child) for child in self.transactions_tree.get_children('')] #-------Get all the transactions from the Treeview

        #--------------------------------------------------------------------------------------------------------------------Sort the data based on the column and order
        try:
            if col == 1:  #---------------------------------------------------------------------------------------------------------------------------------Sort by date
                data.sort(key=lambda x: self.convert_date_for_sorting(x[0]), reverse=reverse)
                
            elif col == 2:  #-----------------------------------------------------------------------------------------------------------------------------Sort by amount
                data.sort(key=lambda x: float(x[0]), reverse=reverse)
                
            else:  #------------------------------------------------------------------------------------------------------------------------------------Sort by category
                data.sort(key=lambda x: x[0].lower().strip(), reverse=reverse)
                
        except ValueError:
            messagebox.showerror("Invalid Data", "One or more transactions have invalid data.")
            return

        #----------------------------------------------------------------------------------------------------------------------------Rearrange items in sorted positions
        for index, (value, child) in enumerate(data):
            self.transactions_tree.move(child, '', index) #---------------------------------------------------------------------Move the transaction to the new position

        #------------------------------------------------------------------------------------------------------------------Update the heading to show the sort direction
        self.transactions_tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))

    def sort_transactions(self):
        sort_option = self.sort_var.get()
        if sort_option == 'Date':
            self.sort_by_column(1)  #--------------------------------------------------------------------------------------------------Sort by the date column (index 1)

    def convert_date_for_sorting(self, date_str):
        '''Convert date string to a format suitable for sorting'''
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d") #------------------------------------------------------------Convert the date string to a datetime object
            return date_obj.year, date_obj.month, date_obj.day
        
        except ValueError:
            return datetime.max.year, datetime.max.month, datetime.max.day #------------------------------------------------Return maximum date values for invalid dates
            
    def sort_transactions(self):
        '''Sort transactions based on user selection'''
        
        sort_option = self.sort_var.get()
        if sort_option == 'Category':
            col = 0  #-------------------------------------------------------------------------------------------------------------Sort by the category column (index 0)
            
        elif sort_option == 'Date':
            col = 1  #-----------------------------------------------------------------------------------------------------------------Sort by the date column (index 1)
            
        elif sort_option == 'Amount':
            col = 2  #---------------------------------------------------------------------------------------------------------------Sort by the amount column (index 2)
        self.sort_by_column(col)

            
def main():
    '''Create the main window and start the application'''
    root = tk.Tk()
    app = FinanceTrackerGUI(root) #--------------------------------------------------------------------------------------------------Create the FinanceTrackerGUI object
    app.display_transactions(app.transactions) #------------------------------------------------------------------------------------Display transactions in the Treeview
    root.mainloop()

if __name__ == "__main__":
    main()
