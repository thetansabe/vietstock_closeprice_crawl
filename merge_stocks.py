import pandas as pd
import os

stocks = ['ANV', 'HAN', 'FPT']
xls_path = './seperate_stock'
xls_files = [f for f in os.listdir(xls_path) if f.endswith('.xls')]

df = pd.read_html('./seperate_stock/ANV-20221127-1319.xls', encoding='utf8', skiprows=(0,7))
print(df)

# close = df.iloc[:, 4].values
# print(close)
# newDf = pd.DataFrame(data={'Date': df})
# for xls in xls_files:
#     df = pd.read_excel(os.path.join(xls_path, xls))
#     print(df)
#     break