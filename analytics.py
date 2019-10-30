import requests
import re
import time
from datetime import datetime



DELAY = 0.1


def get_trees():
    r = requests.get('https://teamtrees.org')
    return int(re.search('data-count="(\\d+)"', r.text).group(1))


def main():    
        now = datetime.now()
        last_trees = get_trees()
        #print(last_trees)
        totalLoops = 0
        loops = 0
        gained_total = 0
        while True:
            trees_now = get_trees()
            #print(trees_now)
            loops += 1
            totalLoops += 1
            if trees_now > last_trees:
                totalLoops += 1
                loops += 1

                diff = trees_now - last_trees
                gained_total += diff

                rate = round(diff/(loops*DELAY), 2)
                rate_total = round(gained_total/(totalLoops*DELAY), 2)
                preditction = (20000000/rate_total)/60/60/24
                #print('TREE, people planted {} trees within the last {} seconds!'.format(trees_now - last_trees, round(loops*DELAY,2)))
                if(preditction < 2):
                    print('\n\nThe donations are running at ${} / second. That would mean we will be done in {} hours! Now the rate is: ${} / second \n+{} in {} seconds'.format(rate_total, round(preditction * 24), rate, diff, round(loops*DELAY, 2)))
                else:
                    print('\n\nThe donations are running at ${} / second. That would mean we will be done in {} days! Now the rate is: ${} / second \n+{} in {} seconds'.format(rate_total, round(preditction), rate, diff, round(loops*DELAY, 1)))
                #myData = {"date": now.strftime("%Y-%m-%d %H:%M:%S"),"sum": trees_now, "diff":(trees_now-last_trees)} 
                #myData = [now.strftime("%Y-%m-%d %H:%M:%S"),trees_now, (trees_now-last_trees)]    

                #print(myData)
                loops = 0
                last_trees = trees_now




if __name__ == '__main__':
    main()
