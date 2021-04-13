import random
import string
# for store account details of all users
user_database = {}

# for new user register
def new_user ():
    print("Enter your Full Name:",end='')
    username = input()

    # generate 8 digit atm id
    new_id = int(''.join(random.choices(string.digits, k=8)))

    # check for existence of atm id if exist generate new id
    while new_id in user_database:
        new_id = ''.join(random.choices(string.digits, k=8))

    # atm pin from user
    pin = input('Please enter your 4 digit ATM Pin:')
    while len(pin) != 4:
        pin = input("Please enter valid PIN and '-1' for exit:")
        if int(pin) == -1:
            return None

    # added to database
    user_database[new_id]=[int(pin),username,0]
    return new_id

# method for user login
def login ():
    card_num = int(input("Enter 8 digit ATM Card Number:"))
    if card_num in user_database:
        pin=int(input('Enter 4 digit ATM Pin:'))
        while user_database[card_num][0]!=pin:
            again = int(input("---Invalid PIN---\nFor retry enter: 1\nFor cancel transaction enter:0"))
            if again==1:
                pin=int(input('Enter 4 digit PIN:'))
            else:
                return None
        return card_num
    else:
        print("User not exist")
        return None

# class for atm transactions
class ATM:
    def __init__(self,n_2000=0,n_500=0,):
        self.atm_blnc=n_2000*2000+n_500*500
        self.atm_note_details={2000:n_2000,500:n_500}
    # method for deposit money in atm machine
    def deposit_atm (self,case):
        self.atm_blnc += case[2000]*2000 + case[500] * 500
        self.atm_note_details[2000] += case[2000]
        self.atm_note_details[500] += case[500]
        return

    # method for check status of atm machine
    def check(self,amount):
        if amount>20000:
            print("Cannot withdraw more than Rs:20,000/- in one transaction.")
            return False

        elif amount>self.atm_blnc:
            print('Sorry!! Not sufficient fund in ATM machine')
            return False

        elif amount%500!=0:
            print('Enter amount in multiple of 500')
            return False
        else:
            rqrd_500=(amount%2000)//500
            if rqrd_500>self.atm_note_details[500]:
                print("Not available required 500 rupee notes.Please enter amount in multiple of 2000")
                return False
            return True

    # method for withdraw money from atm machine
    def withdraw(self,amount):
        rqrd_2000= amount // 2000
        rqrd_500 = (amount % 2000) // 500
        self.atm_blnc -= amount
        self.atm_note_details[2000] -= rqrd_2000
        self.atm_note_details[500] -= rqrd_500
        return

# class for account details and transactions
class Account:

    def __init__(self,card_num):
        self.balance = user_database[card_num][2]

    # for deposit amount to users account
    def deposit(self, details):
        amount_d= details[2000]*2000+details[500]*500
        self.balance += amount_d
        user_database[card_num][2]=self.balance
        print("\n{}/- Deposited successfully!current :{}:".format(amount_d,user_database[card_num][2]))
        return

    # for status of users account
    def check(self,amount_w):
        if self.balance>amount_w:
            return True
        else:
            return False

    # for withdraw amount from users account
    def withdraw (self,amount_w):
        user_database[card_num][2] -= amount_w
        self.balance=user_database[card_num][2]
        return

    # for check accounts balance
    def bank_balance(self):
        print("{} your account Balance is {}/-:".format(user_database[card_num][1],self.balance))
        return

if __name__=="__main__":
    # dictionary for note details
    note_details={2000:0,500:0}
    # initialisation of atm machine
    # having some money initially
    # ATM(no. of 2000 notes ,no. of 500 notes)
    atm = ATM(10,20)
    # for user interface
    choice = None
    while choice != "0":
        print \
            ("""
                ---WELCOME---
    
                0 - Exit
                1 - Login
                2 - Register
                """)

        choice = input("Your choice:")
        print()

        if choice == "0": # when user choose exit
            print("Thank you!")

        elif choice == "1": # when user choose Login
            card_num = login()
            if card_num != None:
                user = user_database[card_num][1]
                # create object of account class for every user
                user = Account(card_num)
                print('Welcome {} \n----Choose any Transaction:----'.format(user_database[card_num][1]))

                print('0:For Deposit\n1:For Withdraw\n2:For Balance check\n3:For Cancel or Exit')

                user_choice = int(input('Enter choice:'))
                if user_choice == 0:  # when user choose Deposit
                    print("Note details,Enter No. of 2000 notes and No. of 500 notes(eg:10 5): ")
                    lst = list(map(int,input().split()))
                    note_details[2000], note_details[500] = lst[0], lst[1]

                    atm.deposit_atm(note_details)
                    user.deposit(note_details)

                elif user_choice == 1:  # when user choose withdraw
                    flag = 1
                    amount = int(input("Enter amount in multiple 500:"))

                    if user.check(amount):
                        if atm.check(amount):
                            user.withdraw(amount)
                            atm.withdraw(amount)
                            print('Dear {} Rs. {} withdrew from your bank account'.format(user_database[card_num][1],amount))
                            print('Please collect you case\nThank you!!')
                    else:
                        print('Insufficient fund')
                elif user_choice == 2:  # when user choose Balance check
                    user.bank_balance()
                elif user_choice == 3:  # when user cancel the transaction
                    pass
                else:  # when user choose exit or enter wrong key
                    print("Session expired")

        elif choice == "2":  # when user choose register as new user
            flag = new_user()
            if flag != None:
                print("Dear {} You have successfully registered.\nYour ATM card No. is {}\nThank You".format(user_database[flag][1],flag))
            else:
                print("You have canceled the registration")
        else:
            print("Enter valid option")
