import os
import asyncio
import aiohttp
import re
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from fake_useragent import UserAgent


async def fetchContentWrapper(session, content, ua, pbar):
    await fetchContent(session, content, ua)
    pbar.update(1)


def fetchContentLinks():
    csv_path = "./output_links.csv"

    with open(csv_path, "r") as file:
        df = pd.read_csv(file)
        filtered_df = df[df["Scraped At"].isnull()]
        contentLinks = []
        for index, row in filtered_df.iterrows():
            contentLinks.append({"link": row["Link"], "category": row["Category"]})

        return contentLinks


def updateTimestamp(link):
    csv_path = "./output_links.csv"
    df = pd.read_csv(csv_path)
    df.loc[
        df["Link"] == link,
        "Scraped At",
    ] = pd.to_datetime("now", utc=True)
    df.to_csv(csv_path, index=False)


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

                    saveData(title, category, content_text)
                    updateTimestamp(content["link"])
                    break

        except Exception as e:
            print(f"Error fetching {content['link']}: {e}")


def saveData(title, category, content):
    try:
        title = re.sub(r"[^a-zA-Z0-9\s]", "", title)
        category_directory = f"./articles/{category}"

        if not os.path.exists(category_directory):
            os.makedirs(category_directory)

        file_path = os.path.join(category_directory, f"{title}.txt")

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Title: {title}\n")
                file.write(f"Category: {category}\n\n")
                file.write(f"Content:\n{content}\n")
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
