import schedule
import time


def job():
    print("I'm working...")


while True:
    schedule.run_pending()
    time.sleep(5)
