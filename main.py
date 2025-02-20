import random
import time
import os
from colorama import Fore, Style

#The main settings of the game
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A" : 3,
    "B" : 4,
    "C" : 6,
    "D" : 8
}

symbol_value = {
    "A" : 5,
    "B" : 4,
    "C" : 3,
    "D" : 2
}


# Rolling effect
def rolling_effect():
    symbols = ["A", "B", "C", "D"]
    for _ in range(3):
        print(" | ".join(random.choices(symbols, k=3)), end = "\r", flush = True)
        time.sleep(0.5)
    print(" " * 20, end = "\r")

def deposit():
    while True:
        amount = input(Fore.GREEN + "\nWhat would you like to deposit? $" + Style.RESET_ALL)

        if amount.isdigit(): #if the input variable "amount" is a number or not
            amount = int(amount)

            if amount > 0:
                break
            else:
                print(Fore.RED + "\nThe amount must be greater than 0." + Style.RESET_ALL)
        else:
            print(Fore.RED + "\nPlease enter a number...." + Style.RESET_ALL)

    return amount


def get_number_of_lines():
    while True:
        lines = input(Fore.YELLOW + "\nEnter the number of lines to bet on (1-" + str(MAX_LINES) + ") : " + Style.RESET_ALL)

        if lines.isdigit(): #if the input variable "lines" is a number or not
            lines = int(lines)

            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(Fore.RED + "\nEnter a valid number of lines.... " + Style.RESET_ALL)
        else:
            print(Fore.RED + "\nPlease enter a number...." + Style.RESET_ALL)

    return lines


def get_bet():
    while True:
        amount = input(Fore.YELLOW + "\nHow much money would you like to bet on each line? : $" + Style.RESET_ALL)

        if amount.isdigit():                        #if the input variable "amount" is a number or not
            amount = int(amount)

            if MIN_BET <= amount <= MAX_BET :
                break
            else:
                print(Fore.RED + f'\nAmount must be between ${MIN_BET} and ${MAX_BET}...' + Style.RESET_ALL)
        else:
            print(Fore.RED + "\nPlease enter a number...." + Style.RESET_ALL)

    return amount


def get_slot_machine_spin(rows,cols,symbols) : 
    all_symbols = []
    for symbol, symbol_count in symbols.items() :
        for _ in range(symbol_count) :              # _ is an anonymous variable used in python
            all_symbols.append(symbol)              # when there is no use of the variable
            

    columns = [[] for _ in range(cols)]             #correctly initializing empty lists fo each column

    for i in range(cols) : 
        column = []
        current_symbols = all_symbols[:]            # this is a way to copy a list ":" is a slice operator
        for _ in range(rows) :
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns[i] = column # correctly assigning the column data

    return columns


def print_slot_machine(columns):
    rolling_effect()
    print("\n🎰 SLOT MACHINE 🎰") 
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns)-1:
                print(Fore.BLUE + column[row] + Style.RESET_ALL, end = " | ")
            else:
                print(Fore.BLUE + column[row] + Style.RESET_ALL, end = "")

        print()


def check_winnings(columns,lines,bet, values):
    winnings = 0
    winning_lines = []
    jackpot = False

    for line in range(lines):
        symbol = columns[0][line]
        won = True

        for column in columns : 
            if column[line] != symbol : 
                won = False
                break
        if won : 
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

# Special feature "JACKPOT"

    if winnings > 0 and len(winning_lines) == lines:
        winnings *= 10
        jackpot = True

    return winnings, winning_lines,jackpot


def spin(balance) : 
    lines = get_number_of_lines()

    while True:
        bet = get_bet()
        total_bet = bet * lines
        
        if total_bet > balance : 
            print(Fore.RED + f"\nYou do not have enough balance to bet that amount.\nYour current balance is ${balance}.\n" + Style.RESET_ALL)
        else :
            break
    
    print(Fore.CYAN + f'\nYou are betting ${bet} on {lines} lines.\nTotal bet is equal to ${total_bet}\n' + Style.RESET_ALL )

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)


    winnings, winning_lines,jackpot = check_winnings(slots, lines, bet, symbol_value)

    if winnings > 0:
        if jackpot:
            print(Fore.GREEN + "\n🎉 JACKPOT WINNER! 🎉" + Style.RESET_ALL)
        print(Fore.GREEN + f'\nCongratulations!!....\nYou won ${winnings}.' + Style.RESET_ALL)
        print(Fore.YELLOW + "And won on the lines : ", *winning_lines, Style.RESET_ALL)
    else : 
        print(Fore.RED + "\n!! You Lose !! ❌" + Style.RESET_ALL)


    print()

    return winnings - total_bet

def main():
    print(Fore.MAGENTA + "\n\t\t\t\t🎰 Welcome to the Ultimate Slot Machine! 🎰\n\n", Style.RESET_ALL)
    balance = deposit()
    streak = 0 # Tracking win streak

    while balance > 0 : 
        print(Fore.CYAN + f'\nCurrent Balance is ${balance}.' + Style.RESET_ALL)
        answer = input(Fore.YELLOW + "\nPress enter to Play (q to Quit)." + Style.RESET_ALL)

        if answer.lower() == 'q' : 
            break
        
        balance_before = balance
        balance += spin(balance)

        if balance > balance_before:
            streak += 1
            if streak ==3:
                print(Fore.CYAN + "\n🔥 Bonus Round! You get a Free Spin! 🔥" + Style.RESET_ALL)
                balance += spin(balance)
                streak = 0
        else:
            streak = 0


        if balance <= 0 : 
            print(Fore.MAGENTA + "\nYour balance is now empty.\nYou lost everything.\n💀 !! GAME OVER !! 💀\nBetter luck next time.\n\n" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"\n🎮 You leave with ${balance}. Thanks for playing!" + Style.RESET_ALL)

main()
