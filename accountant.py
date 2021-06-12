from typing import Dict, List

ALLOWED_COMMANDS = ('payment', 'sale', 'purchase', 'account', 'warehouse', 'history', 'stop')


class Product:
    def __init__(self, nm, nb):
        self.name = nm  # unikalna
        self.number = nb  # ile mamy na stanie

    def __str__(self):
        return f'{self.name}: {self.number}'


class Warehouse:
    def __init__(self, local_account):
        self.products = {}  # warehouse status - key - name, value - Product
        self.account = local_account
        self.read_warehouse()  # tworząc obiekt wywołujemy metodę czytającą z pliku,
                                # zapisującą dane do słownika produktów
        self.read_history()  # i tak samo z historią, też ją ładujemy od razu

    def read_warehouse(self):
        with open("warehouse.txt", "r") as file:  # otwieramy plik do odczytu
            for line in file.readlines():
                current_line = line.split(",")
                self.products[current_line[0]] = Product(current_line[0], int(current_line[1].split("\n")[0]))
                # dodajemy kolejne produkty

    def read_history(self):
        with open("history.txt", "r") as file:
            for line in file.readlines():
                self.account.account_history.append(line)

    # purchase
    def add_product(self, local_product, price):
        if not self.account.update_balance(-price * local_product.number):  # jeśli nie mamy tyle pieniędzy
            return False
        if local_product.name in self.products:
            self.products[local_product.name].number += local_product.number
        else:
            self.products[local_product.name] = local_product
        self.account.account_history.append(f'Purchase: {local_product.name}, {price}, {local_product.number}')
        return True

    # sale
    def remove_product(self, local_product, price):
        if local_product.name not in self.products:
            return False
        if self.products[local_product.name].number < local_product.number:
            return False
        self.products[local_product.name].number -= local_product.number
        self.account.update_balance(price * local_product.number)
        self.account.account_history.append(f'Sale: {local_product.name}, {price}, {local_product.number}')
        return True

    # warehouse
    def show_products(self, local_input):
        for product_name in local_input:
            if product_name not in self.products:
                print(f'Product: {product_name} not in offer.')
            else:
                print(f'Product: {product_name} - in stock: {self.products[product_name].number}')
        self.account.account_history.append(f'Stock status for: {local_input}')

    def save_stock(self):
        last_product = list(self.products.keys())[-1]
        with open("warehouse.txt", "w") as file:
            for name, product in self.products.items():
                file.write(name + "," + str(product.number))
                if name != last_product:
                    file.write("\n")

    def save_history(self):
        with open("history.txt", "a") as file:  # tutaj nadpisujemy, nie zapisujemy od nowa
            for action in self.account.account_history:
                file.write(action + "\n")


class Account:
    def __init__(self):
        self.balance = 0
        self.account_history = []
        self.read_account()

    def read_account(self):
        with open("account.txt", "r") as file:  # otwieramy plik do odczytu
            self.balance = int(file.readline())

    # account
    def show_account_balance(self):
        print(f'Current account balance is {self.balance}.')
        self.account_history.append(f'Show balance: {self.balance}')

    # payment
    def add_payment(self, local_input_list):
        payment_amount = int(local_input_list[1])
        comment = local_input_list[2]
        self.update_balance(payment_amount)  # update account balance
        self.account_history.append(f'payment: {payment_amount}, {comment}')

    # sale, purchase, payment
    def update_balance(self, amount):  # amount can be negative
        if self.balance + amount < 0:
            return False
        self.balance += amount
        return True

    def save_account(self):
        with open("account.txt", "w") as file:  # otwieramy plik do zapisu
            file.write(str(self.balance))


# print("Hello! Welcome to our online magazine tracker! \n "
#       "You can now make some actions on your account. \n"
#       f"To perform an action type as follows:\n"
#       f"1. To record a payment: {ALLOWED_COMMANDS[0]} <amount in gr> <comment> \n"
#       f"2. To note a sale: {ALLOWED_COMMANDS[1]} <product> <price> <number>\n"
#       f"3. To note a purchase: {ALLOWED_COMMANDS[2]} <product> <price> <number>\n"
#       f"4. To preview your account balance: {ALLOWED_COMMANDS[3]}\n"
#       f"5. To preview stock status of chosen products: {ALLOWED_COMMANDS[4]} <product1> <product2> etc.\n"
#       f"6. To see account history: {ALLOWED_COMMANDS[5]}\n"
#       f"When you are done with updates, type {ALLOWED_COMMANDS[6]} to proceed to summary.")  # Welcome message

my_account = Account()
my_warehouse = Warehouse(my_account)

print(my_account.account_history)

# actions
while True:
    input_string = input("Write action: ")  # get input - tego nie ma sensu wydzielać
    if not input_string:
        break
    input_list = input_string.split()
    command = input_list[0]
    if command == 'stop':
        my_warehouse.save_stock()  # zapisuję stan magazynu do pliku
        my_warehouse.save_history()  # zapisuję wykonane akcje
        my_account.save_account()  # zapisuję stan konta
        break
    if command not in ALLOWED_COMMANDS:
        print(f'Please write one of allowed commands: {ALLOWED_COMMANDS}')
        continue
    if command == 'payment':  # entering payment mode
        if len(input_list) >= 3:  # if enough parameters given
            my_account.add_payment(input_list)
        continue
    if command == 'account':
        my_account.show_account_balance()
        continue
    if command == 'history':
        print(my_account.account_history)
        continue
    if command == 'warehouse':
        print(f'Stock status:')
        my_warehouse.show_products(input_list[1:])
        continue
    if len(input_list) < 4:  # if not enough parameters given
        continue
    input_product = Product(input_list[1], int(input_list[3]))  # adding product with its name and number
    product_price = int(input_list[2])
    if product_price < 0 or input_product.number < 0:  # price and number must be positive
        print('Error - price and number must be positive.')
        continue  # try again
    if command == 'sale':
        if not my_warehouse.remove_product(input_product, product_price):  # gdy nie udało się odjąć produktu
            print(f'Error - out of stock')
        continue
    if command == 'purchase':
        if not my_warehouse.add_product(input_product, product_price):  # gdy nie udało się kupić produktu
            print(f'Error - not enough money!')
        continue






