from typing import Dict, List

ALLOWED_COMMANDS = ('payment', 'sale', 'purchase', 'account', 'warehouse', 'history', 'stop')
# input_string = ''
# input_list = []


class Product:
    def __init__(self, nm, nb):
        self.name = nm  # unikalna
        # self.price = pr  # cena jednego
        self.number = nb  # ile mamy na stanie

    def __str__(self):
        return f'{self.name}: {self.number}'


class Warehouse:
    def __init__(self, acnt):
        self.products = {}  # warehouse status - key - name, value - Product
        self.account = acnt
        # tutaj wczytujemy dane z pliku o produktach

    def add_product(self, product, price):  # najpierw piszemy logikę w klasach, potem zajmujemy się wywołaniami
        if not self.account.update_balance(-price * product.number):  # jeśli nie mamy tyle pieniędzy, to zwraca False
            return False  # metody wykonują się też w ifie, jeśli robię test!!!!!!!!!!!!
                            # czyli update_balance się wykona jeśli to będzie możliwe!!!!!
        if product.name in self.products:
            self.products[product.name].number += product.number
        else:
            self.products[product.name] = product
        self.account.account_history.append(f'Purchase: {product.name}, {price}, {product.number}')
        return True

    def remove_product(self, product, price):
        if product.name not in self.products:
            return False  # tu nie trzymamy komunikatu o błędzie - to w wywołaniu funkcji dopiero, tu nie ma komunikacji
        if self.products[product.name].number < product.number:
            return False  # early return - lepiej najpierw obsłuzyć błędy, potem juz wchodzi do prawidłowego działania
                            # to dobrze wpływa na formatowanie i wygląd kodu i czytelność
        # ta metoda zwraca false, jak nie mamy tyle produktów
        self.products[product.name].number -= product.number
        self.account.update_balance(price * product.number)
        # self.account.balance += product.number * price - nie działam bezpośrednio na atrybucie, bo nie sprawdzam
        # wtedy, czy operacja ma sens. lepiej do tego zrobić metodę.
        self.account.account_history.append(f'Sale: {product.name}, {price}, {product.number}')
        return True

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
        self.update_balance(payment_amount)  # update account balance
        self.account_history.append(f'payment: {payment_amount}, {comment}')

    def update_balance(self, amount):  # amount can be negative
        if self.balance + amount < 0:
            return False
        self.balance += amount
        return True

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
my_warehouse = Warehouse(my_account)

# actions
while True:
    input_string = input("Write action: ")  # get input - tego nie ma sensu wydzielać
    if not input_string:
        break
    input_list = input_string.split()
    command = input_list[0]
    if command == 'stop':
        break
    if command not in ALLOWED_COMMANDS:
        print(f'Please write one of allowed commands: {ALLOWED_COMMANDS}')
        continue
    if command == 'payment':  # entering payment mode
        if len(input_list) >= 3:  # if not enough parameters given
            my_account.add_payment(input_list)
        continue
    if command == 'account':
        my_account.show_account_balance()
        continue
    if command == 'history':
        print(my_account.account_history)
        continue
    if command == 'warehouse':  #obadaj czy można wrzucić do metody to
        print(f'Stock status:')
        for product in input_list[1:]:
            if product in my_warehouse.products:
                print(product)
            else:
                print(f'Product not in offer.')
        continue
    if len(input_list) < 4:  # if not enough parameters given
        continue
    input_product = Product(input_list[1], int(input_list[3]))
    product_price = int(input_list[2])
    if product_price < 0 or input_product.number < 0:  # price and number must be positive
        print('Error - price and number must be positive.')
        continue  # try again
    if command == 'sale':
        # zamiast wykonywać metodę ja robię test z jej wykorzystaniem. to zadziała jak wykonanie + test: 2w1
        if not my_warehouse.remove_product(input_product, product_price):  #gdy nie udało się odjąć produktu
            print(f'Error - out of stock')
        continue
    if command == 'purchase':
        if not my_warehouse.add_product(input_product, product_price):  #gdy nie udało się odjąć produktu
            print(f'Error - not enough money!!!!!!!!!!!!!')
        continue






