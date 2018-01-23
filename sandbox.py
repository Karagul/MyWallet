from wallet_app import *

try:
    # import tkinter as tk
    from tkinter import *

except ImportError:
    # import Tkinter as tk
    from Tkinter import *


class AppGUI(Frame):

    def create_widgets(self):

        # input fields-----------------------------------------------------------------------------
        self.input_transaction_value = Entry(self)
        self.input_transaction_value.grid(row=10, column=1)
        self.input_transaction_value.insert(0, "10")

        self.input_account_value = Entry(self)
        self.input_account_value.grid(row=4, column=1)
        self.input_account_value.insert(0, "100")

        self.input_account_name = Entry(self)
        self.input_account_name.grid(row=2, column=1)
        self.input_account_name.insert(0, "cash")

        self.input_category_name = Entry(self)
        self.input_category_name.grid(row=4, column=2)
        self.input_category_name.insert(0, "transport")
        # lebels------------------------------------------------------------------------------
        self.input_account_name_label = Label(self, text="Enter Account name:")
        self.input_account_name_label.grid(row=1, column=1)

        self.input_account_value_label = Label(self, text="Enter Account value:")
        self.input_account_value_label.grid(row=3, column=1)

        self.input_category_name_label = Label(self, text="Enter Category name:")
        self.input_category_name_label.grid(row=3, column=2)

        self.input_transaction_value_label = Label(self, text="Enter Transaction value:")
        self.input_transaction_value_label.grid(row=9, column=1)

        self.input_account_value_label = Label(self, text="Select account:")
        self.input_account_value_label.grid(row=6, column=1)

        self.input_category_value_label = Label(self, text="Select category:")
        self.input_category_value_label.grid(row=6, column=2)

        self.account_display_label = Label(self, text="Current account value:")
        self.account_display_label.grid(row=1, column=2)

        self.account_display = Label(self)
        self.account_display.grid(row=2, column=2)

        self.transaction_label_display = Label(self, text="Last Transaction:")
        self.transaction_label_display.grid(row=9, column=2)

        self.transaction_display = Label(self)
        self.transaction_display.grid(row=10, column=2)

        # add buttons----------------------------------------------------------------------
        self.add_account_btn = Button(self, text="Add/Update Account", command=self.check_account)
        self.add_account_btn.grid(row=5, column=1)

        self.add_transaction_btn = Button(self, text="Add Transaction", command=self.check_transation)
        self.add_transaction_btn.grid(row=11, column=1)

        self.add_category = Button(self, text="Add category", command=self.check_category)
        self.add_category.grid(row=5, column=2)
        # del buttons-------------------------------------------------------------------
        self.del_account_btn = Button(self, text="Del Account", command=self.del_ac)
        self.del_account_btn.grid(row=8, column=1)

        self.del_category_btn = Button(self, text="Del Category", command=self.del_cat)
        self.del_category_btn.grid(row=8, column=2)

        self.del_transaction_btn = Button(self, text="Del last transaction", command=self.del_tr)
        self.del_transaction_btn.grid(row=12, column=2)
        # 0ther buttons--------------------------------------------------------
        self.quit = Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=13, column=1)

        self.transaction_view_btn = Button(self, text="View all transactions", command=self.display_list)
        self.transaction_view_btn.grid(row=11, column=2)

        # listboxes---------------------------------------------------------
        self.account_listbox = Listbox(self, height=5, selectmode='SINGLE', exportselection=0)
        self.account_listbox.grid(row=7, column=1)
        self.account_listbox.select_set(first=0)

        self.category_listbox = Listbox(self, height=5, selectmode='SINGLE')
        self.category_listbox.grid(row=7, column=2)
        # initialisation---------------------------------------------------------------------------
        self.master.title('My wallet')

        for key in wallet.account_list:
            self.account_listbox.insert(END, key)

        for key in wallet.category_list:
            self.category_listbox.insert(END, key)

        self.account_listbox.select_set(0)
        self.category_listbox.selection_set(0)

        def callback_event(e):
            self.display_account(
                wallet.account_list[self.account_listbox.get(self.account_listbox.curselection(), last=None)])

        callback_event(e=None)
        self.account_listbox.bind('<<ListboxSelect>>', callback_event)
        try:
            self.display_transaction((sorted(wallet.transaction_list.keys(), reverse=True))[0])
        except IndexError:
            self.display_transaction(transaction=None)

    # --------------------------------------------------------------------------------------------

    def check_account(self):
        if ((self.input_account_value.get()).isdigit() and
                (self.input_account_name.get()).isalpha()):
            self.account_callback()
        else:
            self.error_window()

    def check_category(self):
        if (self.input_category_name.get() not in wallet.category_list.keys() and
                (self.input_category_name.get()).isalpha()):
            self.category_callback()
        else:
            self.error_window()

    def check_transation(self):
        if (self.input_transaction_value.get()).isdigit():
            self.transaction_callback()
        else:
            self.error_window()

    def error_window(self):
        self.top = Toplevel(self)
        self.top.title("Error")
        self.label_info = Label(self.top, text=("Wrong input,\n"
                                                "Please check input fields for correct filling in:\n"
                                                "name fields can't containe digits  and value field can't chars\n"
                                                "name fields can't contains of already existing object\n"))
        self.label_info.grid(row=1, column=1)
        self.back_button = Button(self.top, text="ok", command=self.top.destroy)
        self.back_button.grid(row=2, column=1)

    def update_window(self, account):
        self.top = Toplevel(self)
        self.top.title("Account was updated")
        self.label_info = Label(self.top, text=("%s account value was updated to %s" %
                                                (account.account_name, account.account_value)))
        self.label_info.grid(row=1, column=1)
        self.back_button = Button(self.top, text="ok", command=self.top.destroy)
        self.back_button.grid(row=2, column=1)

    def account_callback(self):
        entered_value = Decimal(self.input_account_value.get()).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        entered_name = self.input_account_name.get()
        account = Account(entered_name, entered_value)
        if entered_name in wallet.account_list.keys():
            self.update_window(account)
        else:
            self.account_listbox.insert(END, entered_name)
        wallet.add_account(account)
        # self.display_account(wallet.account_list[entered_name])
        wallet.save_to_file('accounts.json', wallet.account_list)

    def transaction_callback(self):

        entered_value = Decimal(self.input_transaction_value.get()).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        selected_category = self.category_listbox.get(self.category_listbox.curselection(), last=None)
        selected_account = self.account_listbox.get(self.account_listbox.curselection(), last=None)
        transaction = Transaction(entered_value, selected_account, selected_category)
        wallet.add_transaction(transaction)
        self.display_transaction((sorted(wallet.transaction_list.keys(), reverse=True))[0])
        wallet.account_list[selected_account] = wallet.spend(wallet.account_list[selected_account],
                                                             wallet.transaction_list[
                                                                 transaction.transaction_name]["value"])
        self.display_account(wallet.account_list[selected_account])
        print(wallet.transaction_list, 'this is transaction list')
        wallet.save_to_file('transactions.json', wallet.transaction_list)
        wallet.save_to_file('accounts.json', wallet.account_list)
        print(wallet.account_list)

    def category_callback(self):
        category_name = self.input_category_name.get()
        wallet.category_list[category_name] = None
        self.category_listbox.insert(END, category_name)
        wallet.save_to_file('categories.json', wallet.category_list)

    def display_transaction(self, transaction):
        self.transaction_display['fg'] = '#42f477'
        self.transaction_display['bg'] = "#000000"
        if transaction:
            self.transaction_display['text'] = "%s:" % transaction
            for k, v in sorted(wallet.transaction_list[transaction].items(), reverse=True):
                self.transaction_display['text'] += "\n%s:%s" % (k, v)
        else:
            self.transaction_display['text'] = 'There \n are \n no transactions'

    def display_account(self, account):
        self.account_display['text'] = "%s UAH" % account
        self.account_display['fg'] = '#42f477'
        self.account_display['bg'] = "#000000"

    def del_ac(self):
        del (wallet.account_list[self.account_listbox.get(self.account_listbox.curselection(), last=None)])
        wallet.save_to_file('accounts.json', wallet.account_list)
        self.account_listbox.delete(self.account_listbox.curselection(), last=None)

    def del_cat(self):
        del (wallet.category_list[self.category_listbox.get(self.category_listbox.curselection(), last=None)])
        wallet.save_to_file('categories.json', wallet.category_list)
        self.category_listbox.delete(self.category_listbox.curselection()[0])

    def del_tr(self):
        del (wallet.transaction_list[(sorted(wallet.transaction_list.keys(), reverse=True))[0]])
        wallet.save_to_file('transactions.json', wallet.transaction_list)
        try:
            self.display_transaction((sorted(wallet.transaction_list.keys(), reverse=True))[0])
        except IndexError:
            self.display_transaction(transaction=None)

    def transaction_window(self):

        self.top = Toplevel(self)
        self.top.title("View all transactions")
        self.scroll = Scrollbar(self.top)
        self.scroll.grid(row=2, column=2, sticky='NSW')
        self.transaction_textbox = Text(self.top, font="Arial", width="30", yscrollcommand=self.scroll.set)
        self.transaction_textbox.grid(row=2, column=1)
        self.back_button = Button(self.top, text="Back", command=self.top.destroy)
        self.back_button.grid(row=3, column=1)
        self.label = Label(self.top)
        self.label.grid(row=2, column=3)
        self.scroll.config(command=self.transaction_textbox.yview)
        self.entry = Entry(self.top, width=38)
        self.entry.grid(row=1, column=1)
        self.search_button = Button(self.top, text="Search", command=self.search)
        self.search_button.grid(row=1, column=3)

    def transaction_view(self, tuple_list):
        total = 0
        for key, value in sorted(tuple_list, reverse=True):
            self.transaction_textbox.insert(END, "\n" + key + ":\n")
            for k, v in value.items():
                text_row = (" %s:%s\n") % (k, v)
                if k == "value":
                    total += Decimal(v).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
                self.transaction_textbox.insert(END, text_row)
        self.label["text"] = 'Total:\n %s UAH' % total
        self.label['fg'] = '#42f477'
        self.label['bg'] = "#000000"

    def display_list(self):
        self.transaction_window()
        self.transaction_view(wallet.transaction_list.items())

    def search(self):
        filt_word = self.entry.get()
        filter_list = []
        for item in wallet.transaction_list.items():
            if filt_word in item[0]:
                filter_list.append(item)
            else:
                for value in item[1].values():
                    if filt_word in value:
                        filter_list.append(item)
        self.transaction_textbox.delete("1.0", END)
        self.transaction_view(filter_list)

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()


root = Tk()
app = AppGUI(master=root)
app.mainloop()
