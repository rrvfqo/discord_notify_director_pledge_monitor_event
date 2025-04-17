import sys
import requests


from fetch_today_pledged_shares import check_pledged  # 匯入函式


def notify_discord_webhook(msg):
    url = 'https://discord.com/api/webhooks/1362281753045242016/G8c3HDjLxYUq0b-ES6ogVPKYP4nqvYzJIecsMt8RFRYUoOdKFGBZwxan41bSooW7HsfH'
    headers = {"Content-Type": "application/json"}
    data = {"content": msg, "username": "公告-董監質設"}
    res = requests.post(url, headers = headers, json = data) 
    if res.status_code in (200, 204):
            print(f"Request fulfilled with response: {res.text}")
    else:
            print(f"Request failed with response: {res.status_code}-{res.text}")


def generate_msg():
    new_announcements = check_pledged()  # 呼叫函式取得新公告

    if not new_announcements.empty:
        msg = '\n\n'.join(
            f"股票代號：{row['股票代號']}  公司名稱：{row['公司名稱']}\n"
            f"身份別：{row['設質人 身份別']}  姓名：{row['設質人 姓名']}\n"
            f"異動日期：{row['質設異動 發生日期']}\n"
            f"設質股數：{row['設質 股數']}  解質股數：{row['解質 股數']}\n"
            f"累積質設股數：{row['累積質 設股數']}\n"
            f"質權人姓名：{row['質權人 姓名']}\n"
            f"備註：{row['備註']}\n"
            f"申報日期：{row['申報日期']}"
            for _, row in new_announcements.iterrows()
        )
        return msg
    return None

def job():
    msg = generate_msg()
    if msg is None:
        print("No new news")
        return
    if len(msg) > 2000:
        msg_list = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
        for msg in msg_list:
            notify_discord_webhook(msg)
        return
    else:
        notify_discord_webhook(msg)
        return

def signal_handler(sig, frame):
    global running
    print('Stopping the scheduler...')
    running = False
    sys.exit(0)

if __name__ == "__main__":

    job()  # 執行一次工作


