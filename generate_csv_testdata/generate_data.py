import csv
import os

file = 'csv_testdata/data.csv'

generated_data = []
trikot = []

file2 = open('generated_data.txt', 'w', encoding='utf8')
rn = open('./csv_testdata/new.txt', 'r')

for r in rn:
    trikot.append(r)

with open(file, 'r', encoding='utf8') as csvfile:
      reader = csv.reader(csvfile, delimiter=' ')
      for row in reader:
         generated_data.append(row)

x = 0
for line in generated_data:
    file2.write(line[0] + ' ')
    file2.write(line[1] + ' ')
    if x == 0:
        file2.write('Username ')
        file2.write('Password ')
        file2.write('Role\n')
        #file2.write('Trikot' + '\n')
    else:
        file2.write(line[0] + '.' + line[1] + ' ')
        file2.write(line[0] + '1234' + ' ')
        file2.write('PLAYER\n')
        #file2.write(trikot[x-1])
    x = x + 1
# tfv = open('./csv_testdata/test.txt', 'r')

# x = 0
# for row in tfv:
#     if x == 5:
#         rn.write(row)
#         x = -3
#     x = x + 1

