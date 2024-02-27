from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
import configparser
from neobus_checker import check_neobus_tickets
import urllib3
from date_persistence import save_start_date, load_start_date
import os

# Disable warnings from unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NeobusScheduler:
    def __init__(self, date_file="last_start_date.txt", default_start_date="30.04.2024"):
        self.date_file = date_file
        self.start_date = load_start_date(default_start_date, date_file)
        self.cfg = configparser.ConfigParser()

    def job(self):
        now = datetime.now()
        print("Status: ", now.strftime("%H:%M:%S"))
        self.start_date = check_neobus_tickets(self.start_date)
        save_start_date(self.start_date, self.date_file)


    def start(self):
        self.cfg.read('config/settings.ini')
        scheduler = BlockingScheduler()
        refresh_minutes = int(self.cfg.get('Default', 'RefreshMinutes'))
        scheduler.add_job(self.job, 'interval', minutes=refresh_minutes)
        try:
            print("Scheduler started at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("Scheduler stopped.")

   

if __name__ == '__main__':
    neobus_scheduler = NeobusScheduler()
    neobus_scheduler.start()
