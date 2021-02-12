# import schedule
# import time
# import threading
# import discord
# import os
# import asyncio
# from scrape.finviz import finvizReport
# from database.docs import User, WatchList

# client = None


# async def sendReport(username, channel):
#     try:
#         await channel.send(f"📈 Report for **{username}**",
#                 file=discord.File(r'./xlsxwrite/report.xlsx'))
#         if os.path.exists(r'./xlsxwrite/report.xlsx'):
#             os.remove(r'./xlsxwrite/report.xlsx')
#         else:
#             print('The file does not exist')
#     except Exception as e:
#         print(e)
#         await channel.send(f'💀 There was an error retrieving the report for {username}')

# def run_continuously(c, interval=1):
#     cease_continuous_run = threading.Event()
#     global client
#     client = c
#     class ScheduleThread(threading.Thread):
#         @classmethod
#         def run(cls):
#             while not cease_continuous_run.is_set():
#                 schedule.run_pending()
#                 time.sleep(interval)

#     continuous_thread = ScheduleThread()
#     continuous_thread.start()
#     return cease_continuous_run


# def morningReport():
#     watchlists = WatchList.objects
#     # send the report made
#     c = client.get_channel(808789990233604146)
#     for w in watchlists:
#         username = w.user.user_name
#         tickers = w.tickers

#         # make report
#         finvizReport(tickers)

#         # send report
#         print('SENDING REPORT')
#         sendReport(username, c)

# async def eveningReport():
#     print('Hello evenenig')

# schedule.every(3).seconds.do(morningReport)
# schedule.every().day.at("07:00").do(morningReport)
# schedule.every().day.at("15:00").do(eveningReport)

# if __name__ == "__main__":
#     morningReport()
