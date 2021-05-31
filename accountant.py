from typing import Dict, List

ALLOWED_COMMANDS = ('payment', 'sale', 'purchase', 'account', 'warehouse', 'history', 'stop')
# input_string = ''
# input_list = []


class Product:
    def __init__(self, nm, pr, nb):
        self.name = nm  # unikalna
        self.price = pr  # cena jednego
        self.number = nb  # ile mamy na stanie

    def __str__(self):
        return f'{self.name}: {self.number}'


class Warehouse:
    def __init__(self):
        self.products = []  # this will be the new list for warehouse status
        # tutaj wczytujemy dane z pliku o produktach

    def check_if_in_stock(self):
        pass


class Account:
    def __init__(self):
        self.balance = 0
        self.account_history = []

    # def read_account(self):
        # with open("account.txt", "a") as file:  # otwieramy plik do odczytu
            # self.balance = file.readline()

    def show_account_balance(self):
        print(f'Current account balance is {self.balance}.')
        self.account_history.append(f'Show balance: {self.balance}')

    def add_payment(self, local_input_list):
        payment_amount = int(local_input_list[1])
        comment = local_input_list[2]
        self.balance += payment_amount  # update account balance
        self.account_history.append(f'payment: {payment_amount}, {comment}')


print("Hello! Welcome to our online magazine tracker! \n "
      "You can now make some actions on your account. \n"
      f"To perform an action type as follows:\n"
      f"1. To record a payment: {ALLOWED_COMMANDS[0]} <amount in gr> <comment> \n"
      f"2. To note a sale: {ALLOWED_COMMANDS[1]} <product> <price> <number>\n"
      f"3. To note a purchase: {ALLOWED_COMMANDS[2]} <product> <price> <number>\n"
      f"4. To preview your account balance: {ALLOWED_COMMANDS[3]}\n"
      f"5. To preview stock status of chosen products: {ALLOWED_COMMANDS[4]} <product1> <product2> etc.\n"
      f"6. To see account history: {ALLOWED_COMMANDS[5]}\n"
      f"When you are done with updates, type {ALLOWED_COMMANDS[6]} to proceed to summary.")  # Welcome message

my_account = Account()
my_warehouse = Warehouse()
# my_product = Product()

# actions
while True:
    input_string = input("Write action: ")  # get input - tego nie ma sensu wydzielać
    if not input_string:
        break
    input_list = input_string.split()
    command = input_list[0]
    if command in ALLOWED_COMMANDS:
        if command == 'payment':  # entering payment mode
            if len(input_list) < 3:  # if not enough parameters given
                continue
            my_account.add_payment(input_list)
        elif command == 'account':
            my_account.show_account_balance()
        elif command == 'history':
            print(my_account.account_history)
        elif input_list[0] == 'warehouse':
            print(f'Stock status:')
            for product in input_list[1:]:
                if product in my_warehouse.products:
                    print(product)
                else:
                    print(f'Product not in offer.')
        elif command == 'stop':
            break
        else:
            if len(input_list) < 4:  # if not enough parameters given
                continue
            input_product = Product(input_list[1], int(input_list[2]), int(input_list[3]))
            if input_product.price > 0 and input_product.number > 0:  # price and number must be positive
                if command == 'sale':
                    for stock_product in my_warehouse.products:  # !!! musimy lecieć pętlą po wszystkich i tak naprawdę
                                        # w całej pętli if wykona się tylko raz, tam, gdzie name się zgadza
                        if input_product.name == stock_product.name: # sprawdzam, czy wpisana nazwa jest w magazynie
                            if stock_product.number >= input_product.number:
                                stock_product.number -= input_product.number  # subtracting number of sold products from warehouse
                                my_account.balance += input_product.price * input_product.number  # adding income
                                # print(f'debug print in sale mode: account balance: {my_account.balance}, '
                                      # f'input product number: {input_product.number}'
                                      # f'input product price: {input_product.price}')
                               # !!!!! don't forget to add sale to the account history
                            else:
                                print(f'Error - out of stock')
                                continue  # try again
                            if stock_product.number == 0:  # if after the sale the number of items is zero, we remove the product
                                my_warehouse.products.remove(stock_product)  # is it right????????????
                        else:
                            print(f'Not in offer! Pick another product')
                            continue  # try again...
                elif command == 'purchase':
                    my_account.balance -= input_product.price * input_product.number  # subtracting the expense
                    # !!!!! don't forget to add the expense to the account history
                    # print(f"debug print in purchase, account balance: {my_account.balance}")
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!LOOK BELOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    if my_warehouse.products:  # if there are any items in this list
                        for stock_product in my_warehouse.products:  # the problem is here - the loop doesnt even start as
                            # there are no element in this list yet. should i use a set instead?
                            # how do i check if the product is there and if it is not - add it?
                            if input_product.name == stock_product.name:
                                stock_product.number += input_product.number  # adding number of purchased products to warehouse
                            else:
                                my_warehouse.products.append(input_product)  # adding purchased products to warehouse
                            # print(f'debug print in purchase mode: account balance: {my_account.balance}, '
                                  # f'input product number: {input_product.number}'
                                  # f'input product price: {input_product.price}')
                    else:  # if this is the first item
                        my_warehouse.products.append(input_product)
            else:
                print('Error - price and number must be positive.')
                continue  # try again
    else:
        print(f'Please write one of allowed commands: {ALLOWED_COMMANDS}')



