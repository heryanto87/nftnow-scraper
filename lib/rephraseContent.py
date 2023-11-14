import os
import json
import pandas as pd
from lib.dbConn import connect
from openai import OpenAI

def clear_terminal():
  os.system('cls' if os.name == 'nt' else 'clear')


def selectContent():
  contents = connect()["contents"]
  contents_data = list(contents.find({}, {"title": 1, "category": 1, "author": 1, "date": 1, "_id": 1}))

  pd.set_option('display.max_rows', None)

  df = pd.DataFrame(contents_data)
  df['index'] = range(1, len(df) + 1)

  page_size = 10
  total_rows = len(df)

  start, end = 0, min(page_size, total_rows)

  while True:
    clear_terminal()

    print(df[['index', 'title', 'category', 'author']][start:end].to_string(index=False))

    user_input = input("Enter the number corresponding to the title you want to choose, \n'n' for the next page, \n'p' for the previous page, \n'q' to quit: ")

    if user_input.lower() == 'q':
      break
    elif user_input.lower() == 'n':
      start = end
      end = min(start + page_size, total_rows)
    elif user_input.lower() == 'p':
      start = max(0, start - page_size)
      end = min(start + page_size, total_rows)
    else:
      try:
        selected_index = int(user_input)
        if 1 <= selected_index <= len(df):
          selected_id = df.loc[selected_index - 1, '_id']
          rephraseContent(selected_id)
          input('')
        else:
          print("Invalid input. Please enter a valid number.")
      except ValueError:
        print("Invalid input. Please enter a valid number.")


def rephraseContent(id):
  try:
    client = OpenAI()
    contents = connect()["contents"]
    contents_data = contents.find_one({"_id": id})

    userPrompt = input("Enter your custom prompt, or press enter to use default: ")

    if userPrompt:
      messages = [{"role": "user", "content": f"{userPrompt} content: {contents_data['content']}"}]
    else:
      messages = [
        {"role": "user", "content": f"i need same content with different phrasing. improve the content and more interesting for reading but don't do it too much. content: {contents_data['content']}"},
      ]

    print("Rephrasing content...")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    contents_rephrased = connect()["contents_rephrased"]
    contents_rephrased.insert_one({
      "title": contents_data["title"],
      "category": contents_data["category"],
      "author": contents_data["author"],
      "date": contents_data["date"],
      "content": completion.choices[0].message.content.strip(),
    })

    print("Rephrased successfully, press enter to continue...")
  except Exception as e:
    print(f"Error rephrasing content: {e}")
    input()