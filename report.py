# CS 186 Results Logger courtesy of Noel Moldvai and Kevin "Young Kevin" Sheng

import subprocess as sp

def getFreqsFromQuery(query, top, freqs):
  result = sp.Popen(query, stdout=sp.PIPE, shell=True).communicate()[0]
  rows = result.split('\n')[2:-3]
  for row in rows:
    item, freq = [int(x) for x in row.split('|')]
    top.append(item)
    freqs[item] = freq
  top.sort()

def is_accurate(reported, actual):
  for k in actual.keys():
    r = float(reported[k])
    a = float(actual[k])
    if (abs(r-a) / a) >= 0.04:
      return False
  return True

results_file = open('results.txt', 'w')

data_tables = (1,2,3)
ks = (10,5)
outputs = [(a,b) for a in data_tables for b in ks]

width = (100, 300, 700, 1300, 2300, 4300)
depth = (2, 4, 8, 16)

combos = [(a,b,a*b) for a in width for b in depth]
combos.sort(cmp= lambda x, y: 1 if x[2] > y[2] else -1)

for data_table, k in outputs:
  actual_top = []
  actual_freqs = {}
  # call the actual query and store the top 10 values and their frequencies
  getFreqsFromQuery("$HOME/pgsql/bin/psql -p 11111 nums -c 'SELECT num, COUNT(*) as count from numbers%d GROUP BY num ORDER BY count DESC limit %d;'"
      % (data_table, k), actual_top, actual_freqs)

  for width, depth, product in combos:
    # call the stuff
    cur_top = []
    cur_freqs = {}
    getFreqsFromQuery(("$HOME/pgsql/bin/psql -p 11111 nums -c 'SELECT num, APPROX_COUNT(%d, %d, %d) as count from numbers%d GROUP BY num ORDER BY count DESC limit %d;'"
        % (k, width, depth, data_table, k)), cur_top, cur_freqs)
    if cur_top == actual_top and is_accurate(cur_freqs, actual_freqs):
      string = "data%d,%d,%d,%d" % (data_table, k, width, depth)
      print string
      results_file.write(string + '\n')
      break
