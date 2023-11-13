import os
import asyncio
from lib.fetchLinks import fetchLinks
from lib.fetchContents import fetchArticles
from lib.rephraseContent import selectContent

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\n=== Menu ===")
    print("1. Fetch Links")
    print("2. Fetch Articles")
    print("3. Rephrase Content")
    print("0. Exit")

async def main():
    while True:
        clear_terminal()
        print_menu()
        user_input = input("Enter your choice (0-3): ")

        try:
            choice = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")
            continue

        if choice == 1:
            fetchLinks()
        elif choice == 2:
            await fetchArticles()
        elif choice == 3:
            selectContent()
        elif choice == 0:
            break
        else:
            print("Invalid input. Please enter a number between 0 and 3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())
