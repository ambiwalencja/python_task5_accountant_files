from accountant import Account, Warehouse, my_warehouse, my_account

# my_account = Account()
# my_warehouse = Warehouse(my_account)

input_string = input("Write amount and comment: ")  # get input - tego nie ma sensu wydzielać
input_list = input_string.split()
if len(input_list) >= 2:  # if enough parameters given
    my_account.add_payment(input_list)

my_warehouse.save_history()  # zapisuję wykonane akcje
my_account.save_account()  # zapisuję stan konta

