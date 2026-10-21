import pandas as pd

df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")

print(df.shape)            # (24, 4)
print(df.head(3))         # pierwsze wiersze
print(df.isnull().sum())   # braki w kolumnach