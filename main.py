import asyncio
from lib.fetchLinks import fetchLinks
from lib.fetchContents import fetchArticles
from lib.rephraseContent import selectContent

async def main():
    print("What do you want to fetch?")
    print("1. Links")
    print("2. Articles")
    print("3. Rephrase Content")
    print("0. Exit")

    while True:
        com = int(input(">> "))

        if com == 1:
            fetchLinks()
        elif com == 2:
            await fetchArticles()
        elif com == 3:
            selectContent()
        elif com == 0:
            break
        else:
            print("Invalid input. Please enter 0, 1, or 2.")


if __name__ == "__main__":
    asyncio.run(main())
