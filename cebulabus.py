import requests
import json
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime,timedelta
import smtplib
from email.message import EmailMessage
import configparser

departure_date = "11.02.2022"
Now = datetime.now() + timedelta(days=52)
cfg = configparser.ConfigParser()
cfg.read('config.ini')
flexbus_last_max_date = None
neobus_last_max_date = None
f = open('emailList.json')
emails = json.load(f)

def write_log(text):
    print(text)

def send_email(busname, newDate):
    msg = EmailMessage()
    msg.set_content('Na stronie https://'+busname+'.pl pojawiły się nowe bilety dostępne na dzień: ' + newDate)
                        
    msg['Subject'] = busname + f' - dostępne są nowe bilety!'
    msg['From'] = "CebulaBus"
    msg['To'] = ", ".join(emails)

    s = smtplib.SMTP_SSL(cfg.get('Email', 'Smtp'))
    s.login(cfg.get('Email', 'Login'), cfg.get('Email', 'Password'))
    s.send_message(msg)
    s.quit()
    write_log("emial send to: " + ", ".join(emails))

def print_neobus():
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    do = True
    global Now
    global neobus_last_max_date
    
    while do:
        search_format =Now.strftime("%d.%m.%Y")
        format = Now.strftime("%Y-%m-%d")
#       print("sprawdzana data: " + search_format)
        data = requests.post("https://neobus.pl/", data = "ajax=true&dataType=json&module=neotickets&step=1&ticket_type=student&initial_stop=75&final_stop=44&passengers=1&date_there="+search_format+"&date_return=&initial_stop_name=WARSZAWA+Dw.+Zach.+st.7&final_stop_name=BRZOZ%C3%93W+Dworzec+PKS+Plac+Grunwaldzki+01+",headers=headers)
        max_date = Now - timedelta(days=1);
        Now = Now + timedelta(days=1)
#       print("wystąpenia: " + str(data.text.count(format)))
        
        if not data.text.count(format) >1:
            do = False
            Now = max_date
            if neobus_last_max_date is None:#first run
                neobus_last_max_date=max_date
                
            if neobus_last_max_date != max_date:
                neobus_last_max_date=max_date
                send_email('neobus', max_date)
                write_log("NEO BUS: NOWE BILETY DOSTĘPNE")
            
            write_log("NEOBUS: bilety dostępne do dnia: " + max_date.strftime("%d-%m-%Y"))    

def print_flixbus():
    vgm_url = 'https://search.k8s.mfb.io/api/v4/search?from_city_id=40e19c59-8646-11e6-9066-549f350fcb0c&to_city_id=40e279fe-8646-11e6-9066-549f350fcb0c&departure_date='+departure_date+'&products=%7B%22adult%22%3A1%2C%22bike_slot%22%3A0%7D&currency=PLN&locale=pl&search_by=cities&include_after_midnight_rides=1'
    data = requests.get(vgm_url).text
    json_object = json.loads(str(data))
    dat=json_object["no_bikes_period"]
    max_date = dat["from"]
    global flexbus_last_max_date
    
    if flexbus_last_max_date is None:#first run
        flexbus_last_max_date=max_date

    if flexbus_last_max_date != max_date:
        flexbus_last_max_date=max_date
        send_email('flixbus', max_date)
        write_log("FLIX BUS: NOWE BILETY DOSTĘPNE")

    write_log("FLIX BUS: bilety dostępne do dnia: " + str(max_date))
    
def job():
    now = datetime.now()
    write_log("Status: " +now.strftime("%H:%M:%S"))
    print_neobus()
    print_flixbus()

job()
sched = BlockingScheduler()
sched.add_job(job, 'interval', minutes = int(cfg.get('Default', 'RefreshMinutes')))
sched.start()