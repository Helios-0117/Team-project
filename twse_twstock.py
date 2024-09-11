import twstock
import pandas as pd

# (00679B)可更換股票代  號股票代碼:(0050,0055,0056,00635U,00642U,00679B,00692,00711B,00712)
target_stock = '00712'   
# 告訴twstock我們要查詢的股票                  
stock = twstock.Stock(target_stock)
#取用2018/10至今每天的交易資料         
target_price = stock.fetch_from(2018, 10)  

# 將資料整理成一個字典列表，每個元素是一個字典，包含日期和收盤價
data = [{'日期': target.date, '收盤價': target.close} for target in target_price]

# 建立 DataFrame
df = pd.DataFrame(data)

# 儲存一個CSV檔取名叫(股票代碼).csv到TWSE_CSV資料夾目錄
filename = f'./TWSE_CSV/{target_stock}.csv'
#將Data Frame轉存為csv檔案
df.to_csv(filename)