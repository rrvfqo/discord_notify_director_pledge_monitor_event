'''
查詢公開資訊觀測站，取得當日上市上櫃的董監質設的資料
'''
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def get_today_date():

    # 取得當天的日期，並只取出年與月，年的格式要轉換成民國年，然後2個變數都要轉換成字串
    today = datetime.today()
    year = str(today.year - 1911).zfill(3)  # 民國年
    month = str(today.month).zfill(2)  # 月份
    day = str(today.day).zfill(2)  # 日
    # 取得當天的日期，並只取出日，然後轉換成字串
    print(f"今天是{year}年{month}月{day}日")

    return year, month, day



def get_sii_today_pledged_shares(roc_year, month, day):

    # 上市公司的董監質設資料的網址
    url = f"https://siis.twse.com.tw/server-java/STAMAK03?colorchg=1&step=1&order=1&TYPEK=sii&year={roc_year}&smonth={month}&emonth={month}&"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'big5'  # 指定正確的編碼
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到第一個表格
    table = soup.find("table")
    # 用 pandas 直接讀取 HTML 表格
    df_list = pd.read_html(str(table))

    if df_list:
        df = df_list[0]

         # 先將 MultiIndex 轉成單層欄位（只取第一層或第二層，看你要哪一層）
        # 這裡以取第二層為例（通常是你要的欄位名稱）
        df.columns = [col[0] if col[0] != col[1] else col[1] for col in df.columns]

        # 只保留你要的欄位
        keep_cols = [
            '股票代號', '公司名稱', '設質人 身份別', '設質人 姓名', '質設異動 發生日期',
            '設質 股數', '解質 股數', '累積質 設股數', '質權人 姓名', '備註', '申報日期'
        ]
        df = df[keep_cols]

        print(df.head())  # 顯示前幾列
        # print(df.columns)  # 顯示欄位名稱
        # 儲存成 CSV
        # df.to_csv("sii_pledged_shares.csv", index=False, encoding="utf-8-sig")
    else:
        print("找不到表格")

    # 篩選出"申報日期"為今天的資料
    today_str = f"{roc_year}/{month}/{day}"
    today_df = df[df["申報日期"] == today_str]

    print(f"今天的董監質設資料：\n{today_df}")

    return today_df


def get_otc_today_pledged_shares(roc_year, month, day):

    # 上櫃公司的董監質設資料的網址
    url = f"https://siis.twse.com.tw/server-java/STAMAK03?colorchg=1&step=1&order=1&TYPEK=otc&year={roc_year}&smonth={month}&emonth={month}&"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'big5'  # 指定正確的編碼
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到第一個表格
    table = soup.find("table")
    # 用 pandas 直接讀取 HTML 表格
    df_list = pd.read_html(str(table))

    if df_list:
        df = df_list[0]

         # 先將 MultiIndex 轉成單層欄位（只取第一層或第二層，看你要哪一層）
        # 這裡以取第二層為例（通常是你要的欄位名稱）
        df.columns = [col[0] if col[0] != col[1] else col[1] for col in df.columns]

        # 只保留你要的欄位
        keep_cols = [
            '股票代號', '公司名稱', '設質人 身份別', '設質人 姓名', '質設異動 發生日期',
            '設質 股數', '解質 股數', '累積質 設股數', '質權人 姓名', '備註', '申報日期'
        ]
        df = df[keep_cols]

        print(df.head())  # 顯示前幾列
        # print(df.columns)  # 顯示欄位名稱
        # 儲存成 CSV
        # df.to_csv("sii_pledged_shares.csv", index=False, encoding="utf-8-sig")
    else:
        print("找不到表格")

    # 篩選出"申報日期"為今天的資料
    today_str = f"{roc_year}/{month}/{day}"
    today_df = df[df["申報日期"] == today_str]

    print(f"今天的董監質設資料：\n{today_df}")

    return  today_df

def check_pledged():

    # 取得今天的日期
    roc_year, month, day = get_today_date()

    # 取得今天上市的董監質設資料
    today_sii_pledged = get_sii_today_pledged_shares(roc_year, month, day)
    today_otc_pledged = get_otc_today_pledged_shares(roc_year, month, day)

    # new_pledged = today_sii_pledged + today_otc_pledged
    # 合併兩個 DataFrame（上下合併）
    new_pledged = pd.concat([today_sii_pledged, today_otc_pledged], ignore_index=True)

    print(f"今天的董監質設資料：\n{new_pledged}")

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not new_pledged.empty:
        # 處理新公告，例如發送通知
        print(f"有新的news - {current_time}") 

    else:
        print(f"沒有新的news - {current_time}")

    return new_pledged

if __name__ == "__main__":
    
    # roc_year, month, day = get_today_date()
    # get_sii_today_pledged_shares(roc_year, month, day)
    # get_otc_today_pledged_shares(roc_year, month, day)
    check_pledged()