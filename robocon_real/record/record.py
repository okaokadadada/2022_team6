import datetime
import csv
import os

move, distance_F, distance_L, difference = "turn_L", 100, 50, 20   

now_time = datetime.datetime.now()
filename = os.path.join("record_folder","record_"+now_time.strftime('%Y%m%d_%H%M%S')+".csv")


with open(filename,'a',newline='') as f: 
    writer = csv.writer(f)
    writer.writerow(["move", "distance_F", "distance_L", "difference"])


with open(filename,'a',newline='') as f: 
    writer = csv.writer(f)
    writer.writerow([move, distance_F, distance_L, difference])
