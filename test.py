import pandas as pd

csv_path = "./output_links.csv"

with open(csv_path, "r") as file:
    df = pd.read_csv(file)

df.loc[
    df["Link"]
    == "https://nftnow.com/art/exclusive-xcopy-lifts-the-veil-on-remnants-rarepass-project/",
    "Scraped At",
] = pd.to_datetime("now", utc=True)

df.to_csv(csv_path, index=False)

# import pandas as pd

# csv_path = "./output_links.csv"

# with open(csv_path, "r") as file:
#     df = pd.read_csv(file)

# df["Scraped At"] = ""

# df.to_csv(csv_path, index=False)
