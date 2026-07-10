import schedule
import time
import subprocess
import datetime
import os

def run_daily_etl():
    print(f"[{datetime.datetime.now()}] Starting scheduled ETL pipeline...")
    
    try:
        # Step 1: Fetch Live NAV
        print("Fetching latest NAV from mfapi.in...")
        subprocess.run(['python', 'scripts/live_nav_fetch.py'], check=True)
        
        # Step 2: Run ETL Pipeline to process new data and update DB
        print("Running ETL pipeline...")
        subprocess.run(['python', 'scripts/etl_pipeline.py'], check=True)
        
        print(f"[{datetime.datetime.now()}] Scheduled ETL completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.datetime.now()}] Error during scheduled ETL execution: {e}")

# Schedule the job every weekday at 20:00 (8:00 PM)
schedule.every().monday.at("20:00").do(run_daily_etl)
schedule.every().tuesday.at("20:00").do(run_daily_etl)
schedule.every().wednesday.at("20:00").do(run_daily_etl)
schedule.every().thursday.at("20:00").do(run_daily_etl)
schedule.every().friday.at("20:00").do(run_daily_etl)

if __name__ == "__main__":
    print(f"[{datetime.datetime.now()}] Scheduler started. Waiting for 8:00 PM on weekdays...")
    print("Keep this terminal open for the schedule to run.")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60) # check every minute
