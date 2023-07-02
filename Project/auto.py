import schedule
import time
import menu
import subprocess

def run_python_file1():
    # Use subprocess to run the first Python file
    subprocess.call(['python', 'menu.py'])

 
schedule.every(10).minutes.do(run_python_file1)
 

while True:
    schedule.run_pending()
    time.sleep(1)
