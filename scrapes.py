import sys
import csv

f = open('news.csv', 'rb')
try:
    reader = csv.reader(f)
    rownum = 0
    for row in reader:
        if rownum == 3:
            print(row)
        rownum += 1
finally:
    f.close()