import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from fake_useragent import UserAgent
from lib.dbConn import connect

db = connect()

async def fetchContentWrapper(session, content, ua, pbar):
  await fetchContent(session, content, ua)
  pbar.update(1)


def fetchContentLinks():
  links = db["links"]
  links_data = list(links.find())
  return links_data


def updateTimestamp(link):
  links = db["links"]
  links.update_one({"link": link}, {"$set": {"scraped_at": pd.to_datetime("now", utc=True)}})


async def fetchContent(session, content, ua):
  while True:
    try:
      async with session.get(
        content["link"], headers={"User-Agent": ua.random}
      ) as response:
        html = await response.text()

        soup = BeautifulSoup(html, "html.parser")

        title_element = soup.find(class_="single__intro--title")
        content_element = soup.find(class_="cell small-12 medium-8 large-8")

        if title_element and content_element:
          title = title_element.text.strip()
          category = content["category"]
          content_text = content_element.text.strip()

          saveData(title, category, content_text, content["author"], content["date"])
          updateTimestamp(content["link"])
          break

    except Exception as e:
      print(f"Error fetching {content['link']}: {e}")


def saveData(title, category, content, author, date):
  try:
    contents = db['contents']
    contents.insert_one({"title": title, "category": category, "author": author, "date": date, "content": content})
  except Exception as e:
    print(title)
    print(f"Error saving data: {e}")


async def fetchArticles():
  contents = fetchContentLinks()
  ua = UserAgent()

  async with aiohttp.ClientSession() as session:
    tasks = []
    total_links = len(contents)

    with tqdm(total=total_links, desc="Fetching Articles", unit="link") as pbar:
      for content in contents:
        task = asyncio.ensure_future(
            fetchContentWrapper(session, content, ua, pbar)
        )
        tasks.append(task)

      await asyncio.gather(*tasks)

  input("Press Enter to continue...")
