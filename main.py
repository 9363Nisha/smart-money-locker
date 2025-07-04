from smart_wallet import SmartWallet

wallet = SmartWallet(5000)

def menu():
    while True:
        print("\n📲 Smart Money Locker Menu")
        print("1. Lock Amount")
        print("2. Unlock Funds")
        print("3. Set Spending Goal")
        print("4. Spend Money")
        print("5. Show Wallet Summary")
        print("6. Exit")
        print("7. Set Password")

        choice = input("Choose an option: ")

        if choice == "1":
            amt = int(input("Enter amount to lock: ₹"))
            mins = int(input("Lock duration in minutes: "))
            wallet.lock_amount(amt, mins)

        elif choice == "2":
            wallet.unlock_prompt()

        elif choice == "3":
            goal = int(input("Set your spending goal: ₹"))
            wallet.set_spending_goal(goal)

        elif choice == "4":
            spend_amt = int(input("Enter amount to spend: ₹"))
            wallet.spend(spend_amt)

        elif choice == "5":
            wallet.show_summary()

        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            break

        elif choice == "7":
            pwd = input("Set your new password: ")
            wallet.set_password(pwd)

        else:
            print("❌ Invalid choice. Try again.")

menu()
