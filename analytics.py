import requests
import re
import time
from datetime import datetime
import json
import os

DELAY = 1


def get_trees():
    r = requests.get('https://teamtrees.org')
    return int(re.search('data-count="(\\d+)"', r.text).group(1))


def main():    
        last_trees = get_trees()
        #print(last_trees)
        totalLoops = 0
        loops = 0
        gained_total = 0
        while True:
            now = datetime.now()
            time.sleep(DELAY - 0.1)
            trees_now = get_trees()
            #print(trees_now)
            loops += 1
            totalLoops += 1

            WriteData = open("data/"+now.strftime("%Y.%m.%d")+"-count.csv", "a")   
            WriteData.write(str(trees_now)+","+now.strftime("%Y-%m-%d %H:%M:%S")+"\n")
            WriteData.close()



            if trees_now > last_trees:
                totalLoops += 1
                loops += 1

                diff = trees_now - last_trees
                gained_total += diff
                goal = 20000000 - trees_now
                rate = round(diff/(loops*DELAY), 2)
                rate_total = round(gained_total/(totalLoops*DELAY), 2)
                preditction = (goal/rate_total)/60/60/24

                #data = [now.strftime("%Y-%m-%d %H:%M:%S"),trees_now, (trees_now-last_trees)]    
                #data = json.dumps({"date": now.strftime("%Y-%m-%d %H:%M:%S"),"sum": trees_now, "diff":(trees_now-last_trees)})

                WriteRate = open("data/"+now.strftime("%Y.%m.%d")+"-rate.csv", "a")   
                WriteRate.write(str(rate)+","+now.strftime("%Y-%m-%d %H:%M:%S")+"\n")
                WriteRate.close()    

                if(preditction < 2):
                    print('\n\nThe donations are running at ${} / second. That would mean we will be done in {} hours! Now the rate is: ${} / second \n+{} in {} seconds'.format(rate_total, round(preditction * 24), rate, diff, round(loops*DELAY, 2)))
                else:
                    print('\n\nThe donations are running at ${} / second. That would mean we will be done in {} days! Now the rate is: ${} / second \n+{} in {} seconds'.format(rate_total, round(preditction), rate, diff, round(loops*DELAY, 1)))

                #print(myData)
                loops = 0
                last_trees = trees_now




if __name__ == '__main__':
    main()
