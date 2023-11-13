import openai
import pandas as pd

def selectContent():
  pd.set_option('display.max_colwidth', None)
  df = pd.read_csv('./output_links.csv')
  print(df[['Title','Category','Author','Date']].to_markdown(index=True))