import schedule
import time
import os
from datetime import datetime
from src.scraper import SocGenScraper
from utils.email_sender import EmailEngine
from utils.database import DatabaseHandler
from utils.processor import json_to_pandas

def run_work():
    sg = SocGenScraper()
    name = f"final_{datetime.now().strftime('%d-%m-%Y--%H:%M:%S')}.json"
    path = os.path.join('json', name)
    sg.save_final_data(name)
    df = json_to_pandas(path)
    os.remove(path)
    db = DatabaseHandler(df)
    new_df = db.run()
    ee = EmailEngine('eloidieme@gmail.com', new_df)
    ee.send_email()

#schedule.every().day.at("02:12").do(run_work)

#while True:
#    schedule.run_pending()
#    time.sleep(1)
    
if __name__ == '__main__':
    run_work()