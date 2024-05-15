import tkinter as tk
from tkinter import messagebox
import random
import string
import csv

# Global variables
registered_users = {}
balance = {}
transaction_history = {}  # Dictionary to store transaction history

currency_rates = {
    'USD': {'USD': 1.0, 'EUR': 0.85, 'ZAR': 0.75},
    'EUR': {'USD': 1.18, 'EUR': 1.0, 'ZAR': 0.88},
    'ZAR': {'USD': 1.33, 'EUR': 1.14, 'ZAR': 1.0}
}


# Function to convert amount from one currency to another
def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount  # No conversion needed if currencies are the same
    else:
        conversion_rate = currency_rates[from_currency][to_currency]
        converted_amount = amount * conversion_rate
        return converted_amount


# Function to generate a random password
def generate_password():
    password_length = 6
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(password_length))
    return password


# Function to assign a unique account number
def assign_account_number():
    return ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit account number


# Function to handle registration form submission
def register_user():
    username = reg_username.get()
    password = reg_password.get()

    if username in registered_users:
        messagebox.showerror("Registration Error", "Username already exists. Please choose a different username.")
    else:
        if not password:  # If password field is empty, generate a random password
            password = generate_password()
            reg_password.delete(0, tk.END)  # Clear the password entry field
            reg_password.insert(0, password)  # Insert generated password into the field

        account_number = assign_account_number()
        registered_users[username] = {'password': password, 'account_number': account_number}
        balance[account_number] = {'USD': 0.0, 'EUR': 0.0, 'ZAR': 0.0}  # Initialize balances for different currencies
        transaction_history[username] = []  # Initialize empty transaction history for the user
        messagebox.showinfo("Registration", f"Registered User - Username: {username}, Account Number: {account_number}")


# Function to handle login form submission
def login_user():
    username = login_username.get()
    password = login_password.get()

    if username in registered_users and registered_users[username]['password'] == password:
        messagebox.showinfo("Login", f"Logged In - Username: {username}")
        show_banking_app(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


# Function to display banking application after successful login
def show_banking_app(username):
    # Hide login and registration frames
    login_frame.pack_forget()
    register_frame.pack_forget()

    # Show banking frames
    frame_deposit.pack()
    frame_withdraw.pack()
    frame_balance.pack()
    update_balance_label(username)


# Function to handle deposit
def deposit_amount():
    username = login_username.get()
    currency = deposit_currency.get()
    amount = float(deposit_entry.get())

    if amount <= 0:
        messagebox.showwarning("Invalid Amount", "Please enter a valid positive amount.")
        return

    account_number = registered_users[username]['account_number']
    balance[account_number][currency] += amount

    # Log transaction
    balance_after_transaction = balance[account_number][currency]
    transaction = {'type': 'Deposit', 'currency': currency, 'amount': amount, 'balance_after_transaction': balance_after_transaction}
    transaction_history[username].append(transaction)

    update_balance_label(username)
    messagebox.showinfo("Deposit",
                        f"Deposit successful. Current balance: {currency} {balance[account_number][currency]:.2f}")


# Function to handle withdrawal
def withdraw_amount():
    username = login_username.get()
    currency = withdraw_currency.get()
    amount = float(withdraw_entry.get())

    if amount <= 0:
        messagebox.showwarning("Invalid Amount", "Please enter a valid positive amount.")
        return

    account_number = registered_users[username]['account_number']
    if amount > balance[account_number][currency]:
        messagebox.showwarning("Insufficient Funds", "You have insufficient funds for this withdrawal.")
    else:
        balance[account_number][currency] -= amount

        # Log transaction
        balance_after_transaction = balance[account_number][currency]
        transaction = {'type': 'Withdrawal', 'currency': currency, 'amount': amount, 'balance_after_transaction': balance_after_transaction}
        transaction_history[username].append(transaction)

        update_balance_label(username)
        messagebox.showinfo("Withdrawal",
                            f"Withdrawal successful. Current balance: {currency} {balance[account_number][currency]:.2f}")


# Function to update balance label
def update_balance_label(username):
    account_number = registered_users[username]['account_number']
    current_currency = balance_currency.get()
    current_balance = balance[account_number][current_currency]
    balance_label.config(text=f"Current Balance: {current_currency} {current_balance:.2f}")


# Function to save transaction history to a CSV file
def save_transaction_history(username):
    if username in transaction_history:
        filename = f"{username}_transactions.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['User Name', 'Account Number', 'Type', 'Currency', 'Amount', 'Balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write user name and account number at the beginning of the file
            writer.writerow({'User Name': username,
                             'Account Number': registered_users[username]['account_number'],
                             'Type': '', 'Currency': '', 'Amount': '', 'Balance': ''})

            # Write transaction history
            for transaction in transaction_history[username]:
                transaction_type = transaction['type']
                currency = transaction['currency']
                amount = transaction['amount']
                balance_after_transaction = transaction['balance_after_transaction']

                writer.writerow({'User Name': username,
                                 'Account Number': registered_users[username]['account_number'],
                                 'Type': transaction_type,
                                 'Currency': currency,
                                 'Amount': amount,
                                 'Balance': balance_after_transaction})

        messagebox.showinfo("Transaction History", f"Transaction history saved to {filename}")
    else:
        messagebox.showerror("Transaction History", "No transaction history found for this user.")


# Create the main window
root = tk.Tk()
root.title("Binary Finance")
root.configure(bg="black")

# Load the logo image
logo_image = tk.PhotoImage(file="logo.png")
logo_image_resized = logo_image.subsample(2)
logo_label = tk.Label(root, image=logo_image_resized, bg="black")
logo_label.pack()

# Container for Registration Form
register_frame = tk.Frame(root, padx=20, pady=20, bg="black")
register_frame.pack()

tk.Label(register_frame, text="Register", font=("Helvetica", 20, "bold"), fg="gold", bg="black").grid(row=0,
                                                                                                      columnspan=2)

tk.Label(register_frame, text="Username:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=1, column=0,
                                                                                               sticky="e")
reg_username = tk.Entry(register_frame, font=("Helvetica", 12))
reg_username.grid(row=1, column=1)

tk.Label(register_frame, text="Password:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=2, column=0,
                                                                                               sticky="e")
reg_password = tk.Entry(register_frame, show="*", font=("Helvetica", 12))
reg_password.grid(row=2, column=1)

tk.Button(register_frame, text="Register", command=register_user, bg="gold", fg="black",
          font=("Helvetica", 12, "bold")).grid(row=3, columnspan=2)

# Container for Login Form
login_frame = tk.Frame(root, padx=50, pady=50, bg="black")
login_frame.pack()

tk.Label(login_frame, text="Login", font=("Helvetica", 20, "bold"), fg="gold", bg="black").grid(row=0, columnspan=2)

tk.Label(login_frame, text="Username:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=1, column=0, sticky="e")
login_username = tk.Entry(login_frame, font=("Helvetica", 12))
login_username.grid(row=1, column=1)

tk.Label(login_frame, text="Password:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=2, column=0, sticky="e")
login_password = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
login_password.grid(row=2, column=1)

tk.Button(login_frame, text="Login", command=login_user, bg="gold", fg="black", font=("Helvetica", 12, "bold")).grid(
    row=3, columnspan=2)

# Containers for Banking Application
frame_deposit = tk.Frame(root, padx=30, pady=20, bg="black")
frame_withdraw = tk.Frame(root, padx=30, pady=20, bg="black")
frame_balance = tk.Frame(root, padx=30, pady=20, bg="black")

# Additional Styling for Banking Application
tk.Label(frame_deposit, text="Deposit", font=("Helvetica", 20, "bold"), fg="gold", bg="black").grid(row=0, column=0,
                                                                                                    columnspan=2)

tk.Label(frame_deposit, text="Amount:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=1, column=0, sticky="e")
deposit_entry = tk.Entry(frame_deposit, font=("Helvetica", 12))
deposit_entry.grid(row=1, column=1)

tk.Label(frame_deposit, text="Currency:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=2, column=0,
                                                                                              sticky="e")
deposit_currency = tk.StringVar()
deposit_currency.set('USD')  # Default currency
currency_options = ['USD', 'EUR', 'ZAR']
tk.OptionMenu(frame_deposit, deposit_currency, *currency_options).grid(row=2, column=1)

tk.Button(frame_deposit, text="Deposit", command=deposit_amount, bg="gold", fg="black",
          font=("Helvetica", 12, "bold")).grid(row=3, columnspan=2)

tk.Label(frame_withdraw, text="Withdraw", font=("Helvetica", 20, "bold"), fg="gold", bg="black").grid(row=0, column=0,
                                                                                                      columnspan=2)

tk.Label(frame_withdraw, text="Amount:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=1, column=0,
                                                                                             sticky="e")
withdraw_entry = tk.Entry(frame_withdraw, font=("Helvetica", 12))
withdraw_entry.grid(row=1, column=1)

tk.Label(frame_withdraw, text="Currency:", fg="gold", bg="black", font=("Helvetica", 12)).grid(row=2, column=0,
                                                                                               sticky="e")
withdraw_currency = tk.StringVar()
withdraw_currency.set('USD')  # Default currency
tk.OptionMenu(frame_withdraw, withdraw_currency, *currency_options).grid(row=2, column=1)

tk.Button(frame_withdraw, text="Withdraw", command=withdraw_amount, bg="gold", fg="black",
          font=("Helvetica", 12, "bold")).grid(row=3, columnspan=2)

balance_currency = tk.StringVar()
balance_currency.set('USD')  # Default currency for balance display

balance_label = tk.Label(frame_balance, text="Current Balance: 0.00", fg="gold", bg="black", font=("Helvetica", 16))
balance_label.pack()

tk.Label(frame_balance, text="Display Balance In:", fg="gold", bg="black", font=("Helvetica", 12)).pack()
tk.OptionMenu(frame_balance, balance_currency, *currency_options,
              command=lambda _: update_balance_label(login_username.get())).pack()

# Button to save transaction history
save_history_button = tk.Button(root, text="Download Transaction History",
                                command=lambda: save_transaction_history(login_username.get()), bg="gold", fg="black",
                                font=("Helvetica", 12, "bold"))
save_history_button.pack()

# Start the main event loop
root.mainloop()
