import commands, re

best_value = {}

for k in (10, 20, 50, 100):
  for depth in (4,):
    for width in (1000,):
      approx_sql = '$HOME/pgsql/bin/psql -p 11111 nums -c "select num, approx_count(%i, %i, %i) as C from numbers3 group by num order by C desc;"' % (k, width, depth)
      sql = '$HOME/pgsql/bin/psql -p 11111 nums -c "SELECT num, COUNT(*) AS count FROM numbers3 GROUP BY num ORDER BY count DESC limit %i;"' % k

      commands.getoutput(approx_sql)
      commands.getoutput(sql)

log = open("postgres-8.4.2/hw5.log", 'r')

approx = {}
count = {}

for line in log:
  m = re.search('([0-9]+\.[0-9]+) elapsed', line)
  if m:
    elapsed = m.group(1)

  m = re.search('limit ([0-9]+);', line)
  if m:
    k = int(m.group(1))

  m = re.search('approx_count\(([0-9]+)', line)
  if m:
    k = int(m.group(1))

  m = re.search('approx_count', line)
  if m:
    approx[k] = elapsed

  m = re.search('COUNT\(\*\)', line)
  if m:
    count[k] = elapsed

ks = approx.keys()
ks.sort()

for k in ks:
  print "%s,%s,%s" % (k, approx[k], count[k])
