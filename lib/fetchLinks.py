from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.dbConn import connect

db = connect()

def fetchLinks():
  print("Fetching Links...")
  url = "https://nftnow.com/"

  chrome_options = Options()
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  wait = WebDriverWait(driver, 30)

  links = db['links']
  links_data = links.find()

  scrapNewData = True
  scrapedLinks = []

  while scrapNewData:
    try:
      load_more_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "alm-load-more-btn"))
      )
      load_more_button.click()

      updated_page_source = driver.page_source

      soup = BeautifulSoup(updated_page_source, "html.parser")

      link_elements = soup.find_all(class_="section-home-latest__article-title")
      link_categories = soup.find_all(class_="section-home-latest__category")
      link_date = soup.find_all(class_="section-home-latest__date")
      link_author = soup.find_all(class_="section-home-latest__author")

      new_data = []

      for i in range(len(link_elements)):
        link_element = link_elements[i]
        title = link_element.text.strip()
        category = link_categories[i].text.strip()
        author = link_author[i].text.strip()
        date = link_date[i].text.strip()
        link = link_element.a["href"]
        if link in scrapedLinks:
          continue

        if link not in [doc['link'] for doc in links_data]:
          new_data.append(
            {
              "title": title,
              "category": category,
              "author": author,
              "date": date,
              "link": link,
              "scraped_at": "",
            }
          )
          scrapedLinks.append(link)
        else:
          scrapNewData = False
          break

      if new_data:
        links.insert_many(new_data)

    except Exception as e:
      break

  driver.quit()
